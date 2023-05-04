from flask import Flask, render_template, request, session, redirect, url_for

import Queue
import Search
import secrets
from math import ceil

app = Flask(__name__)
app.secret_key = secrets.token_bytes(256)

skip_count = 0
user_count = 0
users = []
voted = []


@app.route('/', methods=["GET", "POST"])
def login():
    global user_count
    global users
    if request.method == "POST":
        if request.form['username'] not in users:
            session['username'] = request.form['username']
            user_count += 1
            users.append(session['username'])
            print("USER COUNT =", user_count)
            print("USERS:", users)
            print("SKIP COUNT =", skip_count)
            return redirect(url_for("search"))
    return render_template("login.html", title="Login")


@app.route('/logout')
def logout():
    global user_count
    global users
    global skip_count
    user_count -= 1
    users.remove(session['username'])
    print("USER COUNT =", user_count)
    print("USERS:", users)
    print("SKIP COUNT =", skip_count)
    session.pop('username', None)
    return redirect(url_for("login"))


@app.route('/search', methods=['GET', 'POST'])
def search():  # put application's code here
    global user_count
    global skip_count
    global users
    global voted
    print("USER COUNT =", user_count)
    print("USERS:", users)
    print("SKIP COUNT =", skip_count)
    print("VOTED =", voted)
    if 'username' not in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        if request.form['title']:
            song_title = request.form['title']
            search_manager = Search.Search()
            tracks = search_manager.get_tracks(song_title)
            return render_template("index.html", search_results=tracks, title="GroupListen", user_count=user_count,
                                   skip_count=skip_count)
    else:
        return render_template("index.html", title="GroupListen", user_count=user_count, skip_count=skip_count)


@app.route("/queue", methods=['GET', 'POST', 'PUT'])
def queue():
    global user_count
    global skip_count
    global users
    print("USER COUNT =", user_count)
    print("USERS:", users)
    print("SKIP COUNT =", skip_count)
    if 'username' not in session:
        return redirect(url_for("login"))
    qm = Queue.Queue()
    title = "Queue"
    try:
        if request.method == 'POST':
            toast = "Added to queue successfully"
            if not qm.add_to_queue(request.form['uri']):
                toast = "Error: Failed to add to queue, please try again"
            return render_template("index.html", toast=toast, title="GroupListen", user_count=user_count,
                                   skip_count=skip_count)
        else:
            current_queue = qm.get_queue()
            return render_template("queue.html", current_queue=current_queue, title=title)
    except Exception as err:
        print("ERROR", err)
        current_queue = qm.get_queue()
        return render_template("queue.html", title=title, current_queue=current_queue)


@app.route("/skip")
def skip():
    global skip_count
    global user_count
    global users
    global voted
    print("USER COUNT =", user_count)
    print("USERS:", users)
    print("SKIP COUNT =", skip_count)
    print("VOTED:", voted)
    if 'username' not in session:
        return redirect(url_for("login"))

    if session['username'] not in voted:
        skip_count += 1
        voted.append(session['username'])
    if skip_count >= ceil(user_count / 2):
        qm = Queue.Queue()
        qm.skip()
        skip_count = 0
        voted = []

    return redirect(url_for("search"))


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("login")), 404


@app.errorhandler(500)
def server_error(error):
    print("[SERVER ERROR]", error)
    return redirect(url_for("login")), 500


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=False)
