# Figure and Table Inventory

## Required Figures

### Figure 1: Conceptual Framework

Purpose: Show the theoretical relationship among genre atypicality, novelty/familiarity mechanisms, popularity, and evaluation.

Suggested structure:

- Genre norms
- Product atypicality
- Differentiation / attention mechanism
- Categorization difficulty / uncertainty mechanism
- Popularity
- Evaluation

### Figure 2: Measurement Pipeline

Purpose: Show the empirical construction of atypicality.

Suggested pipeline:

- raw product metadata
- summary / overview / keywords
- genre classification
- genre-level typical words or keywords
- product-level atypicality measures
- regression models

### Figure 3: Distribution of Atypicality

Purpose: Show the distribution of atypicality in Goodreads and possibly TMDb.

Include:

- histogram or density plot of `atyp_jaccard`
- optional comparison across major genres

### Figure 4: Main Linear Effect

Purpose: Show predicted popularity or evaluation across the atypicality range.

Use model predictions from H1.

### Figure 5: Nonlinear Effect

Purpose: Show predicted market response from the quadratic model.

Use H1-U predictions.

### Figure 6: Typical / Moderate / Radical Comparison

Purpose: Show predicted outcomes for typical, moderate, and radical products.

Use H2-3 predictions.

### Figure 7: Genre Context Moderation

Purpose: Show whether atypicality effects differ by genre mean atypicality or genre dispersion.

Use H3 Spec A and H3 Spec B plots.

## Required Tables

### Table 1: Sample Construction

Purpose: Show how the Goodreads and TMDb samples are cleaned and filtered.

Include:

- raw observations
- observations with valid summaries / overviews
- observations with valid genres
- observations with valid outcomes
- final analysis sample

### Table 2: Descriptive Statistics

Purpose: Summarize key variables.

Include:

- popularity outcome
- evaluation outcome
- atypicality measures
- summary length
- publication or release decade
- genre counts

### Table 3: Correlation Matrix

Purpose: Show relationships among atypicality, popularity, evaluation, and controls.

### Table 4: Main Goodreads Results

Purpose: Report H1 and H1-U for Goodreads popularity and rating outcomes.

### Table 5: Typical / Moderate / Radical Results

Purpose: Report H2 and H2-3 group comparisons.

### Table 6: Genre Context Moderation Results

Purpose: Report H3 results for mean genre atypicality and genre dispersion.

### Table 7: Alternative Atypicality Measure Robustness

Purpose: Summarize results across all measures from `S5_Analyses.py`.

### Table 8: TMDb Supplementary Results

Purpose: Report TMDb popularity and rating analyses.

## Existing Generated Graphs

The scripts generate graphs for:

- H1 linear effect
- H1-U quadratic effect
- H2 binary typical vs atypical
- H2-3 typical / moderate / radical
- H3 genre mean atypicality moderation
- H3 genre dispersion moderation

## Missing Items

[NEEDS FIGURE: final conceptual framework]

[NEEDS FIGURE: measurement pipeline diagram]

[NEEDS TABLE: sample construction table]

[NEEDS TABLE: clean descriptive statistics table]

[NEEDS TABLE: coefficient summary across Goodreads and TMDb]

[NEEDS TABLE: multi-measure robustness summary from S5]

[NEEDS FIGURE: publication-quality versions of generated prediction plots]
