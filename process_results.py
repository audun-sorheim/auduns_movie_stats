import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections
import geopandas as gpd
import country_converter as coco

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
    plt.savefig(f"plots/{dir}/rated_films_ratings_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/rated_films_ratings_vs_IMDb_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/rated_films_ratings_vs_metascore_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig(f"plots/{dir}/rated_films_all_ratings_hist.png")
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
    plt.savefig(f"plots/{dir}/IMDb_vs_metascore_hist.png")
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
    plt.savefig(f"plots/{dir}/{people_type}_frequency.png", dpi=300)
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
    plt.savefig(f"plots/{dir}/{filename}.png", dpi=300)
    plt.close()

def plot_year_histogram(years, dir):
    bins = np.arange(1940, 2026, 5)

    os.makedirs(f"plots/{dir}", exist_ok=True)

    plt.figure()
    plt.hist(years, bins=bins, label="years", alpha=1)
    plt.xlim((np.min(years)-1, np.max(years)+1))
    plt.xticks(bins[:-1], labels=bins[:-1], rotation=45)
    plt.savefig(f"plots/{dir}/films_years_hist.png")
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

def get_ratings_averages(people_ratings_dict):
    people_avg_ratings = {person: np.round(np.mean(ratings), 3) for person, ratings in people_ratings_dict.items()}
    return {k: v for k, v in sorted(people_avg_ratings.items(), key=lambda item: item[1], reverse=True)}

def get_people_ratings(df, role):

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

    people_ratings_dict = {person: ratings for person, ratings in people_ratings_dict.items() if len(ratings) >= 3}

    people_avg_ratings = get_ratings_averages(people_ratings_dict)

    return people_ratings_dict, people_avg_ratings