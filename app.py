from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from simplexml import dumps
import yaml
from flask_accept import accept
from requests import get
import sqlite3
import traceback
import sys
from os import path
import re

app = Flask(__name__)

app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per hour", "5 per minute"]
)

DATABASE = path.realpath(path.join(path.dirname(__file__), 'db', 'ips.db'))


@app.route("/", methods=["GET"])
@accept('text/html')
def home():
    ips = get_data()
    return render_template('home.html', ips=ips), 200


@home.support('text/plain')
def home_txt():
    ips = get_data()
    return f"public_ip: {ips['public']}\nlocal_ip: {ips['local']}\npublic_ips: {ips['public_ips']}\nlocal_ips: {ips['local_ips']}"


@home.support('application/json')
def home_json():
    ips = get_data()
    return jsonify(public_ip=ips['public'], local_ip=ips['local'], public_ips=ips['public_ips'], local_ips=ips['local_ips'])


@home.support('application/xml')
def home_xml():
    ips = get_data()
    return dumps({'response' : ips})


@home.support('application/x-yaml')
def home_yaml():
    ips = get_data()
    return yaml.dump(ips)


def get_db():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()

    # cur.execute("drop table if exists public_ips;")
    # cur.execute("drop table if exists local_ips;")
    # cur.execute("drop table if exists test_ips;")

    cur.execute("create table if not exists public_ips (id integer primary key autoincrement, address text unique, time_accessed timestamp default (datetime('now','localtime')));")
    cur.execute("create table if not exists local_ips (id integer primary key autoincrement, address text unique, time_accessed timestamp default (datetime('now','localtime')));")
    
    db.commit()

    return db, cur

def get_data():
    db, cur = get_db()

    public_ip = get('https://api.ipify.org').text
    local_ip = request.remote_addr

    insert(db, cur, "public_ips", (public_ip,))
    insert(db, cur, "local_ips", (local_ip,))

    ips = {
        'public': public_ip,
        'local': local_ip,
        'public_ips': query_all(cur, "public_ips"),
        'local_ips': query_all(cur, "local_ips")
    }

    db.close()

    return ips


def query_all(cur, table):
    query = f"select * from {table};"
    cur.execute(query)
    results = cur.fetchall()

    table_data = []
    for result in results:
        table_data.append({
            'ID': result[0],
            'IP': result[1],
            'time_accessed': result[2]
        })
    
    return table_data


def insert(db, cur, table, arguments):    
    try:
        command = f"insert into {table} (address) values(?);"
        cur.execute(command, arguments)
        db.commit()
    except sqlite3.Error as er:
        if re.search("UNIQUE constraint failed: ", er.args[0]):
            print(f"This particular IP address ({arguments[0]}) has accesed the webapp in the past and can't be added to the {table} table again.")
        else:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


@app.teardown_appcontext
def close_connection(exception):
    db = sqlite3.connect(DATABASE)
    db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
