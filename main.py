from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection, CursorResult

app = Flask("Article_site")


def connection_to_database_article():
    path_to_database: str = "C:\\Users\\capit\\Desktop\\Coding\\articles.db"
    engine: Engine = create_engine(f"sqlite:///{path_to_database}")
    connection: Connection = engine.connect()
    return connection


@app.route("/")
def home():
    connection = connection_to_database_article()
    cursor_to_result: CursorResult = connection.execute("""
    SELECT Title, Id 
    FROM Articles;
    """)
    list_with_article_titles: list[tuple] = cursor_to_result.fetchall()
    connection.close()

    return render_template("home.html", list_with_article_titles=list_with_article_titles)


@app.route("/single_article")
def single_article():
    id = request.args["id"]
    connection = connection_to_database_article()
    cursor_to_result: CursorResult = connection.execute("""
    SELECT Title,  Content, Publish_date
    FROM Articles
    WHERE ID = ?;
    """, id)

    data_for_single_article: tuple = cursor_to_result.fetchone()

    connection.close()

    # TODO: Easier way to pass arguments

    return render_template("single_article.html", data_for_single_article=data_for_single_article, id=id)


@app.route("/create_new_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template("create_article.html")

    else:
        title = request.form["title"]
        content = request.form["content"]
        publish_date = request.form["publish_date"]

        connection = connection_to_database_article()
        connection.execute("""
        INSERT INTO "Articles" (Title, Content, Publish_date)
        VALUES(?,?,?);
        """, title, content, publish_date)

        connection.close()
        return redirect("/")


@app.route("/update_article", methods=["GET", "POST"])
def update_article():
    if request.method == "GET":

        id = request.args["id"]

        connection = connection_to_database_article()
        cursor_result: CursorResult = connection.execute("""
        SELECT Title, Content, Publish_date
        FROM Articles
        WHERE Id = ?;
        """, id)

        list_with_article: tuple = cursor_result.fetchone()

        connection.close()

        return render_template("update_article.html", list_with_article=list_with_article, id=id)

    else:

        id = request.form["id"]
        title = request.form["title"]
        content = request.form["content"]
        publish_date = request.form["publish_date"]

        connection = connection_to_database_article()
        connection.execute("""
        UPDATE Articles
        SET Title = ?, Content = ?, Publish_date = ?
        WHERE Id = ?;
        """, title, content, publish_date, id)

        connection.close()

        return redirect(f"/single_article?id={id}")


@app.route("/delete_article")
def delete_article():

    id = request.args["id"]

    connection = connection_to_database_article()
    connection.execute("""
    DELETE FROM Articles
    WHERE Id = ?;
    """, id)

    return redirect("/")


app.run("localhost", 80, True)
