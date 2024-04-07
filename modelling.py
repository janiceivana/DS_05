import pandas as pd  
import matplotlib.pylab as plt   
import numpy as np  
from scipy.stats import linregress  
import scipy.stats as stats  
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import confusion_matrix  
from matplotlib.colors import ListedColormap  
from sklearn.ensemble import RandomForestClassifier  
from sklearn.cluster import KMeans  
from sklearn.preprocessing import StandardScaler  
from sklearn.model_selection import train_test_split  


# %%
# Read CSV files from Wendy directories
calendar = pd.read_csv("calendar.csv")
evaluation = pd.read_csv("sales_train_evaluation.csv")
validation = pd.read_csv("sales_train_validation.csv")
prices = pd.read_csv("sell_prices.csv")
sample = pd.read_csv("sample_submission.csv")



# %%
# Display information about the sample DataFrame
sample.info()

# %%
include = ['object', 'float', 'int']
sample.describe(include=include)

# %%
sample.describe()

# %%
sample.isnull().any()

# %%
calendar.info()

# %%
include = ['object', 'float', 'int']
calendar.describe(include=include)

# %%
calendar.describe()

# %%
calendar.isnull().any()

# %%
evaluation.info()

# %%
include = ['object', 'float', 'int']
evaluation.describe(include=include)

# %%
evaluation.isnull().any()

# %%
validation.info()

# %%
include = ['object', 'float', 'int']
validation.describe(include=include)

# %%
validation.isnull().any()

# %%
prices.info()

# %%
include = ['object', 'float', 'int']
prices.describe(include=include)

# %%
prices.isnull().any()

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time

# %%
d_cols = [col for col in evaluation.columns if col.startswith('d_')]
d_cols

# %%
fix = evaluation[d_cols].stack().reset_index(level=1)
fix.columns = ['d','unit_sale']
fix

# %%
my_data = evaluation.drop(d_cols, axis=1).join(fix)
my_data

# %%
my_data.info()

# %%
my_data['id']=my_data['id'].astype('category')
my_data['item_id']=my_data['item_id'].astype('category')
my_data['dept_id']=my_data['dept_id'].astype('category')
my_data['cat_id']=my_data['cat_id'].astype('category')
my_data['store_id']=my_data['store_id'].astype('category')
my_data['state_id']=my_data['state_id'].astype('category')
my_data['d']=my_data['d'].astype('category')

my_data['unit_sale']=pd.to_numeric(my_data['unit_sale'],downcast='unsigned')
my_data.info()

# %%

calendar['date']=calendar['date'].astype('datetime64')

calendar['weekday']=calendar['weekday'].astype('category')
calendar['d']=calendar['d'].astype('category')
calendar['event_name_1']=calendar['event_name_1'].astype('category')
calendar['event_name_2']=calendar['event_name_2'].astype('category')
calendar['event_type_1']=calendar['event_type_1'].astype('category')
calendar['event_type_2']=calendar['event_type_2'].astype('category')
calendar['snap_CA']=calendar['snap_CA'].astype('bool')
calendar['snap_TX']=calendar['snap_TX'].astype('bool')
calendar['snap_WI']=calendar['snap_WI'].astype('bool')

calendar['wm_yr_wk'] = pd.to_numeric(calendar['wm_yr_wk'], downcast='unsigned')
calendar['wday'] = pd.to_numeric(calendar['wday'], downcast='unsigned')
calendar['month'] = pd.to_numeric(calendar['month'], downcast='unsigned')
calendar['year'] = pd.to_numeric(calendar['year'], downcast='unsigned')

calendar.info()

# %%
prices['store_id'] = prices['store_id'].astype('category')
prices['item_id'] = prices['item_id'].astype('category')

prices['wm_yr_wk'] = pd.to_numeric(prices['wm_yr_wk'], downcast='unsigned')
prices['sell_price'] = pd.to_numeric(prices['sell_price'], downcast='float')

prices.info()

# %%
my_data = my_data.merge(calendar, on='d', how='left').merge(prices, on=['store_id','item_id','wm_yr_wk'], how='left')

# %%
my_data

# %%
my_data.isnull().any()

# %%
my_data['d']=my_data['d'].astype('category')

# %%
my_data.info()

# %%


# %%
category_prices = my_data.groupby("cat_id")["sell_price"].mean()

# %%
category_prices

# %%
sales_by_category= my_data.groupby("cat_id")["unit_sale"].sum()

# %%
sales_by_category

# %%
category_prices_df = pd.DataFrame({'cat_id': category_prices.index, 'mean_price': category_prices.values})
sales_by_category_df = pd.DataFrame({'cat_id': sales_by_category.index, 'sum_sale': sales_by_category.values})
category_df = pd.merge(category_prices_df, sales_by_category_df, on='cat_id')
category_df['revenue'] = category_df['mean_price']*category_df['sum_sale']
category_df

# %%
plt.figure(figsize=(10, 6))

# Plotting relationship between average prices and total sales volume for each category
plt.scatter(category_prices, sales_by_category)
plt.title('Relationship between Prices and Sales Volumes by Product Category')
plt.xlabel('Average Price')
plt.ylabel('Total Sales Volume')
plt.grid(True)

for i, txt in enumerate(category_prices.index):
    plt.annotate(txt, (category_prices[i], sales_by_category[i]), xytext=(5, -5), textcoords='offset points')

plt.show()

# %%
plt.figure(figsize=(10, 6))

# Plot a bar graph of average price and total sales for each category
plt.bar(category_prices.index, sales_by_category, color='skyblue')
plt.title('Total Sales Volumes by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales Volume')
plt.xticks(rotation=45)  
plt.grid(True)


# %%
my_data.groupby('cat_id')['item_id'].count().plot(kind='bar', figsize=(10,6))
plt.title('Total count by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Count')
plt.show()

# %%
evaluation_data=evaluation[evaluation.columns[6:]].transpose()
training_dates=pd.to_datetime(calendar['date'])[:evaluation_data.shape[0]]
evaluation_data.index=training_dates
training_dates

# %%
cat_sales=evaluation.groupby('cat_id').sum().transpose()
cat_sales.index=training_dates
cat_sales

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
cat_sales.resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Category')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%


# %%


# %%
dept_prices = my_data.groupby("dept_id")["sell_price"].mean()
dept_prices

# %%
sales_by_dept = my_data.groupby('dept_id')["unit_sale"].sum()
sales_by_dept

# %%
dept_prices_df = pd.DataFrame({'dept_id': dept_prices.index, 'mean_price': dept_prices.values})
sales_by_dept_df = pd.DataFrame({'dept_id': sales_by_dept.index, 'sum_sale': sales_by_dept.values})
dept_df = pd.merge(dept_prices_df, sales_by_dept_df, on='dept_id')
dept_df['revenue'] = dept_df['mean_price']*dept_df['sum_sale']
dept_df

# %%
plt.figure(figsize=(10, 6))

# Plotting relationship between average prices and total sales volume for each category
plt.scatter(dept_prices, sales_by_dept)
plt.title('Relationship between Prices and Sales Volumes by Product Department')
plt.xlabel('Average Price')
plt.ylabel('Total Sales Volume')
plt.grid(True)

for i, txt in enumerate(dept_prices.index):
    plt.annotate(txt, (dept_prices[i], sales_by_dept[i]), xytext=(5, -5), textcoords='offset points')

plt.show()

# %%
plt.figure(figsize=(10, 6))

# Plot a bar graph of average price and total sales for each category
plt.bar(dept_prices.index, sales_by_dept, color='skyblue')
plt.title('Total Sales Volumes by Product Department')
plt.xlabel('Product Department')
plt.ylabel('Total Sales Volume')
plt.xticks(rotation=45)  
plt.grid(True)



# %%
my_data.groupby('dept_id')['item_id'].count().plot(kind='bar', figsize=(10,6))
plt.title('Total count by Product Department')
plt.xlabel('Product Department')
plt.ylabel('Count')
plt.show()

# %%
dept_sales=evaluation.groupby('dept_id').sum().transpose()
dept_sales.index=training_dates
dept_sales

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
dept_sales.resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Deptartment')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
dept_sales[['FOODS_1','FOODS_2','FOODS_3']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each FOODS')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
dept_sales[['HOBBIES_1','HOBBIES_2']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each HOBBIES')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
dept_sales[['HOUSEHOLD_1','HOUSEHOLD_2']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each HOUSEHOLD')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%


# %%


# %%


# %%


# %%
state_prices = my_data.groupby("state_id")["sell_price"].mean()
state_prices

# %%
sales_by_state = my_data.groupby('state_id')["unit_sale"].sum()
sales_by_state

# %%
state_prices_df = pd.DataFrame({'state_id': state_prices.index, 'mean_price': state_prices.values})
sales_by_state_df = pd.DataFrame({'state_id': sales_by_state.index, 'sum_sale': sales_by_state.values})
state_df = pd.merge(state_prices_df, sales_by_state_df, on='state_id')
state_df['revenue'] = state_df['mean_price']*state_df['sum_sale']
state_df

# %%
plt.figure(figsize=(10, 6))

# Plotting relationship between average prices and total sales volume for each category
plt.scatter(state_prices, sales_by_state)
plt.title('Relationship between Prices and Sales Volumes by Product State')
plt.xlabel('Average Price')
plt.ylabel('Total Sales Volume')
plt.grid(True)

for i, txt in enumerate(state_prices.index):
    plt.annotate(txt, (state_prices[i], sales_by_state[i]), xytext=(5, -5), textcoords='offset points')

plt.show()

# %%
plt.figure(figsize=(10, 6))

# Plot a bar graph of average price and total sales for each category
plt.bar(state_prices.index, sales_by_state, color='skyblue')
plt.title('Total Sales Volumes by Product State')
plt.xlabel('Product State')
plt.ylabel('Total Sales Volume')
plt.xticks(rotation=45)  
plt.grid(True)


# %%
my_data.groupby('state_id')['item_id'].count().plot(kind='bar', figsize=(10,6))
plt.title('Total count by Product State')
plt.xlabel('Product State')
plt.ylabel('Count')
plt.show()

# %%
state_sales=evaluation.groupby('state_id').sum().transpose()
state_sales.index=training_dates
state_sales

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
state_sales.resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each State')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%


# %%


# %%


# %%
store_prices = my_data.groupby("store_id")["sell_price"].mean()
store_prices

# %%
sales_by_store = my_data.groupby('store_id')["unit_sale"].sum()
sales_by_store

# %%
store_prices_df = pd.DataFrame({'store_id': store_prices.index, 'mean_price': store_prices.values})
sales_by_store_df = pd.DataFrame({'store_id': sales_by_store.index, 'sum_sale': sales_by_store.values})
store_df = pd.merge(store_prices_df, sales_by_store_df, on='store_id')
store_df['revenue'] = store_df['mean_price']*store_df['sum_sale']
store_df

# %%
plt.figure(figsize=(10, 6))

# Plotting relationship between average prices and total sales volume for each category
plt.scatter(store_prices, sales_by_store)
plt.title('Relationship between Prices and Sales Volumes by Product Store')
plt.xlabel('Average Price')
plt.ylabel('Total Sales Volume')
plt.grid(True)

for i, txt in enumerate(store_prices.index):
    plt.annotate(txt, (store_prices[i], sales_by_store[i]), xytext=(5, -5), textcoords='offset points')

plt.show()

# %%
plt.figure(figsize=(10, 6))

# Plot a bar graph of average price and total sales for each category
plt.bar(store_prices.index, sales_by_store, color='skyblue')
plt.title('Total Sales Volumes by Product Store')
plt.xlabel('Product Store')
plt.ylabel('Total Sales Volume')
plt.xticks(rotation=45)  
plt.grid(True)

# %%
my_data.groupby('store_id')['item_id'].count().plot(kind='bar', figsize=(10,6))
plt.title('Total count by Product Store')
plt.xlabel('Product Store')
plt.ylabel('Count')
plt.show()

# %%
store_sales=evaluation.groupby('store_id').sum().transpose()
store_sales.index=training_dates
store_sales

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
store_sales.resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Store')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
store_sales[['CA_1','CA_2','CA_3','CA_4']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Store in Canada')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
store_sales[['TX_1','TX_2','TX_3']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Store in Texas')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%
start_date = datetime.datetime(2011,1,19)
end_date = datetime.datetime(2016,6,19)

plt.rcParams.update({'font.size': 12})
store_sales[['WI_1','WI_2','WI_3']].resample('M').sum().plot(figsize=(10,6))

plt.title('Sales as Months for Each Store in Texas')
plt.xlabel('Months')
plt.ylabel('Sales volumes')
for year in range(start_date.year,end_date.year):
    plt.axvline(pd.to_datetime(str(year)+'-01-01'), linestyle='--')
plt.show()

# %%


# %%


# %%


# %%
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,5))
fig.suptitle("Days with Event_1 ", fontsize=20)

calendar["event_name_1"].isnull().value_counts(normalize=True)\
                                                .plot(kind="bar", xlabel="Days without Events (%)", ax=ax1, title="Days without Events (%)")

calendar["event_type_1"].value_counts(normalize=True)\
                                                .plot(kind="bar", xlabel="Days with Events (%)", ax=ax2, title="Events Type (%)")

# %%
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(24,6))
fig.suptitle("Days with Event_2", fontsize=20)

calendar["event_name_2"].isnull().value_counts(normalize=True)\
                                                .plot(kind="bar", xlabel="Days without Events (%)", ax=ax1, title="Count of Days without Events")

calendar["event_type_2"].value_counts(normalize=True)\
                                                .plot(kind="bar", xlabel="Days with Events (%)", ax=ax2, title="Events Type")

calendar["event_name_2"].value_counts(normalize=True)\
                                                .plot(kind="bar", xlabel="Event Name", ax=ax3, title="Events Names")

# %%


# %%
hobbies_1=my_data[my_data['dept_id']=="HOBBIES_1"]
hobbies_1

# %%
#a=hobbies_1.dropna(subset=['event_name_1','event_name_2'],how='all')
#a

# %%
hobbies_1 = hobbies_1.drop(hobbies_1[hobbies_1['unit_sale'] == 0].index)
hobbies_1

# %%


# %%
h1_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in hobbies_1['item_id'].unique():
    entry_df = hobbies_1[hobbies_1['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
                

                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                hobbies_1_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                hobbies_1_df = hobbies_1_df.dropna()

                h1_df = h1_df.append(hobbies_1_df, ignore_index=True)

                h1_df['price_change'] = h1_df['price'].pct_change()*100
                h1_df['sale_change'] = h1_df['sale_perday'].pct_change()*100
                h1_df['elasticity'] = -h1_df['sale_change']/h1_df['price_change'] 
h1_df=h1_df.dropna()
h1_df

# %%
level_values = []


for elasticity in h1_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


h1_df['level'] = level_values
h1_df

# %%
Vis_h1 = pd.DataFrame()

for item_id in h1_df['item_id'].unique():
    entry_df = h1_df[h1_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_h1 = Vis_h1.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_h1['price_change'], Vis_h1['sale_change'])

plt.title('Hobbies_1 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%


# %%


# %%


# %%
hobbies_2=my_data[my_data['dept_id']=="HOBBIES_2"]
hobbies_2 = hobbies_2.drop(hobbies_2[hobbies_2['unit_sale'] == 0].index)

h2_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in hobbies_2['item_id'].unique():
    entry_df = hobbies_2[hobbies_2['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                hobbies_2_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                hobbies_2_df = hobbies_2_df.dropna()
                
                h2_df = h2_df.append(hobbies_2_df, ignore_index=True)

                h2_df['price_change'] = h2_df['price'].pct_change()*100
                h2_df['sale_change'] = h2_df['sale_perday'].pct_change()*100
                h2_df['elasticity'] = -h2_df['sale_change']/h2_df['price_change'] 
h2_df=h2_df.dropna()
h2_df

# %%
level_values = []


for elasticity in h2_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


h2_df['level'] = level_values
h2_df

# %%
Vis_h2 = pd.DataFrame()

for item_id in h2_df['item_id'].unique():
    entry_df = h2_df[h2_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_h2 = Vis_h2.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_h2['price_change'], Vis_h2['sale_change'])

plt.title('Hobbies_2 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%
food_1=my_data[my_data['dept_id']=="FOODS_1"]
food_1 = food_1.drop(food_1[food_1['unit_sale'] == 0].index)

f1_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in food_1['item_id'].unique():
    entry_df = food_1[food_1['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                food_1_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                food_1_df = food_1_df.dropna()
                
                f1_df = f1_df.append(food_1_df, ignore_index=True)

                f1_df['price_change'] = f1_df['price'].pct_change()*100
                f1_df['sale_change'] = f1_df['sale_perday'].pct_change()*100
                f1_df['elasticity'] = -f1_df['sale_change']/f1_df['price_change'] 
f1_df=f1_df.dropna()
f1_df

# %%
level_values = []


for elasticity in f1_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


f1_df['level'] = level_values
f1_df

# %%
Vis_f1 = pd.DataFrame()

for item_id in f1_df['item_id'].unique():
    entry_df = f1_df[f1_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_f1 = Vis_f1.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_f1['price_change'], Vis_f1['sale_change'])

plt.title('Food_1 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%
food_2=my_data[my_data['dept_id']=="FOODS_2"]
food_2 = food_2.drop(food_2[food_2['unit_sale'] == 0].index)

f2_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in food_2['item_id'].unique():
    entry_df = food_2[food_2['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                food_2_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                food_2_df = food_2_df.dropna()
                
                f2_df = f2_df.append(food_2_df, ignore_index=True)

                f2_df['price_change'] = f2_df['price'].pct_change()*100
                f2_df['sale_change'] = f2_df['sale_perday'].pct_change()*100
                f2_df['elasticity'] = -f2_df['sale_change']/f2_df['price_change'] 
f2_df=f2_df.dropna()
f2_df

# %%
level_values = []


for elasticity in f2_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


f2_df['level'] = level_values
f2_df

# %%
Vis_f2 = pd.DataFrame()

for item_id in f2_df['item_id'].unique():
    entry_df = f2_df[f2_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_f2 = Vis_f2.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_f2['price_change'], Vis_f2['sale_change'])

plt.title('Food_2 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%
food_3=my_data[my_data['dept_id']=="FOODS_3"]
food_3 = food_3.drop(food_3[food_3['unit_sale'] == 0].index)

f3_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in food_3['item_id'].unique():
    entry_df = food_3[food_3['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                food_3_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                food_3_df = food_3_df.dropna()
                
                f3_df = f3_df.append(food_3_df, ignore_index=True)

                f3_df['price_change'] = f3_df['price'].pct_change()*100
                f3_df['sale_change'] = f3_df['sale_perday'].pct_change()*100
                f3_df['elasticity'] = -f3_df['sale_change']/f3_df['price_change'] 
f3_df=f3_df.dropna()
f3_df

# %%
level_values = []


for elasticity in f3_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


f3_df['level'] = level_values
f3_df

# %%
Vis_f3 = pd.DataFrame()

for item_id in f3_df['item_id'].unique():
    entry_df = f3_df[f3_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_f3 = Vis_f3.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_f3['price_change'], Vis_f3['sale_change'])

plt.title('Food_3 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%
household_1=my_data[my_data['dept_id']=="HOUSEHOLD_1"]
household_1 = household_1.drop(household_1[household_1['unit_sale'] == 0].index)

ho1_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in household_1['item_id'].unique():
    entry_df = household_1[household_1['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                household_1_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                household_1_df = household_1_df.dropna()
                
                ho1_df = ho1_df.append(household_1_df, ignore_index=True)

                ho1_df['price_change'] = ho1_df['price'].pct_change()*100
                ho1_df['sale_change'] = ho1_df['sale_perday'].pct_change()*100
                ho1_df['elasticity'] = -ho1_df['sale_change']/ho1_df['price_change'] 
ho1_df = ho1_df.dropna()
ho1_df

# %%
level_values = []


for elasticity in ho1_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


ho1_df['level'] = level_values
ho1_df

# %%
Vis_ho1 = pd.DataFrame()

for item_id in ho1_df['item_id'].unique():
    entry_df = ho1_df[ho1_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_ho1 = Vis_ho1.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_ho1['price_change'], Vis_ho1['sale_change'])

plt.title('Household_1 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%
household_2=my_data[my_data['dept_id']=="HOUSEHOLD_2"]
household_2 = household_2.drop(household_2[household_2['unit_sale'] == 0].index)

ho2_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


for item_id in household_2['item_id'].unique():
    entry_df = household_2[household_2['item_id'] == item_id]
    for sell_price in entry_df['sell_price'].unique():
        for dept_id in entry_df['dept_id'].unique():
            for cat_id in entry_df['cat_id'].unique():
              
                item_df = entry_df[entry_df['sell_price'] == sell_price]
                sale_perday = item_df['unit_sale'].mean()


                household_2_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
                household_2_df = household_2_df.dropna()

                ho2_df = ho2_df.append(household_2_df, ignore_index=True)

                ho2_df['price_change'] = ho2_df['price'].pct_change()*100
                ho2_df['sale_change'] = ho2_df['sale_perday'].pct_change()*100
                ho2_df['elasticity'] = -ho2_df['sale_change']/ho2_df['price_change'] 
ho2_df=ho2_df.dropna()
ho2_df

# %%
level_values = []


for elasticity in ho2_df['elasticity'].values:
    if abs(elasticity) > 1:
        level_values.append('Elastic Demand')
    elif abs(elasticity) == 1:
        level_values.append('Unitary Elastic Demand')
    elif abs(elasticity) == 0:
        level_values.append('Perfectly Inelastic Demand')
    else:# abs(elasticity) < 1
        level_values.append('Inelastic Demand')


ho2_df['level'] = level_values
ho2_df

# %%
Vis_ho2 = pd.DataFrame()

for item_id in ho2_df['item_id'].unique():
    entry_df = ho2_df[ho2_df['item_id'] == item_id]
    
    price_change = entry_df["price_change"].mean()
    sale_change = entry_df["sale_change"].mean()
    elasticity = entry_df["elasticity"].mean()
    
    Vis_ho2 = Vis_ho2.append({'item_id': item_id,
                    'price_change': price_change,
                    'sale_change': sale_change,
                    'elasticity': elasticity},ignore_index=True)

#V1   
plt.scatter(Vis_ho2['price_change'], Vis_ho2['sale_change'])

plt.title('Household_2 Scatter Plot of Price Change% vs Sale Change%')
plt.xlabel('Price Change%')
plt.ylabel('Sale Change%')
plt.grid(True)

plt.show()

# %%


# %%


# %%


# %%
import statsmodels.api as sm

# %%
X_value=np.log(category_prices)
y_value=np.log(my_data.groupby('cat_id')["unit_sale"].sum())

# %%
X = sm.add_constant(X_value)

# %%
model_cat = sm.OLS(y_value, X).fit()

# %%
print(model_cat.summary())

# %%
coefficient = model_cat.params[1]
#elasticity_coefficient = coefficient*(X_value.mean()/y_value.mean())
#print(elasticity_coefficient)

# Scatter plot of log(price) vs log(unit_sale)
plt.scatter(X_value, y_value, label='Data points')

# Plot the fitted line
plt.plot(X_value, model_cat.predict(X), color='red', label='Fitted line')

plt.xlabel('Log(Price)')
plt.ylabel('Log(Unit Sale)')
plt.title('Relationship between Log(Price) and Log(Unit Sale)')
plt.text(plt.xlim()[0], plt.ylim()[1], f'Elasticity Coefficient: {coefficient:.2f}', ha='left', va='top')
plt.legend()
plt.grid(True)
plt.show()

# %%


# %%
elasticity_dicts=[]

# %%
for cat_id in my_data.cat_id.unique():
    entry={}
    entry_df=my_data[my_data.cat_id==cat_id]
   
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value=np.log(entry_df.unit_sale)
        X_value=np.log(entry_df.sell_price)
        X = sm.add_constant(X_value)
        model = sm.OLS(y_value, X).fit()
        print(cat_id,':','elasticity=',model.params[1])
        #print(cat_id,':','elasticity=',model.params[1]*(X_value.mean()/y_value.mean()))
    else:
        print(cat_id,':', 'No valid data for regression')
    entry['Category']=cat_id
    entry['elasticity']=model.params[1]
    #entry['elasticity']=model.params[1]*(X_value.mean()/y_value.mean())
    elasticity_dicts.append(entry)
elasticity_cat=pd.DataFrame(elasticity_dicts)

# %%
elasticity_cat

# %%
from sklearn.preprocessing import PolynomialFeatures

elasticity_dicts = []

for cat_id in my_data.cat_id.unique():
    entry = {}
    entry_df = my_data[my_data.cat_id == cat_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value = np.log(entry_df.unit_sale)
        X_value = np.log(entry_df.sell_price).values.reshape(-1, 1)
        
        poly = PolynomialFeatures(degree=2)  
        X_poly = poly.fit_transform(X_value)
        
        poly = sm.add_constant(X_poly)
        model = sm.OLS(y_value, poly).fit()
        elasticity_coefficient = model.params[1]
        #elasticity_coefficient = model.params[1]*(X_value.mean()/y_value.mean())
        if abs(elasticity_coefficient)>1:
            level = 'Elastic Demand'
        elif abs(elasticity_coefficient)==1:
            level = 'Unitary Elastic Demand'
        elif abs(elasticity_coefficient)<1:
            level='Inelastic Demand'
        elif abs(elasticity_coefficient)==0:
            level='Perfectly Inelastic Demand'
        else:
            level='Perfectly Elastic Demand'
        print(cat_id, ':', 'elasticity=', elasticity_coefficient,',sensitivity level:',level)

# %%


# %%


# %%


# %%


# %%


# %%


# %%
X_value=np.log(my_data.groupby("dept_id")["sell_price"].mean())
y_value=np.log(my_data.groupby('dept_id')["unit_sale"].sum())

# %%
X = sm.add_constant(X_value)

# %%
model_dept = sm.OLS(y_value, X).fit()

# %%
print(model_dept.summary())

# %%

coefficient = model_dept.params[1]
plt.scatter(X_value, y_value, label='Data points')

# Plot the fitted line
plt.plot(X_value, model_dept.predict(X), color='red', label='Fitted line')

plt.xlabel('Log(Price)')
plt.ylabel('Log(Unit Sale)')
plt.title('Relationship between Log(Price) and Log(Unit Sale)')
plt.text(plt.xlim()[0], plt.ylim()[1], f'Elasticity Coefficient: {coefficient:.2f}', ha='left', va='top')
plt.legend()
plt.grid(True)
plt.show()

# %%
elasticity_dicts=[]

# %%
for dept_id in my_data.dept_id.unique():
    entry={}
    entry_df=my_data[my_data.dept_id==dept_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value=np.log(entry_df.unit_sale)
        X_value=np.log(entry_df.sell_price)
        X = sm.add_constant(X_value)
        model = sm.OLS(y_value, X).fit()
        print(dept_id,':','elasticity=',model.params[1])
        #print(dept_id,':','elasticity=',model.params[1]*(X_value.mean()/y_value.mean()))
    else:
        print(dept_id,':', 'No valid data for regression')
    entry['Department']=dept_id
    entry['elasticity']=model.params[1]
    #entry['elasticity']=model.params[1]*(X_value.mean()/y_value.mean())
    elasticity_dicts.append(entry)
elasticity_dept=pd.DataFrame(elasticity_dicts)

# %%
elasticity_dept

# %%
elasticity_dicts = []

for dept_id in my_data.dept_id.unique():
    entry = {}
    entry_df = my_data[my_data.dept_id == dept_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value = np.log(entry_df.unit_sale)
        X_value = np.log(entry_df.sell_price).values.reshape(-1, 1)
        
        poly = PolynomialFeatures(degree=2)  
        X_poly = poly.fit_transform(X_value)
        poly = sm.add_constant(X_poly)
        
        model = sm.OLS(y_value, poly).fit()
        elasticity_coefficient = model.params[1]
        #elasticity_coefficient = model.params[1]*(X_value.mean()/y_value.mean())
        if abs(elasticity_coefficient)>1:
            level = 'Elastic Demand'
        elif abs(elasticity_coefficient)==1:
            level = 'Unitary Elastic Demand'
        elif abs(elasticity_coefficient)<1:
            level='Inelastic Demand'
        elif abs(elasticity_coefficient)==0:
            level='Perfectly Inelastic Demand'
        else:
            level='Perfectly Elastic Demand'
        print(dept_id, ':', 'elasticity=', elasticity_coefficient,',sensitivity level:',level)

# %%


# %%


# %%


# %%
X_value=np.log(my_data.groupby("state_id")["sell_price"].mean())
y_value=np.log(my_data.groupby('state_id')["unit_sale"].sum())

# %%
X = sm.add_constant(X_value)

# %%
model_state = sm.OLS(y_value, X).fit()

# %%
print(model_state.summary())

# %%

coefficient = model_state.params[1]
plt.scatter(X_value, y_value, label='Data points')

# Plot the fitted line
plt.plot(X_value, model_state.predict(X), color='red', label='Fitted line')

plt.xlabel('Log(Price)')
plt.ylabel('Log(Unit Sale)')
plt.title('Relationship between Log(Price) and Log(Unit Sale)')
plt.text(plt.xlim()[0], plt.ylim()[1], f'Elasticity Coefficient: {coefficient:.2f}', ha='left', va='top')
plt.legend()
plt.grid(True)
plt.show()

# %%
elasticity_dicts=[]

# %%
for state_id in my_data.state_id.unique():
    entry={}
    entry_df=my_data[my_data.state_id==state_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value=np.log(entry_df.unit_sale)
        X_value=np.log(entry_df.sell_price)
        X = sm.add_constant(X_value)
        model = sm.OLS(y_value, X).fit()
        print(state_id,':','elasticity=',model.params[1])
        #print(state_id,':','elasticity=',model.params[1]*(X_value.mean()/y_value.mean()))
    else:
        print(state_id,':', 'No valid data for regression')
    entry['Department']=state_id
    entry['elasticity']=model.params[1]
    #entry['elasticity']=model.params[1]*(X_value.mean()/y_value.mean())
    elasticity_dicts.append(entry)
elasticity_state=pd.DataFrame(elasticity_dicts)

# %%
elasticity_state

# %%
elasticity_dicts = []

for state_id in my_data.state_id.unique():
    entry = {}
    entry_df = my_data[my_data.state_id == state_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value = np.log(entry_df.unit_sale)
        X_value = np.log(entry_df.sell_price).values.reshape(-1, 1)
        
        poly = PolynomialFeatures(degree=2)  
        X_poly = poly.fit_transform(X_value)
        poly = sm.add_constant(X_poly)
        
        model = sm.OLS(y_value, poly).fit()
        elasticity_coefficient = model.params[1]
        #elasticity_coefficient = model.params[1]*(X_value.mean()/y_value.mean())
        if abs(elasticity_coefficient)>1:
            level = 'Elastic Demand'
        elif abs(elasticity_coefficient)==1:
            level = 'Unitary Elastic Demand'
        elif abs(elasticity_coefficient)<1:
            level='Inelastic Demand'
        elif abs(elasticity_coefficient)==0:
            level='Perfectly Inelastic Demand'
        else:
            level='Perfectly Elastic Demand'
        print(state_id, ':', 'elasticity=', elasticity_coefficient,',sensitivity level:',level)

# %%


# %%


# %%


# %%
X_value=np.log(my_data.groupby("store_id")["sell_price"].mean())
y_value=np.log(my_data.groupby('store_id')["unit_sale"].sum())

# %%
X = sm.add_constant(X_value)

# %%
model_store = sm.OLS(y_value, X).fit()

# %%
print(model_store.summary())

# %%
coefficient = model_store.params[1]
plt.scatter(X_value, y_value, label='Data points')

# Plot the fitted line
plt.plot(X_value, model_store.predict(X), color='red', label='Fitted line')

plt.xlabel('Log(Price)')
plt.ylabel('Log(Unit Sale)')
plt.title('Relationship between Log(Price) and Log(Unit Sale)')
plt.text(plt.xlim()[0], plt.ylim()[1], f'Elasticity Coefficient: {coefficient:.2f}', ha='left', va='top')
plt.legend()
plt.grid(True)
plt.show()

# %%
elasticity_dicts=[]

# %%
for store_id in my_data.store_id.unique():
    entry={}
    entry_df=my_data[my_data.store_id==store_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value=np.log(entry_df.unit_sale)
        X_value=np.log(entry_df.sell_price)
        X = sm.add_constant(X_value)
        model = sm.OLS(y_value, X).fit()
        print(store_id,':','elasticity=',model.params[1])
        #print(store_id,':','elasticity=',model.params[1]*(X_value.mean()/y_value.mean()))
    else:
        print(store_id,':', 'No valid data for regression')
    entry['Store']=store_id
    entry['elasticity']=model.params[1]
    #entry['elasticity']=model.params[1]*(X_value.mean()/y_value.mean())
    elasticity_dicts.append(entry)
elasticity_store=pd.DataFrame(elasticity_dicts)

# %%
elasticity_store

# %%
elasticity_dicts = []

for store_id in my_data.store_id.unique():
    entry = {}
    entry_df = my_data[my_data.store_id == store_id]
    
    # Filter out invalid data
    entry_df = entry_df[(entry_df.unit_sale > 0) & (entry_df.sell_price > 0)]
    
    if not entry_df.empty:
        y_value = np.log(entry_df.unit_sale)
        X_value = np.log(entry_df.sell_price).values.reshape(-1, 1)
        
        poly = PolynomialFeatures(degree=2)  
        X_poly = poly.fit_transform(X_value)
        poly = sm.add_constant(X_poly)
        
        model = sm.OLS(y_value, poly).fit()
        elasticity_coefficient = model.params[1]
        #elasticity_coefficient = model.params[1]*(X_value.mean()/y_value.mean())
        if abs(elasticity_coefficient)>1:
            level = 'Elastic Demand'
        elif abs(elasticity_coefficient)==1:
            level = 'Unitary Elastic Demand'
        elif abs(elasticity_coefficient)<1:
            level='Inelastic Demand'
        elif abs(elasticity_coefficient)==0:
            level='Perfectly Inelastic Demand'
        else:
            level='Perfectly Elastic Demand'
        print(store_id, ':', 'elasticity=', elasticity_coefficient,',sensitivity level:',level)

# %%


# %%


# %%


# %%



