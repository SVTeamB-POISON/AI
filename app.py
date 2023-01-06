from flask import Flask
from flask import request
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import pickle
import cv2
import os
import urllib.request


app = Flask(__name__)



@app.route('/', methods=['GET'])
def main():
    return 'Backend-server Connect'

@app.route("/model/",methods=['GET', 'POST'])
def test():
    if(request.method == 'POST'):
        params = request.get_json()['id']
        dic = url_to_image(params)
        return dic
    elif(request.method =='GET'):
        return 'Backend-server Connect'

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()),dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    args = {'model': 'p2flower.model', 'labelbin': 'lb2.pickle'}
    output = image.copy()
    
    image = cv2.resize(image, (224,224))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis = 0)
    
    model = load_model(args["model"])
    lb = pickle.loads(open(args["labelbin"], "rb").read())
    proba = model.predict(image)[0]
    idx = np.argsort(-proba)[:3]
    label = lb.classes_[idx]

    proba = proba[idx].astype(np.float64)
    proba = np.floor(proba*1000)/10
    
    image_name_list = [{'flower1':label[0],'accuracy1':proba[0]},{'flower2':label[1],'accuracy2':proba[1]},{'flower3':label[2],'accuracy3':proba[2]}]
    
    return image_name_list

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port = 5001, debug=True)