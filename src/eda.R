# This script contains the exploratory data analysis of the dataset
# Author: Eduardo Adame

library(ggpubr)
library(ggplot2)
library(GGally)
library(sf)

dataset <- read.csv("data/dataset.csv")

target <- dataset$homicideRate
X <- as.matrix(dataset[, 4:ncol(dataset)])
X.df <- data.frame(X)

# Checking correlated groups of variables
ggcorr(X[, c(2, 4, 5, 9, 11, 12, 13)], label = TRUE, label_size = 3, label_round = 3, hjust = .95, size = 4)

# Plot the correlation between some covariates
ggpairs(X.df[, c(2, 4, 5, 9, 11, 12, 13)], upper = list(continuous = wrap("cor", size = 8))) +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
    labs(title = "Correlation between some covariates")

# Save the plot
ggsave("docs/imgs/corr.png", width = 16, height = 10)

# Select the columns to be removed
columns <- -(c(3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14) + 3)
df <- dataset[, columns]


# Plot the correlation between the covariates after the procedure
ggpairs(X.df[, -c(3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14)], upper = list(continuous = wrap("cor", size = 5))) +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, size = 4)) +
    labs(title = "Correlation between covariates after procedure")

# Save the plot
ggsave("docs/imgs/scatter.png", width = 16, height = 10)



#  Correlation between the target variable and the predictors
primary_var <- "homicideRate"
pairs <- ggpairs(df[, -c(2, 3)])
pvar_pos <- match(primary_var, pairs$yAxisLabels)
plots <- lapply(1:pairs$nrow, function(j) getPlot(pairs, i = j, j = pvar_pos))
ggmatrix(
    plots,
    nrow = pairs$nrow,
    ncol = 1,
    yAxisLabels = pairs$yAxisLabels,
    xAxisLabels = primary_var
)

ggsave("docs/imgs/homicideRateCorr.png", width = 8, height = 12)

# Plot the distribution of the target variable and of its log
f1 <- ggdensity(target, 
          main = "Distribution of the target variable",
          xlab = "Target variable")

f2 <- ggdensity(log(target),
            main = "Distribution of the log of the target variable",
            xlab = "Log of the target variable")

ggarrange(f1, f2, nrow = 2, ncol = 1)

ggsave("docs/imgs/density.png", width = 8, height = 12)
