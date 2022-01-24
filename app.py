import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

def left_align(s, props='text-align: left;'):
    return props

st.set_page_config(page_title='Database Barang')
st.header('Database Barang')
st.markdown('_Pengolahan database barang kedalam grafik statistika_')

### --- LOAD DATAFRAME
excel_file = 'Data_Barang.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:F',
                   header=1)

df = df.replace(np.nan, '', regex=True)
df = df.groupby(by=['KATEGORI', 'NAMA BARANG', 'SATUAN', 'TANGGAL EXPIRED', 'HARGA']).sum().reset_index()
# st.dataframe(df)

## --- STREAMLIT SELECTION
category = df['KATEGORI'].unique().tolist()
unit = df['SATUAN'].unique().tolist()
price = df['HARGA'].unique().tolist()
stock = df['STOK'].unique().tolist()

price_selection = st.slider('Harga: ', 
                          min_value = min(price),
                          max_value = max(price),
                          value=(min(price), max(price)))

stock_selection = st.slider('Stok: ',
                           min_value = min(stock),
                           max_value = max(stock),
                           value=(min(stock), max(stock)))

category_selection = st.multiselect('Kategori: ',
                                    category,
                                    default=category)
                                    
unit_selection = st.multiselect('Satuan: ',
                                unit,
                                default=unit)
# st.dataframe(category)
# st.dataframe(unit)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['HARGA'].between(*price_selection) & 
        df['STOK'].between(*stock_selection) & 
        df['SATUAN'].isin(unit_selection) & 
        df['KATEGORI'].isin(category_selection))

number_of_result = df[mask].shape[0]
st.markdown(f'*Hasil yang didapatkan: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION

# --- PLOT BAR CHART PRICE
bar_chart_price = px.bar(df[mask],
                         x='NAMA BARANG',
                         y='HARGA',
                         text='HARGA',
                         color_discrete_sequence=['#F63366']*len(df[mask]),
                         template='plotly_white')
st.plotly_chart(bar_chart_price)

# --- PLOT BAR CHART STOK
bar_chart_stok = px.bar(df[mask],
                         x='NAMA BARANG',
                         y='STOK',
                         text='STOK',
                         color_discrete_sequence=['#F63366']*len(df[mask]),
                         template='plotly_white')
st.plotly_chart(bar_chart_stok)
  
# --- DATAFRAME FILTERED DATA
st.dataframe(df[mask].style.applymap(left_align))

# --- DATAFRAME 3 ITEM MOST INVENTORY
st.markdown('_*3 barang dengan stok terbanyak*_')
st.success('Barang dibawah ini memiliki stok yang banyak karena permintaan pasar yang tinggi')
df_most_inventory = df.nlargest(3, 'STOK').reset_index();
del df_most_inventory['index']
st.dataframe(df_most_inventory.style.applymap(left_align))

# --- DATAFRAME 3 ITEM EXPENSIVE
st.markdown('_*3 barang dengan harga tertinggi*_')
df_most_price = df.nlargest(3, 'HARGA').reset_index();
del df_most_price['index']
st.dataframe(df_most_price.style.applymap(left_align))

# --- DATAFRAME DOESN'T HAVE EXPIRED DATE 
st.markdown('_*Barang tidak memiliki tanggal kadaluarsa*_')
st.warning('Barang dibawah ini beresiko untuk diperjual belikan karena tidak ada tanggal kadaluarsanya')
df_expired_null = df.where(df['TANGGAL EXPIRED'] == '')
df_expired_null.dropna(inplace=True)
df_expired_null = df_expired_null.reset_index() 
df_expired_null['HARGA'] = df_expired_null['HARGA'].astype(int)
df_expired_null['STOK'] = df_expired_null['STOK'].astype(int)

del df_expired_null['index']

st.dataframe(df_expired_null.style.applymap(left_align))

# --- PLOT PIE STOCK CHART
st.markdown('_*Pengelompokan stok berdasarkan kategori*_')
pie_chart = px.pie(df.groupby(by=['KATEGORI']).sum()[['STOK']].reset_index(), 
                title='',
                values='STOK',
                names='KATEGORI')
st.plotly_chart(pie_chart)