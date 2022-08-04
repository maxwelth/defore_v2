import stacking_utils as utils
import stacking_main as mains

from datetime import date
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objs as go

val_dates = pd.read_csv("C:/Users/max/anaconda3/envs/myenv/Defore_v2/data/validation_dates.csv")['val_dates']


coll1,coll2 = st.columns([1,1])
coll1.image(Image.open("C:/Users/max/anaconda3/envs/myenv/Defore_v2/sirclo_logo.png"))

st.title("Demand Forecasting Project")

"""
This app is an automated version of SIRCLO Data Intelligence's Demand Forecasting project.
Resources to get started (READ FIRST):
1. [WORKFLOW](https://www.nyan.cat/)
2. [QUERY TO GET SALES DATA](https://dashboard.srcli.xyz/queries/6077/)
FURTHER NOTE:
blank.
"""

uploaded_file = st.file_uploader("Upload data file:")

with st.sidebar.header('Set Parameters'):
    WH = st.sidebar.selectbox(
                 'Name of Warehouse:',
                 ('ALL BSD', 'ALL LEGOK 10K', 'ALL LEGOK B6, A7', 'ALL SURABAYA', 'ALL FF'))
    pred_start = st.sidebar.date_input(
                 "Prediction Date Start")
    pred_end = st.sidebar.date_input(
                 "Prediction Date End")
    important_date = st.radio(
     "Show only important dates (for Prediction)",
     ('Yes', 'No'), horizontal = True)
    run = st.sidebar.button(label='Run Analysis',key=1)
    
if uploaded_file is not None:
    st.text('Upload successful! Click "Run Analysis" and view the result in the "Forecast" tab')
    
    df = utils.load_data(uploaded_file)
    
    tab1, tab2 = st.tabs(["Overview", "Forecast"])
    
    with tab1:
        df_temp = df[df['warehouse_agg']==WH][['ds','warehouse_agg','y']].reset_index(drop=True)
        fig = go.Figure(data=go.Scatter(x=df_temp['ds'], y=df_temp['y'],
                            marker_color='indianred'))
        fig.update_layout(autosize=False,width=750,height=500)
        
        st.subheader('Overall Sales Graph')
        st.subheader(WH)
        st.write('Number of daily sales - Click "View fullscreen" and simply hover your mouse over the chart to view the number of sales')  
        st.plotly_chart(fig)
        
        col1_1, col1_2 = st.columns([3, 1])

        with col1_1:
            st.subheader('Twin Date Sales')
            df_col1 = utils.plot_twin(df_temp)
            df_col1 = df_col1.tail(12)
            fig = go.Figure(go.Bar(y=df_col1['ds'],x=df_col1['y'],orientation='h'))
            fig.update_layout(autosize=False,width=500,height=500,yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig)
            
        with col1_2:
            st.subheader('Data')
            st.write(df_col1.reset_index(drop=True))
            
            
        col2_1, col2_2 = st.columns([3, 1])
        
        with col2_1:
            st.subheader('Payday Sales')
            df_col2 = utils.plot_payday(df_temp)
            df_col2 = df_col2.tail(12)
            fig = go.Figure(go.Bar(y=df_col2['ds'],x=df_col2['y'],orientation='h'))
            fig.update_layout(autosize=False,width=500,height=500,yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig)
        
        with col2_2:
            st.subheader('Data')
            st.write(df_col2.reset_index(drop=True))
      
    
    with tab2:
    
        if run:
            st.write('Please wait 1-2 minutes')
            result = mains.main(df,WH, pred_start, pred_end, val_dates, important_date)
            st.header(f'Sales prediction result till {pred_end}')
            st.subheader('Plot')
            
            if important_date == 'Yes':
                fig = go.Figure(data=go.Bar(x=result['Date'], y=result['Sales Forecast']))
                fig.update_layout(autosize=False,width=750,height=500)
            elif important_date == 'No':
                fig = go.Figure(data=go.Scatter(x=result['Date'], y=result['Sales Forecast'], marker_color='indianred'))
                fig.update_layout(autosize=False,width=750,height=500)
            st.plotly_chart(fig)
            
            st.subheader('Prediction')
            st.write(result)
        
else:
    '''
    No sales data uploaded, please upload and run.
    '''
