
# Jun Jie Li (PM), Shafin Kazi, Lucas Zheng, Kyle Liu
# lowCortisol
# SoftDev pd4
# p04
# 2026-04-20m

from flask import Flask, render_template, request, session, redirect, url_for, flash
from auth import bp as auth_bp
import sqlite3, os, build_db

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = os.urandom(24)
DB_FILE = "oshi.db"

@app.route("/")
def home_get():
    # session['username'] = 'admin'
    if (session.get('username')):
        return render_template("home.html")
    flash("Please log in to use the website.", 'error')
    return(redirect(url_for("auth.login_get")))


if __name__ == "__main__":
    app.debug = True
    app.run()
