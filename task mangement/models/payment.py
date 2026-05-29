from config.database import db


class Payment(db.Model):

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    razorpay_payment_id = db.Column(db.String(200))

    amount = db.Column(db.Integer)

    status = db.Column(db.String(50))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )