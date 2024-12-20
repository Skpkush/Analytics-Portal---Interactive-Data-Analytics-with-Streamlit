# Create an Interactive Data Analytics Portal with Streamlit in 7 Steps

# import libraries
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Analytics Portal',
    page_icon='📊'
)

# Title and Introduction
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':gray[Explore Data with Ease.]', divider='rainbow')

# File Upload
file = st.file_uploader('Drop a CSV or Excel file', type=['csv', 'xlsx'])
if file is not None:
    try:
        if file.name.endswith('csv'):
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)

        st.dataframe(data)
        st.info('File has been successfully uploaded!', icon='🚨')

        st.subheader(':rainbow[Basic Information of the Dataset]', divider='rainbow')

        # Display basic info and summaries
        tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])

        with tab1:
            st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
            st.subheader(':gray[Statistical Summary of the Dataset]')
            st.dataframe(data.describe())
        
        with tab2:
            st.subheader(':gray[Top Rows]')
            toprows = st.slider('Number of rows to preview', 1, 100, 5)
            st.dataframe(data.head(toprows))
            st.subheader(':gray[Bottom Rows]')
            bottomrows = st.slider('Number of rows to preview', 1, 100, 5)
            st.dataframe(data.tail(bottomrows))
        
        with tab3:
            st.subheader(':grey[Data Types of Columns]')
            st.dataframe(data.dtypes)
        
        with tab4:
            st.subheader('Column Names in Dataset')
            st.write(list(data.columns))

        st.subheader(':rainbow[Column Values To Count]', divider='rainbow')

        # Value Count Feature
        with st.expander('Count and Visualize Column Values'):
            col1, col2 = st.columns(2)
            with col1:
                column = st.selectbox('Choose a Column to Analyze', options=list(data.columns))
            with col2:
                toprows = st.number_input('Top Rows to Display', min_value=1, step=1, value=10)

            count = st.button('Count Values')
            if count:
                result = data[column].value_counts().reset_index().head(toprows)
                st.dataframe(result)
                
                st.subheader('Visualization', divider='gray')

                # Create Interactive Plots
                fig = px.bar(result, x='index', y=column, text=column, template='plotly_white')
                st.plotly_chart(fig)

                fig = px.line(result, x='index', y=column, text=column, template='plotly_white')
                st.plotly_chart(fig)

                fig = px.pie(result, names='index', values=column)
                st.plotly_chart(fig)

        st.subheader(':rainbow[GroupBy: Simplify Your Data Analysis]', divider='rainbow')
        st.write('The GroupBy feature lets you summarize data based on categories.')
        
        # GroupBy and Aggregation Operations
        with st.expander('Group By Columns'):
            col1, col2, col3 = st.columns(3)
            with col1:
                groupby_cols = st.multiselect('Select Columns to GroupBy', options=list(data.columns))
            with col2:
                operation_col = st.selectbox('Choose Column for Operation', options=list(data.columns))
            with col3:
                operations = st.multiselect('Choose Operations', options=['sum', 'mean', 'min', 'max', 'count'])

            if groupby_cols:
                result = data.groupby(groupby_cols).agg({operation_col: operations}).reset_index()
                st.dataframe(result)

                st.subheader(':gray[Data Visualization]', divider='gray')

                # Select Chart Type
                chart_type = st.selectbox('Choose Chart Type', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
                
                if chart_type == 'line':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    fig = px.line(result, x=x_axis, y=y_axis, color=color, markers='o')
                    st.plotly_chart(fig)
                elif chart_type == 'bar':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                    fig = px.bar(result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                    st.plotly_chart(fig)
                elif chart_type == 'scatter':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    size = st.selectbox('Size Column', options=[None] + list(result.columns))
                    fig = px.scatter(result, x=x_axis, y=y_axis, color=color, size=size)
                    st.plotly_chart(fig)
                elif chart_type == 'pie':
                    values = st.selectbox('Choose Numerical Values', options=list(result.columns))
                    names = st.selectbox('Choose Labels', options=list(result.columns))
                    fig = px.pie(result, values=values, names=names)
                    st.plotly_chart(fig)
                elif chart_type == 'sunburst':
                    path = st.multiselect('Choose Path', options=list(result.columns))
                    fig = px.sunburst(result, path=path, values=operation_col)
                    st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error loading file: {e}")

