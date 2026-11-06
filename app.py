from flask import Flask
from config import Config
from database import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Реєстрація контролерів
    from controllers.main_controller import main_bp
    from controllers.cart_controller import cart_bp
    from controllers.auth_controller import auth_bp
    from controllers.order_controller import order_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)