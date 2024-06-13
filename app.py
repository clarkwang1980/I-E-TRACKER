from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    if not os.path.exists('data.db'):
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    description TEXT,
                    amount REAL,
                    type TEXT
                )
            ''')
            conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        entry_type = request.form['type']
        
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO entries (date, description, amount, type) VALUES (?, ?, ?, ?)', 
                      (date, description, amount, entry_type))
            conn.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_entry.html')

@app.route('/view')
def view_entries():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, date, description, amount, type FROM entries')
        entries = c.fetchall()
    return render_template('view_entries.html', entries=entries)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        entry_type = request.form['type']

        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE entries SET date = ?, description = ?, amount = ?, type = ? WHERE id = ?', 
                      (date, description, amount, entry_type, id))
            conn.commit()
        
        return redirect(url_for('view_entries'))
    
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT date, description, amount, type FROM entries WHERE id = ?', (id,))
        entry = c.fetchone()
    
    return render_template('edit_entry.html', entry=entry, id=id)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
