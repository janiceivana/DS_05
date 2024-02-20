getwd()
setwd("D:/YEAR 3/Semester 1/FIT3163")

calender = read.csv("calendar.csv", stringsAsFactors = T)
validation = read.csv("sales_train_validation.csv", stringsAsFactors = T)
evaluation = read.csv("sales_train_evaluation.csv", stringsAsFactors = T)
price = read.csv("sell_prices.csv", stringsAsFactors = T)

unique(evaluation$cat_id)
#HOBBIES, HOUSEHOLD,FOODS
calender$date = as.Date(calender$date)

library(dplyr)

dim(price)
max_price = max(price$sell_price)
min_price = min(price$sell_price)
summary(price)

sort(price$sell_price)

max_index = which.max(price$sell_price)
min_index = which.min(price$sell_price)

max_store = price$store_id[max_index]
min_store = price$store_id[min_index]

max_item = price$item_id[max_index]
min_item = price$item_id[min_index]

price$wm_yr_wk[max_index]
price$wm_yr_wk[min_index]

# Accessing the result without levels
max_store_character = as.character(max_store)
# Accessing the result without levels
min_store_character = as.character(min_store)

cat("The highest price in the data is: USD", max_price, "at", max_store_character)
cat("The lowest price in the data is: USD", min_price, "at", min_store_character)


#SUBSETTING EVALUATION DATA BASED ON CATEGORY
library(dplyr)
hobbies = evaluation %>% filter(cat_id == "HOBBIES")
household = evaluation %>% filter(cat_id == "HOUSEHOLD")
foods = evaluation %>% filter(cat_id == "FOODS")

#CREATE NEW COLUMN FOR THE SUM OF UNIT SOLD 
hobbies$sum_unit_sold <- rowSums(hobbies[, 7:1947])
household$sum_unit_sold <- rowSums(household[, 7:1947])
foods$sum_unit_sold <- rowSums(foods[, 7:1947])

#SUBSETTING CATEGORY PRICE
hobbies_price = price[grep("HOBBIES", apply(price, 1, paste, collapse = ",")), ]
household_price = price[grep("HOUSEHOLD", apply(price, 1, paste, collapse = ",")), ]
foods_price = price[grep("FOODS", apply(price, 1, paste, collapse = ",")), ]

dim(hobbies)
dim(household)
dim(foods)

dim(hobbies_price)
dim(household_price)
dim(foods_price)

#CLEANING
hobbies_clean = hobbies %>% distinct()
hobbies_clean = na.omit(hobbies_clean)
household_clean = household %>% distinct()
household_clean = na.omit(household_clean)
foods_clean = foods %>% distinct()
foods_clean = na.omit(foods_clean)

hobbies_price_clean = hobbies_price %>% distinct()
hobbies_price_clean = na.omit(hobbies_price_clean)
household_price_clean = household_price %>% distinct()
household_price_clean = na.omit(household_price_clean)
foods_price_clean = foods_price %>% distinct()
foods_price_clean = na.omit(foods_price_clean)

#AFTER CLEANING
dim(hobbies_clean)
dim(household_clean)
dim(foods_clean)

dim(hobbies_price_clean)
dim(household_price_clean)
dim(foods_price_clean)

#THE RESULT IS THE SAME -> MEANING THE DATA IS CLEANED

#HYPOTHESIS TESTING
t.test(hobbies_price$sell_price,household_price$sell_price)
t.test(hobbies_price$sell_price,foods_price$sell_price)
t.test(household_price$sell_price,foods_price$sell_price)

#CONFIDENCE INTERVAL
t.test(hobbies_price$sell_price, conf.level = 0.95)
t.test(household_price$sell_price, conf.level = 0.95)
t.test(foods_price$sell_price, conf.level = 0.95)

#HYPOTHESIS TESTING
t.test(hobbies$sum_unit_sold,household$sum_unit_sold)
t.test(hobbies$sum_unit_sold,foods$sum_unit_sold)
t.test(household$sum_unit_sold,foods$sum_unit_sold)

#CONFIDENCE INTERVAL
t.test(hobbies$sum_unit_sold, conf.level = 0.95)
t.test(household$sum_unit_sold, conf.level = 0.95)
t.test(foods$sum_unit_sold, conf.level = 0.95)



hobbies_list = unique(hobbies_price$item_id)
for (i in hobbies_list) {
  cat("Mean", i , "=", mean(hobbies_price[hobbies_price$item_id == i,]$sell_price),"\n")
}

# Set the seed for reproducibility
set.seed(3163)
# Specify the number of rows to sample
n = 5000

#HOBBIES SAMPLING
sampled_hobbies = hobbies[sample(nrow(hobbies), n), ]

#HOUSEHOLD SAMPLING
sampled_household = household[sample(nrow(household), n), ]

#FOODS SAMPLING
sampled_foods = foods[sample(nrow(foods), n), ]

#MERGE
hobbies_merge = merge(hobbies_price,calender, by="wm_yr_wk")
household_merge = merge(household_price,calender, by="wm_yr_wk")
foods_merge = merge(foods_price,calender, by="wm_yr_wk")

m = 5000
#HOBBIES MERGE SAMPLING
hobbies_merge_sampling = hobbies_merge[sample(nrow(hobbies_merge), m), ]

#HOUSEHOLD MERGE SAMPLING
household_merge_sampling = household_merge[sample(nrow(household_merge), m), ]

#FOODS MERGE SAMPLING
foods_merge_sampling = foods_merge[sample(nrow(foods_merge), m), ]


hobbies_merge = merge(sampled_hobbies,hobbies_merge_sampling, by="item_id")
household_merge = merge(sampled_household,household_merge_sampling, by="item_id")
foods_merge = merge(sampled_foods,foods_merge_sampling,by="item_id")

x = seq(min(hobbies_merge$sell_price),max(hobbies_merge$sell_price),1)
y = hobbies_merge$sum_unit_sold
plot(hobbies_merge$sell_price,hobbies_merge$sum_unit_sold, main="Hobbies Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")
plot(household_merge$sell_price,household_merge$sum_unit_sold, main="Household Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")
plot(foods_merge$sell_price,foods_merge$sum_unit_sold, main="Foods Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")

hobbies_merge$sum_unit_sold.y[1]
library(ggplot2)
#Hobbies for each state
ggplot(hobbies_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(state_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each State")

#Household for each state
ggplot(household_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(state_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each State")

#Foods for each state
ggplot(foods_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(state_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each State")


#Hobbies for each state
ggplot(hobbies_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(dept_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each Department")

#Household for each state
ggplot(household_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(dept_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each Department")

#Foods for each state
ggplot(foods_merge, aes(x = sell_price, y = sum_unit_sold, color = as.factor(dept_id))) +
  geom_point() + ggtitle("Relationship between Sell Price and Sales Volume for each Department")

################################################################################

#DATA VIZ AND ANALYSIS

hobbies_total_sales = hobbies_merge$sum_unit_sold * hobbies_merge$sell_price
hobbies_merge$sales = hobbies_total_sales

household_total_sales = household_merge$sum_unit_sold * household_merge$sell_price
household_merge$sales = household_total_sales

foods_total_sales = foods_merge$sum_unit_sold * foods_merge$sell_price
foods_merge$sales = foods_total_sales

hobbies_viz = cbind(as.character(hobbies_merge$state_id),as.character(hobbies_merge$dept_id),as.character(hobbies_merge$cat_id), hobbies_merge$sell_price, hobbies_merge$sales, hobbies_merge$sum_unit_sold, hobbies_merge$date)

household_viz = cbind(as.character(household_merge$state_id),as.character(household_merge$dept_id),as.character(household_merge$cat_id), household_merge$sell_price, household_merge$sales, household_merge$sum_unit_sold)

foods_viz = cbind(as.character(foods_merge$state_id),as.character(foods_merge$dept_id),as.character(foods_merge$cat_id), foods_merge$sell_price, foods_merge$sales, foods_merge$sum_unit_sold)


my_data = rbind(hobbies_viz,household_viz,foods_viz)
colnames(my_data) =  c("state_id","dept_id","cat_id","sell_price", "revenue", "sales_volume")

my_data = as.data.frame(my_data)
my_data = unique(my_data) 
View(my_data)

#PLOTTING PRICES AND SALES FOR EACH CATEGORY

# Convert cat_id to factor
my_data$cat_id = factor(my_data$cat_id)

# Example using pch for different categories
plot(my_data$sell_price, my_data$revenue, pch = 1:length(levels(my_data$cat_id)),
     main = "Relationship between Prices and Sales (Revenue)",
     xlab = "Price", ylab = "Revenue", col = 1:length(levels(my_data$cat_id)))

# Add legend
legend("topright", legend = levels(my_data$cat_id),
       col = 1:length(levels(my_data$cat_id)), pch = 1:length(levels(my_data$cat_id)))


#PLOTTING PRICES AND SALES FOR EACH DEPARMENT

# Convert cat_id to factor
my_data$dept_id = factor(my_data$dept_id)

# Example using pch for different categories
plot(my_data$sell_price, my_data$revenue, pch = 1:length(levels(my_data$dept_id)),
     main = "Relationship between Prices and Sales (Revenue)",
     xlab = "Price", ylab = "Revenue", col = 1:length(levels(my_data$dept_id)))

# Add legend
legend("topright", legend = levels(my_data$dept_id),
       col = 1:length(levels(my_data$dept_id)), pch = 1:length(levels(my_data$dept_id)))


#PLOTTING PRICES AND SALES FOR EACH STATE

# Convert column to suitable datatype
my_data$state_id = factor(my_data$state_id)
my_data$sell_price = as.numeric(my_data$sell_price)
my_data$revenue = as.numeric(my_data$revenue)
my_data$sales_volume = as.numeric(my_data$sales_volume)


# Example using pch for different categories
plot(my_data$sell_price, my_data$revenue, pch = 1:length(levels(my_data$state_id)),
     main = "Relationship between Prices and Sales (Revenue)",
     xlab = "Price", ylab = "Revenue", col = 1:length(levels(my_data$state_id)))

# Add legend
legend("topright", legend = levels(my_data$state_id),
       col = 1:length(levels(my_data$state_id)), pch = 1:length(levels(my_data$state_id)))


summary(my_data)
#histogram -> show number of distribution for each category, department, and state (for each sales volume, revenue, and price)
hist(my_data$sell_price, ylim = c(0,800), xlab = "Price", main = "Price Distribution")

library(tidyverse)

# Histogram for sales volume
ggplot(my_data, aes(x = sales_volume)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Sales Volume by Category") +
  facet_wrap(~ cat_id)

ggplot(my_data, aes(x = sales_volume)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Sales Volume by Department") +
  facet_wrap(~ dept_id)

ggplot(my_data, aes(x = sales_volume)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Sales Volume by State") +
  facet_wrap(~ state_id)

# Histogram for revenue
ggplot(my_data, aes(x = revenue)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Revenue by Category") +
  facet_wrap(~ cat_id)

ggplot(my_data, aes(x = revenue)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Revenue by Deparment") +
  facet_wrap(~ dept_id)


ggplot(my_data, aes(x = revenue)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Revenue by State") +
  facet_wrap(~ state_id)


# Histogram for price
ggplot(my_data, aes(x = sell_price)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Price by Category") +
  facet_wrap(~ cat_id)

ggplot(my_data, aes(x = sell_price)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Price by Department") +
  facet_wrap(~ dept_id)

ggplot(my_data, aes(x = sell_price)) +
  geom_histogram(bins = 20) +
  labs(title = "Distribution of Price by State") +
  facet_wrap(~ state_id)

#find out on which occasion, and which day that have the highest number of sales and sales volume -> bar chart

#HOBBIES
# Find occasion with highest sales volume
max_occasion <- hobbies_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sum_unit_sold, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(hobbies_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sum_unit_sold)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasions with Highest Sales Volume",
       x = "Occasion",
       y = "Total Sales Volume") +
  geom_vline(xintercept = max_occasion, linetype = "dashed", color = "red")

# Find occasion with highest price
max_occasion_price <- hobbies_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sell_price, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(hobbies_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sell_price)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasion with Highest Price",
       x = "Occasion",
       y = "Price") +
  geom_vline(xintercept = max_occasion_price, linetype = "dashed", color = "red") 

# Find occasion with highest revenue
max_occasion_revenue <- hobbies_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sales, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(hobbies_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sales)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasion with Highest Revenue",
       x = "Occasion",
       y = "Total Revenue") +
  geom_vline(xintercept = max_occasion_revenue, linetype = "dashed", color = "red") 


#####################################################################

#HOUSEHOLD
# Find occasion with highest sales volume
max_occasion <- household_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sum_unit_sold, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(household_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sum_unit_sold)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasions with Highest Sales Volume (Hobbies)",
       x = "Occasion",
       y = "Total Sales Volume") +
  geom_vline(xintercept = max_occasion, linetype = "dashed", color = "red")

# Find occasion with highest price
max_occasion_price <- household_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sell_price, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(household_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sell_price)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasion with Highest Price (Hobbies)",
       x = "Occasion",
       y = "Price") +
  geom_vline(xintercept = max_occasion_price, linetype = "dashed", color = "red") 

# Find occasion with highest revenue
max_occasion_revenue <- household_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sales, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(household_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sales)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasion with Highest Revenue (Hobbies)",
       x = "Occasion",
       y = "Total Revenue") +
  geom_vline(xintercept = max_occasion_revenue, linetype = "dashed", color = "red") 




#####################################################################

#FOODS
# Find occasion with highest sales volume
max_occasion <- foods_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sum_unit_sold, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(foods_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sum_unit_sold)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasions with Highest Sales Volume (Hobbies)",
       x = "Occasion",
       y = "Total Sales Volume") +
  geom_vline(xintercept = max_occasion, linetype = "dashed", color = "red")

# Find occasion with highest price
max_occasion_price <- foods_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sell_price, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(foods_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sell_price)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasions with Highest Price (Hobbies)",
       x = "Occasion",
       y = "Price") +
  geom_vline(xintercept = max_occasion_price, linetype = "dashed", color = "red") 

# Find occasion with highest revenue
max_occasion_revenue <- foods_merge %>%
  filter(str_trim(event_type_1) != "") %>%
  group_by(event_type_1) %>%
  summarise(total_sales = sum(sales, na.rm = TRUE)) %>%
  top_n(1, total_sales) %>%
  pull(event_type_1)

# Bar chart
ggplot(foods_merge %>% filter(event_type_1 != ""), aes(x = event_type_1, y = sales)) +
  geom_bar(stat = "identity") +
  labs(title = "Occasion with Highest Revenue (Hobbies)",
       x = "Occasion",
       y = "Total Revenue") +
  geom_vline(xintercept = max_occasion_revenue, linetype = "dashed", color = "red") 


#By event name 
#By which day - debug tgt

#for each category see the price fluctuation throughout each occasion or year (price) -> line chart
  
#HOBBIES
# Calculate average sell price for hobbies and year
average_prices <- hobbies_merge %>%
  group_by(year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE))

# Plot average sell price per year for hobbies
ggplot(average_prices, aes(x = year, y = avg_sell_price)) +
  geom_line() +
  labs(title = "Average Price Fluctuation (Hobbies)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for hobbies and year by state
average_prices <- hobbies_merge %>%
  group_by(state_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for hobbies
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = state_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by State (Hobbies)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for hobbies and year by department
average_prices <- hobbies_merge %>%
  group_by(dept_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for hobbies
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = dept_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Deparment (Hobbies)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Calculate average sell price for hobbies and year by event type
average_prices <- hobbies_merge %>%
  group_by(event_type_1, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for hobbies
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = event_type_1)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Event Type (Hobbies)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

######################################################################  
#HOUSEHOLD

# Calculate average sell price for household and year
average_prices <- household_merge %>%
  group_by(year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE))

# Plot average sell price per year for household
ggplot(average_prices, aes(x = year, y = avg_sell_price)) +
  geom_line() +
  labs(title = "Average Price Fluctuation (Household)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for household and year by state
average_prices <- household_merge %>%
  group_by(state_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for household
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = state_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by State (Household)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for household and year by department
average_prices <- household_merge %>%
  group_by(dept_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for household
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = dept_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Deparment (Household)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for household and year by event type
average_prices <- household_merge %>%
  group_by(event_type_1, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for household
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = event_type_1)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Event Type (Household)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#####################################################################
#FOODS

# Calculate average sell price for foods and year
average_prices <- foods_merge %>%
  group_by(year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE))

# Plot average sell price per year for foods
ggplot(average_prices, aes(x = year, y = avg_sell_price)) +
  geom_line() +
  labs(title = "Average Price Fluctuation (Foods)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for foods and year by state
average_prices <- foods_merge %>%
  group_by(state_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for foods
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = state_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by State (Foods)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Calculate average sell price for foods and year by department
average_prices <- foods_merge %>%
  group_by(dept_id, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for foods
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = dept_id)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Deparment (Foods)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Calculate average sell price for foods and year by event type
average_prices <- foods_merge %>%
  group_by(event_type_1, year) %>%
  summarise(avg_sell_price = mean(sell_price, na.rm = TRUE), .groups = "drop")

# Plot average sell price per year for foods
ggplot(average_prices, aes(x = year, y = avg_sell_price, color = event_type_1)) +
  geom_line() +
  labs(title = "Average Price Fluctuation by Event Type (Foods)",
       x = "Year",
       y = "Average Sell Price") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#– How does price affect sales volumes and revenue?
library(ggplot2)

# Calculate average price
average_price <- my_data %>%
  group_by(dept_id) %>%
  summarise(avg_price = mean(sell_price, na.rm = TRUE))

# Merge average price with the original data frame
my_data <- merge(my_data, average_price, by = "dept_id")

# Scatter plot for average price vs. sales volume
ggplot(my_data, aes(x = avg_price, y = sales_volume, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs. Sales Volume",
       x = "Average Price",
       y = "Sales Volume")

# Scatter plot for average price vs. revenue
ggplot(my_data, aes(x = avg_price, y = revenue, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs. Revenue",
       x = "Average Price",
       y = "Revenue")


library(dplyr)
library(ggplot2)

# Calculate total sales volume and total revenue for each product_id
summary_data <- my_data %>%
  group_by(dept_id) %>%
  summarise(total_sales_volume = sum(sales_volume, na.rm = TRUE),
            total_revenue = sum(revenue, na.rm = TRUE),
            avg_price = mean(sell_price, na.rm = TRUE)) %>%
  ungroup()

# Scatter plot for average price vs total sales volume
ggplot(summary_data, aes(x = avg_price, y = total_sales_volume, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs Total Sales Volume",
       x = "Average Price",
       y = "Total Sales Volume") +
  geom_text(aes(label = dept_id), vjust = -0.5, hjust = 0.5, size =2.5) 

# Scatter plot for average price vs total revenue
ggplot(summary_data, aes(x = avg_price, y = total_revenue, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs Total Revenue",
       x = "Average Price",
       y = "Total Revenue")  +
  geom_text(aes(label = dept_id), vjust = -0.5, hjust = 0.5, size =2.5) 



# Calculate average sales volume and average revenue for each product_id
summary_data <- my_data %>%
  group_by(dept_id) %>%
  summarise(avg_sales_volume = mean(sales_volume, na.rm = TRUE),
            avg_revenue = mean(revenue, na.rm = TRUE),
            avg_price = mean(sell_price, na.rm = TRUE)) %>%
  ungroup()

# Scatter plot for average price vs total sales volume
ggplot(summary_data, aes(x = avg_price, y = avg_sales_volume, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs Total Sales Volume",
       x = "Average Price",
       y = "Average Sales Volume") +
  geom_text(aes(label = dept_id), vjust = -0.5, hjust = 0.5, size =2.5) 

# Scatter plot for average price vs total revenue
ggplot(summary_data, aes(x = avg_price, y = avg_revenue, color = dept_id)) +
  geom_point() +
  labs(title = "Average Price vs Total Revenue",
       x = "Average Price",
       y = "Average Revenue")  +
  geom_text(aes(label = dept_id), vjust = -0.5, hjust = 0.5, size =2.5) 

################################################################################

#Price Elasticity Modelling

# Calculate the percentage change in price and quantity demanded
df <- my_data %>%
  group_by(cat_id) %>%
  arrange(cat_id, date) %>%
  mutate(price_change = sell_price / lag(sell_price) - 1,
         quantity_change = sales_volume / lag(sales_volume) - 1)

# Calculate the price elasticity of demand
df <- df %>%
  mutate(price_elasticity = quantity_change / price_change)

# Plot price elasticity of demand for each product
ggplot(df, aes(x = product_id, y = price_elasticity)) +
  geom_bar(stat = "identity") +
  labs(title = "Price Elasticity of Demand for Different Products",
       x = "Product ID",
       y = "Price Elasticity")



################################################################################

#APPENDIX
TARGET = 'sales'         # Our main target

monday_sales = hobbies_merge[hobbies_merge$weekday == "Monday", "sales"]
sum(monday_sales)END_TRAIN = 1941         # Last day in train set
MAIN_INDEX = c('id','d')  # We can identify item by these columns

# Loading required library
library(tidyr)

# Define index columns in R
index_columns = c('id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id')

# Perform the equivalent melt operation in R using gather() from tidyr
evaluation_df = evaluation %>% gather(key = 'd', value = TARGET, -one_of(index_columns))


print(evaluation_df)

# Print the lengths of evaluation and evaluation_df
cat("Train rows:", length(evaluation), length(evaluation_df), "\n")

# To be able to make predictions, we need to add "test set" to our grid

# Create an empty dataframe to store the additional grid
add_grid = data.frame()

for (i in 1:28) {
  temp_df = evaluation[index_columns, drop = FALSE]  # Subset train_df with index_columns
  temp_df = unique(temp_df)  # Remove duplicates
  temp_df$d = paste0('d_', END_TRAIN + i)  # Add 'd_' and the incremented value to 'd' column
  temp_df[[TARGET]] <- NA  # Set TARGET column to NA
  add_grid = rbind(add_grid, temp_df)  # Concatenate temp_df to add_grid
}

# Concatenate grid_df and add_grid
evaluation_df = rbind(evaluation_df, add_grid)

# Reset the index of grid_df
evaluation_df = evaluation_df[order(row.names(evaluation_df)), ]  # Order by row names to reset index
rownames(evaluation_df) = NULL  # Reset row names
colnames(evaluation_df)[colnames(evaluation_df) == TARGET] = "TARGET"  # Rename TARGET column

# Remove temporary dataframes
rm(temp_df, add_grid)

# Remove the original train_df
rm(evaluation)

# Convert index columns to factors to save memory
for (col in index_columns) {
  evaluation_df[[col]] <- as.factor(evaluation_df[[col]])
}

# Print memory usage before and after reducing memory usage
print(sprintf("%20s: %8s", 'Original grid_df', format(object.size(grid_df), units = "auto")))
print(sprintf("%20s: %8s", 'Reduced grid_df', format(object.size(grid_df), units = "auto")))

#LINEAR REGRESSION - HOBBIES
hobbies_merge_fit_data = hobbies_merge[,7:1951]
fit.hobbies = lm(sell_price ~ ., data = hobbies_merge_fit_data)
summary(fit.hobbies)
sort(summary(fit.hobbies)$coefficients[, "Pr(>|t|)"])

fit.hobbies = lm(sell_price ~ sum_unit_sold, data = hobbies_merge_fit_data)
summary(fit.hobbies)

#LINEAR REGRESSION - HOUSEHOLD
household_merge_fit_data = household_merge[,7:1951]
fit.household = lm(sell_price ~ ., data = household_merge_fit_data)
summary(fit.household)
sort(summary(fit.household)$coefficients[, "Pr(>|t|)"])

fit.household = lm(sell_price ~ sum_unit_sold, data = household_merge_fit_data)
summary(fit.household)

#LINEAR REGRESSION - FOODS
foods_merge_fit_data = foods_merge[,7:1951]
fit.foods = lm(sell_price ~ ., data = foods_merge_fit_data)
summary(fit.foods)
sort(summary(fit.foods)$coefficients[, "Pr(>|t|)"])

fit.foods = lm(sell_price ~ sum_unit_sold, data = foods_merge_fit_data)
summary(fit.foods)


