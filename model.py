import os,shutil,glob,keras
import numpy as np
from keras.applications.vgg16 import VGG16
from keras.models import Sequential,Model
from keras.layers import Dense,Flatten,Input
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from keras.optimizers import SGD
image_path = "./images/"
kind_list = ['Abyssinian','Bengal','Birman','Bombay','British_Shorthair','Egyptian_Mau',
             'Maine_Coon','Persian','Ragdoll','Russian_Blue','Siamese','Sphynx']

# アノテーションを作成
for i in kind_list:
    if os.path.exists(image_path+str(i)+'/') ==True:
        pass
    else:
        os.mkdir(image_path+str(i)+'/')

for i in kind_list:
    for j in range(1,300):
        if os.path.exists(image_path+str(i)+'_'+str(j)+'.jpg') ==False:
            pass
        else:
            shutil.move(image_path+str(i)+'_'+str(j)+'.jpg',
                        image_path+str(i)+'/')
img_cat=[] #画像（array）を格納するリスト
kind_label=[] #ラベルを格納するリスト　
#リストに入れる際の画像のサイズを指定
img_size = 224

for i in kind_list:
    for j in range(1,300):
        if os.path.exists(image_path+str(i)+'/'+str(i)+'_'+str(j)+'.jpg') ==False:
            pass
        else:
            #file_listのなかに画像ファイルのpathを取得
            file_list = glob.glob(image_path+str(i)+'/'+str(i)+'_'+str(j)+'.jpg')
            for file in file_list:
                img_path = file
                #画像を読み込む
                img = load_img(img_path, target_size=(img_size, img_size))
                #読み込んだ画像を配列に変換
                x = img_to_array(img)
                #作成したimg_catに配列に変換した画像データを格納
                img_cat.append(x)
                #猫の種類(kind_listのindex)をラベルとしてkind_labelのリストの中に入れる
                kind_label.append(kind_list.index(i))

X = np.array(img_cat)
X = X/224.0
#ラベルデータをダミー変数化
y = to_categorical(kind_label)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

input_tensor = Input(shape=(img_size, img_size, 3))
base_model = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

#base_modelのoutputからクラス分類する層を定義
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(256,activation='sigmoid'))
top_model.add(Dense(len(kind_list), activation='softmax'))

# base_modelとtop_modelを連結
model = Model(base_model.inputs, top_model(base_model.output))

# base_modelの層の重みを固定
for layer in model.layers[:19]:
    layer.trainable = False

# コンパイル
model.compile(loss='categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

model.summary()

# 学習
history=model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))
print(history.history)

#可視化
plt.plot(history.history['accuracy'], label="acc", ls="-", marker="o")
plt.plot(history.history['val_accuracy'], label="val_acc", ls="-", marker="x")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(loc="best")
plt.show()

# 精度の評価
scores = model.evaluate(X_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
#resultsディレクトリを作成
result_dir = './results'
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
# h5ファイルで保存
model.save(os.path.join(result_dir, 'model.h5'))