import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections
import geopandas as gpd
import country_converter as coco
from collections import Counter
import gender_guesser.detector as gg

def load_rated_dataframe(dir):
    return pd.read_csv(f"{dir}/ltrbxd_rated_films_with_metadata.csv")

def load_all_dataframe(dir):
    return pd.read_csv(f"{dir}/ltrbxd_all_films_with_metadata.csv")

def plot_rated_ratings(ratings, imdb_ratings, metascore, dir):

    bins = np.arange(0.5, 6.0, 0.5)

    os.makedirs(f"plots/{dir}", exist_ok=True)

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=1)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.savefig(f"plots/{dir}/hists/rated_films_ratings_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/hists/rated_films_ratings_vs_IMDb_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/hists/rated_films_ratings_vs_metascore_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/hists/rated_films_all_ratings_hist.png")
    plt.close()

def plot_all_ratings(imdb_ratings, metascore, dir):

    imdb_ratings /= 2
    metascore /= 20
    
    bins = np.arange(0.5, 6.0, 0.5)

    os.makedirs(f"plots/{dir}", exist_ok=True)

    plt.figure()
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/hists/IMDb_vs_metascore_hist.png")
    plt.close()

def plot_people_bar_graph(people_counts, people_type, dir):
    
    people = [el[0] for el in people_counts]
    counts = [el[1] for el in people_counts]
    os.makedirs(f"plots/{dir}", exist_ok=True)

    plt.figure(figsize=(12,6))
    bars = plt.bar(people, counts, width=0.7, color="steelblue", edgecolor="black")
    plt.title(f"{people_type} Frequency", fontsize=16, weight="bold")
    plt.xlabel(people_type, fontsize=14)
    plt.ylabel("Count", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"plots/{dir}/freqs/{people_type}_frequency.png", dpi=300)
    plt.close()

def plot_world_map(df, dir):
    df_countries = (
    df["OriginCountry"]
    .str.split(", ")
    .explode()
    .value_counts()
    .reset_index()
    )
    df_countries.columns = ["country", "count"]
    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)
    world["country_std"] = coco.convert(names=world["ADMIN"], to="name_short")
    world = world.merge(df_countries, how="left", left_on="country_std", right_on="country")

    fig, ax = plt.subplots(figsize=(15, 8))

    world.plot(
        column="count",
        cmap="OrRd",  # red gradient
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        missing_kwds={"color": "lightgrey", "label": "No data"}
    )

    ax.set_title("Movies by Country (from TMDb origin_country)", fontsize=16)
    ax.axis("off")
    plt.savefig(f"plots/{dir}/world_plot.png")

    return None

def plot_contrarian_bars(rating_diffs, title, filename, dir):

    os.makedirs(f"plots/{dir}", exist_ok=True)

    people = list(rating_diffs.keys())[:10]
    diffs = list(rating_diffs.values())[:10]

    plt.figure(figsize=(12,6))
    bars = plt.bar(people, diffs, width=0.7, color="salmon", edgecolor="black")
    plt.title(title, fontsize=16, weight="bold")
    plt.xlabel("Person", fontsize=14)
    plt.ylabel("Average Rating Difference", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"plots/{dir}/ratings/{filename}.png", dpi=300)
    plt.close()

def plot_year_histogram(years, dir):
    bins = np.arange(1940, 2026, 5)

    os.makedirs(f"plots/{dir}", exist_ok=True)

    plt.figure()
    plt.hist(years, bins=bins, label="years", alpha=1)
    plt.xlim((np.min(years)-1, np.max(years)+1))
    plt.xticks(bins[:-1], labels=bins[:-1], rotation=45)
    plt.savefig(f"plots/{dir}/hists/films_years_hist.png")
    plt.close()

def process_people(peoples):

    peoples_list = []

    for people in peoples:
        if pd.isna(people):  # skip NaN values
            continue
        if type(people) == float or type(people) == int:
            people_list = [people]
        elif len(people) > 1:
            people_list = people.split(", ")
        peoples_list.append(people_list)

    return peoples_list

def get_person_counts(peoples):

    peoples = process_people(peoples)

    person_counts = collections.Counter(person for people in peoples for person in people)

    return person_counts

def person_films(df, person, role):

    if role not in df.columns:
        raise ValueError(f"Role '{role}' not found in DataFrame columns. Role must be one of {df.columns.tolist()}")

    films = []

    for _, row in df.iterrows():
        if person in str(row[role]):
            films.append(row["Title"])

    return sorted(films)

def get_ratings_averages(people_ratings_dict, reverse_bool):
    people_avg_ratings = {person: np.round(np.mean(ratings), 3) for person, ratings in people_ratings_dict.items()}
    return {k: v for k, v in sorted(people_avg_ratings.items(), key=lambda item: item[1], reverse=reverse_bool)}

def get_ratings_medians(people_ratings_dict, reverse_bool):
    people_avg_ratings = {person: np.round(np.median(ratings), 1) for person, ratings in people_ratings_dict.items()}
    return {k: v for k, v in sorted(people_avg_ratings.items(), key=lambda item: item[1], reverse=reverse_bool)}

def get_people_ratings(df, role, reverse_bool, num):

    if role not in df.columns:
        raise ValueError(f"Role '{role}' not found in DataFrame columns. Role must be one of {df.columns.tolist()}")
    
    people_ratings_dict = {}

    for _, row in df.iterrows():
        for person in str(row[role]).split(", "):
            if person == 'nan':
                continue
            if person not in people_ratings_dict:
                people_ratings_dict[person] = []
            people_ratings_dict[person].append(row["Rating"])

    people_ratings_dict = {person: ratings for person, ratings in people_ratings_dict.items() if len(ratings) >= num}

    people_avg_ratings = get_ratings_averages(people_ratings_dict, reverse_bool)
    people_median_ratings = get_ratings_medians(people_ratings_dict, reverse_bool)

    return people_ratings_dict, people_avg_ratings, people_median_ratings

def plot_rated_people(people_ratings, role, type, title, filename, dir):


    people = [p for p in people_ratings.keys()][:15]
    ratings = [r for r in people_ratings.values()][:15]
    plt.figure(figsize=(12,6))
    bars = plt.bar(people, ratings, width=0.7, color="salmon", edgecolor="black")
    plt.title(title, fontsize=16, weight="bold")
    plt.xlabel(f"{role}", fontsize=14)
    plt.ylabel(f"{type} rating", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"plots/{dir}/ratings/{filename}.png", dpi=300)
    plt.close()

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

def build_unique_set_of_workers(df_workers, countries):
    workers_set = set()
    for i, workers in enumerate(df_workers):
        if type(workers) != str: 
            continue
        workers_list = workers.split(', ')
        country = check_country(countries[i].lower())
        for worker in workers_list:
            if worker not in workers_set:
                workers_set.add((worker, country))
    return workers_set

def count_unique_gender_in_workers(df, worker_type, gender_registry, countries):
    workers_set = build_unique_set_of_workers(df[worker_type], countries)

    if worker_type == "Cast":
        gender_detector = gg.Detector()
        gender_counter = Counter({'female': 0, 'male': 0, 'mostly_female': 0, 'mostly_male': 0, 'unknown': 0, 'andy': 0})
    else:
        gender_counter = Counter({'female': 0, 'male': 0})

    for i, worker_and_country in enumerate(workers_set):

        name, country = worker_and_country
        if worker_type == "Cast":
            first_name = get_first_name(country, name)
            gender = gender_detector.get_gender(first_name, country)
        else:
            gender = gender_registry.loc[gender_registry['name'] == name, 'gender'].iloc[0]
        gender_counter[gender] += 1

    return gender_counter

def count_gender_in_workers(df, worker_type, gender_registry, rated_bool=False):
    gender_counter = Counter({'female': 0, 'male': 0})
    gender_ratings = {'male': [], 'female': []}

    for i, workers in enumerate(df[worker_type]):
        if type(workers) != str: 
            continue
        workers_list = workers.split(', ')
        
        for j, name in enumerate(workers_list):
            gender = gender_registry.loc[gender_registry['name'] == name, 'gender'].iloc[0]
            if j == 0 and rated_bool:
                gender_ratings[gender].append(df['Rating'][i])
            gender_counter[gender] += 1

    return gender_counter, gender_ratings

def get_movies_of_specific_worker_and_gender(df, worker_type, gender_type, gender_registry):
    worker_dict = {}
    for i, workers in enumerate(df[worker_type]):
        if type(workers) != str: 
            continue
        workers_list = workers.split(', ')
        worker = workers_list[0]
        gender = gender_registry.loc[gender_registry['name'] == worker, 'gender'].iloc[0]
        if gender == gender_type:
            if worker not in worker_dict:
                worker_dict[worker] = []
            worker_dict[worker].append((df['Title'][i], df['Rating'][i]))
    return worker_dict

def update_excel_sheet_with_ratings():
    
    table_data = []
    counter_data = []
    unique_counter_data = []
    persons = ['audun', 'mali']
    roles = ['Directors', 'Writers', 'Composers']

    for person in persons:
        df_rated = load_rated_dataframe(person)
        df_all = load_all_dataframe(person)
        for role in roles:
            df_gender = pd.read_csv(fr"gender_registry\{role[:-1].lower()}_gender_registry.csv")
            gender_counter, gender_ratings = count_gender_in_workers(df_rated, role, df_gender, True)
            averages = get_ratings_averages(gender_ratings, True)
            medians = get_ratings_medians(gender_ratings, True)

            gender_counter, gender_ratings = count_gender_in_workers(df_all, role, df_gender, False)
            table_data.append([person.capitalize(), role[:-1], 'Female', averages['female'], medians['female']])
            table_data.append([person.capitalize(), role[:-1], 'Male', averages['male'], medians['male']])

            counter_data.append([person.capitalize(), role[:-1], 'Female', gender_counter['female']])
            counter_data.append([person.capitalize(), role[:-1], 'Male', gender_counter['male']])
            
            unique_gender_counter = count_unique_gender_in_workers(df_all, role, df_gender, df_all['OriginCountry'])
            unique_counter_data.append([person.capitalize(), role[:-1], 'Female', unique_gender_counter['female']])
            unique_counter_data.append([person.capitalize(), role[:-1], 'Male', unique_gender_counter['male']])

    df_table = pd.DataFrame(table_data, columns=['Person', 'Role', 'Gender', 'Average Rating', 'Median Rating'])
    df_counter = pd.DataFrame(counter_data, columns=['Person', 'Role', 'Gender', 'Number'])
    df_unique_counter = pd.DataFrame(unique_counter_data, columns=['Person', 'Role', 'Gender', 'Number'])
    with pd.ExcelWriter("gender_ratings_table.xlsx", engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_table.to_excel(writer, sheet_name='Ratings', index=False)
        df_counter.to_excel(writer, sheet_name='Counts', index=False)
        df_unique_counter.to_excel(writer, sheet_name='UniqueCounts', index=False)

    return None