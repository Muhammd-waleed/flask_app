from flask import render_template,request,redirect,url_for,flash
from market import app,connection,bcrypt
from market.forms import RegisterForm,LoginForm



@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    
    try:
        query=''' 
                select * from items;'''
        cursor=connection.cursor()  
        cursor.execute(query)
        result=cursor.fetchall()
    except Exception as e:
        print(f"{e.args}")
    finally:
        cursor.close()

    return render_template('market.html', items=result)

@app.route('/register',methods=['POST', 'GET'])
def register_page():
    form=RegisterForm()
    if request.method == 'POST' and form.validate():
        try:
            query=''' 
                    insert into users(name,email,password)
                    values(%s, %s, %s);'''
            hash_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            data=(form.username.data, form.email.data, hash_password)
            cursor=connection.cursor()  
            cursor.execute(query, data)
            connection.commit()
            return redirect( url_for('market_page'))
        except Exception as e:
            print(f"{e.args}")
        finally:
            cursor.close()
    if form.errors != {}:
        for err_msg  in form.errors.values():
            flash(f' There was an Error: {err_msg}',category='danger')
            
    return render_template('form.html',form=form)


@app.route('/login',methods=['POST','GET'])
def login_page():
    form=LoginForm()
    return render_template('login.html',form=form)
