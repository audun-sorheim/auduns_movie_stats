import numpy as np
from process_results import (
    load_rated_dataframe,
    load_all_dataframe,
    plot_rated_ratings,
    plot_all_ratings,
    plot_world_map,
    get_person_counts,
    get_people_ratings,
    plot_people_bar_graph,
    person_films
)

def main_rated():
    df_rated = load_rated_dataframe()

    ratings = df_rated["Rating"]
    imdb_ratings = df_rated["IMDbRating"]
    metascore = df_rated["Metascore"]
    plot_rated_ratings(ratings, imdb_ratings, metascore)

    actor_counts = get_person_counts(df_rated["Cast"].copy())
    director_counts = get_person_counts(df_rated["Directors"].copy())
    writer_counts = get_person_counts(df_rated["Writers"].copy())
    composer_counts = get_person_counts(df_rated["Composers"].copy())
    # print(f"The 20 actors I have seen the most movies with:\n{actor_counts.most_common(20)}")
    # print(f"The 20 directors I have seen the most movies with:\n{director_counts.most_common(20)}")
    # print(f"The 20 writers I have seen the most movies with:\n{writer_counts.most_common(20)}")
    # print(f"The 20 composers I have seen the most movies with:\n{composer_counts.most_common(20)}")


    rating_diff_public = np.float64(df_rated["Rating"] - df_rated["IMDbRating"])
    rating_diff_critics = np.float64(df_rated["Rating"] - df_rated["Metascore"])
    print(df_rated["Title"][np.nanargmax(rating_diff_public)], np.round(rating_diff_public[np.nanargmax(rating_diff_public)], 2))
    print(df_rated["Title"][np.nanargmin(rating_diff_public)], rating_diff_public[np.nanargmin(rating_diff_public)])
    print(df_rated["Title"][np.nanargmax(rating_diff_critics)], rating_diff_critics[np.nanargmax(rating_diff_critics)])
    print(df_rated["Title"][np.nanargmin(rating_diff_critics)], rating_diff_critics[np.nanargmin(rating_diff_critics)])
    print(df_rated["Title"][np.where(np.abs(rating_diff_public)<0.001)[0]])
    print(df_rated["Title"][np.where(np.abs(rating_diff_critics)<0.001)[0]])
    rating_diff_public = rating_diff_public[~np.isnan(rating_diff_public)]
    rating_diff_critics = rating_diff_critics[~np.isnan(rating_diff_critics)]
    avg_rating_diff_public = np.round(np.mean(rating_diff_public),3)
    avg_rating_diff_critics = np.round(np.mean(rating_diff_critics),3)
    median_rating_diff_public = np.round(np.median(rating_diff_public),2)
    median_rating_diff_critics = np.round(np.median(rating_diff_critics),2)
    print(avg_rating_diff_critics, avg_rating_diff_public, median_rating_diff_critics, median_rating_diff_public)
    print(np.sum(rating_diff_public), np.sum(rating_diff_critics))

    composer_ratings, composer_avg_ratings = get_people_ratings(df_rated, "Composers")
    actor_ratings, actor_avg_ratings = get_people_ratings(df_rated, "Cast")
    director_ratings, director_avg_ratings = get_people_ratings(df_rated, "Directors")
    writer_ratings, writer_avg_ratings = get_people_ratings(df_rated, "Writers")
    print(composer_avg_ratings)
    print(actor_avg_ratings)
    print(director_avg_ratings)
    print(writer_avg_ratings)

    return None

def main_all():
    df_all = load_all_dataframe()

    imdb_ratings = df_all["IMDbRating"]
    metascore = df_all["Metascore"]
    plot_all_ratings(imdb_ratings, metascore)

    plot_world_map(df_all)

    actor_counts = get_person_counts(df_all["Cast"].copy())
    director_counts = get_person_counts(df_all["Directors"].copy())
    writer_counts = get_person_counts(df_all["Writers"].copy())
    composer_counts = get_person_counts(df_all["Composers"].copy())
    lang_counts = get_person_counts(df_all["OriginalLanguage"].copy())
    coun_counts = get_person_counts(df_all["OriginCountry"].copy())

    filtered_actor_counts = [(actor, count) for actor, count in actor_counts.most_common() if count >= 10]
    filtered_director_counts = [(director, count) for director, count in director_counts.most_common() if count >= 3]
    filtered_writer_counts = [(writer, count) for writer, count in writer_counts.most_common() if count >= 4]
    filtered_composer_counts = [(composer, count) for composer, count in composer_counts.most_common() if count >= 4]

    plot_people_bar_graph(filtered_actor_counts, "actor")
    plot_people_bar_graph(filtered_director_counts, "director")
    plot_people_bar_graph(filtered_writer_counts, "writer")
    plot_people_bar_graph(filtered_composer_counts, "composer")

    print(f"The 20 actors I have seen the most movies with:\n{filtered_actor_counts}")
    print(f"The 20 directors I have seen the most movies with:\n{filtered_director_counts}")
    print(f"The 20 writers I have seen the most movies with:\n{filtered_writer_counts}")
    print(f"The 20 composers I have seen the most movies with:\n{filtered_composer_counts}\n")
    print(f"The languages I have seen the most movies with:\n{lang_counts.most_common()}")
    print(f"The countries I have seen the most movies from:\n{coun_counts.most_common()}\n")

    print(f"I have seen {actor_counts['Rachel McAdams']} Rachel McAdams films:\n{person_films(df_all, 'Rachel McAdams', 'Cast')}")
    print(f"I have seen {actor_counts['Mark Ruffalo']} Mark Ruffalo films:\n{person_films(df_all, 'Mark Ruffalo', 'Cast')}")
    print(f"I have seen {actor_counts['Tom Cruise']} Tom Cruise films:\n{person_films(df_all, 'Tom Cruise', 'Cast')}")
    print(f"I have seen {actor_counts['Matt Damon']} Matt Damon films:\n{person_films(df_all, 'Matt Damon', 'Cast')}")
    print(f"I have seen {actor_counts['Vera Farmiga']} Vera Farmiga films:\n{person_films(df_all, 'Vera Farmiga', 'Cast')}")
    print(f"I have seen {actor_counts['Anne Hathaway']} Anne Hathaway films:\n{person_films(df_all, 'Anne Hathaway', 'Cast')}\n")

    print(f"I have seen {director_counts['Stanley Kubrick']} Stanley Kubrick films:\n{person_films(df_all, 'Stanley Kubrick', 'Directors')}")
    print(f"I have seen {director_counts['Christopher Nolan']} Christopher Nolan films:\n{person_films(df_all, 'Christopher Nolan', 'Directors')}")
    print(f"I have seen {director_counts['Steven Spielberg']} Steven Spielberg films:\n{person_films(df_all, 'Steven Spielberg', 'Directors')}")
    print(f"I have seen {director_counts['Greta Gerwig']} Greta Gerwig films:\n{person_films(df_all, 'Greta Gerwig', 'Directors')}")
    print(f"I have seen {director_counts['Sofia Coppola']} Sofia Coppola films:\n{person_films(df_all, 'Sofia Coppola', 'Directors')}")
    print(f"I have seen {director_counts['David Fincher']} David Fincher films:\n{person_films(df_all, 'David Fincher', 'Directors')}\n")

    print(f"I have seen {composer_counts['John Williams']} John Williams films:\n{person_films(df_all, 'John Williams', 'Composers')}")
    print(f"I have seen {composer_counts['Howard Shore']} Howard Shore films:\n{person_films(df_all, 'Howard Shore', 'Composers')}")
    print(f"I have seen {composer_counts['Hans Zimmer']} Hans Zimmer films:\n{person_films(df_all, 'Hans Zimmer', 'Composers')}")

    return None

if __name__=='__main__':
    main_rated()
    main_all()