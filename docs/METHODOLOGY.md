# Research methodology

This document summarizes the experimental pipeline described in the accompanying manuscript. It is intended for technical review and project presentation, not as a substitute for the underlying participant-level data or the original research code.

## Dataset and synchronization

- Wearable device: INNOMES smartwatch
- Sample: 1 male worker in his 50s
- Duration: 28 days; initial 14-day warm-up/reference and 14-day evaluation
- Activity indicators: step count and a device-provided sport-value indicator
- Physiological indicator: optical/PPG-derived heart rate
- Harmonized sampling: 5-minute intervals, with heart rate aggregated from 1-minute readings
- Data handling: invalid sensor readings and missing intervals excluded without interpolation

## Personalized normalization

For each activity-related signal `x`, the reference-window median and interquartile range provide the normalizing terms:

`Z_x(t) = (x(t) - median(x_reference)) / IQR(x_reference)`

The reported reference-window selection compares candidate periods from 7 to 14 days, selecting 14 days for the analysis. This is a within-case methodological choice, not an established multi-person optimum.

## Feature combination

`ActivityProxy(t) = max(Z_step(t), Z_sport(t))`

The maximum operator uses the larger normalized activity signal at each time bin to combine the two movement-derived indicators.

## State definition

| State | Rule |
|:--|:--|
| Baseline | Activity proxy < 0.5 |
| Elevated | 0.5 ≤ activity proxy < 3 |
| High | Activity proxy ≥ 3 |

The resulting sequence is explored with histograms, daily activity summaries, and a row-normalized transition matrix.

## Physiological evaluation

Heart rate is not used to create the activity proxy or assign activity states. After classification, it is used to examine:

1. HR distribution across activity states
2. Proxy–HR association (reported correlation ≈ 0.285)
3. Cross-correlation of activity/HR signals (peak observed at lag 0 in 5-minute bins)
4. HR trajectories around activity-state transitions
5. Observed post-activity HR recovery events (n=124; mean 13.27 min; median 5 min)

These analyses evaluate within-case physiological consistency, not activity-recognition classification accuracy.

## What the companion files reproduce

- `assets/activity_states.png`: the reported state counts and percentages
- `assets/state_transition_matrix.png`: the reported 3x3 transition probabilities
- `assets/results_overview.png`: the reported study summary metrics
- `dashboard/index.html`: a new interactive portfolio display of the aggregate metrics

The 28-day raw wearable time series is not bundled, so plots requiring it (such as participant heatmaps or minute-level HR curves) are not reconstructed here.
