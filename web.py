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

# st.write('Hello World')
# name = st.text_input('Whats your name?')
# st.write(sample)

# if st.button("Click Me"):
#     st.write(f"Hello `{name}`")


#######################
# Sidebar
with st.sidebar:
    st.title('🤖 P5: Pricing Optimization and Analysis Dashboard')
    
    year_list = list(calendar.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = calendar[calendar.year == selected_year]
    # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################


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