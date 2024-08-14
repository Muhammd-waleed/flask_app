from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import EqualTo, Length,Email,DataRequired,ValidationError
from  market import connection



class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        try:
            query='''
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

    def validate_email(self,email_to_check):
        try:
            query='''select * from users where email=%s;'''
            cursor=connection.cursor()
            print(email_to_check.data)
            cursor.execute(query,(email_to_check.data,))
            x=cursor.fetchall() 
        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
            if x:
                raise ValidationError("Email Already Exist")

        





    username=StringField(label="User Name: ", validators=[Length(min=2, max=15),DataRequired()])
    email=StringField(label="Enter Email:", validators=[Email(),DataRequired()])
    password=PasswordField(label="Password: " , validators=[DataRequired()])
    confirmPassword=PasswordField(label="Confirm Password:" , validators=[EqualTo('password'),DataRequired()])
    submit=SubmitField()


class LoginForm(FlaskForm):
    username=StringField(label="User Name: ", validators=[DataRequired()])
    password=PasswordField(label="Enter Password: ", validators=[DataRequired()])
    submit=SubmitField()



class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit=SubmitField(label='Sell Item')
