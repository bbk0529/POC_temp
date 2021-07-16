#data organizer
from flask import Flask, request
import numpy as np
import json

from data_organizer import Organizer

app = Flask(__name__)
app.config["DEBUG"] = True

dict_instance = {}

@app.route('/', methods=['GET','POST'])
def main():
    r = json.loads(request.data.decode())
    # print(r)
    subject = r['subject']
    df = r['data']
    if not dict_instance.get(r['id'], False) : 
        dict_instance[r['id']] = Organizer()
    dict_instance[r['id']].organize1(subject, df)
    return df



if __name__ == '__main__':
    app.run(debug=True, host='localhost')
