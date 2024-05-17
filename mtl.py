import mt2csv
import numpy as np
from os import path, listdir
import matplotlib.pyplot as plt

def drawfunc_mt(merged_data,i,latch_name):  #多组折现图
    index=[1,2,3,4,5,6,7,8]
    colors = ['green', 'blue', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow']
    for a in range(i):
        plt.plot(index, merged_data[a],color=colors[a],marker='^',markeredgecolor=colors[a],markersize='10',label=latch_name[a])
    #plt.plot(index, merged_data[:,1],color='red',marker='^',markeredgecolor='red',markersize='10 ',label='Index_ar2')
    plt.xlabel('Index')#横轴
    plt.ylabel('Value')#纵轴
    plt.title('Line Plot of Merged Data')#标题
    plt.legend()
    plt.show()
 

directory=r"C:\Users\zcj\Desktop\资料\pvt\test"
i=len(listdir(directory))
file=[i]
date=list()
latch_name=list()
for filename in listdir(directory):
    latch_name.append(filename)
    full_path = path.join(directory, filename)
    #print(full_path)
    date.append(mt2csv.readalldata(full_path)) 
date_array=np.array(date)
#print(date_array[1])
drawfunc_mt(date_array,i,latch_name)
#print(latch_name)
