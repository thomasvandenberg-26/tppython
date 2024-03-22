from flask import Flask, request, redirect, url_for, session;
from flask import render_template; 
import sqlite3
from flask import g
import os
from pathlib import Path

   
DATABASE = 'ideas.db'
app = Flask(__name__)

app.secret_key ='ok'; 
## Routes to get the differentes views of my application

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

## i send the login page
@app.route("/login")
def login():
    return render_template('login.html')

## i send the ideas table 
@app.route("/tableIdea/<user_id>")
def tableIdea(user_id):
    ## i query the database ideas table
    ideas= returnIdeas(format(user_id))
    return render_template('tableIdeas.html',ideas=ideas)

## i call the function to sort the ideas with the number of the desire
@app.route("/sortedIdeas/<user_id>")
def sortedIdeas(user_id):
    ## i query the database ideas table to sort the data
    ideas = sortByDesire(format(user_id))
    return render_template('tableIdeas.html',ideas=ideas)

        
@app.route('/formIdea/<user_id>')
def formIdea(user_id):
    if session.get('logged_in'):    
        return render_template('formIdeas.html', format(user_id))
    else:
        return redirect(url_for('login'))


## Method to create a function to post idea into the bdd
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
if not Path(DATABASE).exists():
    with app.app_context():
        db = get_db()
        sql = Path('ideas.sql').read_text()
        db.cursor().executescript(sql)
        db.commit()

#method to threat the form id
@app.route('/submit/<user_id>', methods=['POST'])

def submit(user_id):
    if request.method == 'POST':
        name = request.form.get('Name')
        description = request.form.get('Description')
        desire = request.form.get('Desire')
        category = request.form.get('Category')
        needed = request.form.get('Needed')
        if needed.lower() == "yes":
            needed = 1
        elif needed.lower() == "no":
            needed = 0
# Initialiser la base de données si nécessaire
            
# Insérer les données dans la table IDEAS
        db = get_db()

        queryInsert = 'INSERT INTO IDEAS (Name, Description, Desire, Category, Needed, user_id) VALUES (?, ?, ?, ?, ?, ?);'
     
      
        query_db(queryInsert, [name, description, desire, category, needed,user_id] )
        # Sélectionner et afficher les données insérées
      
        db.commit()
        return redirect(url_for('tableIdea', user_id=user_id))
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if one:
        return (rv[0] if rv else None)
    else:
        return rv

## return ideas of the user id (username)
def returnIdeas(id):
    queryCheckIdeas = 'SELECT Name, Description, Desire, Category, Needed FROM IDEAS Where user_id = ?'
    result = query_db(queryCheckIdeas, id)
    return result

# i sort table with the desire, i sort with the most important ideas
def sortByDesire(user_id):
    querySort = 'SELECT Name, Description, Desire, Category, Needed, user_id FROM IDEAS Where user_id = ? ORDER BY Desire DESC  '
    result = query_db(querySort, [user_id])
    return result

## connection
def connection(username, password):
    query = 'SELECT Username, Password FROM Users WHERE Username = ? and Password = ?;'
    result = query_db(query, [username, password], one=True)
    if result:
        session['logged_in'] = True
        session['username='] = username
        
    else:
        return "cet utilisateur n'existe pas"

## is the function which get the password and username from the login form 
@app.route('/connection', methods=['GET','POST'])   
def processLoginForm():
    if request.method == 'POST':
        username= request.form.get('Username')
        password = request.form.get('Password')
        if username and password: 
            connection(username, password)
            user_id = getIdUser(username)
        if user_id:
            return render_template('formIdeas.html', user_id=user_id)
        else:
            return "user not find"

    else:
        return redirect(url_for('login'))
## its the logout  function
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('login'))

def getIdUser(username):
    
    db = get_db()
    cursor = db.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user[0]
    else:
        return None