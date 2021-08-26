from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import werkzeug

mysql = MySQL()
app = Flask(__name__)

# Here we need to replace these config settings
# With ones retrieved from a file
# MySQL configurations

'localhost'
mysql.init_app(app)


def read_config():
    try:
        with open("config.json") as json_file:
            data = json.load(json_file)
            app.config['MYSQL_DATABASE_HOST'] = data['db_host']
            app.config['MYSQL_DATABASE_DB'] = data['db_name']
            app.config['MYSQL_DATABASE_USER'] = data['db_user']
            app.config['MYSQL_DATABASE_PASSWORD'] = data['db_pass']
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


@app.route('/signUp',methods=['POST','GET'])
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
            _hashed_password = werkzeug.generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


if __name__ == "__main__":
    read_config()
    app.run(port=3001)

