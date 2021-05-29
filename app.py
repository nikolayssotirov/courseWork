import re
from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
#import bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash
#from werkzeug.utils import redirect

app = Flask(__name__)
mysql = MySQL()

app.secret_key = 'why would I tell you my secret key?'
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'niki'
app.config['MYSQL_DATABASE_DB'] = 'USERS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')
 
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = bcrypt.hashpw(_password, bcrypt.gensalt())
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Забранен достъп!')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql.
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        
        if len(data) > 0:
            if (_password == str(data[0][3])):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Грешен имейл или парола.')
        else:
            return render_template('error.html',error = 'Грешен имейл или парола.')
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/question1')
def question1():
    return render_template('question1.html')

@app.route('/addRating',methods=['POST'])
def addRating1():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion1',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                conn.commit()
                return redirect('/question2')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question2')
def question2():
    return render_template('question2.html')

@app.route('/question3')
def question3():
    return render_template('question3.html')

@app.route('/question4')
def question4():
    return render_template('question4.html')

@app.route('/question5')
def question5():
    return render_template('question5.html')

@app.route('/question6')
def question6():
    return render_template('question6.html')

@app.route('/question7')
def question7():
    return render_template('question7.html')

@app.route('/question8')
def question8():
    return render_template('question8.html')

@app.route('/question9')
def question9():
    return render_template('question9.html')

@app.route('/question10')
def question10():
    return render_template('question10.html')    

if __name__ == "__main__":
    app.run()