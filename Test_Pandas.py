import pandas as pd
import Get_Stock_Price as pp

st = pp.Get_Datas('6426.TW')
ref = pp.Get_Datas(r'%5ETWII')

dat_List = st.index.to_list()
ref_List = ref.index.to_list()

ind = 0

print(st)
print(ref)

#aa = list(st['2019-08-29'])
'''
a = pd.Series({st.index.to_list()[-1] : 100 })
b = pd.Series({st.index.to_list()[-1] : 200 })
c = pd.Series({st.index.to_list()[-1] : 300 })
d = pd.Series({st.index.to_list()[-1] : 400 })
e = pd.Series({st.index.to_list()[-1] : 500 })
f = pd.Series({st.index.to_list()[-1] : 600 })
'''
'''
a = pd.Series({st.index[-1] : 100.050000 })
b = pd.Series({st.index[-1] : 200.050000 })
c = pd.Series({st.index[-1] : 300.050000 })
d = pd.Series({st.index[-1]: 400.050000 })
e = pd.Series({st.index[-1] : 500.050000 })
f = pd.Series({st.index[-1]: 600.050000 })
t = pd.Series({st.index[-1]: '2021-08-28' })
df = pd.DataFrame({'Open':a ,'High':b,'Low':c,'Close':d,'Adj Close':e,'Volume':f})
df.index.set_names('Data',inplace=True)

print(df.index)
df.append(st)
print(df)

iii = st.loc[st.index[-1]]
iii['Open'] = 0

iii.append(iii)
iii['Close'] = 0
iii.append(iii)
print(iii)
'''


