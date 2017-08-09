import numpy as np
import pandas as pd
from graphTraversal import *



import numpy as np
import random
import math
import pandas as pd

information_file = 'data/location_csv.csv'
time_matrix = 'data/time_matrix.txt'

infos = pd.read_csv(information_file, delimiter=';', low_memory = False)
infos = infos.drop(infos.columns[[5]], axis=1)
with open('data/distance_matrix.txt', 'r') as fobj:
    distances = [[float(num) for num in line.split()] for line in fobj]
distance=np.array(distances)
distance = pd.DataFrame(distance)
​
with open(time_matrix, 'r') as fobj:
    times = [[float(num) for num in line.split()] for line in fobj]
time=np.array(times)
time = pd.DataFrame(time)
​
​
#Separate the three matrices of interest
index = 4673
locations_time = time.iloc[0:index,0:index]
cities_time = time.iloc[0:index,index:len(time)]
cities_locations = time.iloc[index:,0:index]
​
​
#Closest city for each location
argmins = []
time_close = []
for i in range(0,cities_time.shape[0]-1):
    argmins.append(cities_time.iloc[i,:].argmin()-index)
    time_close.append(cities_time.iloc[i,argmins[i]])
​
​
closest = distance.iloc[0:len(argmins),0:3]
for i in range(0,cities_time.shape[0]-1):
    closest.iloc[i,0]=int(cities_time.iloc[i,:].argmin()-index)
    closest.iloc[i,1]=cities_time.iloc[i,argmins[i]]
    closest.iloc[i,2] = i
​
​
closest.columns = ['closest city', 'time', 'location']
closest = closest[['location', 'closest city', 'time']]
​
#get rid of all cities not assigned to a location
final_cities=closest.iloc[:,1].unique()
​

locpercity_less5 = []
for j in range(0,len(final_cities)):
    locpercity_less5.append([]) 
for j in range(0,len(final_cities)):
    locpercity_less5[j] = np.where(cities_locations.iloc[int(final_cities[j]),:]<4)[0]


j = 1
city_index = final_cities[j]
city_index

liste = np.append(city_index,locpercity_less5[j])

#top
top = time.iloc[liste,liste]
tops = distance.iloc[0:len(liste),0:3]
tops.columns = ['index_building', 'service_time', 'risk']
for i in range(0,len(tops)):
    tops.iloc[i,0] = int(liste[i])
    tops.iloc[i,1] = float(infos.iloc[int(tops.iloc[i,0]),2].replace(',',''))
    tops.iloc[i,2] = float(infos.iloc[int(tops.iloc[i,0]),1].replace(',',''))**1.5


def main():
    x = DoubleList()
    hotel = Node([0, 0, 0], "Hotel")
    x.add(hotel)
    replicate = 50
    for k in range(0,replicate):
        x.addTry()












