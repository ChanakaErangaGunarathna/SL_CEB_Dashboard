
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import datetime
import streamlit as st

# df_0=pd.read_csv('CEB-table_energy_data.csv')

# df1=df_0
# df1['date']=[pd.to_datetime(date.date()) for date in pd.to_datetime(df1['date'])]

st.title('CEB daily Power')

df_by_date=pd.read_csv('CEB-table_energy_data_new.csv')
st.dataframe(df_by_date,1200,400)

# df_by_date['date']=pd.to_datetime(df_by_date['date'])
# df_by_date['Hydro']=df_by_date['Laxapana Hydro Complex']+df_by_date['Mahaweli Hydro Complex']+df_by_date['Samanala Hydro Complex']+df_by_date['SPP Minihydro 2']
# df_by_date['Fuel']=df_by_date['CEB Thermal Oil']+df_by_date['IPP Thermal Oil']
# df_by_date['Wind']=df_by_date['CEB Wind']+df_by_date['SPP Wind']

# fig,ax=plt.subplots(figsize=(15,8))
# plt.stackplot(df_by_date['date'],
#               [df_by_date['CEB Thermal Coal'], df_by_date['Fuel'],
#                df_by_date['Hydro'],df_by_date['SPP Solar 1'], df_by_date['Wind'],df_by_date['SPP Biomass']],
#               labels=['CEB Thermal Coal', 'Fuel', 'Hydro','Solar' ,'Wind','Bio_Mass'],
#               alpha=0.8)
# plt.xticks(df_by_date['date'],rotation=75)
# # ax.set_xticklabels(list(df_by_date.index),rotation=90)
# plt.legend(loc=2, fontsize='large')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# st.pyplot(fig)
# plt.show()
# print(df1)

