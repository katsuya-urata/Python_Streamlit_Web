#!/usr/bin/env python
# coding: utf-8

# In[108]:


import streamlit as  st
import pandas as pd
import io
import xlsxwriter
import openpyxl
import datetime
import zipfile
import traceback
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


# In[93]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#日配共配サマリー　取引先別分解
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
st.text('【日配共配サマリー　取引先別分解】')
st.text('日配共配のエクセルで作られたサマリを取引先別のエクセルシートに分解します！')

uploaded_files_nasama = st.file_uploader('ファイルアップロード（日配共配サマリー　取引先別分解）', type='xlsx')
submit_btn_xlsx_nasama = st.button('xlsx処理実行（日配共配サマリー　取引先別分解）')

#ボタンが押されたら処理を実行する
if submit_btn_xlsx_nasama:
    if uploaded_files_nasama == None:
        st.text('ファイルが選択されていません!')
    else:
        #エラー処理を実施
        try:
                #読み込んだエクセルのシート名を取得
            sheet_names = pd.ExcelFile(uploaded_files_nasama).sheet_names
            _df = pd.DataFrame()
            #読み込んだエクセルのBOOKのシートを全て結合していく
            for sheet_name_i in sheet_names:
                _df_l = pd.read_excel(uploaded_files_nasama, sheet_name=sheet_name_i, skiprows=3)
                _df = pd.concat([_df,_df_l])

            #読み込んだデータを整形する
            _df = _df.dropna(subset=['ＪＤ\u3000\u3000   原価'])
            _df = _df[_df['ＪＡＮ'] != 'ＪＡＮ']

            #取引先名のユニークを取得する
            torimei = _df['取引先'].unique()
            torisyousai = _df.groupby(['取引先']).size()

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
                st.download_button(label='エクセルダウンロード（日配共配サマリー　取引先別分解）', data=xlsx_dl, file_name=tori + '_洋日配サマリ.xlsx', mime='application/vnd.ms-excel')

                st.info('処理が完了しました')

        except Exception as ee:
            terr = list(traceback.TracebackException.from_exception(ee).format())
            st.text(terr)
            st.error('エラーが発生しましたので、上記エラー内容を確認してください')


# In[117]:


#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
#まいづるパスコ特売単価分解
#◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
st.text('【まいづるのパスコの特売単価を分解】')

uploaded_files_mpasuko = st.file_uploader('ファイルアップロード（まいづるパスコ特売単価）', type='xlsx')
submit_btn_xlsx_mpasuko = st.button('xlsx処理実行（まいづるパスコ特売単価）')

#ボタンが押されたら処理を実行する
if submit_btn_xlsx_nasama:
    if uploaded_files_nasama == None:
        st.text('ファイルが選択されていません!')
    else:
        #エラー処理を実施
        try:
            #データを読み込む
            _df = pd.read_excel(uploaded_files_mpasuko,skiprows=2)
            #データを整形していく
            df = _df[["ＪＡＮコード","仕入\n新本体.1","まいづる","参考売価","備考"]]#_dfより必要な項目のみを抜粋
            df = df[df["まいづる"] != 0] #数値が0以外のデータのみ抜粋
            df = df.dropna(how='all', axis=0) #すべての行が欠損値のデータを削除する
            df=df.rename(columns={"仕入\n新本体.1": '仕入単価',"まいづる":"まいづる納価単価"})#columnsの名称を変更
            df["ＪＡＮコード"] = df["ＪＡＮコード"].astype('object')
            df["ＪＡＮコード"].map('{:014}'.format)

            df["開始日"] = ""#特売マスタ登録に必要な項目を追加
            df["終了日"] = ""#特売マスタ登録に必要な項目を追加
            today = datetime.today()#今日の日付を取得
            #エクセルでの書き出しはかなり特殊なようでこのような対応が必要
            xlsx_dl_mpasuko = io.BytesIO()
            ############
            #データの集計
            ############
            for index,data in df.iterrows():#iterrowsは１行ずつ処理をするらしい
                if "月特別月間" in data["備考"]: #月間特売の日付は何とか取得できたかな
                    df.loc[index,"開始日"] = format(today + relativedelta(months=+1, day=1),'%Y%m%d')
                    df.loc[index,"終了日"] = format(today + relativedelta(months=+2, day=1,days=-1),'%Y%m%d')
                
                elif "\n" in data["備考"]:#改行が発生した場合の処理は日付違いの別レコードを作成する
                    for kai_count in range(len(df.loc[index,"備考"].splitlines())):#Listに入っている改行文字の回数分LOOP回す
                        if kai_count == 0:
                            #初回は現行のデータに日付セットsplitlines()文字列を改行コードで分割したい時に利用します
                            df.loc[index,"開始日"] = format(pd.to_datetime(format(today + relativedelta(months=+1, day=1),"%Y") + "年" + df.loc[index,"備考"].splitlines()[kai_count], format="%Y年%m月%d日"),"%Y%m%d")
                            df.loc[index,"終了日"] = format(pd.to_datetime(format(today + relativedelta(months=+1, day=1),"%Y") + "年" + df.loc[index,"備考"].splitlines()[kai_count], format="%Y年%m月%d日"),"%Y%m%d")
                        else:#レコードを新たに作成して日付をセットしていく（日付以外の項目は同一の情報（JAN、仕入単価、まいづる納価、参考売価を持ってきて、開始日、終了日は改行後のデータをセット
                            df = df.append(pd.DataFrame([{
                            "ＪＡＮコード":df.loc[index,"ＪＡＮコード"],
                            "仕入単価":df.loc[index,"仕入単価"],
                            "まいづる納価単価":df.loc[index,"まいづる納価単価"],
                            "参考売価":df.loc[index,"参考売価"],
                            "開始日":format(pd.to_datetime(format(today + relativedelta(months=+1, day=1),"%Y") + "年" + df.loc[index,"備考"].splitlines()[kai_count], format="%Y年%m月%d日"),"%Y%m%d"),
                            "終了日":format(pd.to_datetime(format(today + relativedelta(months=+1, day=1),"%Y") + "年" + df.loc[index,"備考"].splitlines()[kai_count], format="%Y年%m月%d日"),"%Y%m%d") 
                            }]))
                elif "～" in data["備考"]:#備考欄の日付で～と入っていた場合
                    dateStr = data["備考"]
                    itr = re.finditer(r"(1[0-2]|0?[1-9])[/\-月](3[01]|[12][0-9]|0?[1-9])日?", dateStr)#正規表現を使用し日付を抽出
                    for count,m in enumerate(itr):#データをカウント
                        if count == 0:#０件目だったら開始日にセット＆zfill(2)で０埋め２桁に
                            df.loc[index,"開始日"] = format(today + relativedelta(months=+1, day=1),"%Y") + m.groups()[0].zfill(2) + m.groups()[1].zfill(2)
                        else:#０件目でなかったら終了日にセット＆zfill(2)で０埋め２桁に
                            df.loc[index,"終了日"] = format(today + relativedelta(months=+1, day=1),"%Y") + m.groups()[0].zfill(2) + m.groups()[1].zfill(2)


            with pd.ExcelWriter(xlsx_dl_mpasuko, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                #出力するデータが表示されたら、ダウンロードボタンが出てくる
                st.download_button(label='エクセルダウンロード（まいづるパスコ特売単価）', data=xlsx_dl_mpasuko, file_name='まいづるパスコ特売単価変換.xlsx', mime='application/vnd.ms-excel')

                st.info('処理が完了しました')

        except Exception as ee:
            terr = list(traceback.TracebackException.from_exception(ee).format())
            st.text(terr)
            st.error('エラーが発生しましたので、上記エラー内容を確認してください')


# In[73]:


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


# In[66]:


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
# list_file = ['test']
            
# for tori in trimei:
#     df = _df[_df['取引先'] == tori]
#     st = tori + 'test.xlsx'
#     list_file.append(st)

# print(list_file)
    


# In[ ]:




