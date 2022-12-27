from ML.recognition import face_regist, face_recog
from fastapi import FastAPI, File, UploadFile, Form
from database.write_to_data import load_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/face_registration")
def image_reg(name_img: str = Form(default=None, max_length=50), image:UploadFile = File(...)):
    img_str = image.file.read() 
    msg = face_regist(img_path=img_str, name_img=name_img)
    return {
        "msg":msg,
        "name_img":name_img
    }


@app.post("/face_recognition")
def image_rec(image:UploadFile = File(...)):
    img_str = image.file.read() 
    database = load_data()
    min_dist, identity = face_recog(img_path=img_str, database=database)
    return {
        "distance":min_dist,
        "identity":identity
    }
