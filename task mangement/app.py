from flask import Flask
from config.database import init_db
from routes.auth_route import auth_bp
from routes.task_route import task_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize Database
init_db(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/task')


# Home Route
@app.route("/")
def home():
    return "Flask Working Successfully"


if __name__ == '__main__':
    app.run(debug=True)