#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as  st
import pandas as pd
import io
import xlsxwriter
import openpyxl


# In[4]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#xlsxデータの処理用
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
name_xlsx = st.text('洋日配サマリー表集約処理_xlsx')
uploaded_files_xlsx = st.file_uploader('ファイルアップロード', type='xlsx')

submit_btn_xlsx = st.button('xlsx処理実行')
#ボタンが押されたら処理を実行する
if submit_btn_xlsx:
    _df_xlsx = pd.read_excel(uploaded_files_xlsx)
    st.datafreme(_df_xlsx)
    
    #エクセルでの書き出しはかなり特殊なようでこのような対応が必要
    xlsx_dl = io.BytesIO()
    
    with pd.ExcelWriter(xlsx_dl, engine='xlsxwriter') as writer:
        _df_xlsx.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        #出力するデータが表示されたら、ダウンロードボタンが出てくる
        st.download_button(label='エクセルダウンロード', data=xlsx_dl, file_name='洋日配サマリ集計後.xlsx', mime='application/vnd.ms-excel')


# In[6]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#CSVデータの処理用
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
name_csv = st.text('洋日配サマリー表集約処理_CSV')
uploaded_files_csv = st.file_uploader('ファイルアップロード', type='csv')
submit_btn_csv = st.button('CSV処理実行')
#ボタンが押されたら処理を実行する
if submit_btn_csv:
    _df_csv = pd.read_csv(uploaded_files_csv, encoding='shift-jis')
    st.dataframe(_df_csv)
    
    #出力するデータが表示されたら、ダウンロードボタンが出てくる
    csv_dl = _df_csv.to_csv()
    st.download_button(label='ＣＳＶダウンロード', data=csv_dl, file_name='洋日配サマリ集計後.csv')


# In[ ]:




