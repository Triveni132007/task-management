try:
    import razorpay # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover - allow editor/linter when package missing
    razorpay = None

from flask import current_app
from models.payment import Payment
from config.database import db


def _get_razorpay_client():
    """Return a razorpay client using app config or raise if razorpay is unavailable."""
    if razorpay is None:
        raise RuntimeError("razorpay package is not installed")

    key_id = current_app.config.get("RAZORPAY_KEY_ID")
    secret = current_app.config.get("RAZORPAY_SECRET")
    if not key_id or not secret:
        raise RuntimeError("Razorpay credentials not configured (RAZORPAY_KEY_ID/RAZORPAY_SECRET)")

    return razorpay.Client(auth=(key_id, secret))


client = None


def create_order_service(amount):
    """Create a razorpay order for the given amount (in INR).

    This obtains a razorpay client at call time so the module can be imported
    even when the razorpay package is not installed.
    """
    client = _get_razorpay_client()

    order = client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1,
    })

    return order


def save_payment_service(data, user_id):

    payment = Payment(
        razorpay_payment_id=data["razorpay_payment_id"],
        amount=data["amount"],
        status="success",
        user_id=user_id
    )

    db.session.add(payment)
    db.session.commit()

    return {
        "message": "Payment saved"
    }