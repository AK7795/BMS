from flask import Flask, render_template,request
import sqlite3

from werkzeug.utils import redirect

app1 = Flask(__name__)

con = sqlite3.connect("bookmngsys.db",check_same_thread=False)

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKS' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")

else:
    con.execute(''' CREATE TABLE BOOKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BOOKNAME TEXT,
    AUTHOR TEXT,
    CATEGORY TEXT,
    PRICE TEXT,
    PUBLISHER TEXT); ''')
    print("Table has created")


@app1.route("/")
def home():
    return render_template("home.html")


@app1.route("/userreg")
def reg():
    return render_template("regis.html")


@app1.route("/adminlogin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "admin":
            if getppass == "9875":
                return redirect("/bookentry")
    return render_template("login.html")


@app1.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getBOOKName = request.form["bname"]
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM BOOKS WHERE BOOKNAME = '"+getBOOKName+"' ")
        res2 = cur2.fetchall()
        return render_template("searchview.html", books2=res2)
    return render_template("search.html")


@app1.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "POST":
        getNewname = request.form["newname"]
        getNewAuthor = request.form["newauthor"]
        getNewCategory = request.form["newcat"]
        getNewPrice = request.form["newprice"]
        getNewPublisher = request.form["newpub"]
        con.execute("UPDATE BOOKS SET BOOKNAME = '"+getNewname+"',AUTHOR = '"+getNewAuthor+"',CATEGORY ='"+getNewCategory+"',PRICE = '"+getNewPrice+"',PUBLISHER = '"+getNewPublisher+"'  ")
        print("successfully Updated !")
        con.commit()
        return redirect("/viewall")
    return render_template("edit.html")


@app1.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        getNAMEDEL = request.form["namedel"]
        cur3 = con.cursor()
        cur3.execute("DELETE FROM BOOKS WHERE BOOKNAME = '"+getNAMEDEL+"' ")
    return render_template("delete.html")


@app1.route("/viewall")
def view():
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKS")
    res = cur.fetchall()
    return render_template("viewall.html", bookss=res)


@app1.route("/cardview")
def cardview():
    cur3 = con.cursor()
    cur3.execute("SELECT * FROM BOOKS")
    res6 = cur3.fetchall()
    return render_template("cardview.html", books3=res6)


@app1.route("/bookentry", methods=["GET", "POST"])
def entry():
    if request.method == "POST":
        getBookName = request.form["name"]
        getAuthor = request.form["author"]
        getCategory = request.form["cat"]
        getPrice = request.form["price"]
        getPublisher = request.form["pub"]
        print(getBookName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        try:
            con.execute("INSERT INTO BOOKS(BOOKNAME,AUTHOR,CATEGORY,PRICE,PUBLISHER) VALUES('"+getBookName+"','"+getAuthor+"','"+getCategory+"','" +getPrice+"','"+getPublisher+"')")
            print("successfully inserted !")
            con.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)
    return render_template("bookentry.html")


if __name__ == "__main__":
    app1.run()
