# coding: utf-8

import os
from slackbot.bot import respond_to
import re
import psycopg2
from sqlalchemy.engine.url import make_url

db_url = make_url(os.getenv('DATABSE_URL'))

def connect_db():
    return psycopg2.connect(database = db_url.database, user = db_url.username, password = db_url.password, host = db_url.host, port = db_url.port)

@respond_to("^join (.*)", re.IGNORECASE)
def user_join(message, username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select id,username from users where username = %(username)s limit 1", {"username": username})
    row = cur.fetchone()
    if row is None:
        user = message._client.find_user_by_name(username)
        if user is None:
            message.reply("Not found user by username. Please check username.")
        else:
            cur.execute("insert into users (username, created_at) values (%(username)s, now())", {"username": username})
            conn.commit()
            message.reply("Joined!!")
    else:
        message.reply("Already joined.")

    conn.close()

@respond_to("^unjoin (.*)", re.IGNORECASE)
def user_unjoin(message, username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select id,username from users where username = %(username)s limit 1", {"username": username})
    row = cur.fetchone()
    if row is None:
        message.reply("Already unjoined.")
    else:
        cur.execute("delete from users where username = %(username)s", {"username": username})
        conn.commit()
        message.reply("Unjoined...")

    conn.close()
