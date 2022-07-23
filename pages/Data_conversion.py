#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as  st
import pandas as pd
import io
import xlsxwriter
import openpyxl
import datetime


# In[44]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#日配共配サマリー　取引先別分解
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
st.text('【日配共配サマリー　取引先別分解】')
st.text('日配共配のエクセルで作られたサマリを取引先別のエクセルシートに分解します！')

uploaded_files_xlsx = st.file_uploader('ファイルアップロード', type='xlsx')
submit_btn_xlsx = st.button('xlsx処理実行')

#ボタンが押されたら処理を実行する
if submit_btn_xlsx:
    if uploaded_files_xlsx == None:
        st.text('ファイルが選択されていません!')
    else:
        #エラー処理を実施
        try:
            #読み込んだエクセルのシート名を取得
            sheet_names = pd.ExcelFile(uploaded_files_xlsx).sheet_names
            _df = pd.DataFrame()
            #読み込んだエクセルのBOOKのシートを全て結合していく
            for sheet_name_i in sheet_names:
                _df_l = pd.read_excel(uploaded_files_xlsx, sheet_name=sheet_name_i, skiprows=3)
                _df = pd.concat([_df,_df_l])
            
            #読み込んだデータを整形する
            _df = _df.dropna(subset=['ＪＤ\u3000\u3000   原価'])
            _df = _df[_df['ＪＡＮ'] != 'ＪＡＮ']
            
            #取引先名のユニークを取得する
            torimei = _df['取引先'].unique()
            
            #エクセルでの書き出しはかなり特殊なようでこのような対応が必要
            xlsx_dl = io.BytesIO()

            #取得した取引先名をキーにデータを抽出して、エクスポートしていく
            for tori in torimei:
                df = _df[_df['取引先'] == tori]
                #データを社別に出力していく
                with pd.ExcelWriter(xlsx_dl, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Sheet1')
                    writer.save()
                    #出力するデータが表示されたら、ダウンロードボタンが出てくる
                    st.download_button(label='エクセルダウンロード', data=xlsx_dl, file_name=tori + '_洋日配サマリ集計後.xlsx', mime='application/vnd.ms-excel')
            
        except:
            st.text('エラーが発生しました')
            pass


# In[32]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#CSVデータの処理用
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#name_csv = st.text('洋日配サマリー表集約処理_CSV')
#uploaded_files_csv = st.file_uploader('ファイルアップロード', type='csv')
#submit_btn_csv = st.button('CSV処理実行')
#ボタンが押されたら処理を実行する
#if submit_btn_csv:
#    _df_csv = pd.read_csv(uploaded_files_csv, encoding='shift-jis')
#    st.dataframe(_df_csv)
    
    #出力するデータが表示されたら、ダウンロードボタンが出てくる
#    csv_dl = _df_csv.to_csv()
#    st.download_button(label='ＣＳＶダウンロード', data=csv_dl, file_name='洋日配サマリ集計後.csv')


# In[40]:


# uploaded_files_xlsx = 'C:\\Users\\katsu\\Desktop\\2022_08メーカー洋日配販売計画書1（素案）.xlsx'
# sheet_names = pd.ExcelFile(uploaded_files_xlsx).sheet_names
# _df = pd.DataFrame()
# for sheet_name in sheet_names:
#     _df_l = pd.read_excel(uploaded_files_xlsx, sheet_name=sheet_name, skiprows=3)
#     _df = pd.concat([_df,_df_l])

# _df = _df.dropna(subset=['ＪＤ\u3000\u3000   原価'])
# _df = _df[_df['ＪＡＮ'] != 'ＪＡＮ']

# trimei = _df['取引先'].unique()
            
#             #取得した取引先名をキーにデータを抽出して、エクスポートしていく
#             #エクセルでの書き出しはかなり特殊なようでこのような対応が必要
# xlsx_dl = io.BytesIO()
            
# for tori in trimei:
#     df = _df[_df['取引先'] == tori]


# In[ ]:




