import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections

def load_rated_dataframe():
    return pd.read_csv("ltrbxd_rated_films_with_metadata.csv")

def load_all_dataframe():
    return pd.read_csv("ltrbxd_all_films_with_metadata.csv")

def plot_rated_ratings(ratings, imdb_ratings, metascore):
    imdb_ratings /= 2
    metascore /= 20

    bins = np.arange(0.5, 6.0, 0.5)

    os.makedirs("plots", exist_ok=True)

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=1)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.savefig("plots/rated_films_ratings_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig("plots/rated_films_ratings_vs_IMDb_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig("plots/rated_films_ratings_vs_metascore_hist.png")
    plt.close()

    plt.figure()
    plt.hist(ratings, bins=bins, label="ratings", alpha=0.3)
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig("plots/rated_films_all_ratings_hist.png")
    plt.close()

def plot_all_ratings(imdb_ratings, metascore):

    imdb_ratings /= 2
    metascore /= 20

    bins = np.arange(0.5, 6.0, 0.5)

    os.makedirs("plots", exist_ok=True)

    plt.figure()
    plt.hist(imdb_ratings, bins=bins, label="IMDb ratings", alpha=0.3)
    plt.hist(metascore, bins=bins, label="metascore", alpha=0.3)
    plt.xlim((0.5,5.5))
    plt.xticks(bins[:-1]+0.25, labels=bins[:-1])
    plt.legend()
    plt.savefig("plots/IMDb_vs_metascore_hist.png")
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

def main_rated():
    df_rated = load_rated_dataframe()

    # ratings = df_rated["Rating"]
    # imdb_ratings = df_rated["IMDbRating"]
    # metascore = df_rated["Metascore"]
    # plot_rated_ratings(ratings, imdb_ratings, metascore)

    actor_counts = get_person_counts(df_rated["Cast"].copy())
    director_counts = get_person_counts(df_rated["Directors"].copy())
    writer_counts = get_person_counts(df_rated["Writers"].copy())
    composer_counts = get_person_counts(df_rated["Composers"].copy())
    print(f"The 20 actors I have seen the most movies with:\n{actor_counts.most_common()[:20]}")
    print(f"The 20 directors I have seen the most movies with:\n{director_counts.most_common()[:20]}")
    print(f"The 20 writers I have seen the most movies with:\n{writer_counts.most_common()[:20]}")
    print(f"The 20 composers I have seen the most movies with:\n{composer_counts.most_common()[:20]}")

    return None

def main_all():
    df_all = load_all_dataframe()

    # imdb_ratings = df_all["IMDbRating"]
    # metascore = df_all["Metascore"]
    # plot_all_ratings(imdb_ratings, metascore)

    actor_counts = get_person_counts(df_all["Cast"].copy())
    director_counts = get_person_counts(df_all["Directors"].copy())
    writer_counts = get_person_counts(df_all["Writers"].copy())
    composer_counts = get_person_counts(df_all["Composers"].copy())
    print(f"The 20 actors I have seen the most movies with:\n{actor_counts.most_common()[:20]}")
    print(f"The 20 directors I have seen the most movies with:\n{director_counts.most_common()[:20]}")
    print(f"The 20 writers I have seen the most movies with:\n{writer_counts.most_common()[:20]}")
    print(f"The 20 composers I have seen the most movies with:\n{composer_counts.most_common()[:20]}")
    print(f"I have seen {actor_counts['Rachel McAdams']} Rachel McAdams films.")
    return None

if __name__=='__main__':
    main_all()