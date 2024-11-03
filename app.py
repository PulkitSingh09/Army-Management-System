import dataclasses
from flask import Flask,render_template,request,redirect,url_for,flash
from os.path import join, dirname
import mysql.connector
app = Flask(__name__)
  
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  password ="enter",
  database ="army_database"
)

cursor= dataBase.cursor()

@app.route('/')
def home():
    return render_template("sign_in.html")

@app.route('/SIGN_IN',methods=["POST","GET"])
def SIGN_IN():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    cursor.execute(f"insert into credentials (username,password) values ('{username}','{password}')")
    dataBase.commit()
    return redirect('/')


@app.route('/login',methods=["POST","GET"])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor.execute(f"select password from credentials where username='{username}'")
    paswrd = cursor.fetchall()[0][0]
    if password==paswrd:
      return redirect('/main')
    else:
      return redirect('/error')

  else:
    return render_template('login.html')

@app.route('/main')
def main():
  return render_template('main.html')

@app.route('/error')
def error():
  return render_template('error.html')

@app.route('/Soldier_Details',methods=["POST","GET"])
def soldier():
  if request.method == 'POST':
    name = request.form['name']
    age = request.form['age']
    rank = request.form['rank']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    contact_number = request.form['contact_number']
    cursor.execute(f"insert into soldier (name,age,post,date_of_birth,address,contact_number) values ('{name}', {age}, '{rank}', '{date_of_birth}', '{address}', {contact_number})")
    dataBase.commit()
    cursor.execute('select * from soldier')
    data = cursor.fetchall()
    return render_template('soldier.html', data=data)
  else:
    cursor.execute('select * from soldier')
    data = cursor.fetchall()
    return render_template('soldier.html', data=data)

@app.route('/about',methods=["POST","GET"])
def about():
  return render_template('about.html')


@app.route('/delete/<id>', methods=['GET'])
def delete_soldier(id):
    cursor.execute(f"DELETE FROM soldier WHERE id='{id}'")
    dataBase.commit()
    return redirect('/Soldier_Details')



@app.route('/update/<id>', methods=['POST', 'GET'])
def update_soldier(id):
    if request.method == "GET":
      cursor.execute(f"SELECT * FROM soldier WHERE id='{id}'")
      data = cursor.fetchall()
      return render_template('update.html', data=data)
    else:
      name = request.form['name']
      age = request.form['age']
      rank = request.form['rank']
      date_of_birth = request.form['date_of_birth']
      address = request.form['address']
      contact_number = request.form['contact_number']
      cursor.execute("UPDATE soldier SET name=%s, age=%s, post=%s, date_of_birth=%s, address=%s, contact_number=%s WHERE id=%s", (name, age, rank, date_of_birth, address, contact_number, id))
      dataBase.commit()
      return redirect('/Soldier_Details')


@app.route('/edit', methods=['POST'])
def edit():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    rank = request.form['rank']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    contact_number = request.form['contact_number']
    cursor.execute("UPDATE soldier SET name=%s, age=%s, post=%s, date_of_birth=%s, address=%s, contact_number=%s WHERE id=%s", (name, age, rank, date_of_birth, address, contact_number, id))
    dataBase.commit()
    return render_template('edit.html')


def reseq(table_name):
    post_id = []
    cursor.execute('select id from {}'.format(table_name))
    for id in cursor.fetchall():
        post_id.append(id[0])

    if post_id:
        max_id = max(post_id)
    else:
        max_id = 0

    cursor.execute('alter sequence {}_id_seq restart with {}'.format(
        table_name, max_id + 1))    


if __name__ == '__main__':
    app.run(debug=True,port=5000)
