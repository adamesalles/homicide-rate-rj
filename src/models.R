# This script contains the models used in the paper
# Author: Eduardo Adame

library(cmdstanr)
library(rstanarm)
library(bayesplot)
library(parallel)
library(modelsummary)
library(loo)

options(mc.cores = parallel::detectCores())


dataset <- read.csv("data/dataset.csv")
columns <- -(c(3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14) + 3)

# Final dataset
df <- dataset[, columns]

M1 <- stan_glm(
  homicideRate ~ .,
  data = df[, -c(2, 3)],
  family = gaussian(link = "log"),
  prior = normal(0, 1),
  prior_intercept = normal(0, 1),
  chains = 8,
  iter = 8000,
  cores = 4
)

M2 <- stan_glmer(
  homicideRate ~ (1|year) + . - year,
  data = df[, -c(2)],
  family = gaussian(link = "log"),
  prior = normal(0, 1),
  prior_intercept = normal(0, 1),
  chains = 8,
  iter = 8000,
  cores = 4
)

M3 <- stan_glmer(
  homicideRate ~ (1|administrativeRegion) + . - administrativeRegion,
  data = df[, -c(3)],
  family = gaussian(link = "log"),
  prior = normal(0, 1),
  prior_intercept = normal(0, 1),
  chains = 10,
  iter = 12000,
  cores = 4
)

models <- list(M1, M2, M3)

summary(M1)
summary(M2)
summary(M3)

# Save M3 varying intercepts 
write.csv(as.data.frame(summary(M3)), "data/M3.csv")

plot(M3, pars = c("b"))
ggsave("docs/imgs/M3.png", width = 16, height = 10)

# RMSE
sqrt(mean((M1$fitted.values - df$homicideRate)^2))
sqrt(mean((M2$fitted.values - df$homicideRate)^2))
sqrt(mean((M3$fitted.values - df$homicideRate)^2))

# Residuals
r1 <- M1$fitted.values - df$homicideRate
r2 <- M2$fitted.values - df$homicideRate
r3 <- M3$fitted.values - df$homicideRate

# Create dataframe with region/year and residuals

residuals <- data.frame(
  administrativeRegion = df$administrativeRegion,
  year = df$year,
  r1 = r1,
  r2 = r2,
  r3 = r3
)

# Save residuals
write.csv(residuals, "data/residuals.csv")

# WAIC
waic(M1)
waic(M2)
waic(M3)