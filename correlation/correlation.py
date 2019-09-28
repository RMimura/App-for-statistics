## 相関を求める

# Guiアプリの作成
import tkinter as tk
from tkinter import messagebox as mbox

import pandas as pd
import numpy as np

# 相関係数の計算
from scipy.stats import pearsonr

# ウィンドウを作成
win = tk.Tk()
# サイズを指定
win.geometry("500x250")
win.title("Correlation")

# 部品を作成
# ラベルを作成
label = tk.Label(win, text='データファイルの名前')
label.pack()

# テキストボックスを作成
data_file = tk.Entry(win)
data_file.pack()
data_file.insert(tk.END, '.csv') # 初期値を指定

# OKボタンを押した時
def ok_click():
    # テキストボックスの内容を得る
    datafile_name = data_file.get()
    # ダイアログを表示
    mbox.showinfo('データファイル', datafile_name + 'を取得しました！')
    
    #------------------相関を求め、無相関検定を行う--------------------------
    dat=pd.read_csv(datafile_name,encoding="SHIFT-JIS")
    # naを含む行を削除
    dat=dat.dropna()
    
    # 数字か否か判定する関数
    def is_num(s):
        s=str(s)
        return s.replace(',', '').replace('.', '').replace('-', '').isnumeric()
    
    not_num=len(dat.columns)*len(dat)
    not_num_col=[]
    for row in range(0,len(dat)):
        for col in range(0,len(dat.columns)):
            if is_num(dat.iloc[row,col]):
                not_num -= 1
            else:
                if (not dat.columns[col] in not_num_col):
                    not_num_col.append(dat.columns[col])
    print(str(not_num)+" 個の数字でないセルがあったため、それを含む以下の列を削除しました。")
    print(not_num_col)
    
    # 数字でない列を削除
    dat=dat.drop(columns=not_num_col,axis=1)
    
    # 相関の結果ファイルの作成
    matA=np.zeros([len(dat.columns),len(dat.columns)])
    matA[:,:]=np.nan
    matA=pd.DataFrame(matA,columns=[dat.columns],index=[dat.columns])
    # 無相関検定の結果ファイルの作成
    matB=np.zeros([len(dat.columns),len(dat.columns)])
    matB[:,:]=np.nan
    matB=pd.DataFrame(matB,columns=[dat.columns],index=[dat.columns])
    
    # 結果の書き込み
    for i in range(0,len(dat.columns)):
        for j in range(0,len(dat.columns)):
            a, b = pearsonr(np.ravel(dat.iloc[:,i]), np.ravel(dat.iloc[:,j]))
            if b < 0.01:
                result= str(round(a,2))+"**"
            elif b < 0.05:
                result= str(round(a,2))+"*"
            else:
                result= str(round(a,2))
            matA.iloc[i,j]=result
            matB.iloc[i,j]=round(b,2)
    
    # 右上にだけ数字が残るように加工
    for i in range(0,len(dat.columns)):
        for j in range(i,len(dat.columns)):
            matA.iloc[j,i]=""
            matB.iloc[j,i]=""
    
    # 相関の結果を出す。
    matA.to_csv("corr_result.csv")
    
    # 無相関検定の結果を出す。欲しければ井桁を削除してください。上記の"corr_result.csv"にも*の形で記載はされています。
    matB.to_csv("corr_test_result.csv")
    print("完了しました")


# ボタンを作成
okButton = tk.Button(win, text='OK', command=ok_click)
okButton.pack(fill = 'x', padx=100)

# ウィンドウを動かす
win.mainloop()