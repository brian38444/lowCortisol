# Jun Jie Li (PM), Shafin Kazi, Lucas Zheng, Kyle Liu
# lowCortisol
# SoftDev pd4
# p04
# 2026-04-20m

from flask import Flask, render_template, request, session, redirect, url_for, flash
from auth import bp as auth_bp
import sqlite3, os, build_db, download_datasets, loader

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = "secretkey"
DB_FILE = "oshi.db"

@app.route("/")
def disp_homepage():
    if session.get("username"):
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()
        vtubers = cursor.execute("""
            SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count
            FROM vtubers
            WHERE channel_id IN (
                SELECT channel_id FROM favorites WHERE username = ?
            )
            ORDER BY channel_name
        """, (session["username"],)).fetchall()
        db.close()
        return render_template("home.html", vtubers=vtubers)
    else:
        return redirect(url_for("auth.login_get"))
    
@app.route("/profile/<channel_id>/favorite", methods=["POST"])
def toggle_favorite(channel_id):
    if session.get("username"):
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()
        if cursor.execute("""SELECT 1 FROM favorites WHERE username=? AND channel_id=?""", (session["username"], channel_id)).fetchone():
            cursor.execute("""DELETE FROM favorites WHERE username=? AND channel_id=?""", (session["username"], channel_id))
        else:
            cursor.execute("""INSERT INTO favorites VALUES (?, ?)""", (session["username"], channel_id))
        db.commit()
        db.close()
        return redirect(url_for("disp_profile", channel_id=channel_id))
    else:
        return redirect(url_for("auth.login_get"))
    
@app.route("/quiz")
def disp_quiz():
    if session.get("username"):
        return render_template("quiz.html")
    else:
        return redirect(url_for("auth.login_get"))
    
@app.route("/browse")
def disp_browse():
    if session.get("username"):
        filter = request.args.get("filter", "all")
        q = request.args.get("q", "").strip()
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()

        agencies = cursor.execute(
            "SELECT DISTINCT agency FROM vtubers WHERE agency IS NOT NULL ORDER BY agency"
        ).fetchall()

        all_vtubers = cursor.execute(
            "SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count FROM vtubers ORDER BY channel_name"
        ).fetchall()

        if filter != "all" and q:
            vtubers = cursor.execute(
                "SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count FROM vtubers WHERE agency = ? AND channel_name LIKE ? ORDER BY channel_name",
                (filter, f"%{q}%")
            ).fetchall()
        elif filter != "all":
            vtubers = cursor.execute(
                "SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count FROM vtubers WHERE agency = ? ORDER BY channel_name",
                (filter,)
            ).fetchall()
        elif q:
            vtubers = cursor.execute(
                "SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count FROM vtubers WHERE channel_name LIKE ? ORDER BY channel_name",
                (f"%{q}%",)
            ).fetchall()
        else:
            vtubers = cursor.execute(
                "SELECT channel_id, channel_name, profile_image_url, agency, total_subscriber_count FROM vtubers ORDER BY channel_name"
            ).fetchall()

        db.close()
        return render_template("browse.html", vtubers=vtubers, all_vtubers=all_vtubers, agencies=agencies, filter=filter, q=q)
    else:
        return redirect(url_for("auth.login_get"))
    

@app.route("/profile/<channel_id>")
def disp_profile(channel_id):
    if session.get("username"):
        db = sqlite3.connect(DB_FILE)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
    
        vtuber = cursor.execute(
            "SELECT * FROM vtubers WHERE channel_id = ?", (channel_id,)
        ).fetchone()
    
        if not vtuber:
            db.close()
            return "VTuber not found"
    
        chats = cursor.execute(
            "SELECT * FROM chats WHERE channel_id = ? ORDER BY period", (channel_id,)
        ).fetchall()
    
        superchats = cursor.execute(
            "SELECT * FROM superchats WHERE channel_id = ? ORDER BY period", (channel_id,)
        ).fetchall()
    
        comments = cursor.execute(
            """SELECT c.desc, c.username FROM comments c WHERE c.channel_id = ? ORDER BY c.comment_id DESC""",
            (channel_id,)
        ).fetchall()

        result = cursor.execute(
            """SELECT 1 FROM favorites WHERE username=? AND channel_id=?""",
            (session["username"], channel_id)
        ).fetchone()
        is_favorite = result is not None
    
        db.close()
        return render_template("profile.html", vtuber=vtuber, chats=chats, superchats=superchats, comments=comments, is_favorite=is_favorite)
    else: 
        return redirect(url_for("auth.login_get"))
 
 
@app.route("/profile/<channel_id>/comment", methods=["POST"])
def post_comment(channel_id):
    if session.get("username"):
        desc = request.form.get("desc", "").strip()
        if desc:
            db = sqlite3.connect(DB_FILE)
            db.execute(
                "INSERT INTO comments (channel_id, username, desc) VALUES (?, ?, ?)",
                (channel_id, session["username"], desc),
            )
            db.commit()
            db.close()
        return redirect(url_for("disp_profile", channel_id=channel_id))
    else:
        return redirect(url_for("auth.login_get"))


if __name__ == "__main__":
    app.debug = True
    app.run()
