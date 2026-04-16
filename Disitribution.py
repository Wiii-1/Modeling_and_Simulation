import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dataset display via pandas
pd.set_option("display.max_columns", None)
df = pd.read_csv("gtr_auction_resale_dataset.csv")
print(df.dtypes)


# Data extraction & Price 

price = df["final_price_usd"].dropna()

mean_price = price.mean()
std_price = price.std()
min_price = price.min()
max_price = price.max()

# Exponential Distribution

exponential_price = np.random.exponential(scale=mean_price / 2, size=(len(price)))

plt.figure(figsize=(8,5))
plt.hist(exponential_price, bins=20, color='salmon', edgecolor='black')
plt.title("Exponential Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Exponential_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Normal Distribution

normal_price = np.random.normal(loc=mean_price, scale=std_price, size=(len(price)))

plt.figure(figsize=(8,5))
plt.hist(normal_price, bins=20, color="pink", edgecolor='black')
plt.title("Normal Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Normal_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Poisson Distribution

lam = (price > mean_price).sum() / len(price) *10

poison_price = np.random.poisson(lam=lam, size=len(price))

plt.figure(figsize=(8,5))
plt.hist(poison_price, bins=20, color="lightgreen", edgecolor="black")
plt.title("Poison Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Poison_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Binomial Distribution

p = (price > mean_price).mean()
n = 20

binomial_price = np.random.binomial(n=n, p=p, size=(len(price)))

plt.figure(figsize=(8,5))
plt.hist(binomial_price, bins=range(n + 2), color="skyblue", edgecolor="black", align="left")
plt.title("Binomial Distribution")
plt.xlabel("The number of Successes in 20 auction sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Binomial_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Triangular Distribution
    
triangular_price = np.random.triangular(left=min_price, mode=mean_price, right=max_price, size=(len(price)))

plt.figure(figsize=(8,5))
plt.hist(triangular_price, bins=20, color="royalblue", edgecolor="black")
plt.title("Triangular Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Triangular_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Lognormal Distribution

log_price = np.log(price)
log_mean = log_price.mean()
log_std = log_price.std()

lognormal_price = np.random.lognormal(mean=log_mean, sigma=log_std, size=len(price))

plt.figure(figsize=(8,5))
plt.hist(lognormal_price, bins=20, color="lightgreen", edgecolor="black")
plt.title("Lognormal Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Lognormal_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Gamma Distribution

shape = 2.0
scale = mean_price / shape

gamma_price = np.random.gamma(shape=shape, scale=scale, size=len(price))

plt.figure(figsize=(8,5))
plt.hist(gamma_price, bins=20, color="blue", edgecolor="black")
plt.title("Gamma Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Gamma_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Beta Distribution

price_scaled = (price - min_price) / (max_price - min_price)

beta_price = np.random.beta(a=5.0, b=2.0, size=(len(price_scaled)))

plt.figure(figsize=(8,5))
plt.hist(beta_price, bins=20, color="yellow", edgecolor="black")
plt.title("Beta Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Beta_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Weibull Distribution

weibull_price = np.random.weibull(a=1.5, size=(len(price))) * mean_price

plt.figure(figsize=(8,5))
plt.hist(weibull_price, bins=20, color="yellowgreen", edgecolor="black")
plt.title("Weibull Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Weibull_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# Uniform Distribution

uniform_price = np.random.uniform(low=min_price, high=max_price, size=(len(price)))

plt.figure(figsize=(8,5))
plt.hist(uniform_price, bins=20, color="gold", edgecolor="black")
plt.title("Uniform Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("Pics/Uniform_histogram.png", dpi=200, bbox_inches="tight")
plt.close()