from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


import views

@login_manager.user_loader
def load_user(user_id):
    from controllers import get_user_by_id
    return get_user_by_id(user_id)

app.secret_key = "sldgw;aru8tuj20349haiufQ7F"

if __name__ == '__main__':
    app.run(debug=True)