# LaTeX Table Patterns

Conventions for building LaTeX tables from `experimental_log.md` raw numeric
data, per the Section Writing Agent prompt requirements (App. F.1 p.47, item
2 "Data & Tables").

## Required: booktabs

Always use the `booktabs` package. The preamble in a typical conference
template already includes it; if not, add:

```latex
\usepackage{booktabs}
```

## Three rules only

Booktabs uses **only** three horizontal rules: `\toprule`, `\midrule`,
`\bottomrule`. No `\hline`. No vertical bars.

```latex
\begin{table}[t]
\centering
\caption{Comparison of methods on Dataset X.}
\label{tab:main_results}
\begin{tabular}{lccc}
\toprule
Method      & Accuracy & F1 & Latency (ms) \\
\midrule
Baseline    & 78.2     & 0.79 & 12.3 \\
\textbf{Ours} & \textbf{85.4} & \textbf{0.87} & \textbf{8.1} \\
\bottomrule
\end{tabular}
\end{table}
```

## From experimental_log markdown table → LaTeX

`experimental_log.md` contains tables in plain markdown:

```markdown
## 2. Raw Numeric Data

### Table 1: Performance comparison on Dataset X

| Method   | Accuracy | F1   | Latency (ms) |
|----------|----------|------|--------------|
| Baseline | 78.2     | 0.79 | 12.3         |
| Ours-S   | 82.1     | 0.83 | 9.4          |
| Ours-L   | 85.4     | 0.87 | 8.1          |
```

The `extract_metrics.py` helper parses these into JSON:

```json
{
  "tables": [
    {
      "label": "Performance comparison on Dataset X",
      "headers": ["Method", "Accuracy", "F1", "Latency (ms)"],
      "rows": [
        ["Baseline", "78.2", "0.79", "12.3"],
        ["Ours-S", "82.1", "0.83", "9.4"],
        ["Ours-L", "85.4", "0.87", "8.1"]
      ]
    }
  ]
}
```

The Section Writing Agent then converts each entry to a `table` environment
verbatim. Important rules from the prompt:

- **Do not hallucinate numbers.** Copy the exact values from
  `extract_metrics.py`'s output.
- **Bold the best result** in each column (the convention for top-tier ML
  papers).
- **Use `\multicolumn{N}{c}{...}` for grouped headers** when the table has
  metric families (e.g., "Seen (J%)", "Seen F", "Unseen (J%)", "Unseen F").
- **Right-align numeric columns** with `r`, left-align text columns with `l`.
  Use `c` only for narrow centered identifiers.
- **Use `\textbf{...}` for bold**, never `**...**` (markdown).

## Wide tables (2-column conference templates)

For tables that don't fit single-column width, use `table*` and `tabular*`
or `tabularx`:

```latex
\begin{table*}[t]
\centering
\caption{Ablation across all 6 components on 4 splits.}
\label{tab:ablation}
\begin{tabular}{lcccccc}
\toprule
Variant       & Seen J & Seen F & Unseen J & Unseen F & Mix J & Mix F \\
\midrule
Full          & 43.43  & 0.568  & 54.58    & 0.664    & 49.01 & 0.616 \\
- TB          & 33.05  & 0.507  & 50.48    & 0.657    & 41.77 & 0.582 \\
- TMFL        & 40.35  & 0.579  & 45.54    & 0.627    & 42.95 & 0.603 \\
\bottomrule
\end{tabular}
\end{table*}
```

The closing `\end{table*}` must match the opening `\begin{table*}`. The
`latex_sanity.py` script catches mismatches.

## Caption placement

```latex
\begin{table}[t]
\centering
\caption{Caption text here.}        % BEFORE the tabular for tables
\label{tab:my_label}
\begin{tabular}{...}
...
\end{tabular}
\end{table}
```

(For figures, `\caption` goes AFTER `\includegraphics`, not before. See
`figure-integration.md`.)

## Common pitfalls

| Issue | Fix |
|---|---|
| `\hline` everywhere | Replace with `\toprule` (top), `\midrule` (between header and body), `\bottomrule` (bottom). |
| Column too wide, runs off page | Switch to `table*` + `tabular*`. |
| Vertical bars | Remove. Booktabs forbids vertical rules. |
| Misaligned decimals | Use `S[table-format=2.2]` from `siunitx` if available, else right-align with `r`. |
| Table after Conclusion | Move it before. The prompt mandates this. |
| Hallucinated values | Cross-check against `extract_metrics.py` output. |
