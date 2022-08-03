#from importlib.resources import path
import pickle
import json
#import os
import warnings
warnings.filterwarnings(action='ignore')
import numpy as np
#import sklearn

__locations = None
__data_columns = None
__model = None

def get_estimated_price(Location,Area,bhk,Gymnasium,Lift):
    try:
        loc_index = __data_columns.index(Location.lower())
        len(loc_index)
        #print('number:',len(loc_index))
    except:
        loc_index = -1

      #  loc_index = np.where(X.columns==Location)[0][0]

        x = np.zeros(len(__data_columns))
        x[0] = Area
        x[1] = bhk
        x[2] = Gymnasium
        x[3] = Lift

        if loc_index >=0:
             x[loc_index] = 1
    return __model.predict([x])[0]

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts ...starts..")
    global __data_columns
    global __locations
    global __model
    
    with open('data/columns.json','r') as f:
        __data_columns = json.load(f)['data_column']
        __locations = __data_columns[11:]
    print('locations online')

    with open('data/mumbai.pickle','rb') as f:
        __model = pickle.load(f)
    print("loading saved artifacts ...completed")

def get_data_columns():
    return __data_columns

#os.chdir('ML/data/columns.json')

if __name__== '__main__':
    load_saved_artifacts()
    #print(get_location_names())
    # print(get_estimated_price('thane',500,1,1,1))
    # print(get_estimated_price('Airoli',475,2,0,1))