# 先在cmd终端进行这个操作 pip install fix_yahoo_finance --upgrade --no-cache-dir
# pip install pandas_datareader
# PYTHON 中使用PANDAS_DATAREADER 报错 IMPORTERROR: CANNOT IMPORT NAME ‘IS_LIST_LIKE’
# 修改fred.py 中的 from pandas.core.common import is_list_like 为 from pandas.api.types import is_list_like

# 下面就用对6家巨头公司 GATAFA（谷歌、阿里、腾讯、亚马逊、脸书、苹果）在2017年内的股票价格，进行简要的分析

from pandas_datareader import data
import fix_yahoo_finance as yf
yf.pdr_override() # 导入 Yahoo 数据修复功能, yahoo 财经的数据需要修复否则无法下载
import pandas as pd

# 先创建一个字典
gafataDict = {'谷歌':'GOOG', '亚马逊':'AMZN', '脸书':'FB',
                '苹果':'AAPL', '阿里':'BABA', '腾讯':'0700.hk'}

# 定义一个函数用来计算股票的涨跌幅
def change(column):
    buyPrice = column[0]                #买入价
    curPrice = column[column.size-1]    #现价
    priceChange=(curPrice-buyPrice)/buyPrice    #累计涨幅
    #判断股票是否上涨
    if (priceChange > 0):
        print('股票累计上涨 = ', priceChange*100, '%')
    elif (priceChange == 0):
        print('股票价格累计没有变化 = ', priceChange*100, '%')
    else:
        print('股票累计下跌 = ', priceChange*100, '%')
    return priceChange 

def calc(companyname):
    # 获取公司2017年股票数据
    start_date = '2017-01-01'
    end_date = '2018-01-01'
    companyDf = data.get_data_yahoo(gafataDict[companyname],start_date,end_date)
    # 累计涨幅
    closeCol = companyDf['Close']
    companyChange = change(closeCol)
    return companyChange

#获取阿里巴巴2017年的股票数据
start_date = '2017-01-01'
end_date = '2018-01-01'
babaDf=data.get_data_yahoo(gafataDict['阿里'],start_date, end_date)
#累计涨幅
closeCol=babaDf['Close']
babaChange=change(closeCol)

#谷歌
googDf=data.get_data_yahoo(gafataDict['谷歌'],start_date, end_date)
closeCol=googDf['Close']
googChange=change(closeCol)


#亚马逊
amazDf=data.get_data_yahoo(gafataDict['亚马逊'],start_date, end_date)
closeCol=amazDf['Close']
amazChange=change(closeCol)


#Facebook
fbDf=data.get_data_yahoo(gafataDict['脸书'],start_date, end_date)
closeCol=fbDf['Close']
fbChange=change(closeCol)



#苹果
applDf=data.get_data_yahoo(gafataDict['苹果'],start_date,end_date)
closeCol=applDf['Close']
applChange=change(closeCol)


#腾讯
txDf=data.get_data_yahoo(gafataDict['腾讯'],start_date,end_date)
#由于腾讯在港股上市，本案例都是美元显示，所以需要将港元兑换成美元
exchange=0.1274
txDf['Close_dollar']=txDf['Close']*exchange
closeCol=txDf['Close']
txChange=change(closeCol)

# 可视化
import matplotlib.pyplot as plt
# 修改 matplotlib 的字体设置，解决无法显示中文问题
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #制定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像时负号'-'显示为方块

plt.plot(babaDf['Close'])              #plot默认是线条图
plt.xlabel('时间')                     #x坐标轴文本
plt.ylabel('股价（美元）')             #y坐标轴文本
plt.title('2017年阿里巴巴股价走势')    #图片标题  
plt.grid(True)                         #显示网格
plt.show()                             #显示图形

#散点图：成交量和股价
babaDf.plot(x='Volume',y='Close',kind='scatter')       #scatter表示绘制散点图
plt.xlabel('成交量')
plt.ylabel('股价（美元）')
plt.title('成交量和股价')
plt.grid(True)
plt.show()
babaDf.corr()        #通过corr()获取数据框babaDf内说有变量的相关系数

#绘制GAFATA股价走势比较
plt.plot(googDf['Close'],label='谷歌')
plt.plot(amazDf['Close'],label='亚马逊')
plt.plot(fbDf['Close'],label='Facebook')
plt.plot(applDf['Close'],label='苹果')
plt.plot(babaDf['Close'],label='阿里巴巴')
plt.plot(txDf['Close'],label='腾讯')

plt.xlabel('时间')
plt.ylabel('股价（美元）')
plt.title('2018年GAFATA股价累计涨幅比较')
plt.grid(True)
plt.legend(loc=5)                               
plt.show()

#柱状图：六家公司股票的平均值
#先定义一个列表，将股票的平均值放入
gafataMeanList=[googDf['Close'].mean(),#谷歌
               amazDf['Close'].mean(),#亚马逊
               fbDf['Close'].mean(),#Facebook
               applDf['Close'].mean(),#苹果 
               babaDf['Close'].mean(),#阿里巴巴
               txDf['Close_dollar'].mean()#腾讯
               ]
#将列表转化为pandas的一维数据Series
gafataMeanSer=pd.Series(gafataMeanList,index=['谷歌',
                             '亚马逊',
                            'Facebook',
                              '苹果',
                             '阿里巴巴',
                             '腾讯'])
gafataMeanSer.plot(kind='bar',label='GAFATA')
plt.title('2017年GAFATA股价平均值')
plt.xlabel('公司名称')
plt.ylabel('股价平均值（美元）')
plt.grid(True)
plt.legend(loc=1)
plt.show()

#箱线图
closeDf=pd.DataFrame()
#合并6家公司的收盘价
closeDf=pd.concat([closeDf,googDf['Close'],#谷歌
                      amazDf['Close'],#亚马逊
                      fbDf['Close'],#Facebook
                      applDf['Close'],#苹果
                      babaDf['Close'],#阿里巴巴
                      txDf['Close_dollar']#腾讯 
                 ],axis=1)
#重命名列名为公司名称
closeDf.columns=['谷歌','亚马逊','Facebook','苹果','阿里巴巴','腾讯']

#箱线图
closeDf.plot(kind='box')
plt.grid(True)
plt.show()