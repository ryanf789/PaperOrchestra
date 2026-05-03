# Results Log

## Available Result Files

The uploaded result files include:

- `goodreads_popularity.txt`
- `goodreads_ratings.txt`
- `tmdb_popularity.txt`
- `tmdb_ratings.txt`

The uploaded analysis scripts include:

- `Goodreads Popularity.py`
- `Goodreads Ratings.py`
- `TMDB Popularity.py`
- `TMDB Ratings.py`
- `S5_Analyses.py`

## Main Goodreads Popularity Results

The Goodreads popularity analysis uses:

`log_num_ratings`

as the dependent variable.

The H1 model estimates:

`log_num_ratings ~ atypicality + log_summary_len + C(primary_genre) + C(pub_decade)`

The result file shows a negative association between atypicality and log number of ratings in the main Goodreads popularity model.

The visible H1 coefficient for atypicality in the Goodreads popularity output is negative and statistically significant.

Exact visible value:

- atypicality coefficient: approximately -5.0933
- p-value: 0.000
- standard errors: HC3

## Main Goodreads Evaluation Results

The Goodreads rating analysis uses:

`star_rating`

as the dependent variable.

The model includes:

- atypicality
- log summary length
- log number of ratings
- genre controls
- decade controls

The result file reports OLS models with HC3 robust standard errors.

[NEEDS RESULT: exact Goodreads rating coefficient for atypicality from `goodreads_ratings.txt`]

## Main TMDb Popularity Results

The TMDb popularity analysis uses:

`log_num_ratings = log(1 + vote_count)`

as the dependent variable.

The model includes:

- atypicality
- log summary length
- primary genre controls
- release decade controls

[NEEDS RESULT: exact TMDb popularity coefficient for atypicality from `tmdb_popularity.txt`]

## Main TMDb Evaluation Results

The TMDb rating analysis uses:

`vote_average`

as the dependent variable.

The visible TMDb rating result shows a negative and statistically significant association between atypicality and vote average.

Exact visible value:

- atypicality coefficient: approximately -2.1791
- p-value: 0.001
- standard errors: HC3

## Multi-Measure Goodreads Analysis

The `S5_Analyses.py` script runs models across multiple atypicality and typicality measures:

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

For each measure, the script estimates popularity and rating models and stores coefficient-level and model-level output.

[NEEDS RESULT: summary table of signs and significance across all measures]

## Interpretation Direction

The results should be written carefully.

If atypicality is negatively associated with popularity or rating, the interpretation is that greater deviation from genre norms may reduce consumer attention, adoption, or evaluation.

If moderate atypicality outperforms both typical and radical products, the interpretation is consistent with an optimal distinctiveness or novelty-familiarity trade-off.

If the quadratic term is significant, the paper should discuss whether the shape is U-shaped or inverted-U-shaped, based on the signs and predicted values.

## Important Caution

Do not generalize the result as causal.

Do not claim that atypicality always hurts or helps product success unless the full set of results supports that claim.

Do not mix up atypicality and typicality measures. Some variables are coded as atypicality, while others are recoded as 0-1 typicality.

## Missing Result Items

[NEEDS RESULT: exact H1, H1-U, H2, H2-3, and H3 results for Goodreads popularity]

[NEEDS RESULT: exact H1, H1-U, H2, H2-3, and H3 results for Goodreads ratings]

[NEEDS RESULT: exact H1, H1-U, H2, H2-3, and H3 results for TMDb popularity]

[NEEDS RESULT: exact H1, H1-U, H2, H2-3, and H3 results for TMDb ratings]

[NEEDS RESULT: coefficient summary table from S5 multi-measure analyses]

[NEEDS RESULT: model fit statistics and sample sizes for all main models]

[NEEDS RESULT: generated figures from the graphs folder]
