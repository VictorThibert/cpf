import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

N = 1000
x = np.random.rand(N)
y = np.random.rand(N)

area = 1

mu, sigma = 0, 100 # mean and standard deviation
x = np.random.normal(mu, sigma, N)
y = np.random.normal(mu,sigma)