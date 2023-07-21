from flask import Flask,flash, render_template, request, redirect, url_for, session
from database import *
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.secret_key = b'_Preetham'
app.config['SESSION_TYPE'] = 'filesystem'




@app.route('/')
def index():
    if not session.get("name"):
        return render_template('index.html')
    else:
        mycursor.execute("SELECT * from BOOKS")
        books = mycursor.fetchall()
        return render_template('books.html',books = enumerate(books))

#signin ---------------
@app.route('/sign_in', methods=['POST','GET'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user_check = "SELECT PASSWORD FROM USERDATA WHERE USERNAME = %s"
        user_data= (username,)
        mycursor.execute(user_check , user_data)
        data = mycursor.fetchall()
        if(data[0][0] == password):
            session.permanent = False
            session["name"] = username
            mycursor.execute("SELECT * from BOOKS")
            books = mycursor.fetchall()
            return render_template('books.html',books = enumerate(books))   
        else:
            flash('incorrect username and password')
            return redirect(url_for('sign_in'))     

@app.route('/login',methods= ['POST'])
def login():
    return redirect(url_for('sign_in'))
#----------------------


#admin -------
@app.route('/admin_login',methods= ['POST'])
def admin_login():
    return render_template('admin.html')

@app.route('/admin_signin',methods=['POST'])
def admin_signup():
    username = request.form['Admin_username']
    pwd = request.form['password']
    if(username == "ADMIN" and pwd == "ADMIN123"):
        return render_template('update.html')
    else:
        flash("Incorrect username and Password plz try again")
        return render_template('admin.html')



@app.route('/delete_book',methods = ['POST'])
def delete():
    name = request.form['TITLE']
    author = request.form['AUTHOR']
    user_check = "SELECT ID FROM BOOKS WHERE TITLE = %s AND AUTHOR = %s"
    mycursor.execute(user_check,(name,author))
    data = mycursor.fetchall()
    if(data):
        dele = "DELETE FROM BOOKS WHERE ID = %s"
        id = data[0]
        mycursor.execute(dele,id)
        mydb.commit()
        flash("BOOK DELETED SUCCESFULLY",'del')
        return render_template('update.html')
    else:
        flash("NO SUCH BOOK EXISTS",category='del')
        return render_template('update.html')

@app.route('/add_book',methods = ['POST'])
def add_book():
    name = request.form['TITLE']
    author = request.form['AUTHOR']
    user_check = "SELECT ID FROM BOOKS WHERE TITLE = %s AND AUTHOR = %s"
    vals = (name,author)
    mycursor.execute(user_check,vals)
    data = mycursor.fetchall()
    if(data):
        
        flash("BOOK ALREADY EXISTS",'add')
        return render_template('update.html')
    else:
        query = "INSERT INTO BOOKS (TITLE,AUTHOR) VALUES (%s,%s)"
        # books = b'qqq'
        mycursor.execute(query, vals)
        mydb.commit()
        flash("BOOK ADDED SUCESSFULLY",category='add')
        return render_template('update.html')
#---------------------


@app.route('/sign_up',methods= ['POST','GET'])
def sign_up():
    username = request.form['username']
    password = request.form['psw']
    pwd2 = request.form['psw_repeat']
    user_check = "SELECT USERNAME FROM USERDATA WHERE USERNAME = %s"
    user_data= (username,)
    mycursor.execute(user_check , user_data)
    data = mycursor.fetchall()

    if(data):
        flash("username already taken plz try again")
        return render_template('index.html')
    elif password != pwd2:
        flash("passwords didnt match plz try again")
        return redirect(url_for('index'))
    else:
        query = "INSERT INTO USERDATA (USERNAME,PASSWORD,BOOKS) VALUES (%s,%s,%s)"
        books = " "
        update = (username,password,books,)
        
        try:
            mycursor.execute(query, update)
            mydb.commit()
            session.permanent = False
            session["name"]= username
            return redirect(url_for('index'))
        except Exception as e:
            print("Error:", e)
    # Handle the error appropriately


#logout-----
@app.route('/logout',methods= ['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))
#-----------------

if __name__ == '__main__':
    app.run(debug=True)
