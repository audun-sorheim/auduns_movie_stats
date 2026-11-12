
import pandas as pd
import requests
import time
import tqdm


TMDB_API_KEY = "c4e8c4ca2a6f4c6411dc47aca067218f"


def fetch_tmdb_cast(imdb_id):

    imdb_id_full = f"tt{str(imdb_id).zfill(7)}"
    url_find = f"https://api.themoviedb.org/3/find/{imdb_id_full}"
    params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
    r = requests.get(url_find, params=params).json()

    if not r.get("movie_results"):
        print(f"TMDb: Movie {imdb_id} not found")
        return {
            "Cast": "not found",
            }

    url_credits = f"https://api.themoviedb.org/3/movie/{imdb_id_full}/credits"
    r = requests.get(url_credits, params={"api_key": TMDB_API_KEY}).json()

    cast = [a["name"] for a in r["cast"]]

    return ", ".join(cast)

def refresh_cast_csv(input_csv, output_csv, tmdb_api_key=TMDB_API_KEY):
    df = pd.read_csv(input_csv, dtype={"imdbID": str})

    session = requests.Session()
    cast_cache = {}

    updated = 0
    not_found = 0
    failed = 0

    for index, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        imdb_id = str(row["imdbID"]).strip()

        if not imdb_id or imdb_id == "nan":
            continue

        if imdb_id in cast_cache:
            df.at[index, "Cast"] = cast_cache[imdb_id]
            print(f"found the same imdb_id for movie: {df.at[index, 'Title']}")
            continue

        cast = fetch_tmdb_cast(imdb_id)
        cast_cache[imdb_id] = cast
        df.at[index, "Cast"] = cast
        updated += 1
        time.sleep(0.1)


    # Save updated CSV
    df.to_csv(output_csv, index=False)

    print("\nFinished!")
    print(f"Updated: {updated}")
    print(f"Not found: {not_found}")
    print(f"Failed: {failed}")
    print(f"Saved to: {output_csv}")

    return df


def main():
    input_rated = "audun\ltrbxd_rated_films_with_metadata_old.csv"
    input_all = "audun\ltrbxd_all_films_with_metadata_old.csv"

    output_rated = "audun\ltrbxd_rated_films_with_metadata.csv"
    output_all = "audun\ltrbxd_all_films_with_metadata.csv"

    # refresh_cast_csv(input_rated, output_rated)
    refresh_cast_csv(input_all, output_all)

    return None

if __name__ == '__main__':
    main()