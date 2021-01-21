import streamlit as st
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px

@st.cache
def make_state_dict():
    states_df = pd.read_csv('states.txt', delim_whitespace = True)
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
@st.cache
def load_data_2019():
    car_accidents_df_2019 = pd.read_csv('car_accidents_2019.csv')
    return car_accidents_df_2019

car_accidents_df_2019 = load_data_2019()

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

default_location = dict(lon=state_coord_dict[state_name_input][1],
                        lat = state_coord_dict[state_name_input][0])

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


