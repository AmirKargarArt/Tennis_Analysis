"""Question 04 — longest recorded match, with transparent time validation.

Run after loading the project `matches` DataFrame and defining `OUT` and `FIG`.
The raw maximum is reported separately from the cleaned analytical maximum.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display


# -----------------------------------------------------------------------------
# 1) Prepare the duration field and document its unit
# -----------------------------------------------------------------------------
q04 = matches.copy()
q04['duration_hours'] = pd.to_numeric(
    q04['duration_hours'],
    errors='coerce'
)

q04_total = len(q04)
q04_invalid = q04[
    q04['duration_hours'].isna()
    | (q04['duration_hours'] <= 0)
].copy()

q04_suspicious = q04[
    q04['duration_hours'] > 12
].copy()

# Twelve hours is used as a transparent quality-review threshold.
# It is not presented as a tennis rule; it prevents timestamp/interval errors
# from dominating the answer.
q04_clean = q04[
    q04['duration_hours'].notna()
    & (q04['duration_hours'] > 0)
    & (q04['duration_hours'] <= 12)
].copy()


# -----------------------------------------------------------------------------
# 2) Convert decimal hours to a reader-friendly hours/minutes label
# -----------------------------------------------------------------------------
q04_clean['duration_minutes'] = (
    q04_clean['duration_hours'] * 60
).round().astype(int)

q04_clean['duration_hm'] = q04_clean['duration_minutes'].map(
    lambda minutes: (
        f'{minutes // 60} hours {minutes % 60:02d} minutes'
    )
)

q04_clean = q04_clean.sort_values(
    'duration_minutes',
    ascending=False
)


# -----------------------------------------------------------------------------
# 3) Report raw, excluded and final analytical answers
# -----------------------------------------------------------------------------
q04_raw_max = q04['duration_hours'].max()
q04_logical_max = q04_clean['duration_hours'].max()
q04_logical_row = q04_clean.iloc[0]

q04_summary = pd.DataFrame({
    'metric': [
        'total_records',
        'invalid_or_nonpositive_records',
        'suspicious_over_12_hours',
        'valid_records_after_filter',
        'raw_maximum_hours',
        'logical_maximum_hours',
        'logical_maximum_minutes',
        'logical_maximum_hm'
    ],
    'value': [
        q04_total,
        len(q04_invalid),
        len(q04_suspicious),
        len(q04_clean),
        q04_raw_max,
        q04_logical_max,
        int(round(q04_logical_max * 60)),
        q04_logical_row['duration_hm']
    ]
})

q04_summary.to_csv(
    OUT / 'q04_duration_summary.csv',
    index=False,
    encoding='utf-8-sig'
)

q04_suspicious.sort_values(
    'duration_hours',
    ascending=False
).to_csv(
    OUT / 'q04_suspicious_over_12_hours.csv',
    index=False,
    encoding='utf-8-sig'
)

q04_clean.to_csv(
    OUT / 'q04_clean_duration_8056.csv',
    index=False,
    encoding='utf-8-sig'
)

print(f'Total records: {q04_total:,}')
print(f'Invalid/non-positive records: {len(q04_invalid):,}')
print(f'Suspicious records over 12 hours: {len(q04_suspicious):,}')
print(f'Valid records after filter: {len(q04_clean):,}')
print(f'Raw maximum: {q04_raw_max:.2f} hours')
print(f'Logical maximum: {q04_logical_max:.2f} hours')
print(f'Logical maximum: {q04_logical_row["duration_hm"]}')

display(q04_clean.head(20))


# -----------------------------------------------------------------------------
# 4) Project-style chart based only on the validated records
# -----------------------------------------------------------------------------
q04_top = q04_clean.head(20).sort_values('duration_hours')
q04_top['match_label'] = (
    q04_top['h_name'].fillna('Unknown')
    + ' vs '
    + q04_top['a_name'].fillna('Unknown')
)

q04_fig, q04_ax = plt.subplots(figsize=(14, 10), layout='constrained')
q04_fig.set_facecolor('#F4F6F0')
q04_ax.set_facecolor('#FFFFFF')
q04_bars = q04_ax.barh(
    q04_top['match_label'],
    q04_top['duration_hours'],
    color='#5A7263',
    height=.62,
    edgecolor='none'
)
q04_ax.bar_label(
    q04_bars,
    labels=[f'{v:.2f} h' for v in q04_top['duration_hours']],
    padding=4,
    color='#0F3826',
    fontsize=9,
    fontweight='bold'
)
q04_ax.set_title(
    'Longest Logical Tennis Matches',
    loc='left',
    fontsize=19,
    fontweight='bold',
    color='#0F3826',
    pad=18
)
q04_ax.set_xlabel('Duration (hours)', fontsize=12, color='#20352A', labelpad=10)
q04_ax.set_ylabel('Match', fontsize=12, color='#20352A', labelpad=10)
q04_ax.set_xlim(0, max(12.5, q04_top['duration_hours'].max() + .8))
q04_ax.grid(axis='x', linestyle=(0, (3, 4)), color='#E6EAE2', alpha=.9, linewidth=.8)
q04_ax.grid(axis='y', visible=False)
q04_ax.spines[['top', 'right']].set_visible(False)
q04_ax.spines[['left', 'bottom']].set_color('#D0D7CA')
q04_ax.tick_params(colors='#20352A', labelsize=10, length=0, pad=8)
q04_fig.savefig(FIG / 'q04_longest_logical_matches.png', dpi=220, bbox_inches='tight', facecolor='#F4F6F0')
q04_fig.savefig(FIG / 'q04_longest_logical_matches.svg', bbox_inches='tight', facecolor='#F4F6F0')
plt.show()
plt.close(q04_fig)
