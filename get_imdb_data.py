import pandas as pd
import time
from imdb import IMDb

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

def extract_metadata(movie):
    """Extract metadata fields from IMDbPY movie object."""
    return {
        "imdbID": movie.movieID,
        "Title": movie.get('title'),
        "Year": movie.get('year')
    }

def main():
    # Load your Letterboxd CSV (adjust column names if needed)
    df = pd.read_csv("watched.csv")
    
    results = []
    for _, row in df.iterrows():
        title = row["Name"]
        year = row["Year"]

        try:
            movie = search_movie(title, year)
            if movie:
                metadata = extract_metadata(movie)
                results.append(metadata)
                print(f"✅ Found: {title} ({year})")
            else:
                print(f"❌ Not found: {title} ({year})")
        except Exception as e:
            print(f"⚠️ Error with {title} ({year}): {e}")

        time.sleep(0.1)  # be nice to IMDb servers

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("ltrbxd_all_films.csv", index=False)
    print("Export complete: ltrbxd_all_films.csv")

if __name__ == "__main__":
    main()