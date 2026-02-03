import pandas as pd
import time
from imdb import IMDb
from imdb import IMDbDataAccessError
import requests
TMDB_API_KEY = "c4e8c4ca2a6f4c6411dc47aca067218f"

# Initialize IMDbPY
ia = IMDb()

def search_movie(title, year):
    """Search for a movie by title and year, return IMDb movie object."""
    results = ia.search_movie(title)
    if not results:
        return None
    
    allowed_kinds = {"movie", "tv movie", "video"}
    year = int(year)

    for movie in results:
        ia.update(movie)

        if (
            movie.get("kind") in allowed_kinds
            and movie.get("title", "").lower() == title.lower()
            and abs(int(movie["year"]) - year) <= 1
        ):
            return movie
        

def tmdb_search_movie(title: str, year: int):
    """Return best TMDb match (dict) for a title + year, or None."""
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "year": int(year),
        "include_adult": "false",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    results = data.get("results", [])
    if not results:
        return None

    # pick top result; TMDb search ranking is usually good with year specified
    return results[0]

def tmdb_to_imdb_id(tmdb_id: int):
    """Return IMDb ID string like 'tt1234567' for a TMDb movie id, or None."""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("imdb_id")[2:]

def extract_metadata_from_tmdb(tmdb_movie: dict, imdb_id: str):
    year = None
    release_date = tmdb_movie.get("release_date")
    if release_date and len(release_date) >= 4:
        year = int(release_date[:4])

    return {
        "imdbID": imdb_id,
        "Title": tmdb_movie.get("title"),
        "Year": year
    }

def build_all_films_csv(dir_):
    df = pd.read_csv(f"{dir_}/watched.csv")
    results = []

    for _, row in df.iterrows():
        title = row["Name"]
        year = int(row["Year"])

        try:
            tmdb_movie = tmdb_search_movie(title, year)
            if not tmdb_movie:
                print(f"❌ Not found (TMDb): {title} ({year})")
                continue

            imdb_id = tmdb_to_imdb_id(tmdb_movie["id"])
            if not imdb_id:
                print(f"⚠️ No IMDb ID via TMDb: {title} ({year})")
                continue

            results.append(extract_metadata_from_tmdb(tmdb_movie, imdb_id))
            print(f"✅ Found: {title} ({year}) -> {imdb_id}")

        except Exception as e:
            print(f"⚠️ Error with {title} ({year}): {e}")

        time.sleep(0.05)  # TMDb is fine with this; can raise if you want

    pd.DataFrame(results).to_csv(f"{dir_}/ltrbxd_all_films.csv", index=False)
    print(f"Export complete: {dir_}/ltrbxd_all_films.csv")

def build_rated_films_csv(dir_):
    df = pd.read_csv(f"{dir_}/ratings.csv")
    results = []

    for _, row in df.iterrows():
        title = row["Name"]
        year = int(row["Year"])
        rating = row["Rating"]

        try:
            tmdb_movie = tmdb_search_movie(title, year)
            if not tmdb_movie:
                print(f"❌ Not found (TMDb): {title} ({year})")
                continue

            imdb_id = tmdb_to_imdb_id(tmdb_movie["id"])
            if not imdb_id:
                print(f"⚠️ No IMDb ID via TMDb: {title} ({year})")
                continue

            md = extract_metadata_from_tmdb(tmdb_movie, imdb_id)
            md["Rating"] = rating
            results.append(md)
            print(f"✅ Found: {title} ({year}) -> {imdb_id}")

        except Exception as e:
            print(f"⚠️ Error with {title} ({year}): {e}")

        time.sleep(0.05)

    pd.DataFrame(results).to_csv(f"{dir_}/ltrbxd_rated_films.csv", index=False)
    print(f"Export complete: {dir_}/ltrbxd_rated_films.csv")

def main(dir_):
    build_all_films_csv(dir_)
    build_rated_films_csv(dir_)

if __name__ == "__main__":
    audun_bool = input("Is this for Audun? (y/n): ").lower() == "y"
    mali_bool = input("Is this for Mali? (y/n): ").lower() == "y"
    if audun_bool:
        dir_ = "audun"
    elif mali_bool:
        dir_ = "mali"
    else:
        raise ValueError("Invalid user specified.")
    main(dir_)