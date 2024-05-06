from fastapi import FastAPI, UploadFile, File,Response,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os,uuid,datetime
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
# print(tf.config.list_physical_devices('GPU'))

classes = ['Abyssinian','Bengal','Birman','Bombay','British_Shorthair','Egyptian_Mau','Maine_Coon','Persian','Ragdoll','Russian_Blue','Siamese','Sphynx']
image_size = 224
model = load_model('./results/model.h5', compile=False)

origins = [
"*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
    
)

@app.post("/v1")
async def process_image(file: UploadFile=None):
    dt_now = datetime.datetime.now()
    if file is None:
        raise HTTPException(status_code=403, detail="Image not Upload.")
    filename = uuid.uuid4()
    with open(f"./temp/{filename}.png", "wb") as stream_img:
        stream_img.write(file.file.read())
    img = image.load_img(os.path.join("./temp", f"{filename}.png"), target_size=(image_size,image_size))
    img = image.img_to_array(img)
    data = np.array([img])
    data = data/image_size
    #変換したデータをモデルに渡して推論
    result = model.predict(data)[0]
    predicted = result.argmax()
    per = int(result[predicted]*100)
    print(f"============\nリクエスト時間：{dt_now}\n判定結果：{classes[predicted]}\n可能性：{per}%\n============")
    #使い終わったファイルは消しておく
    os.remove(f"./temp/{filename}.png")
    probability = "{}".format(per)
    return {"result": classes[predicted],"probability":probability}
