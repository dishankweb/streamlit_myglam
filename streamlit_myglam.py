import streamlit as st
import pandas as pd
import plotly.express as px
# from faker import Faker
import random
import numpy as np
import math
import datetime
import uuid
# import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots

# src imports
from src.charts.tile import kpi_tile
from src.charts.charts import default_chart,twin_axis_chart, pie_chart, horizontal_bar_chart_with_value,bar_chart_with_line_chart, trend_comparison_line_chart,trend_comparison_line_chart_aov, grouped_bar_chart, grouped_bar_chart_with_line_chart,horizontal_grouped_bar_chart, horizontal_grouped_bar_chart_channel

date_today = datetime.datetime.now().date()
date_today = datetime.datetime(2023, 10, 20)


st.set_page_config(layout="wide", page_title="E-commerce Dashboard")

def date_change_timedelta(string_1): # convert date string to timedelta
    return datetime.datetime.strptime(string_1, "%Y-%m-%d").date()

def previous_time_delta_percentage(dataframe, date_today, option):
    if option=='This Month':
        start_date = date_today.replace(day=1)
        dataframe_ = dataframe[(dataframe['OrderDate'] >= start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - relativedelta(months=1)
        delta_end_date = date_today - relativedelta(months=1)
    elif option=='This Quarter':
        start_date = date_today - pd.DateOffset(months=(date_today.month - 1) % 3, days=date_today.day - 1)
        dataframe_ = dataframe[(dataframe['OrderDate'] >= start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - relativedelta(months=3)
        delta_end_date = date_today - relativedelta(months=3)
    elif option=='This Year':
        start_date = date_today.replace(day=1, month=1)
        dataframe_ = dataframe[(dataframe['OrderDate'] >= start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - relativedelta(months=12)
        delta_end_date = date_today - relativedelta(months=12)
    elif option == 'Last 7 Days':
        start_date = date_today - pd.Timedelta(days=7)
        dataframe_ = dataframe[(dataframe['OrderDate'] > start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - pd.Timedelta(days=7)
        delta_end_date = date_today - pd.Timedelta(days=7)
    elif option == 'Last 30 Days':
        start_date = date_today - pd.Timedelta(days=30)
        dataframe_ = dataframe[(dataframe['OrderDate'] > start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - pd.Timedelta(days=30)
        delta_end_date = date_today - pd.Timedelta(days=30)
    dataframe_delta = dataframe[(dataframe['OrderDate'] > delta_start_date) & (dataframe['OrderDate'] <= delta_end_date)]
    return dataframe_, dataframe_delta

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# data import
Ecom_Ordertable = pd.read_csv('src/data/Ecom_Ordertable.csv', encoding='utf-8', parse_dates=['OrderDate', 'FirstOrderDate'])
Ecom_CustomerAttribute = pd.read_csv('src/data/Ecom_CustomerAttribute.csv', encoding='utf-8', parse_dates=[])
# Ecom_Ordertable['OrderDate'] = Ecom_Ordertable['OrderDate'].apply(date_change_timedelta) # date string to timedelta
Ecom_Orderlinetable = pd.read_csv('src/data/Ecom_Orderlinetable.csv', encoding='utf-8', parse_dates=['OrderDate'])
worst_channel_cohort_agg = pd.read_csv('src/data/worst_channel_cohort_agg.csv',encoding='utf-8', parse_dates=['FirstOrderDate'])
worst_city_cohort_agg = pd.read_csv('src/data/worst_city_cohort_agg.csv', encoding='utf-8', parse_dates=['FirstOrderDate'])
customer_cohort_retention_1a = pd.read_csv('src/data/customer_cohort_retention_1a.csv')
customer_cohort_retention_1b = pd.read_csv('src/data/customer_cohort_retention_1b.csv')
customer_cohort_retention_1c = pd.read_csv('src/data/customer_cohort_retention_1c.csv')
customer_cohort_retention_2a = pd.read_csv('src/data/customer_cohort_retention_2a.csv')
RecencyBucket_rev = pd.read_csv('src/data/RecencyBucket_rev.csv')
Customer_attribute_4yr_rev = pd.read_csv('src/data/Customer_attribute_4yr_rev.csv')
AOVquart = pd.read_csv('src/data/AOVquart.csv')

# Main df read
# df = pd.read_csv('fake_ecom_data.csv', encoding='utf-8')
# df['Purchase Date'] = df['Purchase Date'].apply(date_change_timedelta) # date string to timedelta

# Streamlit dashboard layout

col1, col2 = st.columns([3, 1])    
with col1:
    st.title('E-Commerce Executive Dashboard')
with col2:
    option = st.selectbox('',
        ('This Year', 'This Quarter', 'This Month', 'Last 7 Days', 'Last 30 Days', 'All Data', 'Custom Range'))

if option == 'Last 7 Days': 
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today,option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
elif option == 'Last 30 Days':
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today,option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
elif option == 'This Month':
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today,option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
elif option == 'This Quarter':
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today, option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
elif option == 'This Year':
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today, option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
elif option == 'All Data':
    pass
elif option == 'Custom Range':
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today, option=option)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option)
else:
    pass


# Display KPIs

listTabs = ['Performance Summary', 'Customer value cohort', 'Customer retention by first source', 'Best Customer profile','Worst cohorts', 'Cohort Analysis', 
            'Cohort Analysis 2', 'Audience Overview']
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([s.center(15,"\u2001") for s in listTabs]) # [s.center(29,"\u2001")

# listTabs = ['Business Overview', 'Website vs Marketplace', 'Geo Sales', 'Product Insights', 'Retention', 'Performance Marketing']
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([s.center(20,"\u2001") for s in listTabs]) # [s.center(29,"\u2001")
# tab1, tab2 = st.tabs(['Revenue', 'Retention'])

# Run the Streamlit app by saving this script as `app.py` and running `streamlit run app.py` in your terminal.

total_revenue = Ecom_Ordertable['Total_Price'].sum()
total_orders = Ecom_Ordertable['OrderID'].nunique()
aov = total_revenue / total_orders if total_orders else 0
new_customers = Ecom_Ordertable[Ecom_Ordertable['OrderDate'] == Ecom_Ordertable['FirstOrderDate']]['CustomerID'].nunique()
repeat_customers = Ecom_Ordertable[Ecom_Ordertable['OrderDate'] != Ecom_Ordertable['FirstOrderDate']]['CustomerID'].nunique()
discounted_order = Ecom_Ordertable[Ecom_Ordertable['Total_DiscVal']>0]['OrderID'].nunique()*100/total_orders

# # total_orders = df['Order ID'].nunique()
# total_orders_website = df.loc[df['Sales Channel']== 'Mobile App', :]['Order ID'].nunique()
# total_orders_marketplace = df.loc[df['Sales Channel']== 'Online', :]['Order ID'].nunique()
# # total_revenue = df['Net Sales'].sum()
# total_revenue_website = df.loc[df['Sales Channel']== 'Mobile App', :]['Net Sales'].sum()
# total_revenue_marketplace = df.loc[df['Sales Channel']== 'Online', :]['Net Sales'].sum()
# # aov = total_revenue / total_orders if total_orders else 0
# aov_website = total_revenue_website / total_orders_website if total_orders_website else 0
# aov_marketplace = total_revenue_marketplace / total_orders_marketplace if total_orders_marketplace else 0

# Delta KPIs
new_customers_delta = Ecom_Ordertable_delta[Ecom_Ordertable_delta['OrderDate'] == Ecom_Ordertable_delta['FirstOrderDate']]['CustomerID'].nunique()
repeat_customers_delta = Ecom_Ordertable_delta[Ecom_Ordertable_delta['OrderDate'] != Ecom_Ordertable_delta['FirstOrderDate']]['CustomerID'].nunique()

total_orders_delta = Ecom_Ordertable_delta['OrderID'].nunique()
# total_orders_website_delta = Ecom_Ordertable_delta.loc[Ecom_Ordertable_delta['Sales Channel']== 'Mobile App', :]['Order ID'].nunique()
# total_orders_marketplace_delta = Ecom_Ordertable_delta.loc[Ecom_Ordertable_delta['Sales Channel']== 'Online', :]['Order ID'].nunique()
total_revenue_delta = Ecom_Ordertable_delta['Total_Price'].sum()
# total_revenue_website_delta = Ecom_Ordertable_delta.loc[Ecom_Ordertable_delta['Sales Channel']== 'Mobile App', :]['Net Sales'].sum()
# total_revenue_marketplace_delta = Ecom_Ordertable_delta.loc[Ecom_Ordertable_delta['Sales Channel']== 'Online', :]['Net Sales'].sum()
aov_delta = total_revenue_delta / total_orders_delta if total_orders else 0
# aov_website_delta = total_revenue_website_delta / total_orders_website_delta if total_orders_website_delta else 0
# aov_marketplace_delta = total_revenue_marketplace_delta / total_orders_marketplace_delta if total_orders_marketplace_delta else 0
discounted_order_delta = Ecom_Ordertable_delta[Ecom_Ordertable_delta['Total_DiscVal']>0]['OrderID'].nunique()*100/total_orders_delta
    
with tab1:
    kpi1, kpi2, kpi3 = st.columns(3) # row 1 - 3 KPIs
    kpi4, kpi5, kpi6 = st.columns(3)
    
    with st.container():
        with kpi1:
            kpi_tile(kpi1,tile_text='Revenue', tile_label='', tile_value=total_revenue,
                     tile_value_prefix='$',delta_value=(total_revenue-total_revenue_delta)*100/total_revenue_delta,integer=True)
            # tile = kpi1.container(height=240)
            # tile.header('Blended Revenue')
            # tile.metric(label="", value=f"${total_revenue:,.2f}", delta='9.3%')

        with kpi2:
            kpi_tile(kpi2,tile_text='Total Orders', tile_label='', tile_value=total_orders,
                     tile_value_prefix='',delta_value=(total_orders-total_orders_delta)*100/total_orders_delta,integer=True)
            # tile = kpi2.container(height=240)
            # tile.header('Blended Orders')
            # tile.metric(label="", value=f"{total_orders:,}", delta='-1.2%')
            
        with kpi3:
            kpi_tile(kpi3,tile_text='Average Order Value', tile_label='', tile_value=aov,
                     tile_value_prefix='$',delta_value=(aov-aov_delta)*100/aov_delta,integer=True)
            # tile = kpi3.container(height=240)
            # tile.header('Blended AOV')
            # tile.metric(label="", value=f"${aov:,.2f}", delta='11%')
    
        with kpi4:
            kpi_tile(kpi4,tile_text='New Customers', tile_label='', tile_value=new_customers,
                     tile_value_prefix='',delta_value=(new_customers-new_customers_delta)*100/new_customers_delta,integer=True) 
            # tile = kpi4.container(height=240)
            # tile.header('Blended New Customers')
            # tile.metric(label="", value=f"{new_customers:,}", delta='6%') 
        
        with kpi5:
            kpi_tile(kpi5,tile_text="Repeat Customers", tile_label='', tile_value=repeat_customers,
                     tile_value_prefix='',delta_value=(repeat_customers-repeat_customers_delta)*100/repeat_customers_delta,integer=True)
            # tile = kpi5.container(height=240)
            # tile.header('Blended Repeat Customers')
            # tile.metric(label="", value=f"{math.floor(total_orders*0.75):,}", delta='6%')     

        with kpi6:
            kpi_tile(kpi6,tile_text='Discounted Orders', tile_label='', tile_value=discounted_order,
                     tile_value_prefix='',delta_value=(discounted_order-discounted_order_delta)*100/discounted_order_delta,
                     integer=False, delta_color_inversion='inverse', tile_value_suffix='%')
            # tile = kpi6.container(height=240)
            # tile.header('Blended Cancellation Rate')
            # tile.metric(label="", value=f"{math.floor(total_orders*0.75):,}", delta='6%', delta_color='inverse') 
        
    with st.container(height=50):
        st.text('How our key metrics are trending?')    
        

    with st.container(height=620):
        st.text('Revenue trend & comparison with the previous period')   
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_1')
             
    with st.container(height=620):
        st.text('Revenue trend & comparison with the previous period - Cumulative')   
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_2', cumulative_sum=True)
    
    with st.container(height=620):
        st.text('Total Orders trend and Comparison with the previous period')   
        # trend_comparison_line_chart()
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='OrderID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_3', unique_count=True)

    with st.container(height=620):
        st.text('Average Order Value trend and Comparison with the previous period')   
        # trend_comparison_line_chart()
        trend_comparison_line_chart_aov(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',col_2='OrderID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_4', unique_count=True)


    with st.container(height=620):
        st.text('New Customers trend and Comparison with the previous period')
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='CustomerID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_5', unique_count=True, new_customer=True)
        # trend_comparison_line_chart()
    
    with st.container(height=660):
        st.text('Sales by Product - Top 10')   
        horizontal_bar_chart_with_value(Ecom_Orderlinetable, col_1='ItemName')
    
    with st.container(height=660):
        st.text('Revenue by Coupon Code - Top 10')   
        horizontal_bar_chart_with_value(Ecom_Ordertable, col_1='Discount_Code')

with tab2:
    with st.container(height=50):
        st.text('How valuable are our Customers over time?') 
    
    with st.container(height=600):
        st.text('Average Customer Value by Acquisition Month in 1/30/60/90/180 days')   
        grouped_bar_chart_with_line_chart(Ecom_Ordertable)

    with st.container(height=600):
        st.text('Top 10 Average Customer Value by  Discount Code Coupon')   
        # horizontal_grouped_bar_chart()
    
    with st.container(height=600):
        st.text('Average Customer Value by Marketing Channel over 1/30/60/90/180 days time period')   
        horizontal_grouped_bar_chart_channel(Ecom_Ordertable)

with tab3:
    with st.container(height=50):
        st.text('How well are we retaining our customers?')

    kpi3_1,kpi3_2,kpi3_3 = st.columns(3) 
    kpi_tile(kpi3_1,tile_text='Interval between 1st and 2nd Order', tile_label='', tile_value=new_customers,
                     tile_value_prefix='',delta_value=2,integer=True)
    kpi_tile(kpi3_2,tile_text='Interval between 2nd and 3rd Order', tile_label='', tile_value=new_customers,
                     tile_value_prefix='',delta_value=2,integer=True)
    kpi_tile(kpi3_3,tile_text='Interval between 3rd and 4th Order', tile_label='', tile_value=new_customers,
                     tile_value_prefix='',delta_value=2,integer=True)
    
    # with st.container(height=600):
    #     st.text('How Many Customers repeat?')   
    #     grouped_bar_chart_with_line_chart()

    # with st.container(height=600):
    #     st.text('Average Order Value at 1st Order, 2nd Order, 3rd Order, 4th Order')   
    #     grouped_bar_chart_with_line_chart()

    # with st.container(height=600):
    #     st.text('Repeat Order Intervals')   
    #     grouped_bar_chart_with_line_chart()

    # with st.container(height=600):
    #     st.text('Order count at 1st Order, 2nd Order, 3rd Order, 4th Order over months')   
    #     grouped_bar_chart()

    # with st.container(height=600):
    #     st.text('Customer count who purchased 1 Item, 2 Items, 3 items, 3+ items')   
    #     grouped_bar_chart_with_line_chart()

with tab4:
    with st.container(height=50):
        st.text('Best Vs Average Customer Profile - Comparison View')

    with st.container(height=600):
        st.text('Customer Profile by Channel Comparison View')   
        df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        st.dataframe(df_demo)
    with st.container(height=600):
        st.text('Product Level Profile by Channel') 
        df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        st.dataframe(df_demo)  
        #dataframe here

with tab5:
    with st.container(height=50):
        st.text('Worst Cohort View')

    with st.container(height=600):
        st.text('Worst Channel Cohorts')
        bar_chart_with_line_chart(worst_channel_cohort_agg, 'marketing_channel')
        
    with st.container(height=600):
        st.text('Worst City Cohorts')  
        bar_chart_with_line_chart(worst_city_cohort_agg, 'CustomerCity')
        
with tab6:
    with st.container(height=50):
        st.text('Cohort Analysis')

    with st.container(height=600):
        st.text('Customer Retention by First Order')
        st.dataframe(customer_cohort_retention_1a, use_container_width=True)
        
    with st.container(height=600):
        st.text('Retention Cohorts')
        st.dataframe(customer_cohort_retention_1b, use_container_width=True)

    with st.container(height=600):
        st.text('Customer Average monthly Revenue')
        st.dataframe(customer_cohort_retention_1c, use_container_width=True)
        # df here

with tab7:
    with st.container(height=50):
        st.text('Cohort Analysis')

    with st.container(height=600):
        st.text('Customer Retention by City')
        customer_cohort_retention_2a = customer_cohort_retention_2a.sort_values(by='month_0_count', ascending=False).reset_index(drop=True)
        st.dataframe(customer_cohort_retention_2a)
        
    with st.container(height=600):
        st.text('Customer Percentage Retention by City')  

    with st.container(height=600):
        st.text('Channel-wise Cohorts')  
    
    with st.container(height=600):
        st.text('Channel-wise Cohorts - Customer count')

with tab8:
    with st.container(height=50):
        st.text('Audience Overview')

    with st.container(height=600):
        st.text('Audience Split by Recency Buckets - 0-7,7-15,15-30,30-90, 90-180, >180 days')   
        # RecencyBucket_rev
        pie_chart(RecencyBucket_rev, 'RecencyBucket')
        
    with st.container(height=620):
        st.text('Audience Split by Frequency Buckets - 0, 1, 2, 3, 4, 4+')
        col_1,col_2 = st.columns(2)
        with col_1:
            channel = st.selectbox('',Customer_attribute_4yr_rev['marketing_channel'].unique(), key='tab_8_1')
        with col_2:
            tier = st.selectbox('',Customer_attribute_4yr_rev['Tier'].unique(), key='tab_8_2')
        Customer_attribute_4yr_rev = Customer_attribute_4yr_rev[Customer_attribute_4yr_rev['marketing_channel']==channel]
        Customer_attribute_4yr_rev = Customer_attribute_4yr_rev[Customer_attribute_4yr_rev['Tier']==tier]

        pie_chart(Customer_attribute_4yr_rev,'FrequencyBucket') 

    with st.container(height=600):
        st.text('Audience Split by 4 AOV quartiles')
        pie_chart(AOVquart,'quartile')