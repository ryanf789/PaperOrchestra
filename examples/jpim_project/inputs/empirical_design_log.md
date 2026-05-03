# Empirical Design Log

## Research Design

The project uses observational product-level data to estimate the relationship between genre atypicality and market response.

The main setting is Goodreads books. The supplementary setting is TMDb movies.

The empirical design is not randomized. The results should be interpreted as conditional associations rather than causal effects unless additional identification strategies are added.

## Main Independent Variable

The main independent variable is genre atypicality.

Genre atypicality captures the extent to which a product deviates from the typical words or keywords associated with its genre.

## Goodreads Measurement Approach

For Goodreads books, the project uses book summaries to measure genre atypicality.

The pipeline is:

1. Clean Goodreads data.
2. Extract and classify genres.
3. Build genre-level word frequency lists.
4. Tokenize each book summary.
5. Compare each book's summary words against typical words in its classified genre.
6. Compute book-level atypicality and typicality measures.
7. Estimate popularity and evaluation models.

## Goodreads Atypicality Measures

The project computes multiple measures:

### Unigram Jaccard atypicality

`atyp_jaccard`

This is based on the distance between a book's summary word set and the top typical words of its genre.

### TF-IDF within-genre score

`tfidf_within_genre_score`

This captures how strongly a book uses words that are informative within its genre.

### Log-odds z-score

`logodds_z_score`

This captures whether a book uses words that are distinctive of its genre relative to other genres.

### Keyness LLR score

`keyness_llr_score`

This captures genre-specific word keyness.

### Bigram Jaccard atypicality

`atyp_bigram_jaccard`

This measures atypicality based on bigram patterns rather than single words.

### Embedding cosine atypicality

`atyp_embedding_cosine`

This measures distance using embedding-based representation.

## Typicality Recoding

The project also recodes several measures into 0-1 typicality scales:

- `tfidf_within_genre_typical01`
- `logodds_z_typical01`
- `keyness_llr_typical01`
- `bigram_jaccard_typical01`
- `embedding_cosine_typical01`

## Scaling

In the main `S5_Analyses.py` script, each atypicality measure is standardized:

`A = (A_raw - mean(A_raw)) / sd(A_raw)`

The squared term is:

`A2 = A^2`

## Main Popularity Model

The popularity outcome is:

`Y_pop = log(1 + num_ratings)`

The baseline linear model is:

`Y_pop ~ A + L + C(genre_classified) + C(decade)`

where:

- `A` is the standardized atypicality or typicality measure
- `L` is log summary length
- `C(genre_classified)` are genre fixed effects
- `C(decade)` are decade fixed effects

## Main Evaluation Model

The evaluation outcome is:

`Y_rate = star_rating`

The baseline rating model is:

`Y_rate ~ A + L + R + C(genre_classified) + C(decade)`

where:

- `R = log(1 + num_ratings)` controls for popularity in the rating model

## Quadratic Models

The project estimates quadratic specifications to test nonlinear relationships:

Popularity:

`Y_pop ~ A + A2 + L + C(genre_classified) + C(decade)`

Evaluation:

`Y_rate ~ A + A2 + L + R + C(genre_classified) + C(decade)`

## Estimation

The main estimation approach is OLS with heteroskedasticity-robust HC3 standard errors.

The script stores model coefficients, standard errors, t-values, p-values, confidence intervals, model fit statistics, and prediction plots.

## TMDb Supplementary Design

The TMDb scripts mirror the Goodreads structure.

For TMDb:

- primary genre is extracted from the parsed `genres` list
- typical keywords are computed within primary genre
- movie-level atypicality is Jaccard distance between movie keywords and typical genre keywords
- popularity is measured with `log(1 + vote_count)`
- evaluation is measured with `vote_average`
- controls include `log_summary_len`, primary genre fixed effects, and release decade fixed effects

## Hypothesis Structure

### H1

Main linear effect of atypicality on popularity or evaluation.

### H1-U

Quadratic relationship between atypicality and market response.

### H2

Binary comparison between typical and atypical products.

### H2-3

Three-level comparison among typical, moderate, and radical products.

### H3

Moderation by genre context, including genre mean atypicality and genre dispersion in atypicality.

## Identification Caution

The design controls for genre, release decade, and summary length, but unobserved product quality, author reputation, publisher resources, marketing effort, and platform exposure may still confound the relationship.

The paper should avoid language such as "atypicality causes popularity" unless stronger identification is added.

Preferred language:

- "is associated with"
- "predicts"
- "is related to"
- "is consistent with"
