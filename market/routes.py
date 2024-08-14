from flask import render_template,request,redirect,url_for,flash,request
from market import app,connection,bcrypt,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from flask_login import LoginManager,login_user,current_user,logout_user , login_required



@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market" ,methods=['POST','GET'])
@login_required
def market_page():

    purchase_form=PurchaseItemForm()
    sell_form=SellItemForm()
    if request.method=='POST':
        # Purchased Item Logic
        purchased_item_name=request.form.get('purchased')
        cursor=connection.cursor()
        query='select * from items where name = %s'
        cursor.execute(query,(purchased_item_name,))
        x=cursor.fetchone()
        if x:
            if current_user.budget >=x['price']:
                # Update the owner field in the items table
                update_query = 'UPDATE items SET owner = %s WHERE name = %s'
                cursor.execute(update_query, (current_user.id, purchased_item_name))

                # Update the current user's budget
                
                update_query = 'UPDATE users SET budget = %s WHERE id = %s'
                value_to_insert = current_user.budget - x['price']

                cursor.execute(update_query, (int(value_to_insert), current_user.id))


                # Commit the changes to the database
                connection.commit()
                flash(f'''Grate you Purchased {purchased_item_name} for the Price of {x['price']}
                    and your current Balance is {value_to_insert}''', category='info')
                return redirect(url_for('market_page'))
            else:
                flash('You dont have Enough Amount to Buy this item', category='danger')
                return redirect(url_for('market_page'))
        
        # Sell Item Logic

        sold_item_name=request.form.get('sold')
        print(sold_item_name)
        query=''' 
                select * from items where name=%s and owner=%s;  '''
        cursor=connection.cursor()  
        cursor.execute(query,(sold_item_name,current_user.id))
        owned_items=cursor.fetchone()
        print(owned_items)
        if owned_items:
                cursor=connection.cursor()
                update_query = 'UPDATE items SET owner = null WHERE name = %s'
                cursor.execute(update_query, (sold_item_name,))

                
                update_query = 'UPDATE users SET budget = %s WHERE id = %s'
                value_to_insert = current_user.budget + owned_items['price']

                cursor.execute(update_query, (int(value_to_insert), current_user.id,))
                connection.commit()

                flash("You have Palced the Item back in Market and got the money back",category='info')




        return redirect(url_for('market_page'))


        
    if request.method=='GET':           
        try:
            query=''' 
                    select * from items where owner is null;'''
            cursor=connection.cursor()  
            cursor.execute(query)
            result=cursor.fetchall()
        except Exception as e:
            print(f"{e.args}")
        finally:
            cursor.close()

        
            query=''' 
                    select * from items where owner =%s;'''
            cursor=connection.cursor()  
            cursor.execute(query,current_user.id)
            owned_items=cursor.fetchall()
        
        return render_template('market.html', items=result, purchase_form=purchase_form,
                               owned_items=owned_items,sell_form=sell_form)

    




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

            username=form.username.data
            query='select * from users where name=%s'
            cursor=connection.cursor()
            cursor.execute(query,username)
            result=cursor.fetchone()
            user=User(result['id'],result['name'], result['email'], result['password'],result['budget'])
            login_user(user)
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
    if request.method=='POST' and form.validate():
        username=form.username.data
        query='select * from users where name=%s'
        cursor=connection.cursor()
        cursor.execute(query,username)
        result=cursor.fetchone()
        user_db_password=result['password']
        if result and bcrypt.check_password_hash(user_db_password, form.password.data):
            user=User(result['id'],result['name'], result['email'], result['password'],result['budget'])
            login_user(user)
            flash(f"Success! You are Login as {result['name']}", category='success')
            return redirect(url_for('market_page'))

        else:
            flash("Username and the Password are not Correct! Try Again", category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been LogOut!',category='info')

    return redirect(url_for('home_page'))