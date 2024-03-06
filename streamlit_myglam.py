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
from src.charts.charts import default_chart,twin_axis_chart, pie_chart, horizontal_bar_chart_with_value,bar_chart_with_line_chart, trend_comparison_line_chart,trend_comparison_line_chart_aov, grouped_bar_chart, grouped_bar_chart_with_line_chart_2,horizontal_grouped_bar_chart, horizontal_grouped_bar_chart_channel

date_today = datetime.datetime.now().date()
date_today = datetime.datetime(2023, 10, 20)

def header(url, size=24):
     st.markdown(f'<p style="background-color:#8eb5f5;color:#FFFFFF;font-size:{size}px;border-radius:2%;text-align:center; font-weight: bold;">{url}</p>', unsafe_allow_html=True)
    #  st.markdown(f'<p style="background-color:#0066cc;color:#FFFFFF;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def header_chart(url, size=24):
     st.markdown(f'<p style="background-color:#0066cc;color:#FFFFFF;font-size:{size}px;border-radius:2%;text-align:center; font-weight: bold;">{url}</p>', unsafe_allow_html=True)

def header_left(url, size=24):
     st.markdown(f'<p style="background-color:#0066cc;color:#FFFFFF;font-size:{size}px;border-radius:2%;text-align:left; font-weight: bold;">{url}</p>', unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="E-commerce Dashboard")

def date_change_timedelta(string_1): # convert date string to timedelta
    return datetime.datetime.strptime(string_1, "%Y-%m-%d").date()

def previous_time_delta_percentage(dataframe, date_today, option, custom_date_start=datetime.datetime(2023,2,1), custom_date_end=datetime.datetime(2023,6,1)):
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
    elif option == 'Custom Range':
        start_date = custom_date_start
        # start_date = date_today - pd.Timedelta(days=30)
        dataframe_ = dataframe[(dataframe['OrderDate'] > pd.Timestamp(start_date)) & (dataframe['OrderDate'] <= pd.Timestamp(custom_date_end))]
        date_diff = custom_date_end - custom_date_start
        delta_start_date = start_date - date_diff
        delta_end_date = custom_date_end - date_diff
        dataframe_delta = dataframe[(dataframe['OrderDate'] > pd.Timestamp(delta_start_date)) & (dataframe['OrderDate'] <= pd.Timestamp(delta_end_date))]
    else:
        pass

    if option != 'Custom Range':
        dataframe_delta = dataframe[(dataframe['OrderDate'] > delta_start_date) & (dataframe['OrderDate'] <= delta_end_date)]
    return dataframe_, dataframe_delta

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# data import
Ecom_Ordertable = pd.read_csv('src/data/Ecom_Ordertable.csv', encoding='utf-8', parse_dates=['OrderDate', 'FirstOrderDate'])
Ecom_Ordertable_2 = pd.read_csv('src/data/Ecom_Ordertable.csv', encoding='utf-8', parse_dates=['OrderDate', 'FirstOrderDate'])
Ecom_CustomerAttribute = pd.read_csv('src/data/Ecom_CustomerAttribute.csv', encoding='utf-8', parse_dates=[])
# Ecom_Ordertable['OrderDate'] = Ecom_Ordertable['OrderDate'].apply(date_change_timedelta) # date string to timedelta
# Ecom_Orderlinetable = pd.read_csv('src/data/Ecom_Orderlinetable.csv', encoding='utf-8', parse_dates=['OrderDate'])
Ecom_Orderlinetable_1 = pd.read_csv('src/data/Ecom_Orderlinetable_1.csv', encoding='utf-8', parse_dates=['OrderDate'])
Ecom_Orderlinetable_2 = pd.read_csv('src/data/Ecom_Orderlinetable_2.csv', encoding='utf-8', parse_dates=['OrderDate'])
Ecom_Orderlinetable = pd.concat([Ecom_Orderlinetable_1, Ecom_Orderlinetable_2], ignore_index=True)
worst_channel_cohort_agg = pd.read_csv('src/data/worst_channel_cohort_agg.csv',encoding='utf-8', parse_dates=['FirstOrderDate'])
worst_city_cohort_agg = pd.read_csv('src/data/worst_city_cohort_agg.csv', encoding='utf-8', parse_dates=['FirstOrderDate'])
customer_cohort_retention_1a = pd.read_csv('src/data/customer_cohort_retention_1a.csv', parse_dates=['first_month'])
customer_cohort_retention_1b = pd.read_csv('src/data/customer_cohort_retention_1b.csv', parse_dates=['first_month'])
customer_cohort_retention_1c = pd.read_csv('src/data/customer_cohort_retention_1c.csv', parse_dates=['first_month'])
customer_cohort_retention_2a = pd.read_csv('src/data/customer_cohort_retention_2a.csv')
RecencyBucket_rev = pd.read_csv('src/data/RecencyBucket_rev.csv')
Customer_attribute_4yr_rev = pd.read_csv('src/data/Customer_attribute_4yr_rev.csv')
AOVquart = pd.read_csv('src/data/AOVquart.csv')
customer_profile_by_channel_comparison_1 = pd.read_csv('src/data/customer_profile_by_channel_comparison_part1.csv')
customer_profile_by_channel_comparison_2 = pd.read_csv('src/data/customer_profile_by_channel_comparison_part2.csv')
customer_profile_by_channel_comparison_3 = pd.read_csv('src/data/customer_profile_by_channel_comparison_part3.csv')
customer_profile_by_channel_comparison = pd.concat([customer_profile_by_channel_comparison_1, customer_profile_by_channel_comparison_2, customer_profile_by_channel_comparison_3], ignore_index=True)


Order_Attribute_1 = pd.read_csv('src/data/Order_Attribute_part1.csv')
Order_Attribute_2 = pd.read_csv('src/data/Order_Attribute_part2.csv')
Order_Attribute_3 = pd.read_csv('src/data/Order_Attribute_part3.csv')
Order_Attribute = pd.concat([Order_Attribute_1, Order_Attribute_2, Order_Attribute_3], ignore_index=True)

# Main df read
# df = pd.read_csv('fake_ecom_data.csv', encoding='utf-8')
# df['Purchase Date'] = df['Purchase Date'].apply(date_change_timedelta) # date string to timedelta

# Streamlit dashboard layout

col1, col2 = st.columns([3, 1])    
with col1:
    # st.title('E-Commerce Executive Dashboard')
    header_left('E-Commerce Executive Dashboard', 44)
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
    col_1,col_2,col_3, col_4 = st.columns(4)
    with col_3:
        date_start = st.date_input("Start Date", datetime.date(2022, 7, 6))
    with col_4:
        date_end = st.date_input("End Date", datetime.date(2023, 7, 6))
    Ecom_Ordertable,Ecom_Ordertable_delta = previous_time_delta_percentage(dataframe=Ecom_Ordertable, date_today=date_today, option=option,custom_date_start=date_start,custom_date_end=date_end)
    Ecom_Orderlinetable,Ecom_Orderlinetable_delta = previous_time_delta_percentage(dataframe=Ecom_Orderlinetable, date_today=date_today,option=option, custom_date_start=date_start,custom_date_end=date_end)
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
# total_orders_delta = 100
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
        
    # with st.container(height=50):
        # st.subheader("<h1 style='text-align: center; color: blue;'>How our key metrics are trending?</h1>", unsafe_allow_html=True)

    # st.text('How our key metrics are trending?')    
    header(' How our key metrics are trending?', 34)
        

    with st.container(height=620):
        # st.markdown(f'**Revenue trend & comparison with the previous period**', help = 'definition')
        header_chart('Revenue trend & comparison with the previous period')
        # st.text('Revenue trend & comparison with the previous period')   
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_1')
             
    with st.container(height=620):
        # st.text('Revenue trend & comparison with the previous period - Cumulative')
        # st.markdown(f'**Revenue trend & comparison with the previous period - Cumulative**', help = 'definition')  
        header_chart('Revenue trend & comparison with the previous period - Cumulative') 
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_2', cumulative_sum=True)
    
    with st.container(height=620):
        # st.text('Total Orders trend and Comparison with the previous period')  
        # st.markdown(f'**Total Orders trend and Comparison with the previous period**', help = 'definition')  
        header_chart('Total Orders trend and Comparison with the previous period')
        # trend_comparison_line_chart()
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='OrderID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_3', unique_count=True)

    with st.container(height=620):
        # st.text('Average Order Value trend and Comparison with the previous period')   
        # st.markdown(f'**Average Order Value trend and Comparison with the previous period**', help = 'definition') 
        header_chart('Average Order Value trend and Comparison with the previous period')
        # trend_comparison_line_chart()
        trend_comparison_line_chart_aov(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='Total_Price',col_2='OrderID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_4', unique_count=True)


    with st.container(height=620):
        # st.text('New Customers trend and Comparison with the previous period')
        # st.markdown(f'**New Customers trend and Comparison with the previous period**', help = 'definition') 
        header_chart('New Customers trend and Comparison with the previous period')
        trend_comparison_line_chart(df=Ecom_Ordertable,df_delta=Ecom_Ordertable_delta,date_col='OrderDate', 
                                    col_1='CustomerID',x_axis_title='Date', y_axis_title='revenue',
                                    trend_1='trend_1', trend_2='trend_2', key='tab1_5', unique_count=True, new_customer=True)
        # trend_comparison_line_chart()
    
    with st.container(height=660):
        # st.text('Sales by Product - Top 10')   
        # st.markdown(f'**Sales by Product - Top 10**', help = 'definition') 
        header('Sales by Product - Top 10')
        horizontal_bar_chart_with_value(Ecom_Orderlinetable, col_1='ItemName')
    
    with st.container(height=660):
        # st.text('Revenue by Coupon Code - Top 10')   
        # st.markdown(f'**Revenue by Coupon Code - Top 10**', help = 'definition') 
        header('Revenue by Coupon Code - Top 10')
        horizontal_bar_chart_with_value(Ecom_Ordertable, col_1='Discount_Code')

with tab2:
    
    # st.text('How valuable are our Customers over time?') 
    header('How valuable are our Customers over time?', 28)
    
    with st.container(height=600):
        # st.text('Average Customer Value by Acquisition Month in 1/30/60/90/180 days')  
        header_chart('Average Customer Value by Acquisition Month in 1/30/60/90/180 days') 
        grouped_bar_chart_with_line_chart_2(Ecom_Ordertable_2)

    # with st.container(height=600):
    #     st.text('Top 10 Average Customer Value by  Discount Code Coupon')   
    #     # horizontal_grouped_bar_chart()
    
    with st.container(height=600):
        st.markdown(f'**Average Customer Value by Marketing Channel over 1/30/60/90/180 days time period**', help = 'definition')
        # st.text('Average Customer Value by Marketing Channel over 1/30/60/90/180 days time period')   
        horizontal_grouped_bar_chart_channel(Ecom_Ordertable)

with tab3:
    Customer_attribute_4yr_rev = Customer_attribute_4yr_rev.assign(Month = lambda x: pd.to_datetime(x['FirstOrderDate']).dt.strftime('%Y-%m'))
    pivot_customer = Customer_attribute_4yr_rev.pivot_table(index='Month', 
                                       values=['FirstOrderDate','SecondOrderDate','ThirdOrderDate','FourthOrderDate'],
                                       aggfunc=['count']
                                      )
    pivot_customer.columns = [elem[1] for elem in pivot_customer.columns.tolist()]

    pivot_customer = pivot_customer.assign(SecondOrderRate = lambda x: (x['SecondOrderDate']/x['FirstOrderDate'].sum()) * 100,
                                       ThirdOrderRate = lambda x: (x['ThirdOrderDate']/x['FirstOrderDate'].sum()) * 100,
                                       FourthOrderRate = lambda x: (x['FourthOrderDate']/x['FirstOrderDate'].sum()) * 100
                                       )
    # st.text('How well are we retaining our customers?')
    header('How well are we retaining our customers?', 28)
    d2_d1, d3_d2, d4_d3 = Order_Attribute[['D2_D1', 'D3_D2', 'D4_D3']].mean().abs()
    kpi3_1,kpi3_2,kpi3_3 = st.columns(3) 
    kpi_tile(kpi3_1,tile_text='Interval between 1st and 2nd Order', tile_label='', tile_value=d2_d1,
                     tile_value_prefix='',delta_value=2,integer=True)
    kpi_tile(kpi3_2,tile_text='Interval between 2nd and 3rd Order', tile_label='', tile_value=d3_d2,
                     tile_value_prefix='',delta_value=2,integer=True)
    kpi_tile(kpi3_3,tile_text='Interval between 3rd and 4th Order', tile_label='', tile_value=d4_d3,
                     tile_value_prefix='',delta_value=2,integer=True)
    
    with st.container(height=600):
        # st.text('How Many Customers repeat?')
        header_chart('How Many Customers repeat?')
        plot = px.bar(pivot_customer[['SecondOrderRate','ThirdOrderRate','FourthOrderRate']], barmode='group')
        st.plotly_chart(plot, use_container_width=True)

        Order_Attribute = Order_Attribute.assign(Month = lambda x: pd.to_datetime(x['FirstOrderDate']).dt.strftime('%Y-%m'))   
        # grouped_bar_chart_with_line_chart()

    with st.container(height=600):
        header_chart('Average Order Value at 1st Order, 2nd Order, 3rd Order, 4th Order') 
        plot = px.bar(Order_Attribute.pivot_table(index='Month',
                                   columns='Order_Flag', 
                                   values='Total_Price', 
                                   aggfunc='mean'),
        barmode='group'
        )
        st.plotly_chart(plot, use_container_width=True)  
        # grouped_bar_chart_with_line_chart()

    with st.container(height=600):
        header_chart('Repeat Order Intervals')
        plot =px.bar(Order_Attribute.pivot_table(index='Month', values=['D2_D1', 'D3_D2', 'D4_D3'], aggfunc='mean').abs(),
        barmode='group'
        )
        st.plotly_chart(plot, use_container_width=True)

        # grouped_bar_chart_with_line_chart()

    with st.container(height=600):
        header_chart('Order count at 1st Order, 2nd Order, 3rd Order, 4th Order over months')   
        plot = px.bar(Order_Attribute.groupby('Month')['Order_Flag'].value_counts().reset_index(),
        x='Month',
        y='count',
        color='Order_Flag',
        barmode='group'
        )
        st.plotly_chart(plot, use_container_width=True)
        # grouped_bar_chart()

    with st.container(height=600):
        header_chart('Customer count who purchased 1 Item, 2 Items, 3 items, 3+ items')   
        plot= px.bar(Order_Attribute.groupby('Month')['FrequencyBucket'].value_counts().reset_index(),
        x='Month',
        y='count',
        color='FrequencyBucket',
        barmode='group'
        )
        st.plotly_chart(plot, use_container_width=True)

        # grouped_bar_chart_with_line_chart()

with tab4:
    
    # st.text('Best Vs Average Customer Profile - Comparison View')
    header('Best Vs Average Customer Profile - Comparison View', 28)

    with st.container(height=500):
        # st.text('Customer Profile by Channel Comparison View')   
        
        # st.markdown(f'**Customer Profile by Channel Comparison View**', help = 'definition') 
        header_chart('Customer Profile by Channel Comparison View')
        # df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        customer_profile_by_channel_comparison= customer_profile_by_channel_comparison.groupby('marketing_channel').agg({'SecondOrdValue':'mean', 'D2_D1':'mean', 'First_Ord_Value':'mean', 'CV_90':'mean', 'CustomerID':'count'})
        customer_profile_by_channel_comparison['D2_D1'] = customer_profile_by_channel_comparison['D2_D1'].abs().apply(lambda x: int(x))
        customer_profile_by_channel_comparison = customer_profile_by_channel_comparison.astype(int)
        st.dataframe(customer_profile_by_channel_comparison, use_container_width=True)
    with st.container(height=600):
        # st.text('Product Level Profile by Channel') 
        # st.markdown(f'**Product Level Profile by Channel**', help = 'definition') 
        header_chart('Product Level Profile by Channel')
        # df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        # st.dataframe(df_demo)  
        #dataframe here
        data = pd.read_csv('src/data/df.csv')
        data['Total_price'] = data['ItemQuantity'] * data['Item_UnitPrice']
        data = data.groupby('ItemName').agg({'Total_price':'mean', 'OrderID':'count'}).sort_values(by='Total_price', ascending=False)
        data['avg order value'] = data['Total_price']/data['OrderID']
        st.dataframe(data.drop(columns=['Total_price']).rename({'OrderID': 'customer count'}), use_container_width=True)

with tab5:
    # st.text('Worst Cohort View')
    header('Worst Cohort View', 28)

    with st.container(height=600):
        # st.text('Worst Channel Cohorts')
        st.markdown(f'**Worst Channel Cohorts**', help = 'definition')
        bar_chart_with_line_chart(worst_channel_cohort_agg, 'marketing_channel')
        
    with st.container(height=600):
        # st.text('Worst City Cohorts')  
        st.markdown(f'**Worst City Cohorts**', help = 'definition')
        bar_chart_with_line_chart(worst_city_cohort_agg, 'CustomerCity')
        
with tab6:
    # st.text('Cohort Analysis')
    header('Cohort Analysis', 28)

    with st.container(height=600):
        # st.text('Customer Retention by First Order')
        st.markdown(f'**Customer Retention by First Order**', help = 'definition')
        customer_cohort_retention_1a = customer_cohort_retention_1a[customer_cohort_retention_1a['first_month']>(date_today-relativedelta(months=12))]
        customer_cohort_retention_1a = customer_cohort_retention_1a[customer_cohort_retention_1a['first_month']<date_today].reset_index(drop=True)
        customer_cohort_retention_1a['first_month'] = customer_cohort_retention_1a['first_month'].apply(lambda x: pd.to_datetime(x).date())
        st.dataframe(customer_cohort_retention_1a, use_container_width=True)
        
    with st.container(height=600):
        # st.text('Retention Cohorts')
        st.markdown(f'**Retention Cohorts**', help = 'definition')
        customer_cohort_retention_1b = customer_cohort_retention_1b[customer_cohort_retention_1b['first_month']>(date_today-relativedelta(months=12))]
        customer_cohort_retention_1b = customer_cohort_retention_1b[customer_cohort_retention_1b['first_month']<date_today].reset_index(drop=True)
        customer_cohort_retention_1b['first_month'] = customer_cohort_retention_1b['first_month'].apply(lambda x: pd.to_datetime(x).date())
        st.dataframe(customer_cohort_retention_1b, use_container_width=True)

    with st.container(height=600):
        # st.text('Customer Average monthly Revenue')
        st.markdown(f'**Customer Average monthly Revenue**', help = 'definition')
        customer_cohort_retention_1c = customer_cohort_retention_1c[customer_cohort_retention_1c['first_month']>(date_today-relativedelta(months=12))]
        customer_cohort_retention_1c = customer_cohort_retention_1c[customer_cohort_retention_1c['first_month']<date_today].reset_index(drop=True)
        customer_cohort_retention_1c['first_month'] = customer_cohort_retention_1c['first_month'].apply(lambda x: pd.to_datetime(x).date())
        st.dataframe(customer_cohort_retention_1c, use_container_width=True)
        # df here

with tab7:
   
    # st.text('Cohort Analysis')
    header('Cohort Analysis', 28)

    with st.container(height=600):
        # st.text('Customer Retention by City')
        st.markdown(f'**Customer Retention by City**', help = 'definition')
        customer_cohort_retention_2a = customer_cohort_retention_2a.sort_values(by='month_0_count', ascending=False).reset_index(drop=True)
        st.dataframe(customer_cohort_retention_2a)
        
    with st.container(height=600):
        # st.text('Customer Percentage Retention by City')
        st.markdown(f'**Customer Percentage Retention by City**', help = 'definition')  

    with st.container(height=600):
        # st.text('Channel-wise Cohorts')  
        st.markdown(f'**Channel-wise Cohorts**', help = 'definition')
    
    with st.container(height=600):
        # st.text('Channel-wise Cohorts - Customer count')
        st.markdown(f'**Channel-wise Cohorts - Customer count**', help = 'definition')

with tab8:
    
    # st.text('Audience Overview')
    header('Audience Overview', 28)

    with st.container(height=600):
        # st.text('Audience Split by Recency Buckets - 0-7,7-15,15-30,30-90, 90-180, >180 days')   
        st.markdown(f'**Audience Split by Recency Buckets - 0-7,7-15,15-30,30-90, 90-180, >180 days**', help = 'definition')
        # RecencyBucket_rev
        pie_chart(RecencyBucket_rev, 'RecencyBucket')
        
    with st.container(height=620):
        # st.text('Audience Split by Frequency Buckets - 0, 1, 2, 3, 4, 4+')
        st.markdown(f'**Audience Split by Frequency Buckets - 0, 1, 2, 3, 4, 4+**', help = 'definition')
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
        st.markdown(f'**Audience Split by 4 AOV quartiles**', help = 'definition')
        pie_chart(AOVquart,'quartile')