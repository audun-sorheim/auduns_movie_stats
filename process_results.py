import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections
import geopandas as gpd

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

def plot_world_map(df):
    df_countries = (
    df["OriginCountry"]
    .str.split(", ")
    .explode()
    .value_counts()
    .reset_index()
    )
    df_countries.columns = ["country", "count"]
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    world = world.merge(df_countries, how="left", left_on="name", right_on="country")

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
    plt.savefig("plots/world_plot.png")

    return None 

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

def actors_films(actor, df):

    films = []

    for _, row in df.iterrows():
        if actor in row["Cast"]:
            films.append(row["Title"])

    return sorted(films)

def directors_films(director, df):

    films = []

    for _, row in df.iterrows():
        if director in row["Directors"]:
            films.append(row["Title"])

    return sorted(films)

def composers_films(composer, df):

    films = []

    for _, row in df.iterrows():
        if composer in str(row["Composers"]):
            films.append(row["Title"])

    return sorted(films)

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

    plot_world_map(df_all)

    actor_counts = get_person_counts(df_all["Cast"].copy())
    director_counts = get_person_counts(df_all["Directors"].copy())
    writer_counts = get_person_counts(df_all["Writers"].copy())
    composer_counts = get_person_counts(df_all["Composers"].copy())
    print(f"The 20 actors I have seen the most movies with:\n{actor_counts.most_common()[:20]}")
    print(f"The 20 directors I have seen the most movies with:\n{director_counts.most_common()[:20]}")
    print(f"The 20 writers I have seen the most movies with:\n{writer_counts.most_common()[:20]}")
    print(f"The 20 composers I have seen the most movies with:\n{composer_counts.most_common()[:20]}\n")

    print(f"I have seen {actor_counts['Rachel McAdams']} Rachel McAdams films:\n{actors_films('Rachel McAdams', df_all)}")
    print(f"I have seen {actor_counts['Mark Ruffalo']} Mark Ruffalo films:\n{actors_films('Mark Ruffalo', df_all)}")
    print(f"I have seen {actor_counts['Tom Cruise']} Tom Cruise films:\n{actors_films('Tom Cruise', df_all)}")
    print(f"I have seen {actor_counts['Matt Damon']} Matt Damon films:\n{actors_films('Matt Damon', df_all)}")
    print(f"I have seen {actor_counts['Vera Farmiga']} Vera Farmiga films:\n{actors_films('Vera Farmiga', df_all)}")
    print(f"I have seen {actor_counts['Anne Hathaway']} Anne Hathaway films:\n{actors_films('Anne Hathaway', df_all)}\n")

    print(f"I have seen {director_counts['Stanley Kubrick']} Stanley Kubrick films:\n{directors_films('Stanley Kubrick', df_all)}")
    print(f"I have seen {director_counts['Christopher Nolan']} Christopher Nolan films:\n{directors_films('Christopher Nolan', df_all)}")
    print(f"I have seen {director_counts['Steven Spielberg']} Steven Spielberg films:\n{directors_films('Steven Spielberg', df_all)}")
    print(f"I have seen {director_counts['Greta Gerwig']} Greta Gerwig films:\n{directors_films('Greta Gerwig', df_all)}")
    print(f"I have seen {director_counts['Sofia Coppola']} Sofia Coppola films:\n{directors_films('Sofia Coppola', df_all)}")
    print(f"I have seen {director_counts['David Fincher']} David Fincher films:\n{directors_films('David Fincher', df_all)}\n")

    print(f"I have seen {composer_counts['John Williams']} John Williams films:\n{composers_films('John Williams', df_all)}")
    print(f"I have seen {composer_counts['Howard Shore']} Howard Shore films:\n{composers_films('Howard Shore', df_all)}")
    print(f"I have seen {composer_counts['Hans Zimmer']} Hans Zimmer films:\n{composers_films('Hans Zimmer', df_all)}")

    return None

if __name__=='__main__':
    main_all()