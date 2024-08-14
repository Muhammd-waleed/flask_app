from flask import Flask
from flask_bcrypt import Bcrypt
import pymysql as mq
from flask_login import LoginManager,UserMixin


connection=mq.connect(host='localhost', 
                     user='root',
                     password='',
                     port=3306, 
                     database='flask_app_mysql_db',
                     cursorclass=mq.cursors.DictCursor)

app=Flask(__name__)
app.config['SECRET_KEY']='2463ed925ee56413c77f5282'

bcrypt=Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view='login_page'
login_manager.login_message_category = 'info'

    
@login_manager.user_loader
def load_user(user_id):
    cursor = connection.cursor()
    
    # Execute a query to fetch the user by id
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    
    cursor.close()

    if user_data:
        return User(
            id=user_data['id'],
            username=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            budget=user_data['budget']

        )
    return 
class User(UserMixin):
    def __init__(self, id, username, email, password,budget):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.budget=budget
    
    @property
    def budget_pretier(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]}, {str(self.budget)[-3:]} $'
        else :
            return f'{self.budget}$'
from market import routes

