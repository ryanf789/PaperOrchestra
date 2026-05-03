# Data and Context Log

## Main Dataset: Goodreads

The main dataset is Goodreads book-level data.

The raw Goodreads file is:

- `Goodreads-Books.csv`

The main cleaning script is:

- `S1_Goodreads_cleaning.py`

The cleaned output is:

- `Goodreads-Books-cleaned.csv`

The genre-classified output is:

- `Goodreads-Books-cleaned_W_genre.csv`

The final analysis file is:

- `Goodreads_Data_analyses_file.csv`

## Goodreads Variables

The Goodreads analysis uses the following key variables:

- `id`
- `name`
- `star_rating`
- `num_ratings`
- `num_reviews`
- `summary`
- `genres`
- `first_published`

Additional variables are created during cleaning and analysis:

- `genre0`
- `genre1`
- `genre2`
- `genre_classified`
- `summary_tokens`
- `summary_len`
- `L`
- `R`
- `Y_pop`
- `Y_rate`
- `decade`

## Genre Classification

The project classifies books into a single genre using genre frequency information.

The script `S2_identify genre and words.py` begins with `genre0`, then uses `genre1` or `genre2` when the primary genre is too rare. The threshold used in the script is 200 books.

The final genre variable is:

- `genre_classified`

Books with no usable genre are assigned `NONE` or removed from relevant analysis.

## Genre-Level Word Frequencies

The script `S3_Words by Genre.py` identifies words within each genre using a consistent tokenization procedure.

The word identification procedure uses:

- regex `[a-zA-Z]+`
- lowercase conversion
- stopword removal
- minimum word length of 3

The output file is:

- `genre_word_frequencies_all.csv`

The output contains:

- `genre`
- `word`
- `frequency`

## Atypicality Measures

The script `S4_Distance_Calc.py` creates several book-level atypicality or typicality measures.

The final analysis file includes:

- `atyp_jaccard`
- `tfidf_within_genre_score`
- `logodds_z_score`
- `keyness_llr_score`
- `atyp_bigram_jaccard`
- `atyp_embedding_cosine`
- `tfidf_within_genre_typical01`
- `logodds_z_typical01`
- `keyness_llr_typical01`
- `bigram_jaccard_typical01`
- `embedding_cosine_typical01`

## Main Goodreads Outcomes

Popularity:

- `num_ratings`
- `R = log(1 + num_ratings)`
- `Y_pop = R`

Evaluation:

- `star_rating`
- `Y_rate = star_rating`

## Main Goodreads Controls

The models include:

- `L = log(summary_len)`
- `genre_classified` fixed effects
- `decade` fixed effects

For rating models, popularity is also used as a control:

- `R = log(1 + num_ratings)`

## Supplementary Dataset: TMDb

The supplementary dataset is TMDb movie-level data.

The TMDb scripts use:

- `tmdb_5000_movies.csv`

The TMDb analysis includes:

- `title`
- `overview`
- `genres`
- `keywords`
- `popularity`
- `vote_average`
- `vote_count`
- `release_date`

## TMDb Genre and Keyword Processing

TMDb genres and keywords are parsed from JSON-like list columns.

The primary genre is defined as the first genre in the parsed genre list.

Movie-level atypicality is computed using Jaccard distance between a movie's keywords and the top typical keywords in its primary genre.

## TMDb Outcomes

Popularity:

- `log_num_ratings = log(1 + vote_count)`

Evaluation:

- `vote_average`

## Dataset Role

Goodreads is the main empirical setting.

TMDb provides a supplementary cultural product setting that mirrors the Goodreads analysis in films.
