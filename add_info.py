import requests
import tqdm
import pandas as pd
from process_results import load_all_dataframe, load_rated_dataframe
import langcodes
import country_converter as coco

TMDB_API_KEY = "c4e8c4ca2a6f4c6411dc47aca067218f"
OMDB_API_KEY = "7a043e00"

def fetch_new_data(imdb_id):
    imdb_id_full = f"tt{str(imdb_id).zfill(7)}"
    url_find = f"https://api.themoviedb.org/3/find/{imdb_id_full}"
    params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
    r = requests.get(url_find, params=params).json()

    if not r.get("movie_results"):
        print("TMDb: Movie not found")
        return [], []

    url_credits = f"https://api.themoviedb.org/3/movie/{imdb_id_full}"
    r = requests.get(url_credits, params={"api_key": TMDB_API_KEY}).json()

    countries = ", ".join(r.get("origin_country", [])) 
    language = r.get("original_language")

    return countries, language

def process_data(id):
    orig_country, orig_language = fetch_new_data(id)

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

def get_info(df):

    countries = []
    languages = []

    for id in tqdm.tqdm(df["imdbID"]):
        orig_country, orig_language = process_data(id)
        countries.append(orig_country)
        languages.append(orig_language)

    return countries, languages

def main():

    df_all = load_all_dataframe()
    df_rated = load_rated_dataframe()

    all_countries, all_languages = get_info(df_all)
    rated_countries, rated_languages = get_info(df_rated)

    df_all["OriginCountry"] = all_countries
    df_all["OriginalLanguage"] = all_languages
    df_rated["OriginCountry"] = rated_countries
    df_rated["OriginalLanguage"] = rated_languages

    df_all.to_csv("ltrbxd_all_films_with_metadata.csv", index=False)
    df_rated.to_csv("ltrbxd_rated_films_with_metadata.csv", index=False)
    print("✅ New appended and saved ")
    return None

if __name__ == '__main__':
    main()