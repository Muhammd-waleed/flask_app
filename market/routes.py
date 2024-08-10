from flask import render_template,request,redirect,url_for,flash
from market import app,connection
from market.forms import RegisterForm


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
            data=(form.username.data, form.email.data, form.password.data)
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

