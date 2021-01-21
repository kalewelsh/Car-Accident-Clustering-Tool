# Car Accident Clustering Tool
Web Application Link: https://car-accident-clustering.herokuapp.com/

* A web application that can be used to identify clusters in card accidents across the united states
* Uses the DBSCAN clustering algorithm to identify clusters of car accidents
* Allows you to modify the parameters of the algorithm in order to change how the data is clusterd

This tool can be used to identify specific areas where there are a high density of car accidents in order to identify hazardous driving areas. These hazardous driving areas could be as a result of faulty road design, improper speed limits, faulty signage, or potentially other causes. 
# Algorithm
Given a set of geospatial coordinates the DBSCAN algorithm will identify areas where there are lots of car accidents clustered together and remove the car accidents that are not a part of any of the clusters. The algorithm takes two parameters, the max distance between points for them to be considered neighbors, and the number of neighbors required to be considered a core point. 

In lamens terms, the 'Minimum Number of Crashes In Neighborhood' will have an effect on how many car accidents are needed to be considered a cluster and the 
'Distance Between Neighboors' will determine how close together the car accidents need to be in order to be considered a cluster. 
# The Data
Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. “A Countrywide Traffic Accident Dataset.”, 2019. https://arxiv.org/abs/1906.05409

For this project I specifically looked at car accidents from the most recent year available, 2019.
