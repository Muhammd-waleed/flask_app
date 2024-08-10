from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import EqualTo, Length,Email,DataRequired,ValidationError
from  market import connection



class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        try:
            query=f'''
                    select * from users
                    where name = %s;'''

            cursor=connection.cursor()  
            cursor.execute(query,(username_to_check.data,))
            x=cursor.fetchall()
            
        except Exception as e:
            print(f"{e.args}")
        finally:
            cursor.close()
        if x:
                raise ValidationError("Username already Exist Use Different name")


    username=StringField(label="User Name: ", validators=[Length(min=2, max=15),DataRequired()])
    email=StringField(label="Enter Email:", validators=[Email(),DataRequired()])
    password=PasswordField(label="Password: " , validators=[DataRequired()])
    confirmPassword=PasswordField(label="Confirm Password:" , validators=[EqualTo('password'),DataRequired()])
    submit=SubmitField()

