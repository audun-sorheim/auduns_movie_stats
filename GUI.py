from flask import Flask, render_template, request, redirect, url_for, flash
import gender_guesser.detector as gg
import pandas as pd
from add_movie import write_rated_row, write_all_row, write_rated_metadata_row, write_all_metadata_row, add_name_to_gender_registry
from get_metadata import fetch_metadata

app = Flask(__name__)
app.secret_key = "secret12355"  # needed for flash messages

@app.route("/update_gender", methods=["POST"])
def update_gender():

    name = request.form["name"]
    category = request.form["category"]
    gender = request.form["gender"]

    path = f"gender_registry/{category[:-1]}_gender_registry.csv"

    df = pd.read_csv(path)

    df.loc[df["name"] == name, "gender"] = gender

    df.to_csv(path, index=False)

    flash(f"Updated gender for {name}")

    return redirect(url_for("review"))

@app.route("/review")
def review():

    paths = {
        "directors": r"gender_registry\director_gender_registry.csv",
        "writers": r"gender_registry\writer_gender_registry.csv",
        "composers": r"gender_registry\composer_gender_registry.csv"
    }

    unknown_entries = []

    for category, path in paths.items():
        df = pd.read_csv(path)

        unknowns = df[df["gender"] == "unknown"]

        for _, row in unknowns.iterrows():
            unknown_entries.append({
                "category": category,
                "name": row["name"]
            })

    return render_template("review.html", unknown_entries=unknown_entries)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dir = request.form["user_dir"]
        film_name = request.form["film_name"]
        film_year = request.form["film_year"]
        rating = request.form["rating"]
        imdb_id = request.form["imdb_id"]
        confirm_all = request.form.get("confirm_all")
        confirm_rated = request.form.get("confirm_rated")
        metadata = fetch_metadata(imdb_id)
        country = metadata["OriginCountry"]
        gender_detector = gg.Detector()
        unknown_count = 0

        directors = metadata['Directors'].split(', ')
        for name in directors:
            if add_name_to_gender_registry(name, country, r"gender_registry\director_gender_registry.csv", gender_detector):
                unknown_count += 1

        writers = metadata['Writers'].split(', ')
        for name in writers:
            if add_name_to_gender_registry(name, country, r"gender_registry\writer_gender_registry.csv", gender_detector):
                unknown_count += 1

        composers = metadata['Composers'].split(', ')
        for name in composers:
            if add_name_to_gender_registry(name, country, r"gender_registry\composer_gender_registry.csv", gender_detector):
                unknown_count += 1

        if confirm_all == "yes":
            write_all_row(film_name, film_year, imdb_id, dir)
            write_all_metadata_row(film_name, film_year, imdb_id, metadata, dir)
            flash(f"{film_name} written to all CSVs for {dir} ✅")
        if confirm_rated == "yes":
            write_rated_row(film_name, film_year, rating, imdb_id, dir)
            write_rated_metadata_row(film_name, film_year, rating, imdb_id, metadata, dir)
            flash(f"{film_name} written to rated CSVs for {dir} ✅")
        else:
            flash(f"You decided not to write {film_name}.")

        if unknown_count > 0:
            flash(f"{unknown_count} new names need gender verification. Visit /review to fix them ⚠️")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
