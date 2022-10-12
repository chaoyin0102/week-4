from re import template
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect

# for secret key
import os

app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/"
)

# create the secret key (generate random string)
app.secret_key = os.urandom(20)

# account:test, password:test
user={"account": "test", "password": "test"}

# homepage
@app.route("/")
def home():
    return render_template("home.html")

# /signin
@app.route("/signin", methods=["POST"])
def signin():
    # get account and password from form by POST
    account = request.form["account"]
    password = request.form["password"]

    # 確認帳號密碼是否正確
    if (account == user["account"] and password == user["password"]):
        session["username"] = account #save account name in session
        return redirect("/member")
    # if without account or password
    elif (account == "" or password == ""):
        return redirect("/error?message=帳號與密碼皆需要輸入")
    # if account or password is wrong
    else:
        return redirect("/error?message=帳號、或密碼輸入錯誤")

# /member
@app.route("/member")
def member():
    # if user has signed in
    if ("username" in session and session["username"] == user["account"]):
        return render_template("member.html")

# /error
@app.route("/error")
def error():
    # get query string of message
    message = request.args.get("message")
    # show message on error page
    return render_template("error.html", message = message)

# /back
@app.route("/back")
def back():
    return redirect("/")

# /signout
@app.route("/signout")
def signout():
    session.pop("username")
    return redirect("/")

app.run(port = 3000)