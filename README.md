# Modeling and Simulation: Auction Price Distributions

## Project Overview
This project explores probability distributions by simulating synthetic resale price behavior from a real dataset:

- `gtr_auction_resale_dataset.csv`
- Python script: `Disitribution.py`
- Output plots folder: `Pics/`

The script reads auction resale prices (`final_price_usd`), computes summary statistics, generates random samples from multiple probability distributions, and saves a histogram for each distribution as a PNG image.

The goal is educational: compare how different distributions shape possible outcomes and how each one might model auction-related data.

## What the Script Does
1. Loads the dataset with pandas.
2. Extracts non-null values from `final_price_usd`.
3. Calculates key statistics (mean, standard deviation, min, max).
4. Simulates random values for each distribution.
5. Creates and saves histogram plots into `Pics/`.

## Distributions Included and Explanation

### 1) Exponential Distribution
- Used for modeling waiting times and memoryless processes.
- Shape: strongly right-skewed; many small values and a long tail of larger values.
- In this project: generated with `np.random.exponential(scale=mean_price / 2, size=len(price))`.

### 2) Normal Distribution
- The classic bell-shaped distribution.
- Shape: symmetric around the mean.
- In this project: centered at observed mean price with observed standard deviation using `np.random.normal(...)`.

### 3) Poisson Distribution
- Models the count of events in a fixed interval.
- Shape: discrete, non-negative integers.
- In this project: lambda (`lam`) is based on how often prices are above the mean, then used with `np.random.poisson(...)`.
- Note: the script variable and output names use `poison` (spelling typo), but the distribution itself is Poisson.

### 4) Binomial Distribution
- Models number of successes in `n` independent trials with success probability `p`.
- Shape: discrete from `0` to `n`.
- In this project: success is defined as `price > mean_price`, with `n = 20` and `p` from data.

### 5) Triangular Distribution
- Defined by minimum (`left`), most likely value (`mode`), and maximum (`right`).
- Useful when only rough bounds and a likely central value are known.
- In this project: `left=min_price`, `mode=mean_price`, `right=max_price`.

### 6) Lognormal Distribution
- If the log of a variable is normally distributed, the variable is lognormal.
- Shape: positive-only and right-skewed.
- Common for prices and multiplicative growth processes.
- In this project: fit log mean/std from `log(price)` and generate with `np.random.lognormal(...)`.

### 7) Gamma Distribution
- Positive-only, flexible right-skewed distribution.
- Often used for waiting times and non-negative continuous variables.
- In this project: fixed `shape = 2.0` and `scale = mean_price / shape`.

### 8) Beta Distribution
- Defined on the interval `[0, 1]`.
- Useful for proportions and normalized quantities.
- In this project: prices are min-max scaled first, then sampled with `a=5.0`, `b=2.0` via `np.random.beta(...)`.

### 9) Weibull Distribution
- Common in reliability analysis and time-to-failure modeling.
- Shape depends on parameter `a`; can model different hazard behaviors.
- In this project: generated with `np.random.weibull(a=1.5, size=len(price)) * mean_price`.

### 10) Uniform Distribution
- Every value in `[low, high]` is equally likely.
- Shape: flat (constant density).
- In this project: bounded by observed minimum and maximum prices.

## Output Files
The script saves one histogram image per distribution in `Pics/`:

- Exponential_histogram.png
- Normal_histogram.png
- Poison_histogram.png
- Binomial_histogram.png
- Triangular_histogram.png
- Lognormal_histogram.png
- Gamma_histogram.png
- Beta_histogram.png
- Weibull_histogram.png
- Uniform_histogram.png

## How To Run
From the project root:

```bash
python Disitribution.py
```

Dependencies:

- pandas
- numpy
- matplotlib

Install if needed:

```bash
pip install pandas numpy matplotlib
```


