from flask import Flask, render_template, request, redirect, url_for, flash
from add_movie import write_rated_row, write_all_row, write_rated_metadata_row, write_all_metadata_row
from get_metadata import fetch_metadata

app = Flask(__name__)
app.secret_key = "secret123"  # needed for flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        film_name = request.form["film_name"]
        film_year = request.form["film_year"]
        rating = request.form["rating"]
        imdb_id = request.form["imdb_id"]
        confirm = request.form.get("confirm")

        if confirm == "yes":
            write_rated_row(film_name, film_year, rating, imdb_id)
            write_all_row(film_name, film_year, imdb_id)
            metadata = fetch_metadata(imdb_id)
            write_rated_metadata_row(film_name, film_year, rating, imdb_id, metadata)
            write_all_metadata_row(film_name, film_year, imdb_id, metadata)
            flash(f"{film_name} written to CSVs ✅")
        else:
            flash(f"You decided not to write {film_name}.")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
