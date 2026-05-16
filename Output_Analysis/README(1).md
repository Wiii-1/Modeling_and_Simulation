# Sample Output Analysis Simulation

This folder contains a sample **non-terminating simulation** of a single-server queue (M/M/1 style) implemented in Python.

## Files
- `steady_state_queue_sim.py` - main simulation script
- `customer_trace.csv` - detailed output from one long run
- `welch_plot_data.csv` - data you can plot for Welch Method
- `summary_results.csv` - compact results table

## What the script does
1. Simulates multiple replications of a queue with exponential interarrival and service times.
2. Uses a Welch-style smoothing procedure to suggest a warm-up deletion point.
3. Applies the Replication-Deletion approach.
4. Applies the Batch Means method on one long run.

## Current sample results
- Suggested warm-up deletion: 0 customers
- Welch tail smoothed mean waiting time: 7.5918
- Replication-Deletion estimated mean waiting time: 6.7685
- Replication-Deletion sample standard deviation across replications: 0.9077
- Batch Means estimated mean waiting time: 5.6964
- Batch Means sample standard deviation across batches: 1.5784

## Replication means
5.4709, 5.5805, 7.5918, 6.9584, 7.6654, 6.1330, 7.5057, 7.2357, 5.8671, 7.6763

## Batch means
8.1881, 5.2873, 6.3315, 4.9767, 3.5413, 5.1993, 8.3233, 3.9513, 6.6617, 5.3403, 4.6207, 5.1428, 3.8122, 3.7139, 6.4024, 4.6553, 7.2197, 5.9377, 5.5769, 9.0461

## How to run
```bash
python steady_state_queue_sim.py
```

## Dev note

I did the best I could, but I still do not know if this is enough or if my understanding is correct.



