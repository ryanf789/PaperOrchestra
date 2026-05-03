# Robustness Log

## Existing Robustness and Extensions

The project already includes several extensions beyond a single linear model.

## Multiple Atypicality Measures

The `S4_Distance_Calc.py` script constructs multiple atypicality and typicality measures.

The `S5_Analyses.py` script runs the empirical models across the full measure list.

This provides measurement robustness across:

- Jaccard atypicality
- TF-IDF within-genre score
- log-odds z-score
- keyness LLR score
- bigram Jaccard atypicality
- embedding cosine atypicality
- 0-1 typicality recodings

## Nonlinear Specifications

The analysis includes quadratic specifications using:

- `A`
- `A2`

or in the earlier scripts:

- `atypicality_c`
- `atypicality_c2`

This tests whether the relationship between atypicality and market response is nonlinear.

## Group-Based Specifications

The project includes:

- binary typical versus atypical grouping
- three-level typical / moderate / radical grouping

These support interpretation of whether moderate or radical atypicality differs from typical genre positioning.

## Genre Context Moderation

The project includes H3 analyses based on:

- mean genre atypicality
- genre dispersion in atypicality

These analyses test whether atypicality has different implications in more typical, less typical, homogeneous, or heterogeneous genres.

## Cross-Domain Replication

The project includes both Goodreads and TMDb.

Goodreads provides the main book setting.

TMDb provides a supplementary film setting.

This supports cross-domain comparison across cultural product categories.

## Current Controls

Goodreads models include:

- log summary length
- genre fixed effects
- publication decade fixed effects
- log number of ratings as a control in rating models

TMDb models include:

- log overview length
- primary genre fixed effects
- release decade fixed effects

## Current Standard Errors

The scripts use HC3 heteroskedasticity-robust standard errors.

## Remaining Robustness Needs

[NEEDS ROBUSTNESS CHECK: remove implausible publication years or future decades in Goodreads]

[NEEDS ROBUSTNESS CHECK: winsorize or trim extreme popularity outcomes]

[NEEDS ROBUSTNESS CHECK: compare raw popularity with log popularity]

[NEEDS ROBUSTNESS CHECK: include author-level controls if available]

[NEEDS ROBUSTNESS CHECK: include number of reviews as an alternative popularity outcome]

[NEEDS ROBUSTNESS CHECK: test whether results hold within major genres only]

[NEEDS ROBUSTNESS CHECK: test alternative thresholds for typical genre words]

[NEEDS ROBUSTNESS CHECK: test alternative TOP_K genre word values]

[NEEDS ROBUSTNESS CHECK: test alternative minimum genre size thresholds]

[NEEDS ROBUSTNESS CHECK: check sensitivity to books with very short summaries]

[NEEDS ROBUSTNESS CHECK: check whether missing or noisy genre labels affect results]

## Important Caution

Because the design is observational, robustness checks should be framed as addressing alternative explanations and measurement sensitivity, not as proving causality.
