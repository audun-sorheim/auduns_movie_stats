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
    person_films,
    plot_contrarian_bars,
    plot_year_histogram,
    plot_rated_people
)

def main_rated(dir):
    df_rated = load_rated_dataframe(dir=dir)

    ratings = df_rated["Rating"]
    imdb_ratings = df_rated["IMDbRating"]
    metascores = df_rated["Metascore"]
    metascores_nonnan = metascores.dropna()
    # print(imdb_ratings)

    plot_rated_ratings(ratings, np.copy(imdb_ratings)/2, np.copy(metascores_nonnan)/20, dir=dir)

    rating_diff_public = np.array([], dtype=np.float64)
    rating_diff_critics = np.array([], dtype=np.float64)
    for i, imdb_rating in enumerate(imdb_ratings):
        if np.isnan(imdb_rating):
            rating_diff_public =  np.append(rating_diff_public, 0.0)
        else:
            # print(ratings[i], imdb_rating)
            rating_diff_public = np.append(rating_diff_public, np.round(ratings[i] - imdb_rating/2, 3))
    for i, metascore in enumerate(metascores):
        if np.isnan(metascore):
            rating_diff_critics = np.append(rating_diff_critics, 0.0)
        else:
            rating_diff_critics = np.append(rating_diff_critics, np.round(ratings[i] - metascore/20, 3))

    rating_diff_public_dict = dict(key for key in zip(df_rated["Title"], rating_diff_public))
    rating_diff_critics_dict = dict(key for key in zip(df_rated["Title"], rating_diff_critics))
    positive_rating_diff_public_sorted = dict(sorted(rating_diff_public_dict.items(), key=lambda item: item[1], reverse=True))
    negative_rating_diff_public_sorted = dict(sorted(rating_diff_public_dict.items(), key=lambda item: item[1]))
    positive_rating_diff_critics_sorted = dict(sorted(rating_diff_critics_dict.items(), key=lambda item: item[1], reverse=True))
    negative_rating_diff_critics_sorted = dict(sorted(rating_diff_critics_dict.items(), key=lambda item: item[1]))
    # print(positive_rating_diff_public_sorted)
    # print(df_rated["Title"][np.nanargmax(rating_diff_public)], np.round(rating_diff_public[np.nanargmax(rating_diff_public)], 2))
    # print(df_rated["Title"][np.nanargmin(rating_diff_public)], rating_diff_public[np.nanargmin(rating_diff_public)])
    # print(df_rated["Title"][np.nanargmax(rating_diff_critics)], rating_diff_critics[np.nanargmax(rating_diff_critics)])
    # print(df_rated["Title"][np.nanargmin(rating_diff_critics)], rating_diff_critics[np.nanargmin(rating_diff_critics)])
    # print(df_rated["Title"][np.where(np.abs(rating_diff_public)<0.001)[0]])
    # print(df_rated["Title"][np.where(np.abs(rating_diff_critics)<0.001)[0]])
    avg_rating_diff_public = np.round(np.mean(rating_diff_public),3)
    avg_rating_diff_critics = np.round(np.mean(rating_diff_critics),3)
    median_rating_diff_public = np.round(np.median(rating_diff_public),2)
    median_rating_diff_critics = np.round(np.median(rating_diff_critics),2)
    # print(avg_rating_diff_critics, avg_rating_diff_public, median_rating_diff_critics, median_rating_diff_public)
    # print(np.sum(rating_diff_public), np.sum(rating_diff_critics))

    plot_contrarian_bars(positive_rating_diff_public_sorted, "Positive rating difference vs IMDb", "pos_rating_diff_public", dir=dir)
    plot_contrarian_bars(negative_rating_diff_public_sorted, "Negative rating difference vs IMDb", "neg_rating_diff_public", dir=dir)
    plot_contrarian_bars(positive_rating_diff_critics_sorted, "Positive rating difference vs Metascore", "pos_rating_diff_critics", dir=dir)
    plot_contrarian_bars(negative_rating_diff_critics_sorted, "Negative rating difference vs Metascore", "neg_rating_diff_critics", dir=dir)

    composer_ratings, composer_avg_ratings, composer_median_ratings = get_people_ratings(df_rated, "Composers", True)
    actor_ratings, actor_avg_ratings, actor_median_ratings = get_people_ratings(df_rated, "Cast", True)
    director_ratings, director_avg_ratings, director_median_ratings = get_people_ratings(df_rated, "Directors", True)
    writer_ratings, writer_avg_ratings, writer_median_ratings = get_people_ratings(df_rated, "Writers", True)
    genre_ratings, genre_avg_ratings, genre_median_ratings = get_people_ratings(df_rated, "Genres", True)
    
    composer_ratings, composer_avg_ratings_low, composer_median_ratings_low = get_people_ratings(df_rated, "Composers", False)
    actor_ratings, actor_avg_ratings_low, actor_median_ratings_low = get_people_ratings(df_rated, "Cast", False)
    director_ratings, director_avg_ratings_low, director_median_ratings_low = get_people_ratings(df_rated, "Directors", False)
    writer_ratings, writer_avg_ratings_low, writer_median_ratings_low = get_people_ratings(df_rated, "Writers", False)
    genre_ratings, genre_avg_ratings_low, genre_median_ratings_low = get_people_ratings(df_rated, "Genres", False)

    name = "Rachel McAdams"
    df_actor = df_rated[df_rated["Cast"].str.contains(name, na=False)][["Title", "Rating"]]
    film_ratings = dict(zip(df_actor["Title"], df_actor["Rating"]))
    print(f"{dir} has rated {len(actor_ratings[name])} {name} films:\n"
          f"Average: {actor_avg_ratings[name]}\n"
          f"Median: {actor_median_ratings[name]}\n"
          f"{film_ratings}")
    
    name = "Matt Damon"
    df_actor = df_rated[df_rated["Cast"].str.contains(name, na=False)][["Title", "Rating"]]
    film_ratings = dict(zip(df_actor["Title"], df_actor["Rating"]))
    print(f"{dir} has rated {len(actor_ratings[name])} {name} films:\n"
          f"Average: {actor_avg_ratings[name]}\n"
          f"Median: {actor_median_ratings[name]}\n"
          f"{film_ratings}")

    # print(composer_avg_ratings)
    # print(actor_avg_ratings)
    # print(director_avg_ratings)
    # print(writer_avg_ratings)

    plot_rated_people(composer_median_ratings, "Composer", "Median", "Highest rated composers", "composers_highest_median_ratings", dir)
    plot_rated_people(actor_median_ratings, "Actor", "Median", "Highest rated actors", "actors_highest_median_ratings", dir)
    plot_rated_people(director_median_ratings, "Director", "Median", "Highest rated directors", "directors_highest_median_ratings", dir)
    plot_rated_people(writer_median_ratings, "Writer", "Median", "Highest rated writers", "writers_highest_median_ratings", dir)
    plot_rated_people(genre_median_ratings, "Genre", "Median", "Highest rated Genres", "genres_highest_median_ratings", dir)

    plot_rated_people(composer_median_ratings_low, "Composer", "Median", "Lowest rated composers", "composers_lowest_median_ratings", dir)
    plot_rated_people(actor_median_ratings_low, "Actor", "Median", "Lowest rated actors", "actors_lowest_median_ratings", dir)
    plot_rated_people(director_median_ratings_low, "Director", "Median", "Lowest rated directors", "directors_lowest_median_ratings", dir)
    plot_rated_people(writer_median_ratings_low, "Writer", "Median", "Lowest rated writers", "writers_lowest_median_ratings", dir)
    plot_rated_people(genre_median_ratings_low, "Genre", "Median", "Lowest rated Genres", "genres_lowest_median_ratings", dir)

    plot_rated_people(composer_avg_ratings, "Composer", "Average", "Highest rated composers", "composers_highest_average_ratings", dir)
    plot_rated_people(actor_avg_ratings, "Actor", "Average", "Highest rated actors", "actors_highest_average_ratings", dir)
    plot_rated_people(director_avg_ratings, "Director", "Average", "Highest rated directors", "directors_highest_average_ratings", dir)
    plot_rated_people(writer_avg_ratings, "Writer", "Average", "Highest rated writers", "writers_highest_average_ratings", dir)
    plot_rated_people(genre_avg_ratings, "Genre", "Average", "Highest rated Genres", "genres_highest_average_ratings", dir)

    plot_rated_people(composer_avg_ratings_low, "Composer", "Average", "Lowest rated composers", "composers_lowest_average_ratings", dir)
    plot_rated_people(actor_avg_ratings_low, "Actor", "Average", "Lowest rated actors", "actors_lowest_average_ratings", dir)
    plot_rated_people(director_avg_ratings_low, "Director", "Average", "Lowest rated directors", "directors_lowest_average_ratings", dir)
    plot_rated_people(writer_avg_ratings_low, "Writer", "Average", "Lowest rated writers", "writers_lowest_average_ratings", dir)
    plot_rated_people(genre_avg_ratings_low, "Genre", "Average", "Lowest rated Genres", "genres_lowest_average_ratings", dir)

    return None

def main_all(dir):
    df_all = load_all_dataframe(dir=dir)

    imdb_ratings = df_all["IMDbRating"]
    metascore = df_all["Metascore"]
    plot_all_ratings(imdb_ratings, metascore, dir=dir)

    plot_world_map(df_all, dir=dir)

    year_counts = df_all["Year"].value_counts().sort_index()
    plot_year_histogram(df_all["Year"].values, dir=dir)
    # print(f"Number of films seen per year:\n{plotyear_counts}\n")

    actor_counts = get_person_counts(df_all["Cast"].copy())
    director_counts = get_person_counts(df_all["Directors"].copy())
    writer_counts = get_person_counts(df_all["Writers"].copy())
    composer_counts = get_person_counts(df_all["Composers"].copy())
    lang_counts = get_person_counts(df_all["OriginalLanguage"].copy())
    coun_counts = get_person_counts(df_all["OriginCountry"].copy())
    genre_counts = get_person_counts(df_all["Genres"].copy())

    filtered_actor_counts = [(actor, count) for actor, count in actor_counts.most_common(10)]
    filtered_director_counts = [(director, count) for director, count in director_counts.most_common(10)]
    filtered_writer_counts = [(writer, count) for writer, count in writer_counts.most_common(10)]
    filtered_composer_counts = [(composer, count) for composer, count in composer_counts.most_common(10)]
    filtered_genre_counts = [(genre, count) for genre, count in genre_counts.most_common(10)]

    plot_people_bar_graph(filtered_actor_counts, "actor", dir=dir)
    plot_people_bar_graph(filtered_director_counts, "director", dir=dir)
    plot_people_bar_graph(filtered_writer_counts, "writer", dir=dir)
    plot_people_bar_graph(filtered_composer_counts, "composer", dir=dir)
    plot_people_bar_graph(filtered_genre_counts, "genre", dir=dir)



    # print(f"The 20 actors I have seen the most movies with:\n{filtered_actor_counts}")
    # print(f"The 20 directors I have seen the most movies with:\n{filtered_director_counts}")
    # print(f"The 20 writers I have seen the most movies with:\n{filtered_writer_counts}")
    # print(f"The 20 composers I have seen the most movies with:\n{filtered_composer_counts}\n")
    # print(f"The languages I have seen the most movies with:\n{lang_counts.most_common()}")
    # print(f"The countries I have seen the most movies from:\n{coun_counts.most_common()}\n")

    print(f"{dir} has seen {actor_counts['Rachel McAdams']} Rachel McAdams films:\n{person_films(df_all, 'Rachel McAdams', 'Cast')}")
    # print(f"I have seen {actor_counts['Mark Ruffalo']} Mark Ruffalo films:\n{person_films(df_all, 'Mark Ruffalo', 'Cast')}")
    # print(f"I have seen {actor_counts['Tom Cruise']} Tom Cruise films:\n{person_films(df_all, 'Tom Cruise', 'Cast')}")
    print(f"{dir} has seen {actor_counts['Matt Damon']} Matt Damon films:\n{person_films(df_all, 'Matt Damon', 'Cast')}")
    # print(f"I have seen {actor_counts['Vera Farmiga']} Vera Farmiga films:\n{person_films(df_all, 'Vera Farmiga', 'Cast')}")
    # print(f"I have seen {actor_counts['Anne Hathaway']} Anne Hathaway films:\n{person_films(df_all, 'Anne Hathaway', 'Cast')}\n")

    # print(f"I have seen {director_counts['Stanley Kubrick']} Stanley Kubrick films:\n{person_films(df_all, 'Stanley Kubrick', 'Directors')}")
    # print(f"I have seen {director_counts['Christopher Nolan']} Christopher Nolan films:\n{person_films(df_all, 'Christopher Nolan', 'Directors')}")
    # print(f"I have seen {director_counts['Steven Spielberg']} Steven Spielberg films:\n{person_films(df_all, 'Steven Spielberg', 'Directors')}")
    # print(f"I have seen {director_counts['Greta Gerwig']} Greta Gerwig films:\n{person_films(df_all, 'Greta Gerwig', 'Directors')}")
    # print(f"I have seen {director_counts['Sofia Coppola']} Sofia Coppola films:\n{person_films(df_all, 'Sofia Coppola', 'Directors')}")
    # print(f"I have seen {director_counts['David Fincher']} David Fincher films:\n{person_films(df_all, 'David Fincher', 'Directors')}\n")

    # print(f"I have seen {composer_counts['John Williams']} John Williams films:\n{person_films(df_all, 'John Williams', 'Composers')}")
    # print(f"I have seen {composer_counts['Howard Shore']} Howard Shore films:\n{person_films(df_all, 'Howard Shore', 'Composers')}")
    # print(f"I have seen {composer_counts['Hans Zimmer']} Hans Zimmer films:\n{person_films(df_all, 'Hans Zimmer', 'Composers')}")

    return None

if __name__=='__main__':
    audun_bool = input("Is this for Audun? (y/n): ").lower() == 'y'
    mali_bool = input("Is this for Mali? (y/n): ").lower() == 'y'
    if audun_bool:
        dir = "audun"
    elif mali_bool:
        dir = "mali"
    else:
        raise ValueError("Invalid user specified.")
    main_rated(dir)
    main_all(dir)