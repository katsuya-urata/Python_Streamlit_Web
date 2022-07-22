#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as  st #Webアプリ作成の為
import pandas as pd
import io

st.title('Pythonアプリケーション')
st.caption('これはPythonプログラムで作成されたWebアプリです')


# In[5]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#xlsxデータの処理用
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
name_xlsx = st.text('洋日配サマリー表集約処理_xlsx')
#uploaded_files_xlsx = st.file_uploader('ファイルアップロード', type='xlsx')
uploaded_files_xlsx = st.file_uploader('ファイルアップロード')

submit_btn_xlsx = st.button('xlsx処理実行')
#ボタンが押されたら処理を実行する
if submit_btn_xlsx:
    _df_xlsx = pd.read_excel(uploaded_files_xlsx)
    _df_xlsx


# In[ ]:




