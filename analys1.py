
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
from datetime import datetime
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

list_of_days=list(df_by_date['date'].sort_values(ascending=False))
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
        if(date_index!=(len(list_of_days)-1)):
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

df_precentage=df_by_date[['date','CEB Thermal Coal','Hydro','Wind','Fuel','SPP Solar 1']].set_index('date').T
df_precentage['Average']=df_precentage.mean(axis=1).round(2)
df_precentage.reset_index(inplace=True)
df_precentage.sort_values('Average',inplace=True)

if(all):
    circles = circlify.circlify(
    df_precentage['Average'].tolist(), 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
else:
    circles = circlify.circlify(
    df_precentage[option].tolist(), 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

# Create just a figure and only one subplot
fig3, ax3 = plt.subplots(figsize=(10,10))

# Remove axes
ax3.axis('off')

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
labels = df_precentage['index'].tolist()
Colors = ['#99B898','#355C7D','#FFCEAB','#FF847C','#F5C6EC']
if(all):
    Counts=df_precentage['Average']
else:
    Counts=df_precentage[option]
# print circles
for circle,label,color,count in zip(circles,labels,Colors,Counts):
    x, y, r = circle
    ax3.add_patch(plt.Circle((x, y), r*0.99, alpha=0.95, linewidth=2,facecolor=color))
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

'''
    This section is besed on the data related to the peak enery in day time and night time.
    Mainly check the changes over the time and changes over the each day of a week day.
'''
# Import the data frame and clean the data frame 

df_peak_data=pd.read_csv('CEB-table_peak_data.csv')
df_peak_data.drop('Unnamed: 0',axis=1,inplace=True)
df_peak_data.drop_duplicates(inplace=True)
df_peak_data['date_name']=[datetime.strptime(date,'%m/%d/%Y').strftime("%a") for date in df_peak_data['date']] 


# Active Power plot 
fig4, ax4=plt.subplots(figsize=(8,4))
sns.lineplot(x='date', y='Active Power (MW)',hue='Description' ,data=df_peak_data,ax=ax4)
ax4.set_xticklabels(labels=list_of_days,rotation=90)
ax4.set_title('Day Time power over time')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
st.pyplot(fig4)
st.write("")
# Reactive Power plot 
fig5, ax5=plt.subplots(figsize=(8,4))
sns.lineplot(x='date', y='Reactive Power (Mvar)',hue='Description' ,data=df_peak_data,ax=ax5)
ax5.set_title('Reactive Power over time')
ax5.set_xticklabels(labels=list_of_days,rotation=90)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
st.pyplot(fig5)

# Analysis over CEB-table_night_peak_data 

df_night=pd.read_csv('CEB-table_night_peak_data.csv')
df_night.drop('Unnamed: 0',axis=1,inplace=True)
df_night.drop_duplicates(inplace=True)
df_night.set_index('Night Peak Data (Complex Wise)',inplace=True)
dates=df_night['date'].unique().tolist()
df_night_new=pd.DataFrame(columns=['Ap','RP','date'])
for date in dates:
    df_test=df_night[df_night['date']==date]
    df_temp=pd.DataFrame(columns=['Ap','RP','date'])
    # df_night.groupby('date')[['']]
    # AP=df_test.loc[[0,1,2,9,10]]['Active Power (MW)']
    # RP=df_test.loc[[0,1,2,9,10]]['Reactive Power (Mvar)']
    # Coal=df_test.loc[5]['Reactive Power (Mvar)']
    Hy_AP=df_test.loc[['Laxapana Hydro Complex','Mahaweli Hydro Complex','Samanala Hydro Complex','SPP Minihydro','CEB Small Hydro']]['Active Power (MW)'].sum()
    Hy_RP=df_test.loc[['Laxapana Hydro Complex','Mahaweli Hydro Complex','Samanala Hydro Complex','SPP Minihydro','CEB Small Hydro']]['Reactive Power (Mvar)'].sum()
    Wind_AP=df_test.loc[['CEB Wind','SPP Wind']]['Active Power (MW)'].sum()
    Wind_RP=df_test.loc[['CEB Wind','SPP Wind']]['Reactive Power (Mvar)'].sum()
    Oil_AP=df_test.loc[['CEB Thermal Oil','IPP Thermal Oil']]['Active Power (MW)'].sum()
    Oil_RP=df_test.loc[['CEB Thermal Oil','IPP Thermal Oil']]['Reactive Power (Mvar)'].sum()
    Renew_AP=Hy_AP+Wind_AP+df_test.loc[['SPP Biomass']]['Active Power (MW)'].sum()+df_test.loc[['Capacitors']]['Active Power (MW)'].sum()
    Renew_RP=Hy_RP+Wind_RP+df_test.loc[['SPP Biomass']]['Reactive Power (Mvar)'].sum()+df_test.loc[['Capacitors']]['Reactive Power (Mvar)'].sum()
    Fuel_AP=Oil_AP+df_test.loc[['CEB Thermal Coal']]['Active Power (MW)'].sum()
    Fuel_RP=Oil_RP+df_test.loc[['CEB Thermal Coal']]['Reactive Power (Mvar)'].sum()
    
    df_temp.loc['Wind']=[Wind_AP,Wind_RP,date]
    df_temp.loc['Hydro']=[Hy_AP,Hy_RP,date]
    df_temp.loc['Renew']=[Renew_AP,Renew_RP,date]
    df_temp.loc['Fuel']=[Fuel_AP,Fuel_RP,date]
    df_temp.loc['Oil']=[Oil_AP,Oil_RP,date]
    df_night_new=pd.concat([df_night_new,df_temp])


df_plot=df_night_new.reset_index()
fig6, ax6=plt.subplots(figsize=(8,4))
sns.lineplot(x='date', y='Ap',hue='index',data=df_plot[(df_plot['index']=='Renew') | (df_plot['index']=='Fuel')],ax=ax6)
ax6.set_title('Night time power distribution')
ax6.set_xticklabels(labels=dates,rotation=90)
plt.ylim([0,2000])
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
st.pyplot(fig6)



# Analysis over Rainfall and resover limits data
st.header('Rainfall data and power plant details')

df_pond=pd.read_csv('CEB-table_pond_rainfall_data.csv')
df_pond.drop('Unnamed: 0',axis=1,inplace=True)
df_pond.drop_duplicates(inplace=True)

df_major_resovoers=pd.read_csv('CEB-table_reservoir_rainfall_data.csv')
df_major_resovoers.drop('Unnamed: 0',axis=1,inplace=True)
df_major_resovoers.drop_duplicates(inplace=True)
df_major_resovoers.rename(columns={'Major Reservoir':'Reservoir/Pond'},inplace=True)

df_pond=pd.concat([df_pond,df_major_resovoers])
columns=df_pond.columns
df_filterd=df_pond[df_pond['Present Level (masl)']!='Not available']
df_filterd['Present Level (masl)']=df_filterd['Present Level (masl)'].astype(float)

resovoers_details=pd.read_csv('resovire_csv.csv')
resovoers_details.dropna(inplace=True)
resovoers_details=resovoers_details[['Reservoir/Pond','Split level']]
df_filterd=df_filterd.merge(resovoers_details,how='inner')

list_of_resovers=df_filterd['Reservoir/Pond'].unique()

with st.sidebar:
    st.header('Select a resover')
    resovor_option= st.selectbox(
                'Select a resover',
                list_of_resovers)


df_pond_selected=df_filterd[df_filterd['Reservoir/Pond']==resovor_option]

# Curret Level Indication graph 

fig7, ax7=plt.subplots()
sns.lineplot(x='date', y='Present Level (masl)',hue='Reservoir/Pond',data=df_pond_selected,ax=ax7)
ax7.set_title('Resovoer Level')
ax7.set_xticklabels(labels=dates,rotation=90)
# if(df_pond_selected['Split level'].tolist()[0]!=0):
#     ax7.axhline(df_pond_selected['Split level'].tolist()[0], ls='--')
# st.pyplot(fig7)


fig8, ax8=plt.subplots()
sns.barplot(x='date', y='Rainfall (mm) for past 24 h',hue='Reservoir/Pond',data=df_pond_selected,ax=ax8)
ax8.set_title('Resovoer Rainfall')
ax8.set_xticklabels(labels=dates,rotation=90)
# st.pyplot(fig8)


y=df_filterd.groupby('Reservoir/Pond')['Rainfall (mm) for past 24 h'].mean().reset_index()
y.rename(columns={'Rainfall (mm) for past 24 h':'Average rainfall'},inplace=True)
fig9, ax9=plt.subplots()
sns.barplot(x='Reservoir/Pond', y='Average rainfall',data=y,ax=ax9,color='blue',alpha=0.6)
ax9.set_title('Average rainfall data on all major resovers and ponds')
ax9.set_xticklabels(labels=y['Reservoir/Pond'].unique(),rotation=90)
st.pyplot(fig9)


st.subheader(resovor_option)

col8,col9=st.columns(2)

with st.container():
    col8.pyplot(fig7)
    col9.pyplot(fig8)

st.write('Split Level - {}'.format(df_pond_selected['Split level'].tolist()[0]))



