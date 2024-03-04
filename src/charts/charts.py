import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np

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

def horizontal_bar_chart_with_value():

    # Example data
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        'Value': [10, 20, 15, 25, 45, 18, 34, 107, 58, 60]
    })

    # Calculate the cumulative sum for each category
    data['Cumulative_Sum'] = data['Value'].cumsum()

    # Altair chart with horizontal bars and totals
    chart = alt.Chart(data).mark_bar().encode(
        x='Value:Q',
        y='Category:N',
        tooltip=['Category:N', 'Value:Q']
    )

    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Offset for text placement to the right of bars
    ).encode(
        text='Value:Q'
    )

    chart_with_text = (chart + text).properties(
        height=alt.Step(50)  # Adjust the height of the bars
    )

    # Streamlit display
    st.altair_chart(chart_with_text, use_container_width=True)

def trend_comparison_line_chart(df,df_delta,date_col, col_1 ,x_axis_title, y_axis_title,trend_1, trend_2, granularity='Monthly'):
    granularity_dict = {'Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}
    df.set_index(date_col, inplace=True)
    df_delta.set_index(date_col, inplace=True)
    
    df = df[[col_1]].resample(granularity_dict[granularity]).sum()
    df_delta = df_delta[[col_1]].resample(granularity_dict[granularity]).sum()
    time_frame = df.index.to_list()
    trend1_values = df[col_1].to_list()
    trend2_values = df_delta[col_1].to_list()

    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=trend1_values, mode='lines+markers', name=f'{trend_1}_{granularity}')
    trace2 = go.Scatter(x=time_frame, y=trend2_values, mode='lines+markers', name=f'{trend_2}_{granularity}')

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

def grouped_bar_chart_with_line_chart():
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
    ),
        go.Line(
        name= 'Data_3',
        x=x,
        y=[45,92,84,123],
    )
    ])
                    
    st.plotly_chart(plot, use_container_width=True)

def bar_chart_with_line_chart():
    np.random.seed(42)

    random_x= np.random.randint(1,101,100) 
    random_y= np.random.randint(1,101,100)

    x = ['A', 'B', 'C', 'D']

    plot = go.Figure(data=[go.Bar(
        name = 'Data 1',
        x = x,
        y = [100, 200, 500, 673],
    ),
        go.Line(
        name= 'Data_2',
        x=x,
        y=[45,92,84,123],
    )
    ])
                    
    st.plotly_chart(plot, use_container_width=True)


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

def pie_chart(df):
    cat_pie = px.pie(data_frame=df.groupby(['Country'])['Net Sales'].sum().abs().reset_index(),
                    # names='Product Category',
                    hole=0.5,
                    color='Country',
                    values='Net Sales',
                    title='Country'
                )
    st.plotly_chart(cat_pie, theme='streamlit', use_container_width=True)