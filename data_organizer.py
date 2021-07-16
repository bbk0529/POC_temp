import pandas as pd
from classifier import SmoothingAndPredict
import requests
import json

class Organizer() : 
    def __init__(self) : 
        self.organizer_level1 = {}
        self.organizer_level2 = {}

    def organize1(self, subject, data) : 
        organizer = self.organizer_level1 
        pk = subject.split('.')
        timestep = pk[3]
        sensor_no = pk[1]
        if organizer.get(timestep, False) : 
            organizer[timestep][sensor_no] = float(data)
        else : 
            organizer[timestep] = {}
            organizer[timestep][sensor_no] = float(data)
        # print(pd.DataFrame(organizer))
        keys = list(organizer.keys())
        for i in keys: 
            if len(organizer[i]) == 5:
                lst_data = list(organizer[i].values())
                print(f"\n\t {i} {organizer[i]} {lst_data} validated and removed\n")
                # self.organize2(i, organizer[i])
                requests.post('http://localhost:5001', data = json.dumps({
                    "subject": i,
                    "id": int(list(organizer[list(organizer.keys())[0]].keys())[0]) % 2,                    
                    "data": organizer[i]
                }))
                organizer.pop(i)
        
    def organize2(self, key, value) : 
        organizer = self.organizer_level2
        if organizer.get(key, False) : 
            organizer[key] = value
        else : 
            organizer[key] = {}
            organizer[key] = value

        print(pd.DataFrame(organizer))

        keys = list(organizer.keys())
        if len(organizer) >= 30: #trigger
            lst_data = list(organizer.values())
            print(f"\n\t {organizer} {lst_data} validated and removed\n")
            data = pd.DataFrame(organizer).values
            print(pd.DataFrame(organizer))
            predictor = SmoothingAndPredict()
            y = data[0]
            X = data[1:]
            predictor.validate(y,X)
            self.organizer_level2 = {}
        print("\n\n\n")
