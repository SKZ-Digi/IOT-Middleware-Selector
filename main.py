import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from PIL import Image
import os
import base64
st.set_page_config(page_title="Data Infrastructure Wiki ",layout="wide", page_icon = "favicon.png")
#for image rendering with link, magic from https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url,width="1"):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img style="width: {width}%" src="data:image/{img_format};base64,{bin_str} " />
        </a>'''
    return html_code


#remove colored bar and menu
#header {visibility: hidden;}
#MainMenu {visibility: hidden;} #hides Menu in Style
hide_streamlit_style = """
            <style>           
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#remove colored bar and menu
#header {visibility: hidden;}
#MainMenu {visibility: hidden;} #hides Menu in Style
hide_streamlit_style = """
            <style>           
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#remove padding of widgets
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}4em;
        padding-left: {padding}4em;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)














if 'load_excel' not in st.session_state:
    st.session_state['load_excel'] = False

#if st.session_state.load_excel==False:
df=pd.read_excel("Machine_Data_Database_WIP.xlsx", index_col=None,engine='openpyxl')
    #st.session_state.load_excel=True

#st.write(df.head())

list_categories_money_inital=df.inbudget.unique()
list_categories_money_anual=df.anbudget.unique()
list_categories_workload_initial=df.inworkload.unique()
list_categories_workload_anual=df.anworkload.unique()

#--------------------------------SIDEBAR-----------------------------------------------------------------------
Logo_html = get_img_with_href('Logo.PNG', 'https://www.nweurope.eu/projects/project-search/di-plast-digital-circular-economy-for-the-plastics-industry/',width="90")
st.sidebar.markdown(Logo_html, unsafe_allow_html=True)


#image = Image.open('Logo.png')
#st.sidebar.image(image, width=250)
st.sidebar.title('Data Infrastructure Wiki')

money_initial=st.sidebar.selectbox("Initial Budget",list_categories_money_inital,help="Please select your initial software budget​")
money_anual=st.sidebar.selectbox("Anual Budget",list_categories_money_anual,help="Please select your anual software budget​")
time_initial=st.sidebar.selectbox("Workload initial ",list_categories_workload_initial,help="Please select your initial available workload")
time_anual=st.sidebar.selectbox("Workload anual ",list_categories_workload_anual,help="Please select your anual available workload")






SKZ_Logo_html = get_img_with_href('SKZ-Logo.png', 'https://www.skz.de',width="90")
st.sidebar.markdown(SKZ_Logo_html, unsafe_allow_html=True)

st.sidebar.caption("[Bug reports and suggestions welcome ](mailto:c.kugler@skz.de)")

col1 ,col2,col3= st.columns((5,20,5))

#---------------------------------------SIDEBAR END----------------------------------------------------------------------------------------------------------------------------------
dffilter = df[(df['inbudget'] ==money_initial) & (df['anbudget'] ==money_anual) & (df['inworkload'] ==time_initial)& (df['anworkload'] ==time_anual)]

with col1:
    st.write("")

with col2:
    list_products=dffilter['productname']
    st.header("Product Information", anchor=None)
    products=st.selectbox("Recommended Products",list_products,help="Choose product for information​")
    dfproduct= dffilter[dffilter['productname'] ==products]
    if dfproduct.empty:
        
        st.header("No product available for these categories.")
    else:
        product=dfproduct['description'].iloc[0]
        st.header("Description", anchor=None)
        st.write(product)
        st.subheader("License Model")
        st.write(dfproduct['licensemodel'].iloc[0])
        st.subheader("Link to Product Homepage")
        st.write(dfproduct['link'].iloc[0])

with col3:
    st.write("")
