path = "C:/Users/cmpyl/Documents/M1 2025-2026/Webscraping/data/"

library(dplyr)
library(ggplot2)

#Read fuzzy-merged cleaned data
data <- read.csv(paste0(path, "Analysis-Data.csv"))

#Box plot relative price by category
ggplot(data, aes(x = Walkenhorst_Category,
                 y = Markup)) +
  geom_boxplot(outlier.shape = NA) +
  labs(
    x = "Walkenhorst Category",
    y = "Percent Difference in Unit Prices",
    title = "Distribution of Price Differences by Category"
  ) +
  coord_cartesian(ylim = c(-100, 400)) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave(paste0(path,"box_chart.png"))