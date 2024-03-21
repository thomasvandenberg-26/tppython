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
@app.route("/tableauIdees")
def tableauIdees():
    ## i query the database ideas table
    ideas= returnIdeas()
    return render_template('tableauIdees.html',ideas=ideas)

## i call the function to sort the ideas with the number of the desire
@app.route("/sortedIdeas")
def sortedIdeas():
    ## i query the database ideas table to sort the data
    ideas = sortByDesire()
    return render_template('tableauIdees.html',ideas=ideas)

        
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
@app.route('/submit/<user_id>', methods=['GET'])

def submit(user_id):
    if request.method == 'GET':
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

        queryInsert = 'INSERT INTO IDEAS (Name, Description, Desire, Category, Needed WHERE user_id = ?) VALUES (?, ?, ?, ?, ?);'
     
      
        query_db(queryInsert, [user_id,name, description, desire, category, needed] )
        # Sélectionner et afficher les données insérées
      
        db.commit()
        return redirect(url_for('tableauIdees'))
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

## return ideas of the user id (username)
def returnIdeas(id):
    queryCheckIdeas = 'SELECT Name, Description, Desire, Category, Needed FROM IDEAS Where user_id = ?'
    result = query_db(queryCheckIdeas, id)
    return result

# i sort table with the desire, i sort with the most important ideas
def sortByDesire():
    querySort = 'SELECT Name, Description, Desire, Category, Needed FROM IDEAS ORDER BY Desire DESC'
    result = query_db(querySort)
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
            return redirect(url_for('formIdea', user_id=user_id ))
        else:
            return "user not find"

    else:
        return redirect(url_for('login'))
## its the logout  function
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('login'))

def getIdUser(username):
    query = 'SELECT id FROM USERS where Username = ? '
    result = query_db(query, [username] )
    if result:
        return result[0]['id']
    else:
        return None 
    
