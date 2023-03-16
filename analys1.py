
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import datetime
import streamlit as st
import circlify

# df_0=pd.read_csv('CEB-table_energy_data.csv')

# df1=df_0
# df1['date']=[pd.to_datetime(date.date()) for date in pd.to_datetime(df1['date'])]
df_by_date=pd.read_csv('CEB-table_energy_data_new.csv')
df_by_date.drop('Unnamed: 0',axis=1,inplace=True)
df_by_date.drop_duplicates(inplace=True)
# df_by_date['date']=pd.to_datetime(df_by_date['date'])
df_by_date['Hydro']=df_by_date['Laxapana Hydro Complex']+df_by_date['Mahaweli Hydro Complex']+df_by_date['Samanala Hydro Complex']+df_by_date['SPP Minihydro 2']
df_by_date['Fuel']=df_by_date['CEB Thermal Oil']+df_by_date['IPP Thermal Oil']
df_by_date['Wind']=df_by_date['CEB Wind']+df_by_date['SPP Wind']
df_by_date['renuable']=df_by_date['Wind']+df_by_date['SPP Solar 1']+df_by_date['SPP Biomass']
df_by_date['Non_renuable']=df_by_date['CEB Thermal Coal']+df_by_date['Fuel']

list_of_days=list(df_by_date['date'])
total_dates=len(list_of_days)
avg_coal=df_by_date['CEB Thermal Coal'].sum()/total_dates
avg_hydro=df_by_date['Hydro'].sum()/total_dates
avg_fuel=df_by_date['Fuel'].sum()/total_dates
avg_wind=df_by_date['Wind'].sum()/total_dates
avg_solar=df_by_date['SPP Solar 1'].sum()/total_dates
avg_bio=df_by_date['SPP Biomass'].sum()/total_dates
avg_total=df_by_date['Total'].sum()/total_dates

with st.sidebar:
    st.header('CEB Data')
    with st.container():
        all=st.checkbox('Select all')
        if(all):
            option= st.selectbox(
            'Select a date',
            ['All date selected'])
        else:
            option= st.selectbox(
                'Select a date',
                list_of_days)
    
    

st.title('CEB daily Power')

st.write("")

st.write("")

# with st.container():
#     all=st.checkbox('Select all')
#     if(all):
#         option= st.selectbox(
#         'Select a date',
#         ['All date selected'])
#     else:
#         option= st.selectbox(
#             'Select a date',
#             list_of_days)
    

col1,col2,col3,col4,col5,col6,col7=st.columns(7)
with st.container():
    if(all):
        col1.metric(label='Coal',value=round(avg_coal,2))
        col2.metric(label='Hydro',value=round(avg_hydro,2))
        col3.metric(label='Fuel',value=round(avg_fuel,2))
        col4.metric(label='Wind',value=round(avg_wind,2))
        col5.metric(label='Sola',value=round(avg_solar,2))
        col6.metric(label='Biomass',value=round(avg_bio,2))
        col7.metric(label='Total',value=round(avg_total,2))


    else:
        coal_selected=float(df_by_date[df_by_date['date']==option]['CEB Thermal Coal'])
        hydro_selected=float(df_by_date[df_by_date['date']==option]['Hydro'])
        fuel_selected=float(df_by_date[df_by_date['date']==option]['Fuel'])
        wind_selected=float(df_by_date[df_by_date['date']==option]['Wind'])
        solar_selected=float(df_by_date[df_by_date['date']==option]['SPP Solar 1'])
        bio_selected=float(df_by_date[df_by_date['date']==option]['SPP Biomass'])
        total_selected=float(df_by_date[df_by_date['date']==option]['Total'])
    
        date_index=list_of_days.index(option)
        if(date_index!=0):
            privious_coal=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['CEB Thermal Coal'])
            privious_hydro=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['Hydro'])
            privious_fuel=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['Fuel'])
            privious_wind=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['Wind'])
            privious_solar=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['SPP Solar 1'])
            privious_bio=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['SPP Biomass'])
            privious_total=float(df_by_date[df_by_date['date']==list_of_days[date_index-1]]['Total'])
        else:
            privious_coal=coal_selected
            privious_hydro=hydro_selected
            privious_fuel=fuel_selected
            privious_wind=wind_selected
            privious_solar=solar_selected
            privious_bio=bio_selected
            privious_total=total_selected

        col1.metric(label='Coal',value=df_by_date[df_by_date['date']==option]['CEB Thermal Coal'],delta=str(round(coal_selected-privious_coal,2)))
        col2.metric(label='Hydro',value=df_by_date[df_by_date['date']==option]['Hydro'],delta=str(round(hydro_selected-privious_hydro,2)))
        col3.metric(label='Fuel',value=df_by_date[df_by_date['date']==option]['Fuel'],delta=str(round(fuel_selected-privious_fuel,2)))
        col4.metric(label='Wind',value=df_by_date[df_by_date['date']==option]['Wind'],delta=str(round(wind_selected-privious_wind,2)))
        col5.metric(label='Solar',value=df_by_date[df_by_date['date']==option]['SPP Solar 1'],delta=str(round(solar_selected-privious_solar,2)))
        col6.metric(label='Bio',value=df_by_date[df_by_date['date']==option]['SPP Biomass'],delta=str(round(bio_selected-privious_bio,2)))
        col7.metric(label='Total',value=df_by_date[df_by_date['date']==option]['Total'],delta=str(round(total_selected-privious_total,2)))

# Make the presentage bubble graphs of renuable and other enery types
st.write('')

df_precentage=df_by_date[['date','CEB Thermal Coal','Hydro','Wind','Fuel']].set_index('date').T
df_precentage['Average']=df_precentage.mean(axis=1).round(2)
df_precentage.reset_index(inplace=True)

if(all):
    circles = circlify.circlify(
    df_precentage['Average'].sort_values().tolist(), 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
else:
    circles = circlify.circlify(
    df_precentage[option].sort_values().tolist(), 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

# Create just a figure and only one subplot
fig3, ax = plt.subplots(figsize=(10,10))

# Remove axes
ax.axis('off')

# Find axis boundaries
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)
labels = df_precentage.sort_values(by=option)['index'].tolist()
Colors = ['#99B898','#355C7D','#FFCEAB','#FF847C']
if(all):
    Counts=df_precentage['Average'].sort_values()
else:
    Counts=df_precentage[option].sort_values()
# print circles
for circle,label,color,count in zip(circles,labels,Colors,Counts):
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r*0.99, alpha=0.95, linewidth=2,facecolor=color))
    plt.annotate(
          label,
          (x,y ) ,
        fontsize=12,
        fontname="century gothic",
          va='center',
          ha='center'
     )  
    plt.annotate(
          round(count,2),
          (x,y-0.06 ) ,
        fontsize=12,
        fontname="century gothic",
          va='center',
          ha='center'
     )
st.pyplot(fig3)
# Period of time power distribution chart 
st.header('Power Generation Over the Time')
fig,ax=plt.subplots(figsize=(8,4))
plt.stackplot(df_by_date['date'],
              [df_by_date['CEB Thermal Coal'], df_by_date['Fuel'],
               df_by_date['Hydro'],df_by_date['SPP Solar 1'], df_by_date['Wind'],df_by_date['SPP Biomass']],
              labels=['CEB Thermal Coal', 'Fuel', 'Hydro','Solar' ,'Wind','Bio_Mass'],
              alpha=0.8)
plt.xticks(df_by_date['date'],rotation=75)
# ax.set_xticklabels(list(df_by_date.index),rotation=90)
plt.legend(loc=2, fontsize='large')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
st.pyplot(fig)

st.write("")
st.write("")

column_order=['date','CEB Thermal Coal','Fuel','Hydro','Wind','SPP Biomass']



