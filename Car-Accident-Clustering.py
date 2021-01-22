import streamlit as st
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px


#function that reads a lost of states and their GPS coordinates and returns a dictionary of
#state names corresponding with their GPS coordinates
@st.cache
def make_state_dict():
    states_df = pd.read_csv('states.txt', delim_whitespace = True)
    states_df.set_index('State',drop = True, inplace = True)
    states_df.drop(columns = 'State_Name',inplace = True)
    states_df['lat and lng'] = states_df[['Lat','Lng']].values.tolist()
    state_coord_dict = states_df['lat and lng'].to_dict()
    return state_coord_dict


#this function takes the location of the chosen state and the final clustered dataframe and returns
#a density map of clustered car accidents as a plotly figure.
def plot_map(default_location,df):
    mapbox_access_token =  'pk.eyJ1Ijoia3lsZXdlbHNoIiwiYSI6ImNramhlOTBvYjRrZGsyc3NibXlzYXJhYnIifQ.Dp5cYMqjvoSOFNTMMWgo2g'
    px.set_mapbox_access_token(mapbox_access_token)
    #adding coordinate that is not an actual car accident in order to prevent map from deloading when there are no clusters.
    df = df.append({'latitude':20,'longitude':170,'Number Of Accidents':0},ignore_index = True)
    
    fig = px.density_mapbox(df, lat='latitude', 
                        lon = 'longitude', zoom=5, mapbox_style='mapbox://styles/kylewelsh/ckjhej5ei22cq19qisu8h3qjw',
                        radius = 5, center = default_location,hover_data = ['Number Of Accidents'],
                        width = 800, height = 600)
    return fig


#Loads and cache's the car accident data.
@st.cache(allow_output_mutation=True)
def load_data_2019():
    car_accidents_df_2019 = pd.read_csv('car_accidents_2019.csv')
    return car_accidents_df_2019


#takes the selected state and the parameters for the DBSCAN algorithm then returns a dataframe
#of the GPS coordinates and the number of car accidents at each coordinate for the car accident clusters.

def cluster(state,min_samples,max_distance):
    car_accidents_df_2019_state = car_accidents_df_2019[car_accidents_df_2019['State'] == state_name_input]
    coords = car_accidents_df_2019_state[['latitude','longitude']].to_numpy()

    db = DBSCAN(eps= (max_distance/1000)/6371, min_samples = min_samples, 
                algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    
    cluster_accidents_df_2019 = car_accidents_df_2019_state[cluster_labels != -1]
    cluster_accidents_df_2019_grouped = cluster_accidents_df_2019.groupby(by = ['latitude','longitude']).count()
    cluster_accidents_df_2019_grouped.reset_index(inplace = True)

    final_cluster_df = cluster_accidents_df_2019.merge(cluster_accidents_df_2019_grouped,
                                                   on = ['latitude','longitude'],how = 'left',
                                                   validate = 'm:1')
    final_cluster_df.rename(columns = {'weight_y':'Number Of Accidents'}, inplace = True)
    return final_cluster_df


car_accidents_df_2019 = load_data_2019()

state_coord_dict = make_state_dict()
states = list(state_coord_dict.keys())

#Setting the widgets for the web app
st.title('Car Accident Cluster Identifier')

min_samples = st.slider('Minimum Number of Crashes in Neighborhood', value = 30)  
max_distance = st.slider('Max Distance Between Crashes (Meters)',min_value = 1, max_value = 100, value = 30)
state_name_input = st.sidebar.selectbox('State',states)

#default location is the gps coordinates corresponding to the chosen state
default_location = dict(lon=state_coord_dict[state_name_input][1],
                        lat = state_coord_dict[state_name_input][0])


final_cluster_df = cluster(state_name_input,min_samples,max_distance)

fig = plot_map(default_location,final_cluster_df)
st.plotly_chart(fig)





