import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np
import datetime
from plotly.subplots import make_subplots

# Bar and line chart in one
def default_chart(chart_title,chart_key,chart_df,chart_height=630, radio_horizontal=True, color_theme='streamlit'):
    with st.container(height=chart_height):
        # st.subheader(chart_title)
        st.markdown(f'**{chart_title}**')
        col_1, col_2 = st.columns([4,1])
        with col_2:
            chart_type = st.radio(
                "",
                ["Line Chart", "Bar Chart"], horizontal=radio_horizontal, key=chart_key)

        if chart_type == 'Line Chart':
            fig = px.line(data_frame=chart_df) # chart_df=df.groupby('Purchase Date')['Net Sales'].sum()
        else:
            fig = px.bar(data_frame=chart_df)

        fig.update(layout_showlegend=False)
        # fig.update_traces(line=dict(color="Yellow", width=0.4))

        st.plotly_chart(fig, theme=color_theme, use_container_width=True)

# Twin axis charts
def twin_axis_chart():
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    y1 = [10, 20, 15, 25, 30]  # Line plot data
    y2 = [50, 40, 35, 30, 25]  # Bar plot data

    # Create traces
    fig = go.Figure()

    # Line plot
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Line Plot'))

    # Bar plot
    fig.add_trace(go.Bar(x=x, y=y2, name='Bar Plot', yaxis='y2'))

    # Create layout with y-axis and y-axis2
    fig.update_layout(
        title='Twin Axis Chart',
        yaxis=dict(title='Line Plot'),
        yaxis2=dict(title='Bar Plot', overlaying='y', side='right')
    )

    # Show the figure
    fig.show()

# def horizontal_bar_chart(): 
#     df=px.data.tips()
#     fig=px.bar(df,x='total_bill',y='day', orientation='h')
#     st.write(fig)

def horizontal_bar_chart_with_value(data, col_1):
    if 'Total_Price' not in data.columns:
        data['Total_Price'] = data['ItemQuantity'] * data['Item_UnitPrice']
    data_1=data.groupby(col_1)['Total_Price'].sum().to_frame()
    data = data_1.sort_values(by='Total_Price', ascending=False).head(10)
    data = data.reset_index()

    # Altair chart with horizontal bars and totals
    chart = alt.Chart(data).mark_bar().encode(
        x='Total_Price:Q',
        # y='ItemName:N',
        y=alt.Y(f'{col_1}:N', sort=alt.EncodingSortField(field='Total_Price', op='sum', order='descending')),
        tooltip=[f'{col_1}:N', 'Total_Price:Q']
    )

    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Offset for text placement to the right of bars
    ).encode(
        text='Total_Price:Q'
    )

    chart_with_text = (chart + text).properties(
        height=alt.Step(50)  # Adjust the height of the bars
    )

    # Streamlit display
    st.altair_chart(chart_with_text, use_container_width=True)

def trend_comparison_line_chart(df,df_delta,date_col, col_1 ,x_axis_title, y_axis_title,trend_1, trend_2, key, cumulative_sum=False, unique_count=False, new_customer=False):
    granularity_dict = {'Daily': 'D','Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}
    _,_,_,col = st.columns(4)
    with col:
        gran = st.selectbox('Granularity', ('Daily', 'Weekly', 'Monthly', 'Yearly'), key=key)

    if df.index.name != date_col and df_delta.index.name != date_col:
        df.set_index(date_col, inplace=True)
        df_delta.set_index(date_col, inplace=True)
    if new_customer:
        df= df[df.index == df['FirstOrderDate']][col_1]
        df_delta= df_delta[df_delta.index == df_delta['FirstOrderDate']][col_1]
        df = df.to_frame()
        df_delta = df_delta.to_frame()
    if unique_count:
        df = df.groupby(date_col)[col_1].nunique().to_frame()
        df_delta = df_delta.groupby(date_col)[col_1].nunique().to_frame()
    df = df[[col_1]].resample(granularity_dict[gran]).sum()
    df_delta = df_delta[[col_1]].resample(granularity_dict[gran]).sum()
    if cumulative_sum:
        df['Cumulative_Value'] = df[col_1].cumsum()
        df_delta['Cumulative_Value'] = df_delta[col_1].cumsum()
        col_1 = 'Cumulative_Value'
    time_frame = df.index.to_list() # change timeframe
    trend1_values = df[col_1].to_list()
    trend2_values = df_delta[col_1].to_list()

    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=trend1_values, mode='lines+markers', name=f'{trend_1}_{gran}')
    trace2 = go.Scatter(x=time_frame, y=trend2_values, mode='lines+markers', name=f'{trend_2}_{gran}')

    # Create layout
    layout = go.Layout(
        # title='Trend Comparison Chart',
        xaxis=dict(title=x_axis_title),
        yaxis=dict(title=y_axis_title),
    )

    # Create figure
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Show the figure
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)

def trend_comparison_line_chart_aov(df,df_delta,date_col, col_1 ,col_2,x_axis_title, y_axis_title,trend_1, trend_2, key, cumulative_sum=False, unique_count=False):
    df2=df
    df2_delta = df_delta
    granularity_dict = {'Daily': 'D','Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}
    _,_,_,col = st.columns(4)
    with col:
        gran = st.selectbox('Granularity', ('Monthly', 'Yearly'), key=key)
    if df.index.name != date_col and df_delta.index.name != date_col:
        df.set_index(date_col, inplace=True)
        df_delta.set_index(date_col, inplace=True)

    df = df[[col_1]].resample(granularity_dict[gran]).sum()
    df_delta = df_delta[[col_1]].resample(granularity_dict[gran]).sum()

    time_frame = df.index.to_list() # change timeframe
    trend1_values = df[col_1].to_list()
    trend2_values = df_delta[col_1].to_list()

    if df2.index.name != date_col and df2_delta.index.name != date_col:
        df2.set_index(date_col, inplace=True)
        df2_delta.set_index(date_col, inplace=True)
    if unique_count:
        df2 = df2.groupby(date_col)[col_2].nunique().to_frame()
        df2_delta = df2_delta.groupby(date_col)[col_2].nunique().to_frame()
    df2 = df2[[col_2]].resample(granularity_dict[gran]).sum()
    df2_delta = df2_delta[[col_2]].resample(granularity_dict[gran]).sum()

    # time_frame = df2.index.to_list() # change timeframe
    trend1_values2 = df2[col_2].to_list()
    trend2_values2 = df2_delta[col_2].to_list()
    
    y1 = [a / b for a, b in zip(trend1_values, trend1_values2)]
    y2 = [a / b for a, b in zip(trend2_values, trend2_values2)]
    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=y1, mode='lines+markers', name=f'{trend_1}_{gran}')
    trace2 = go.Scatter(x=time_frame, y=y2, mode='lines+markers', name=f'{trend_2}_{gran}')

    # Create layout
    layout = go.Layout(
        # title='Trend Comparison Chart',
        xaxis=dict(title=x_axis_title),
        yaxis=dict(title=y_axis_title),
    )

    # Create figure
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Show the figure
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)

def grouped_bar_chart():
    np.random.seed(42)

    random_x= np.random.randint(1,101,100) 
    random_y= np.random.randint(1,101,100)

    x = ['A', 'B', 'C', 'D']

    plot = go.Figure(data=[go.Bar(
        name = 'Data 1',
        x = x,
        y = [100, 200, 500, 673],
    ),
        go.Bar(
        name = 'Data 2',
        x = x,
        y = [56, 123, 982, 213],
    )
    ])


def grouped_bar_chart_with_line_chart_2(data):
    Ecom_Ordertable = data
    Ecom_Ordertable.reset_index(inplace=True)
    Ecom_Ordertable['Order_interval'] = (pd.to_datetime(Ecom_Ordertable['OrderDate']) - pd.to_datetime(Ecom_Ordertable['FirstOrderDate'])).dt.days

    Ecom_Ordertable['Month'] = pd.to_datetime(Ecom_Ordertable['OrderDate']).dt.strftime('%Y-%m')

    Ecom_Ordertable['CV_1'] = np.where(Ecom_Ordertable['Order_interval'] < 2, Ecom_Ordertable['Total_Price'], 0)
    Ecom_Ordertable['CV_30'] = np.where(Ecom_Ordertable['Order_interval'] < 31, Ecom_Ordertable['Total_Price'], 0)
    Ecom_Ordertable['CV_60'] = np.where(Ecom_Ordertable['Order_interval'] < 61, Ecom_Ordertable['Total_Price'], 0)
    Ecom_Ordertable['CV_90'] = np.where(Ecom_Ordertable['Order_interval'] < 91, Ecom_Ordertable['Total_Price'], 0)
    Ecom_Ordertable['CV_180'] = np.where(Ecom_Ordertable['Order_interval'] < 181, Ecom_Ordertable['Total_Price'], 0)
    plot = px.bar(Ecom_Ordertable.groupby(['Month'])[['CV_1',
       'CV_30', 'CV_60', 'CV_90', 'CV_180']].mean(),
       barmode='group'
      )

    st.plotly_chart(plot, use_container_width=True)

def bar_chart_with_line_chart(data, var):
    data['total'] = data['CV_90'] * data['customer_count']
    data = data.groupby(var)[['total','customer_count']].sum().reset_index()
    data['CV90'] = data['total']/data['customer_count']
    if data.shape[0] > 10:
        data_sorted = data.sort_values(by='CV90', ascending=True).reset_index()
        data_sorted = data_sorted.head(10)
    else:data_sorted = data.sort_values(by='CV90', ascending=True).reset_index()
    x = data_sorted[var]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for each y-axis
    fig.add_trace(go.Bar(x=x, y=data_sorted['CV90'], name='Y1'), secondary_y=False)
    fig.add_trace(go.Line(x=x, y=data_sorted['customer_count'], name='Y2'), secondary_y=True)

    # Update layout with axis labels
    fig.update_layout(
        xaxis=dict(title='X-axis'),
        yaxis=dict(title='Y1-axis', side='left'),
        yaxis2=dict(title='Y2-axis', side='right')
    )

    # plot = go.Figure(data=[go.Bar(
    #     name = 'CV90',
    #     x = x,
    #     y = data['CV90'].to_list(),
    # ),
    #     go.Line(
    #     name= 'CustomerID',
    #     x=x,
    #     y=data['customer_count'].to_list(),
    # )
    # ])
                    
    st.plotly_chart(fig, use_container_width=True)


def horizontal_grouped_bar_chart():
    np.random.seed(42)

    random_x= np.random.randint(1,101,100) 
    random_y= np.random.randint(1,101,100)

    x = ['A', 'B', 'C', 'D']

    plot = go.Figure(data=[go.Bar(
        name = 'Data 1',
        x = [100, 200, 500, 673],
        y = x,
        orientation='h'
    ),
        go.Bar(
        name = 'Data 2',
        x = [56, 123, 982, 213],
        y = x,
        orientation='h'
    )
    ])
                    
    st.plotly_chart(plot, use_container_width=True)

def horizontal_grouped_bar_chart_channel(data):
    # x = ['A', 'B', 'C', 'D']

    data_cv1 = data[data.index-data['FirstOrderDate']<datetime.timedelta(days=2)]
    data_price_cv1 = data_cv1[['Total_Price', 'marketing_channel']].groupby('marketing_channel').sum()
    data_count_cv1 = data_cv1[['CustomerID', 'marketing_channel']].groupby('marketing_channel').nunique()
    x = data_price_cv1.index.to_list()

    data_cv30 = data[data.index-data['FirstOrderDate']<datetime.timedelta(days=31)]
    data_price_cv30 = data_cv30[['Total_Price', 'marketing_channel']].groupby('marketing_channel').sum()
    data_count_cv30 = data_cv30[['CustomerID', 'marketing_channel']].groupby('marketing_channel').nunique()

    data_cv60 = data[data.index-data['FirstOrderDate']<datetime.timedelta(days=61)]
    data_price_cv60 = data_cv60[['Total_Price', 'marketing_channel']].groupby('marketing_channel').sum()
    data_count_cv60 = data_cv60[['CustomerID', 'marketing_channel']].groupby('marketing_channel').nunique()

    data_cv90 = data[data.index-data['FirstOrderDate']<datetime.timedelta(days=91)]
    data_price_cv90 = data_cv90[['Total_Price', 'marketing_channel']].groupby('marketing_channel').sum()
    data_count_cv90 = data_cv90[['CustomerID', 'marketing_channel']].groupby('marketing_channel').nunique()

    data_cv180 = data[data.index-data['FirstOrderDate']<datetime.timedelta(days=181)]
    data_price_cv180 = data_cv180[['Total_Price', 'marketing_channel']].groupby('marketing_channel').sum()
    data_count_cv180 = data_cv180[['CustomerID', 'marketing_channel']].groupby('marketing_channel').nunique()
    
    plot = go.Figure(data=[go.Bar(
        name = 'CV1',
        x = [a/b for a,b in zip(data_price_cv1['Total_Price'].to_list(),data_count_cv1['CustomerID'].to_list())],
        y = x,
        orientation='h'
    ),
        go.Bar(
        name = 'CV30',
        x = [a/b for a,b in zip(data_price_cv30['Total_Price'].to_list(),data_count_cv30['CustomerID'].to_list())],
        y = x,
        orientation='h'
    ),
        go.Bar(
        name = 'CV60',
        x = [a/b for a,b in zip(data_price_cv60['Total_Price'].to_list(),data_count_cv60['CustomerID'].to_list())],
        y = x,
        orientation='h'
    ),
        go.Bar(
        name = 'CV90',
        x = [a/b for a,b in zip(data_price_cv90['Total_Price'].to_list(),data_count_cv90['CustomerID'].to_list())],
        y = x,
        orientation='h'
    ),
        go.Bar(
        name = 'CV180',
        x = [a/b for a,b in zip(data_price_cv180['Total_Price'].to_list(),data_count_cv180['CustomerID'].to_list())],
        y = x,
        orientation='h'
    ),
    ])
                    
    st.plotly_chart(plot, use_container_width=True)    

def pie_chart(df, var):
    cat_pie = px.pie(data_frame=df.groupby(var)['CustomerID'].nunique().to_frame().reset_index(),
                    # names='Product Category',
                    hole=0.5,
                    color=var,
                    values='CustomerID'
                )
    st.plotly_chart(cat_pie, theme='streamlit', use_container_width=True)