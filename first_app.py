import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
#import matplotlib as mpl
#import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
#import datetime
#from streamlit_folium import folium_static
#import folium
#from folium import plugins
import plotly.express as px



@st.cache
def load_data():
    
    car_accidents_df = pd.read_csv('C:/Users/Kyle/Downloads/archive (2)/US_Accidents_June20.csv')
    date_list = car_accidents_df['Start_Time'].to_list()
    year_list = []
    for date in date_list:
        year_list.append(date.split('-')[0])  
    car_accidents_df['Year'] = year_list
    car_accidents_df['wight'] = 1
    car_accidents_df_2019 = car_accidents_df[car_accidents_df['Year'] == '2019']
    car_accidents_df_2019.rename(columns = {'Start_Lat':'latitude','Start_Lng':'longitude'},inplace = True)
    return car_accidents_df_2019[['latitude','longitude','State','Year']]


#def generate_base_map(default_location, default_zoom = 7):
   # base_map = folium.Map(location = default_location, control_scale = True, zoom_start = default_zoom, attr ='Mapbox',titles = 'eyJ1Ijoia3lsZXdlbHNoIiwiYSI6ImNramhlOTBvYjRrZGsyc3NibXlzYXJhYnIifQ.Dp5cYMqjvoSOFNTMMWgo2g Mapbox Attribution' )
   # return base_map

@st.cache
def make_state_dict():
    states_df = pd.read_csv('C:/Users/Kyle/Documents/states.txt', delim_whitespace = True)
    states_df.set_index('State',drop = True, inplace = True)
    states_df.drop(columns = 'State_Name',inplace = True)
    states_df['lat and lng'] = states_df[['Lat','Lng']].values.tolist()
    state_coord_dict = states_df['lat and lng'].to_dict()
    return state_coord_dict


def plot_map(default_locatoin):
    mapbox_access_token =  'pk.eyJ1Ijoia3lsZXdlbHNoIiwiYSI6ImNramhlOTBvYjRrZGsyc3NibXlzYXJhYnIifQ.Dp5cYMqjvoSOFNTMMWgo2g'
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.density_mapbox(final_cluster_df, lat='latitude', 
                        lon = 'longitude', zoom=5, mapbox_style='mapbox://styles/kylewelsh/ckjhej5ei22cq19qisu8h3qjw',
                        radius = 5, center = default_location,hover_data = ['Number Of Accidents'],
                        width = 800, height = 600)
    return fig

car_accidents_df_2019 = load_data()


st.title('Car Accident Cluster Identifier')

min_samples = st.slider('Minimum Number of Crashes in Cluster', value = 30)  
max_distance = st.slider('Max Distance Between Crashes (Meters)',min_value = 1, max_value = 100, value = 30)

state_coord_dict = make_state_dict()
states = list(state_coord_dict.keys())
state_name_input = st.sidebar.selectbox('State',states)


car_accidents_df_2019 = car_accidents_df_2019[car_accidents_df_2019['State'] == state_name_input]
coords = car_accidents_df_2019[['latitude','longitude']].to_numpy()

db = DBSCAN(eps= (max_distance/1000)/6371, min_samples = min_samples, 
            algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_


#cluster_coords = coords[cluster_labels != -1].tolist()

#default_location = [state_coord_dict[state_name_input][0],state_coord_dict[state_name_input][1]]
default_location = dict(lon=state_coord_dict[state_name_input][1],
                        lat = state_coord_dict[state_name_input][0])

#base_map_columbus = generate_base_map(default_location)
#plugins.HeatMap(data = cluster_coords,radius = 5,max_zoom = 10,max_val = 10,blur = 1).add_to(base_map_columbus)

#folium_static(base_map_columbus)


car_accidents_df_2019['weight'] = 1
cluster_accidents_df_2019 = car_accidents_df_2019[cluster_labels != -1]
cluster_accidents_df_2019_grouped = cluster_accidents_df_2019.groupby(by = ['latitude','longitude']).count()
cluster_accidents_df_2019_grouped.reset_index(inplace = True)

final_cluster_df = cluster_accidents_df_2019.merge(cluster_accidents_df_2019_grouped,
                                                   on = ['latitude','longitude'],how = 'left',
                                                   validate = 'm:1')
final_cluster_df.rename(columns = {'weight_y':'Number Of Accidents'}, inplace = True)




    
fig = plot_map(default_location)
st.plotly_chart(fig)


