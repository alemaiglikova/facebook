import datetime
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')


@app.route('/posts/create', methods=['GET', 'POST'])
def post_create():
    if request.method == "GET":
        return render_template("post_create.html")
    elif request.method == "POST":
        title = str(request.form.get("title")).strip()
        description = str(request.form.get("description")).strip()
        date_create = datetime.datetime.now()  # timestamp
        status = "true" if request.form.get("status") is not None else "false"

        if len(title) < 5:
            raise Exception("title is too small")
        with psycopg2.connect(user="facebook_usr", password="12345Qwerty!",
                              host="127.0.0.1", port="5432", dbname="facebook_db") as connection:
            connection.autocommit = False
            with connection.cursor() as cursor:  # syntax sugar
                try:
                    cursor.execute(f"insert into posts "
                                   f"(title, description, date_created, status) values "
                                   f"('{title}', '{description}', '{date_create}','{status}');")
                except Exception as error:
                    print("error: ", error)
                    cursor.rollback()
                else:
                    cursor.commit()
                finally:
                    return redirect(url_for("posts"))
    else:
        raise Exception("Method not allowed")
