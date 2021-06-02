import mysqlx
import multiprocessing
from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
 
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'niki'
app.config['MYSQL_DATABASE_DB'] = 'USERS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/indexLogged')
def indexLogged():
    return render_template('indexLogged.html')
 
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
                return json.dumps({'message':'Потребителят е създаден успешно!'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Въведете всички полета</span>'})

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
        global _username
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
   #print('question1"')
 
   return render_template('question1.html')

@app.route('/addRating1',methods=['POST'])
def addRating1():
    #print('addrating')

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

@app.route('/addRating2',methods=['POST'])
def addRating2():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion2',(_user,_rating))
            data = cursor.fetchall()

            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question3')
                conn.commit()
                return redirect('/question3')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question3')
def question3():
    return render_template('question3.html')

@app.route('/addRating3',methods=['POST'])
def addRating3():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion3',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question4')
                conn.commit()
                return redirect('/question4')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question4')
def question4():
    return render_template('question4.html')

@app.route('/addRating4',methods=['POST'])
def addRating4():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion4',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question5')
                conn.commit()
                return redirect('/question5')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question5')
def question5():
    return render_template('question5.html')

@app.route('/addRating5',methods=['POST'])
def addRating5():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion5',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question6')
                conn.commit()
                return redirect('/question6')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question6')
def question6():
    return render_template('question6.html')

@app.route('/addRating6',methods=['POST'])
def addRating6():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion6',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question7')
                conn.commit()
                return redirect('/question7')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question7')
def question7():
    return render_template('question7.html')

@app.route('/addRating7',methods=['POST'])
def addRating7():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion7',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question8')
                conn.commit()
                return redirect('/question8')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question8')
def question8():
    return render_template('question8.html')

@app.route('/addRating8',methods=['POST'])
def addRating8():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion8',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question9')
                conn.commit()
                return redirect('/question9')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question9')
def question9():
    return render_template('question9.html')

@app.route('/addRating9',methods=['POST'])
def addRating9():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion9',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect('/question10')
                conn.commit()
                return redirect('/question10')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/question10')
def question10():
    return render_template('question10.html')    

@app.route('/addRating10',methods=['POST'])
def addRating10():
    try:
        if session.get('user'):
            _user = session.get('user')
            _rating = int(request.form['rating'])

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addQuestion10',(_user,_rating))
            data = cursor.fetchall()
 
            if len(data) == 0:
                if _rating == 0:
                    return redirect("/indexLogged")
                conn.commit()
                return redirect("/indexLogged")
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

# @app.route('/getRatings')
# def getRatings():
#     try:
#         if session.get('user'):

#             con = mysql.connect()
#             cursor = con.cursor()
#             cursor.callproc('sp_getRatings')
#             ratings = cursor.fetchall()
 
#             ratings_dict = []
#             for rating in ratings:
#                 rating_dict = {
#                         'Въпрос 1': rating[0],
#                         'Въпрос 2': rating[1],
#                         'Въпрос 3': rating[2],
#                         'Въпрос 4': rating[3],
#                         'Въпрос 5': rating[4],
#                         'Въпрос 6': rating[5],
#                         'Въпрос 7': rating[6],
#                         'Въпрос 8': rating[7],
#                         'Въпрос 9': rating[8],
#                         'Въпрос 10': rating[9],
#                         'Средно': rating[10]}
#                 ratings_dict.append(rating_dict)
 
#             return json.dumps(ratings_dict)
#         else:
#             return render_template('error.html', error = 'Unauthorized Access')
#     except Exception as e:
#         return render_template('error.html', error = str(e))

if __name__ == "__main__":
    app.run()