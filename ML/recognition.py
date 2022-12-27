import cv2
import numpy as np
from PIL import Image
from database.write_to_data import write_json
from deepface.basemodels import Facenet


model = Facenet.loadModel()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_regist(img_path:bytes, name_img:str):
    img = cv2.imdecode(np.frombuffer(img_path, np.uint8), cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_array = np.asarray(img)    
    faces = face_cascade.detectMultiScale(img_array, 1.1, 4)
    if faces == []:
        msg = "no face detected"
    elif len(faces)>1:
        msg = "more than one face is detected"
    else:
        for (x1,y1,w,h) in faces:
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + w, y1 + h
            face = img_array[y1:y2, x1:x2]                        
            face = Image.fromarray(face)                       
            face = face.resize((160,160))
            face = np.asarray(face)
            face = face.astype('float32')
            mean, std = face.mean(), face.std()
            face = (face - mean) / std
            face = np.expand_dims(face, axis=0)
            detections = model.predict(face)
            write_json(detections, name_img)
        msg = "face has been registered"
    return msg


def face_recog(img_path:bytes, database:dict):
    img = cv2.imdecode(np.frombuffer(img_path, np.uint8), cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_array = np.asarray(img)    
    faces = face_cascade.detectMultiScale(img_array, 1.1, 4)
    
    min_dist=100
    identity=' '

    if len(faces)>1:
        identity = "more than one face is detected"
    else:
        for (x1,y1,w,h) in faces:
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + w, y1 + h
            face = img_array[y1:y2, x1:x2]                        
            face = Image.fromarray(face)                       
            face = face.resize((160,160))
            face = np.asarray(face)
            face = face.astype('float32')
            mean, std = face.mean(), face.std()
            face = (face - mean) / std
            face = np.expand_dims(face, axis=0)
            signature = model.predict(face)

            for val in database:
                (key, value), = val.items()
                value = np.asarray(value)
                dist = np.linalg.norm(value-signature)
                if dist < min_dist:
                    min_dist = dist
                    identity = key

    if identity==" " and min_dist == 100:
        identity = "no face detected"
    return min_dist, identity
            