from flask import Flask, url_for, render_template, redirect, request, jsonify
import sqlite3
import random
import numpy as np
import pandas as pd
import json
conn = sqlite3.connect('database.db')
print("Opened database successfully")

#conn.execute('CREATE TABLE students (id int,total_people TEXT, m_name TEXT)')
print("Table created successfully")
conn.close()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/Upload"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/insert')
def ins():
    return render_template('ins.html')


@app.route('/update')
def upd():
    try:
        nm = request.form['pk']
        total_people = request.form['tp']
        m_namey = request.form['nm']

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Update students total_people=" + total_people +
                        " and m_namey=" + m_namey + "where id=" + id)

            con.commit()

    except:
        con.rollback()

    finally:
        con.close()

        return render_template("ins.html")


@app.route('/delete')
def dele():
    try:
        nm = request.form['pk']

        with sqlite3.connect("database.db") as cond:
            cur = cond.cursor()
            cur.execute("DELETE FROM students WHERE id=" + int(nm))
            cond.commit()

    except:
        print("Rollback")
        cond.rollback()

    finally:
        cond.close()
        return redirect('/list')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = random.randint(1, 999999999)
            total_people = request.form['tp']
            m_namey = request.form['nm']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO students (id,total_people,m_name) VALUES (?,?,?)",
                    (nm, total_people, m_namey))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("ins.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("upd.html", rows=rows)


@app.route('/csv')
def concsv():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    df = pd.DataFrame.from_records(rows)
    export_csv = df.to_csv('data.csv')
    return render_template("ins.html")


@app.route('/json')
def conjson():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    items = []
    for i in rows:
        items.append({'id': i[0], 'total_people': i[1], 'movie_name': i[2]})

    return json.dumps({'items': items})


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
