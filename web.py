#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

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

#######################
# Page configuration
st.set_page_config(
    page_title="P5: Pricing Optimization and Analysis Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Load data
calendar = pd.read_csv("calendar.csv")
evaluation = pd.read_csv("sales_train_evaluation.csv")
validation = pd.read_csv("sales_train_validation.csv")
prices = pd.read_csv("sell_prices.csv")
sample = pd.read_csv("sample_submission.csv")

d_cols = [col for col in evaluation.columns if col.startswith('d_')]

fix = evaluation[d_cols].stack().reset_index(level=1)
fix.columns = ['d','unit_sale']

my_data = evaluation.drop(d_cols, axis=1).join(fix)

my_data['id']=my_data['id'].astype('category')
my_data['item_id']=my_data['item_id'].astype('category')
my_data['dept_id']=my_data['dept_id'].astype('category')
my_data['cat_id']=my_data['cat_id'].astype('category')
my_data['store_id']=my_data['store_id'].astype('category')
my_data['state_id']=my_data['state_id'].astype('category')
my_data['d']=my_data['d'].astype('category')
my_data['unit_sale']=pd.to_numeric(my_data['unit_sale'],downcast='unsigned')

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

prices['store_id'] = prices['store_id'].astype('category')
prices['item_id'] = prices['item_id'].astype('category')

prices['wm_yr_wk'] = pd.to_numeric(prices['wm_yr_wk'], downcast='unsigned')
prices['sell_price'] = pd.to_numeric(prices['sell_price'], downcast='float')

my_data = my_data.merge(calendar, on='d', how='left').merge(prices, on=['store_id','item_id','wm_yr_wk'], how='left')
my_data['d']=my_data['d'].astype('category')

category_prices = my_data.groupby("cat_id")["sell_price"].mean()
sales_by_category= my_data.groupby("cat_id")["unit_sale"].sum()

category_prices_df = pd.DataFrame({'cat_id': category_prices.index, 'mean_price': category_prices.values})
sales_by_category_df = pd.DataFrame({'cat_id': sales_by_category.index, 'sum_sale': sales_by_category.values})
category_df = pd.merge(category_prices_df, sales_by_category_df, on='cat_id')
category_df['revenue'] = category_df['mean_price']*category_df['sum_sale']

# st.write('Hello World')
# name = st.text_input('Whats your name?')
# st.write(sample)

# if st.button("Click Me"):
#     st.write(f"Hello `{name}`")


# hobbies_1=my_data[my_data['dept_id']=="HOBBIES_1"]
# hobbies_1 = hobbies_1.drop(hobbies_1[hobbies_1['unit_sale'] == 0].index)

# h1_df = pd.DataFrame(columns=['item_id', 'dept_id','cat_id','price', 'sale_perday','price_change','sale_change','elasticity'])


# for item_id in hobbies_1['item_id'].unique():
#     entry_df = hobbies_1[hobbies_1['item_id'] == item_id]
#     for sell_price in entry_df['sell_price'].unique():
#         for dept_id in entry_df['dept_id'].unique():
#             for cat_id in entry_df['cat_id'].unique():
                

#                 item_df = entry_df[entry_df['sell_price'] == sell_price]
#                 sale_perday = item_df['unit_sale'].mean()


#                 hobbies_1_df = pd.DataFrame({'item_id': [item_id], 'dept_id':[dept_id],'cat_id':[cat_id],'price': [sell_price], 'sale_perday': [sale_perday]})
#                 hobbies_1_df = hobbies_1_df.dropna()

#                 h1_df = h1_df.append(hobbies_1_df, ignore_index=True)

#                 h1_df['price_change'] = h1_df['price'].pct_change()*100
#                 h1_df['sale_change'] = h1_df['sale_perday'].pct_change()*100
#                 h1_df['elasticity'] = -h1_df['sale_change']/h1_df['price_change'] 
# h1_df=h1_df.dropna()
# h1_df

# level_values = []


# for elasticity in h1_df['elasticity'].values:
#     if abs(elasticity) > 1:
#         level_values.append('Elastic Demand')
#     elif abs(elasticity) == 1:
#         level_values.append('Unitary Elastic Demand')
#     elif abs(elasticity) == 0:
#         level_values.append('Perfectly Inelastic Demand')
#     else:# abs(elasticity) < 1
#         level_values.append('Inelastic Demand')


# h1_df['level'] = level_values
# h1_df

# Vis_h1 = pd.DataFrame()

# for item_id in h1_df['item_id'].unique():
#     entry_df = h1_df[h1_df['item_id'] == item_id]
    
#     price_change = entry_df["price_change"].mean()
#     sale_change = entry_df["sale_change"].mean()
#     elasticity = entry_df["elasticity"].mean()
    
#     Vis_h1 = Vis_h1.append({'item_id': item_id,
#                     'price_change': price_change,
#                     'sale_change': sale_change,
#                     'elasticity': elasticity},ignore_index=True)

# #V1   
# plt.scatter(Vis_h1['price_change'], Vis_h1['sale_change'])

# plt.title('Hobbies_1 Scatter Plot of Price Change% vs Sale Change%')
# plt.xlabel('Price Change%')
# plt.ylabel('Sale Change%')
# plt.grid(True)

# plt.show()

#######################
# Sidebar
with st.sidebar:
    st.title('🤖 P5: Pricing Optimization and Analysis Dashboard')
    
    year_list = list(my_data.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = my_data[my_data.year == selected_year]
    # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

