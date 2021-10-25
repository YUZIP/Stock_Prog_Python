'''
用此取得股票的ID，比如當季有出權證的股票跟名冊上有編的
其中還可以透過一個CSV檔加入自己想觀察的股票
'''
import requests
import time
import os

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

WarrantStock = [['%5ETWII', '加權指數'], ['1101.TW', '台泥'], ['1102.TW', '亞泥'], ['1103.TW', '嘉泥']]
Ignore_Stock_Numbet = ['2353.TW','6285.TW']
Have_Stock_ID = False
StockList = []

def get_season():
    aa = time.localtime()
    yy = (aa.tm_year - 1911).__str__()
    if (aa.tm_mon in [1,2,3] ):
        se = "01"
    elif (aa.tm_mon in [4,5,6]) :
        se = "02"
    elif (aa.tm_mon in [7,8,9]) :
        se = "03"
    else:
        se = "04"

    ee = "https://mops.twse.com.tw/nas/t110/"+yy+se+"X0.htm?mops=1"
    print(ee)
    return ee

def Get_ID_List_form_Web():
    """
    This will add Stock ID from web you can take it by Get_IDS
    """
    global WarrantStock
    global Have_Stock_ID
    global StockList
    sp_Stock_List = []
    try:
        f = open(os.path.join(os.getcwd(),"SpStock.csv"),'r')
        pt = f.read()
        f.close()
        pp = pt.split("\n")
        for i in pp:
            g = i.split(",")
            if len(g) > 1:
                sp_Stock_List.append([g[1],g[0]])
    except:
        pass
    try:
        del sp_Stock_List[0]
    except:
        pass

    tt_Stock_List = []
    try:
        f = open(os.path.join(os.getcwd(), "TotalStock.csv"), 'r')
        pt = f.read()
        f.close()
        pp = pt.split("\n")
        for i in pp:
            g = i.split(",")
            if len(g) > 1:
                tt_Stock_List.append([g[1], g[0]])
    except:
        pass
    try:
        del tt_Stock_List[0]
    except:
        pass

    sp_Stock_List = [[r"%5ETWII","加權指數"]] + sp_Stock_List + tt_Stock_List

    #print (sp_Stock_List)


    try:
        aa = requests.get(get_season(), verify=False)
    except:
        print("Get Stock ID Faile")
        return False,[]
    aa.encoding = 'big5'
    #print(aa.text)
    st = aa.text
    Geted_Stock_ID = []
    bb = st.split(r"<td>&nbsp;")
    Stock_Infore_List = []
    for i in bb:
        cc = i.split(r"</td>")
        if len(cc[0]) <10 and len(cc[0]) !=0:
            Geted_Stock_ID.append(cc[0])
    tt = []
    for i in range(len(Geted_Stock_ID)):

        if float(i)%2.0 ==0:
            tt.append(Geted_Stock_ID[i]+".TW")
        else:

            tt.append(Geted_Stock_ID[i])
            if tt[0] not in Ignore_Stock_Numbet:
                Stock_Infore_List.append(tt)
            tt = []

    aa.close()

    # 測試模式，只取10個
    Stock_Infore_List = sp_Stock_List + Stock_Infore_List
    #Stock_Infore_List = sp_Stock_List + Stock_Infore_List[:20]
    WarrantStock = Stock_Infore_List
    StockList = WarrantStock[1:]
    print(WarrantStock)
    Have_Stock_ID = True
    return True,WarrantStock
    #return Stock_Infore_List

'''
def Get_IDS():
    global WarrantStock
    #print(WarrantStock)
    return WarrantStock
def Write_IDS(dat):
    global WarrantStock
    WarrantStock = dat

'''