path = "C:/Users/cmpyl/Documents/M1 2025-2026/Webscraping/data/"

library(dplyr)
library(ggplot2)

#Read fuzzy-merged raw data
data <- read.csv(paste0(path, "Merged_Walkenhorst_Walmart.csv"))

#Drop NA weights
data <- data %>%
  filter(data$Walkenhorst_weight != "NA  oz.")

#Clean strings, make walkenhorst price/weight and relative price difference
data$Walkenhorst_price <- as.numeric(sub("^\\$", "", data$Walkenhorst_price))
data$Walkenhorst_weight <- as.numeric(sub(" oz\\.$", "", data$Walkenhorst_weight))
data <- data %>%
  mutate(Walkenhorst_unit_price = Walkenhorst_price/Walkenhorst_weight) %>%
  mutate(relative_price = as.numeric((Walkenhorst_unit_price - Walmart_clean_unit_price)/Walmart_clean_unit_price)) %>%
  filter(!is.na(relative_price))

#Equalize relative price above 25 for better visualization
data$relative_price[data$relative_price > 10] = 10

#Visualize price difference by number of observations
ggplot(data, aes(x = relative_price, fill = Walkenhorst_Category)) +
  geom_histogram(bins = 100) +
  scale_x_continuous(
    breaks = seq(-1, max(data$relative_price, na.rm = TRUE), by = 1),
    labels = function(relative_price) ifelse(relative_price == 10, "10+", relative_price))+
  scale_fill_manual(values = c(
    "SNACKS"                        = "#1f77b4",
    "CONDIMENTS, SAUCES & SPREADS"  = "#ff7f0e",
    "NUTS"                          = "#2ca02c",
    "ASIAN FOOD"                    = "#d62728",
    "MEALS & SIDES"                 = "#9467bd",
    "CHEESE"                        = "#8c564b",
    "SPICES & SEASONINGS"           = "#e377c2",
    "CANDY"                         = "#7f7f7f",
    "SEAFOOD"                       = "#bcbd22",
    "COOKIES"                       = "#17becf",
    "CRACKERS"                      = "#aec7e8",
    "DIET, NUTRITION & SUPPLEMENTS" = "#ffbb78",
    "GRANOLA BARS & BREAKFAST BARS" = "#98df8a",
    "PASTRIES"                      = "#ff9896",
    "TACO SHELLS & TORTILLAS"       = "#c5b0d5",
    "TEA"                           = "#c49c94",
    "CEREAL & OATMEAL"              = "#f7b6d2",
    "COFFEE"                        = "#c7c7c7",
    "BREAD"                         = "#dbdb8d",
    "DRINKS & BEVERAGES"            = "#9edae5",
    "FRUITS & VEGETABLES"           = "#393b79",
    "DRINK MIXES"                   = "#637939",
    "MEATS"                         = "#8c6d31",
    "CREAMERS"                      = "#843c39",
    "OLIVES, PICKLES & PEPPERS"     = "#7b4173",
    "SWEETENERS"                    = "#5254a3"
  ))+
  labs(
    title = "Histogram of Relative Price Difference Between Walkenhorst and Walmart Items",
    y = "Number of Observations",
    x = "Relative Price Difference",
    fill = "Catalogue Category"
  ) + theme_bw() +
  theme(legend.text = element_text(size = 4))

ggsave(paste0(path,"test.png"))

#Scatterplot walmart price by walkenhorst price, color scale by match score
ggplot(data, aes(x = Walkenhorst_unit_price,
               y = Walmart_clean_unit_price,
               fill = match_score)) +
  geom_point(shape = 21, color = "black", size = 1, alpha = 0.7, position = position_dodge2()) +
  scale_fill_viridis_c(option = "plasma") +
  labs(
    x = "Walkenhorst Unit Price",
    y = "Walmart Unit Price",
    fill = "Match Score",
    title = "Price Alignment: Walkenhorst vs Walmart"
  ) +
  theme_minimal()

#Box plot relative price by category
ggplot(data, aes(x = Walkenhorst_Category,
               y = relative_price)) +
  geom_boxplot(outlier.alpha = 0) +
  labs(
    x = "Walkenhorst Category",
    y = "Relative Difference in Unit Prices",
    title = "Distribution of Price Differences by Category"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave(paste0(path,"box_chart.png"))

#Scatterplot relative price by match score 
ggplot(data, aes(x = match_score, y = relative_price)) +
  geom_point(alpha = 0.7) +
  labs(
    x = "Match Score",
    y = "Relative Difference in Unit Prices",
    title = "Match Score vs Relative Price Difference"
  ) +
  theme_minimal()
