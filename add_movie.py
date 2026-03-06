import pandas as pd
from get_metadata import fetch_metadata

def write_rated_row(film_name, film_year, rating, imdb_id, dir):

    df = pd.DataFrame([[imdb_id, film_name, film_year, rating]],
                      columns=["imdbID", "Title", "Year", "Rating"])
    df.to_csv(f"{dir}/ltrbxd_rated_films.csv", mode='a', index=False, header=False)

    return None

def write_all_row(film_name, film_year, imdb_id, dir):
    
    df = pd.DataFrame([[imdb_id, film_name, film_year]],
                      columns=["imdbID", "Title", "Year"])
    df.to_csv(f"{dir}/ltrbxd_all_films.csv", mode='a', index=False, header=False)

    return None

def write_rated_metadata_row(film_name, film_year, rating, imdb_id, metadata, dir):

    orig_data = {
        "imdbID": imdb_id,
        "Title": film_name,
        "Year": film_year,
        "Rating": rating
    }
    row = {**orig_data, **metadata}
    df = pd.DataFrame.from_dict([row], orient='columns')
    df.to_csv(f"{dir}/ltrbxd_rated_films_with_metadata.csv", mode='a', index=False, header=False)

    return None

def write_all_metadata_row(film_name, film_year, imdb_id, metadata, dir):

    orig_data = {
        "imdbID": imdb_id,
        "Title": film_name,
        "Year": film_year
    }
    row = {**orig_data, **metadata}
    df = pd.DataFrame.from_dict([row], orient='columns')
    df.to_csv(f"{dir}/ltrbxd_all_films_with_metadata.csv", mode='a', index=False, header=False)

    return None

def main(dir):

    film_name = input(f"What film did you watch (IMDb title please)? ")
    film_year = input(f"What year was the film released (according to IMDb)? ")
    rating = str(float(input(f"What rating did you give? ")))
    imdb_id = input(f"Write the IMDb ID for the film: ")
    write = input(f"Write 'ye' if you are sure you want to write the film info to csv-files: ")

    if write == 'ye':
        write_rated_row(film_name, film_year, rating, imdb_id, dir)
        write_all_row(film_name, film_year, imdb_id, dir)
        metadata = fetch_metadata(imdb_id)
        write_rated_metadata_row(film_name, film_year, rating, imdb_id, metadata, dir)
        write_all_metadata_row(film_name, film_year, imdb_id, metadata, dir)
        print(f"{film_name} has been written to all relevant csv-files, consider checking whether it was successful.")
    else:
        print(f"You decided not to write {film_name} to csv-files.")

    return None

if __name__ == '__main__':
    audun_bool = input("Is this for Audun? (y/n): ").lower() == 'y'
    mali_bool = input("Is this for Mali? (y/n): ").lower() == 'y'
    if audun_bool:
        dir = "audun"
    elif mali_bool:
        dir = "mali"
    else:
        raise ValueError("Invalid user specified.")
    main(dir)

def check_country(country):
    if ',' in country:
        country = country.split(', ')[0]
    country = country.replace(' ', '_')

    if country == 'south_korea':
        country = 'korea'
    elif country == 'united_states':
        country = 'usa'
    elif country == 'united_kingdom':
        country = 'great_britain'
    elif country == 'australia':
        country = 'great_britain'
    elif country == 'new_zealand':
        country = 'great_britain'
    elif country == 'czechia':
        country = 'czech_republic'

    return country

def get_first_name(country, name):
    if country == 'korea':
        first_name = name.split(' ')[-1].split('-')[0]
    else:
        first_name = name.split(' ')[0]
    return first_name

def add_name_to_gender_registry(name, country, gender_registry_path, gender_detector):
    country = check_country(country.lower())
    df_gender = pd.read_csv(gender_registry_path)
    names = df_gender['name']
    if name in names.values:
        df_gender.to_csv(gender_registry_path, index=False)
        return False
    first_name = get_first_name(country, name)
    gender = gender_detector.get_gender(first_name, country)
    if gender != 'male' and gender != 'female':
        gender = "unknown"
        unknown = True
    else:
        unknown = False
    df_gender = pd.concat([df_gender, pd.DataFrame([{
        "name": name,
        "gender": gender
    }])], ignore_index=True)    
    df_gender.to_csv(gender_registry_path, index=False)
    return unknown