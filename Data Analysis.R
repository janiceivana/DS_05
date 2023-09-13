getwd()
setwd("D:/YEAR 3/Semester 1/FIT3163")

calender = read.csv("calendar.csv")
validation = read.csv("sales_train_validation.csv")
evaluation = read.csv("sales_train_evaluation.csv")
price = read.csv("sell_prices.csv")

unique(evaluation$cat_id)
#HOBBIES, HOUSEHOLD,FOODS

#SUBSETTING EVALUATION DATA BASED ON CATEGORY
library(dplyr)
hobbies = evaluation %>% filter(cat_id == "HOBBIES")
household = evaluation %>% filter(cat_id == "HOUSEHOLD")
foods = evaluation %>% filter(cat_id == "FOODS")

#SUBSETTING CATEGORY PRICE
hobbies_price = price[grep("HOBBIES", apply(price, 1, paste, collapse = ",")), ]
household_price = price[grep("HOUSEHOLD", apply(price, 1, paste, collapse = ",")), ]
foods_price = price[grep("FOODS", apply(price, 1, paste, collapse = ",")), ]

#HYPOTHESIS TESTING
t.test(hobbies_price$sell_price,household_price$sell_price)
t.test(hobbies_price$sell_price,foods_price$sell_price)
t.test(household_price$sell_price,foods_price$sell_price)

#CONFIDENCE INTERVAL
t.test(hobbies_price$sell_price, conf.level = 0.95)
t.test(household_price$sell_price, conf.level = 0.95)
t.test(foods_price$sell_price, conf.level = 0.95)

#MERGE
hobbies_merge = merge(hobbies,hobbies_price)

#APPENDIX
hobbies_list = unique(hobbies_price$item_id)
for (i in hobbies_list) {
  cat("Mean", i , "=", mean(hobbies_price[hobbies_price$item_id == i,]$sell_price),"\n")
}
