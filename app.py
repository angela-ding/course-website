from flask import Flask, render_template, session, redirect, url_for, request, escape
from flask import g
import sqlite3
import sys

DATABASE = "assignment3.db"

#the function get_db is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db=g._database=sqlite3.connect(DATABASE)
    return db
#get_db opens the connection to the database

#the function query_db is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#the function make_dicts is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

app=Flask(__name__)

#the function close_connection is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.secret_key = 'someveryrandomstring'

#global variable to keep user info
gUser = []

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# Authentication #
@app.route('/login', methods=['GET', 'POST'])
def login():
    # db=get_db()
    # db.row_factory = make_dicts
    # if request.method == 'POST':
    #     for result in query_db('SELECT * FROM users'):
    #         if result['username'] == request.form['username']:
    #             if result['password'] == request.form['password']:
    #                 session['username'] = result['username']
    #                 session['sori'] = result['sori']
    #                 return redirect(url_for('home'))
    #     return render_template('login.html')
    # elif 'username' in session:
    #     return redirect(url_for('home'))
    # else:
    #     return render_template('login.html')

    if request.method == 'POST':
        render_template('login.html')
       
        username = request.form['username']
        password = request.form['password']

        with get_db() as db:
            cursor = db.cursor()
        #find_user = ("SELECT * FROM userInfo WHERE username = ? AND pass = ?")
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", [(username), (password)])
        result = cursor.fetchall()
        db.commit()
        db.close()

        if result:            

            session['username'] = request.form['username']
            session['sori'] = result[0][5]

            return redirect(url_for('home'))
        else:
            return render_template('login.html', wrongUser=True)
    elif "username" in session: 
        #already logged in
        return redirect(url_for('home'))
    elif request.form.get('register_button') == 'register':
        #user wants to register
        return render_template('register.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('sori')
    return redirect(url_for('login'))

def get_user(user: str)->str:
    '''Helper function to get user type
    '''
    user = user.lower()
    if user == 'student':
        return 's'
    elif user == 'instructor':
        return 'i'
    else:
        return 'error'


# THIS DOESNT WORK
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        newFirstName = request.form['firstName']
        newLastName = request.form['lastName']
        newEmail = request.form['email']
        newUsername = request.form['username']
        newPassword = request.form['password']
        newSori = request.form['sori']
        newSori = get_user(newSori)

        conn = sqlite3.connect('./assignment3.db')

        if newSori == 'error':
            return render_template('signup.html', soriWrong=True)

        emailExists = conn.execute('SELECT * FROM users WHERE email=?',[newEmail]).fetchall()
        if emailExists:
            return render_template('signup.html', emailInDB = True) #emailInDB is an if statement inside the signup.html file
        usernameExists = conn.execute('SELECT * FROM users WHERE username=?', [newUsername]).fetchall()
        if usernameExists:
            return render_template('signup.html', userTaken = True) #userTaken is an if statement inside the html file

        conn.execute('INSERT INTO users(firstName, lastName, email, username, password, sori) VALUES (?, ?, ?, ?, ?, ?)', [newFirstName, newLastName, newEmail, newUsername, newPassword, newSori])
        conn.commit()
        # If the new user has role student, add an entry to studentMarks
        if newSori == 's':
            # Add an entry in studentMarks
            conn.execute('INSERT INTO studentMarks(username) VALUES (?)', [newUsername ])
            conn.commit()
        conn.close()
        # Require the user to log in with newly created credentials
        return render_template('login.html')
    elif 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

@app.route('/home')
def home():
    if "username" in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/lectures')
def lectures():
    if "username" in session:
        return render_template('lectures.html')
    else:
        return redirect(url_for('login'))

@app.route('/tutorials')
def tutorials():
    if "username" in session:
        return render_template('tutorials.html')
    else:
        return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    if "username" in session:
        return render_template('assignments.html')
    else:
        return redirect(url_for('login'))

@app.route('/tests')
def tests():
    if "username" in session:
        return render_template('tests.html')
    else:
        return redirect(url_for('login'))

@app.route('/remark-request', methods = ["GET", "POST"])
def get_remark_request():
    if "username" in session:
        if request.method == "POST":
            if session['sori'] == 's':
                appendToDb([request.form['subject'], request.form['explanation']], 'remarks')
                # return render_template('remark-request.html', submitted=True)
                return render_template('remark-request-submitted.html')
            else:
                return redirect(url_for('home'))
        else:
            table_headers = get_modified_headers()
            html_table_headers = list()
            for item in table_headers:
                html_table_headers.append(table_headers[item])
            # grades = get_grades(session['username'])
            # grades.pop('username')
            # listOfSubjects = grades.keys()
            return render_template('remark-request.html', value_headers = table_headers)
    else:
        return redirect(url_for('login'))

# Redirect to correct page based on user type
@app.route('/feedback_redirect')
def feedback_redirect():
    if "username" in session:
        if session['sori'] == 's':
            return redirect(url_for('studentfeedback'))
        elif session['sori'] == 'i':
            return redirect(url_for('allstudentfeedback'))
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Redirect to correct page based on user type
@app.route('/grade_redirect')
def grade_redirect():
    try:
        if session['sori'] == 's':
            return redirect(url_for('studentgrades'))
        elif session['sori'] == 'i':
            return redirect(url_for('allstudentgrades'))
    except:
        return redirect(url_for('login'))

@app.route('/studentgrades')
def studentgrades():
    #for one student (in session)
    #pass a dictionary object that contains subject as key and score as content
    #column1: subject
    #column2: score
    if(session['sori'] == 's'): 
        dic = get_grades(session['username'])
        dic.pop('username')
        table_headers = get_modified_headers()
        html_table_headers = list()
        for item in table_headers:
            html_table_headers.append(table_headers[item])
        return render_template('studentgrades.html',dic=dic, table_headers=html_table_headers)
    else:
        return redirect(url_for("home"))


# Instructor Users Specific Functions #
@app.route('/allstudentfeedback')
def allstudentfeedback():
    if ('username' in session):
        instructor_username = session['username']
        questions = get_all_feedback_questions()
        responses = get_all_student_feedbacks(instructor_username)
        return render_template('allstudentfeedbacks.html', questions=questions, responses=responses, instructor_name=get_fullname_by_user(instructor_username))
    else:
        return redirect(url_for('login'))

@app.route('/allremarkrequests')
def all_remark_requests():
    grade_names = get_modified_headers()
    remark_requests = dict()
    for key in grade_names.keys():
        group_by_user = dict()
        conn = sqlite3.connect('./assignment3.db')
        for item in conn.execute('SELECT * FROM remarks'):
            if item[1] == key:
                group_by_user[item[0]] = [get_fullname_by_user(item[0]), item[2]]
        if len(group_by_user) > 0:
            remark_requests[key] = group_by_user
    return render_template('allremarkrequests.html', remark_requests=remark_requests, modified_names=grade_names)

# Page only visible to instructors, shows all student grades
@app.route('/allstudentgrades')
def allstudentgrades():
    user_names = get_users_and_names("s")
    mark_dict = dict()
    for user_key in user_names.keys():
        user_dict = dict()
        # Get all grades by that user
        user_dict['fullname'] = user_names[user_key]
        grades = get_grades(user_key) #######
        # Add grade values into the dictionary
        for grade_key in grades:
            user_dict[grade_key] = grades[grade_key]
        mark_dict[user_key] = user_dict
    table_headers = get_modified_headers()
    html_table_headers = ["Student Name", "Username"]
    for item in table_headers:
        html_table_headers.append(table_headers[item])
    message = request.args.get('message')
    return render_template('allstudentgrades.html', table_header = html_table_headers, mark_dict=mark_dict, users=get_users_and_names('s'),grades=get_modified_headers(), message=message)

# Function to change a student's grades
@app.route('/change_student_grade', methods=["GET", "POST"])
def change_student_grade():
    if session['sori'] == 's':
        return redirect(url_for('home'))
    elif session['sori'] == 'i':
        # This assumes all input values are legal
        if request.method == 'POST':
            student_user = request.form['student_user']
            assignment_to_change = request.form['grade_db_name']
            mark = request.form['changed_mark']
            # Update in database
            conn = sqlite3.connect('./assignment3.db')
            conn.execute('UPDATE studentMarks SET "{}" = ? WHERE username == ?'.format(assignment_to_change), [mark, student_user])
            conn.commit()
            conn.close()
            return redirect(url_for('allstudentgrades', message="success"))
        else:
            return redirect(url_for('grade_redirect'))
    else:
        return redirect(url_for('home')) 

@app.route('/studentfeedback', methods = ["GET", "POST"])
def studentfeedback():
    if "username" in session:
        if request.method == "POST":
            conn = sqlite3.connect('./assignment3.db')
            conn.execute('INSERT INTO feedback(username, q1, q2, q3, q4) VALUES (?, ?, ?, ?, ?)', [request.form["instructor"], request.form["comment1"], request.form["comment2"], request.form["comment3"], request.form["comment4"]])
            conn.commit()
            conn.close()
            #tell html we submitted the data
            return render_template('/studentfeedback_submitted.html')
        else:
            users = get_users_and_names("i")
            feedback = get_all_feedback_questions()
            questions = []
            for key in feedback.keys():
                temp = feedback[key]
                questions.append(temp[0])
            instructors = query_db('SELECT username FROM users WHERE sori = ?', ["i"])
            listOfInstructor = []
            for i in range(len(instructors)):
                listOfInstructor.append(instructors[i][0])
            return render_template('/studentfeedback.html', questions = questions, listOfInstructor = users)
    else:
        return redirect(url_for('login'))

# Helper Functions #
def appendToDb(data: list, name_db:str) -> None:
    '''
    Don't use this for any other table, excpt. remarks
    '''
    conn = sqlite3.connect('./assignment3.db')
    conn.execute('INSERT INTO ' + name_db +'(username, whichMark, explanation) VALUES (?, ?, ?)', [session['username']] + data)
    conn.commit()
    conn.close()



# Get all feedback submitted by students
def get_all_student_feedbacks(instructor_username):
    table_headers = get_table_headers("feedback")
     # Remove the username from the list of questions
    table_headers.remove("username")
    feedbacks = dict()
    for question in table_headers:
        responses = list()
        conn = sqlite3.connect('./assignment3.db')
        for response in conn.execute('SELECT "{}" FROM feedback WHERE username=?'.format(question), [instructor_username]):
            responses.append(response[0])
        conn.commit()
        feedbacks[question] = responses
    return feedbacks
        
def get_all_feedback_questions():
    return get_all_student_feedbacks("-1")

def get_fullname_by_user(username):
    fullname = str()
    conn = sqlite3.connect('./assignment3.db')
    for item in conn.execute('SELECT firstName, lastName FROM users WHERE username=?', [username]):
        fullname = item[0] + ' ' + item[1]
    return fullname

# Gets username and full name of a certain user type
def get_users_and_names(sori):
    if sori == "i" or sori == "s":
        user_first_last = dict()
        conn = sqlite3.connect('./assignment3.db')
        for result in conn.execute('SELECT username, firstName, lastName FROM users WHERE sori=?', [sori]):
            user_first_last[result[0]] = str(result[1]) + ' ' + str(result[2])
        conn.commit()
        return user_first_last

# Get all grades of a certain user
def get_grades(user:str):
    table_headers = get_table_headers("studentMarks")
    grade_by_user = dict()
    i = 0
    conn = sqlite3.connect('./assignment3.db')
    for result in conn.execute('SELECT * FROM studentMarks WHERE username=?', [user]):
        while i < 9:
            grade_by_user[table_headers[i]] = result[i]
            i = i + 1
    conn.commit()
    return grade_by_user

# Gets the table headers (column names) of a certain table
def get_table_headers(table):
    table_headers = []
    conn = sqlite3.connect('./assignment3.db')
    for result in conn.execute('PRAGMA table_info("{}")'.format(table)):
        table_headers.append(result[1])
    conn.commit()
    return table_headers

# Get modified headers of a table to make them look presentable
def get_modified_headers():
    conn = sqlite3.connect('./assignment3.db')
    modified_grade = dict()
    for result in conn.execute('SELECT * FROM header_modified'):
        modified_grade[result[0]] = result[1]
    conn.commit()
    return modified_grade
                
# @app.route('/studentgrades')
# def displayStudentGrade():
#     dic = get_grades(session['username'])
#     return render_template(dic)