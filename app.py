from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            checkin TEXT NOT NULL,
            checkout TEXT NOT NULL,
            room_type TEXT NOT NULL

        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        name = request.form['name']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        room_type = request.form['room_type']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute('''
           INSERT INTO reservations (name, checkin, checkout, room_type)
           VALUES (?,?,?,?)
        ''',(name,checkin,checkout,room_type))

        conn.commit()
        conn.close()

        return render_template('confirmation.html',
                                name=name,
                                checkin=checkin,
                                checkout=checkout,
                               room_type=room_type)

    return render_template('reservation.html')

@app.route('/manager')
def manager():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('SELECT name, checkin, checkout, room_type FROM reservations')
    rows = cur.fetchall()

    conn.close()
    
    reservations = [{'name': r[0], 'checkin': r[1], 'checkout': r[2], 'room_type': r [3]} for r in rows]
    return render_template('reservations.html', reservations = reservations)

if __name__ == '__main__':

    app.run(debug=True)

