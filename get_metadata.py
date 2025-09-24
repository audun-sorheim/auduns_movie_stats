import requests
import pandas as pd
import tqdm

TMDB_API_KEY = "c4e8c4ca2a6f4c6411dc47aca067218f"
OMDB_API_KEY = "7a043e00"

def fetch_tmdb_data(imdb_id):
    imdb_id_full = f"tt{str(imdb_id).zfill(7)}"
    url_find = f"https://api.themoviedb.org/3/find/{imdb_id_full}"
    params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
    r = requests.get(url_find, params=params).json()

    if not r.get("movie_results"):
        print("TMDb: Movie not found")
        return {}

    url_credits = f"https://api.themoviedb.org/3/movie/{imdb_id_full}/credits"
    r = requests.get(url_credits, params={"api_key": TMDB_API_KEY}).json()

    directors = [d["name"] for d in r["crew"] if d["job"]=="Director"]
    writers = [w["name"] for w in r["crew"] if w["job"] in ("Writer","Screenplay")]
    composer = [c["name"] for c in r["crew"] if c["job"]=="Original Music Composer"]
    cast = [a["name"] for a in r["cast"][:100]] # Limit to 100 top billed cast

    return {
            "Directors": ", ".join(directors),
            "Writers": ", ".join(writers),
            "Composers": ", ".join(composer),
            "Cast": ", ".join(cast)
            }

def fetch_omdb_data(imdb_id):
    imdb_id_full = f"tt{str(imdb_id).zfill(7)}"
    url = "http://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "i": imdb_id_full}
    r = requests.get(url, params=params).json()

    if r.get("Response") == "False":
        if "limit" in r.get("Error", "").lower():
            print("⚠️ OMDb daily request limit reached. Try again tomorrow.")
            return {}

    return {
        "IMDbRating": r.get("imdbRating"),
        "Metascore": r.get("Metascore")
    }

def fetch_metadata(imdb_id):
    tmdb_data = fetch_tmdb_data(imdb_id)
    omdb_data = fetch_omdb_data(imdb_id)

    metadata = {**tmdb_data, **omdb_data}
    return metadata

def load_all_data():
    df = pd.read_csv("ltrbxd_all_films.csv")
    return df

def load_rated_data():
    df = pd.read_csv("ltrbxd_rated_films.csv")
    return df

def main():
    df = load_all_data()

    for col in ["Directors", "Writers", "Composer", "Cast", "IMDbRating", "Metascore"]:
        if col not in df.columns:
            df[col] = ""

    for idx, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        imdb_id = str(row["imdbID"])
        # print(f"Fetching metadata for {row['Title']} ({row['Year']})...")

        metadata = fetch_metadata(imdb_id)

        for key, value in metadata.items():
            if key in df.columns:
                df.at[idx, key] = value

    # Save enriched dataframe
    df.to_csv("ltrbxd_all_films_with_metadata.csv", index=False)
    print("✅ Metadata appended and saved to ltrbxd_all_films_with_metadata.csv")

if __name__ == "__main__":
    main()