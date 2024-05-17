#!/usr/bin/env python

from os import path, listdir
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd

def drawfunc(result_s, result_m, sweepNum):   #散点图
    indexs = list(range(1, sweepNum + 1))  # 生成索引序列
    result_s_abs = [abs(val) for val in result_s]  # 将result_s中的值转换为正数
    result_m_abs = [abs(val) for val in result_m]  # 将result_s中的值转换为正数
    fig, axes = plt.subplots(1, 1, figsize=(5, 4))
    axes.tick_params(axis='x', labelsize=15)
    axes.tick_params(axis='y', labelsize=15)
    plt.scatter(indexs, result_s_abs, color='red',s=13, label='Result_s')  # 绘制第一组数据，红色
    plt.scatter(indexs, result_m_abs, color='black',s=13, label='Result_m')  # 绘制第二组数据，蓝色
    plt.legend()  # 添加图例
    plt.show()
    
class Mt2csv:
    def __init__(self):
        self.df = None
        self.simulator = ""
        self.title = ""

    def yield_tokens(self, f):
        for line in f:
            for tok in line.split():
                yield tok

    def read_header(self, tokens):
        """
        tokens: iterator that yields tokens. (Must not be a list!)
        """
        header = []
        for tok in tokens:
            header.append(tok)
            if tok.find('#') >= 0:
                break
        return header

    def yield_rows(self, tokens, header_len):
        # If you have .alter in spice, you get multiple measurements.
        # In other words, you get multiple rows.
        # optimize.mt0 is an example of this case.
        row = []
        for tok in tokens:
            row.append(float(tok))
            if len(row) >= header_len:
                yield row
                row = []
        assert len(row) == 0, "Left-over data detected"

    def parse_tokens(self, f):
        """
        Updates self.data.
        f: stream object
        """
        tokens = self.yield_tokens(f)
        header = self.read_header(tokens)
        df = pd.DataFrame(columns=header,
                          data=self.yield_rows(tokens, len(header)))
        return df

    def read(self, fname):
        with open(fname) as f:
            self.simulator = f.readline().strip()
            self.title = f.readline().strip()
            self.df = self.parse_tokens(f)

    def to_csv(self, f):
        """
        f: stream, str, path object or anything that works with df.to_csv()
        """
        #print(self.simulator)
        #print(self.title)
        self.df.to_csv(f)


def readalldata(directory):
    index=list()
    for filename in listdir(directory):
        full_path = path.join(directory, filename)
        mt2csv = Mt2csv()
        mt2csv.read(full_path)
        power1=mt2csv.df.loc[: , "pwr_latch1"]
        index.append(power1.values)
    index_ar=np.array(index)
    #drawfunc_p(index_ar)
    return index_ar

def drawfunc_p(index_ar):
    index=[1,2,3,4,5,6,7,8]
    plt.plot(index,index_ar)
    plt.show()

def drawfunc_m(merged_data):  #多组折现图，数据自行添加
    index=[1,2,3,4,5,6,7,8]
    plt.plot(index, merged_data[:,0],color='green',marker='^',markeredgecolor='green',markersize='10',label='Index_ar1')
    plt.plot(index, merged_data[:,1],color='red',marker='^',markeredgecolor='red',markersize='10 ',label='Index_ar2')
    plt.xlabel('Index')#横轴
    plt.ylabel('Value')#纵轴
    plt.title('Line Plot of Merged Data')#标题
    plt.legend()
    plt.show()
    
###
### main
###
if __name__ == "__main__":
    index_ar1=readalldata(r"C:\Users\zcj\Desktop\pvt\mt")#mt文件所在文件目录，文件夹中只能包含mt文件
    index_ar2=readalldata(r"C:\Users\zcj\Desktop\pvt\mt1")
    merged_data = np.column_stack((index_ar1, index_ar2))
    print(merged_data)
    drawfunc_m(merged_data)
    pd.DataFrame(merged_data).to_csv('sample.csv')#输出excel文件
