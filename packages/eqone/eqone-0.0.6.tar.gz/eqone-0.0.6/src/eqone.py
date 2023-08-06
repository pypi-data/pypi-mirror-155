import subprocess as sp
import numpy as np
import pandas as pd
import sys 
import folium
from folium.plugins import HeatMap
import geopandas as gpd

sp.call('wget -nc  https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
df=pd.read_csv('all_month.csv',)
def main():      
        if (len(sys.argv)) < 2:
                map = folium.Map(location=[48, -102], zoom_start=1)
                df_2=df[['latitude','longitude','mag','place']]
                df_3=df_2[df_2['mag'] >= float(5)]
                #popup=df_3['mag']+'<br />'+df_3['place']
                for i, r in df_3.iterrows():
                        folium.Marker(location=[r['latitude'], r['longitude']], popup=r['mag']).add_to(map)
                map.save('map.html')
                map
                print('save map.html')
                #sp.call('explorer.exe geomap.html',shell=True)
                #sp.call('open geomap.html',shell=True)
                #sp.call('start geomap.html',shell=True)   

        elif sys.argv[1] == 'all':
                map = folium.Map(location=[48, -102], zoom_start=1)
                df_2=df[['latitude','longitude']]
                geolist=df_2.values.tolist()
                HeatMap(geolist,radius=7,blur=2).add_to(map)
                map.save('map.html')
                map
                print('save map.html')
                #sp.call('explorer.exe geomap.html',shell=True)
                #sp.call('open geomap.html',shell=True)
                #sp.call('start geomap.html',shell=True)
        
        elif sys.argv[1].isnumeric(): #数字以上のマグニチュード以上のヒートマップ
                map = folium.Map(location=[48, -102], zoom_start=1)
                df_2=df[['latitude','longitude','mag']]
                df_3=df_2[df_2['mag'] >= float(sys.argv[1])]
                df_4=df_3[['latitude','longitude']]
                geolist=df_4.values.tolist()
                HeatMap(geolist,radius=7,blur=2).add_to(map)
                map.save('map.html')
                map
                print('save map.html')
                #sp.call('explorer.exe geomap.html',shell=True)
                #sp.call('open geomap.html',shell=True)
                #sp.call('start geomap.html',shell=True)

if __name__=="__main__": 
        main()