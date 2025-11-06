import requests
import pandas as pd
import tqdm
import langcodes
import country_converter as coco

TMDB_API_KEY = "c4e8c4ca2a6f4c6411dc47aca067218f"
OMDB_API_KEY = "7a043e00"

def process_data(orig_country, orig_language):

    if orig_country is None:
        print(f"Country could not be found for IMDbID: {id}")
        coun = None
    else:
        if isinstance(orig_country, list):
            coun = [coco.convert(names=c, to="name_short") for c in orig_country]
        else:
            coun = coco.convert(names=orig_country, to="name_short")

    if orig_language is None:
        print(f"Language could not be found for IMDbID: {id}")
        lang = None
    else:
        if isinstance(orig_language, list):
            lang = [langcodes.Language.get(l).display_name() for l in orig_language]
        else:
            lang = langcodes.Language.get(orig_language).display_name()

    return coun, lang

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

    url_full = f"https://api.themoviedb.org/3/movie/{imdb_id_full}"
    r_full = requests.get(url_full, params={"api_key": TMDB_API_KEY}).json()

    directors = [d["name"] for d in r["crew"] if d["job"]=="Director"]
    writers = [w["name"] for w in r["crew"] if w["job"] in ("Writer","Screenplay")]
    composer = [c["name"] for c in r["crew"] if c["job"] in ("Original Music Composer", "Music", "Composer", "Score Composer")]
    cast = [a["name"] for a in r["cast"][:100]] # Limit to 100 top billed cast
    countries = ", ".join(r_full.get("origin_country", [])) 
    language = r_full.get("original_language")

    origin_country, orig_language = process_data(countries, language)

    return {
            "Directors": ", ".join(directors),
            "Writers": ", ".join(writers),
            "Composers": ", ".join(composer),
            "Cast": ", ".join(cast)
            }, {
            "OriginCountry": origin_country, 
            "OriginalLanguage": orig_language
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
    tmdb_data, extra_data = fetch_tmdb_data(imdb_id)
    omdb_data = fetch_omdb_data(imdb_id)

    metadata = {**tmdb_data, **omdb_data, **extra_data}
    return metadata

def load_all_data(dir):
    df = pd.read_csv(f"{dir}/ltrbxd_all_films.csv")
    return df

def load_rated_data(dir):
    df = pd.read_csv(f"{dir}/ltrbxd_rated_films.csv")
    return df

def main(dir):

    df = load_all_data(dir)

    for col in ["Directors", "Writers", "Composers", "Cast", "IMDbRating", "Metascore", "OriginCountry", "OriginalLanguage"]:
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
    df.to_csv(f"{dir}/ltrbxd_all_films_with_metadata.csv", index=False)
    print(f"✅ Metadata appended and saved to {dir}/ltrbxd_all_films_with_metadata.csv")

    df = load_rated_data(dir)

    for col in ["Directors", "Writers", "Composers", "Cast", "IMDbRating", "Metascore", "OriginCountry", "OriginalLanguage"]:
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
    df.to_csv(f"{dir}/ltrbxd_rated_films_with_metadata.csv", index=False)
    print(f"✅ Metadata appended and saved to {dir}/ltrbxd_rated_films_with_metadata.csv")

if __name__ == "__main__":
    audun_bool = input("Is this for Audun? (y/n): ").lower() == 'y'
    mali_bool = input("Is this for Mali? (y/n): ").lower() == 'y'
    if audun_bool:
        dir = "audun"
    elif mali_bool:
        dir = "mali"
    else:
        raise ValueError("Invalid user specified.")
    main(dir)