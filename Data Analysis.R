getwd()
setwd("D:/YEAR 3/Semester 1/FIT3163")

calender = read.csv("calendar.csv", stringsAsFactors = T)
validation = read.csv("sales_train_validation.csv", stringsAsFactors = T)
evaluation = read.csv("sales_train_evaluation.csv", stringsAsFactors = T)
price = read.csv("sell_prices.csv", stringsAsFactors = T)

unique(evaluation$cat_id)
#HOBBIES, HOUSEHOLD,FOODS

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


#APPENDIX
TARGET = 'sales'         # Our main target
END_TRAIN = 1941         # Last day in train set
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


hobbies_list = unique(hobbies_price$item_id)
for (i in hobbies_list) {
  cat("Mean", i , "=", mean(hobbies_price[hobbies_price$item_id == i,]$sell_price),"\n")
}

# Set the seed for reproducibility
set.seed(3163)
# Specify the number of rows to sample
n = 1000

#HOBBIES SAMPLING
sampled_hobbies = hobbies[sample(nrow(hobbies), n), ]
sampled_hobbies_price = hobbies_price[sample(nrow(hobbies_price), n), ]

#HOUSEHOLD SAMPLING
sampled_household = household[sample(nrow(household), n), ]
sampled_household_price = household_price[sample(nrow(household_price), n), ]

#FOODS SAMPLING
sampled_foods = foods[sample(nrow(foods), n), ]
sampled_foods_price = foods_price[sample(nrow(foods_price), n), ]

#CALENDER SAMPLING
sampled_calender = calender[sample(nrow(calender), n), ]

#MERGE
hobbies_merge = merge(sampled_hobbies,sampled_hobbies_price, by="item_id")
household_merge = merge(sampled_household,sampled_household_price, by="item_id")
foods_merge = merge(sampled_foods,sampled_foods_price,by="item_id")

hobbies_merge = merge(hobbies_merge,calender, by="wm_yr_wk")
household_merge = merge(household_merge,calender, by="wm_yr_wk")
foods_merge = merge(foods_merge,calender, by="wm_yr_wk")

x = seq(min(hobbies_merge$sell_price),max(hobbies_merge$sell_price), 0,1)
y = hobbies_merge$sum_unit_sold
plot(hobbies_merge$sell_price,hobbies_merge$sum_unit_sold, main="Hobbies Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")
plot(household_merge$sell_price,household_merge$sum_unit_sold, main="Household Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")
plot(foods_merge$sell_price,foods_merge$sum_unit_sold, main="Foods Correlation Between Sell Price and Unit Sold", xlab="Sell Price",ylab = "Sum Unit Sold")

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

