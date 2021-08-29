# Source Repo: https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)


def read_config():
    try:
        with open("config.json") as json_file:
            data = json.load(json_file)
            app.config['MYSQL_DATABASE_HOST'] = data['db_host']
            app.config['MYSQL_DATABASE_DB'] = data['db_name']
            temp = data['db_user'] + "@" + data['db_host']
            print("Temp: ", temp)
            app.config['MYSQL_DATABASE_USER'] = temp
            app.config['MYSQL_DATABASE_PASSWORD'] = data['db_pass']
            mysql.init_app(app)
            print("DB Data loaded from config.json: ", data)
    except IOError as err:
        print("IO Error: ", err)
    except:
        print("General Error")


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST','GET'])
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
            _hashed_password = _password
            cursor.execute("INSERT INTO tbl_user (user_name, user_username, user_password) VALUES (%s, %s, %s)", (_name, _email, _password))
            conn.commit()
            result_data = cursor.fetchall()
            print("Result:", result_data)

            if len(result_data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': str(result_data[0])})
            cursor.close()
            conn.close()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    read_config()
    app.run(port=3001)

