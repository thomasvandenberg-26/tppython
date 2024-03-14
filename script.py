from flask import Flask, request, redirect, url_for;
from flask import render_template; 
import sqlite3
from flask import g
import os
from pathlib import Path

   
DATABASE = 'ideas.db'
app = Flask(__name__)

## Routes to get the differentes views of my application

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/tableauIdees")
def tableauIdees():
    ideas= returnIdeas()
    return render_template('tableauIdees.html',ideas=ideas)

@app.route("/sortedIdeas")
def sortedIdeas():
    ideas = sortByDesire()
    return render_template('tableauIdees.html',ideas=ideas)

        
@app.route('/formIdea')
def formIdea():
    return render_template('formIdeas.html')


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


@app.route('/submit', methods=['POST'])

def submit():
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

        queryInsert = 'INSERT INTO IDEAS (Name, Description, Desire, Category, Needed) VALUES (?, ?, ?, ?, ?);'
     
      
        query_db(queryInsert, [name, description, desire, category, needed] )
        # Sélectionner et afficher les données insérées
      
        db.commit()
        return redirect(url_for('tableauIdees'))
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def returnIdeas():
    queryCheckIdeas = 'SELECT Name, Description, Desire, Category, Needed FROM IDEAS;'
    result = query_db(queryCheckIdeas)
    return result

# i sort table with the desire, i sort with the most important ideas
def sortByDesire():
    querySort = 'SELECT Name, Description, Desire, Category, Needed FROM IDEAS ORDER BY Desire DESC'
    result = query_db(querySort)
    return result