'''
用以處理股票的讀取五儲存，主要檔案格式是csv
使用以下函數之前，記得要先在Get_Stock_ID執行一下Get_ID_List_form_Web()取得所有要計算的股票的名稱

Stock_index     << 有效的資料的股票代號跟名稱
List_TWII_Data  << List格式大盤資料
List_Stock_Data << List格式個股資料
def Read_Stock_Data_from_csv():     # 從csv讀取所有股票的資料，這邊讀回來是Pandas Dataframe
def Write_Stock_Data_to_csv():      # 寫成csv的資料，這裡寫成Pandas Data Frame的資料格式
def Read_From_Web():                # 直接從網路上讀取資料，如果沒有的資料就會不使用

data_toList():  #最後都要做這個，將那些Dataframe轉乘List
Resort_length() 將長度跟第一筆不合的股票資料給剃除

'''
import os
import Get_Stock_ID
import Get_Stock_Price
import pandas as pd

Stock_Data = []
Stock_index = []
Base_csv_path = os.path.join(os.getcwd(),'Stock_Datas')
TWII_Data = []

List_TWII_Data = []
List_Stock_Data = []
List_1d_Score_Data =[] #計算今天尾盤到明天尾盤的價格
List_2d_Score_Data =[] #計算明天尾盤到後天尾盤的價格
List_Day_Datas =[] #
if not os.path.exists(Base_csv_path):
    os.makedirs(Base_csv_path)

def Get_List_inIndex(Name= ""):
    for i in range(len(Stock_index)):
        if Name == Stock_index[i][1]:
            return i
def Get_Stock_List_Data(Name= ""):
    global Stock_Data
    if Name == '加權指數':
        return TWII_Data
    inx = Get_List_inIndex(Name)-1
    return Stock_Data[inx]
def Resort_length():
    global Stock_Data
    global Stock_index

    parp_Stk_data = []
    parp_Stk_index = []
    stk_len = len(Stock_Data[0])
    for i,j in zip(Stock_Data,Stock_index):
        if len(i) == stk_len:
            parp_Stk_data.append(i)
            parp_Stk_index.append(j)

    Stock_Data = parp_Stk_data
    Stock_index = parp_Stk_index


def data_toList():
    global Stock_Data
    global Base_csv_path
    global Stock_index
    global TWII_Data

    global List_TWII_Data
    global List_Stock_Data
    global List_1d_Score_Data
    global List_2d_Score_Data
    global List_Day_Datas

    #main_data_index =  TWII_Data.index.to_list()
    Resort_length()

    List_TWII_Data = []
    List_TWII_Data.append(TWII_Data['Open'].to_list())
    List_TWII_Data.append(TWII_Data['High'].to_list())
    List_TWII_Data.append(TWII_Data['Low'].to_list())
    List_TWII_Data.append(TWII_Data['Close'].to_list())
    List_TWII_Data.append(TWII_Data['Adj Close'].to_list())
    List_TWII_Data.append(TWII_Data['Volume'].to_list())

    List_Stock_Data = []
    List_1d_Score_Data = []
    List_2d_Score_Data = []
    List_Day_Datas = []

    bb = Stock_Data[0]['Date']
    for i in bb:
        List_Day_Datas.append(i.__str__())
    print ('Get Data',List_Day_Datas)
    for i in Stock_Data:
        st = []
        st.append(i['Open'].to_list())
        st.append(i['High'].to_list())
        st.append(i['Low'].to_list())
        st.append(i['Close'].to_list())
        st.append(i['Adj Close'].to_list())
        st.append(i['Volume'].to_list())
        List_Stock_Data.append(st)

        '''
        cs = i['Close'].to_list()
        d0 = [cs[0] , cs[0]] + cs
        d1 = [cs[0]]+ cs + [cs[-1]]
        d2 = cs + [cs[-1] , cs[-1]]
        '''
        cs = i['Close']
        d0 = cs.to_list()
        d1 = cs.shift(-1)
        d1.fillna(method='pad', inplace=True)
        d2 = cs.shift(-2)
        d2.fillna(method='pad', inplace=True)

        sc = []
        tc = []
        for i in zip(d0,d1,d2):
            sc.append(i[1]/i[0])
            tc.append(i[2]/i[1])
        #del sc[0]
        #print("In basic Save Load 1d length",sc)
        #print("In basic Save Load 2d length", tc)
        List_1d_Score_Data.append(sc)
        List_2d_Score_Data.append(tc)


def Read_Stock_Data_from_csv():
    global Stock_Data
    global Base_csv_path
    global Stock_index
    global TWII_Data
    Stock_Data = []
    Stock_index = []
    if os.path.exists(os.path.join(Base_csv_path,r'%5ETWII.csv')):
        TWII_Data = pd.read_csv(os.path.join(Base_csv_path,r'%5ETWII.csv'))
        for i in Get_Stock_ID.WarrantStock[1:] :
            if os.path.exists(os.path.join(Base_csv_path,i[0]+'.csv')) :
                Stock_index.append(i)
                Stock_Data.append(pd.read_csv(os.path.join(Base_csv_path,i[0]+'.csv')))
                #Stock_Data.append(Get_Stock_Price(i[0]))
    data_toList()
    aa = map(list, zip(*List_Stock_Data))
    print(List_Stock_Data[0])
    print(list(aa))

def Write_Stock_Data_to_csv():
    global Stock_Data
    global Base_csv_path
    global Stock_index
    global TWII_Data



    print('TWII Data is',TWII_Data)
    TWII_Data.to_csv(path_or_buf=os.path.join(Base_csv_path,r'%5ETWII.csv'))
    for i in range(len(Stock_index)):
        Stock_Data[i].to_csv(path_or_buf=os.path.join(Base_csv_path,Stock_index[i][0]+'.csv'))

def Start_Read_Stock_Data_Form_Web():
    global Stock_Data
    global Base_csv_path
    global Stock_index
    global TWII_Data
    Stock_Data = []
    Stock_index = []

    TWII_Data = Get_Stock_Price.Get_Datas(r'%5ETWII')
    TWII_Data.fillna(method='pad', inplace=True)
    print('TWII', TWII_Data)


def Read_Stock_Data_From_Web(Numb =1):
    global Stock_Data
    global Base_csv_path
    global Stock_index
    global TWII_Data

    i = Get_Stock_ID.WarrantStock[Numb]

    st = Get_Stock_Price.Get_Datas(i[0])
    st.fillna(method='pad', inplace=True)
    #print (i,st)
    #print(len(st),len(TWII_Data))
    #if len(st) == len(TWII_Data):
    Stock_Data.append(st)
    Stock_index.append(i)

    print(st)
    #data_toList()











