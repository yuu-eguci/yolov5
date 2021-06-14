yuu-eguci/yolov5
===

📷 This is the repository forked from the ultralytics/yolov5. Purposes what this repository aims for are to experience until "putting rectangles on my own image" and to peek in the dataset for seeing images have rectangles by annotation files, by myself.

## Original README.md

[README-original.md](README-original.md)

## Until putting rectangles on my own image

```bash
git clone https://github.com/yuu-eguci/yolov5

# NOTE: なぜか pipenv では Locking Failed! が出る。
#       ンモー、機械学習系はこんなんばっかし。
#       pipenv でやるんだったら Locking Failed! を見たあとに、 pip install -r requirements.txt しましょ。
python3 -m pip install -r requirements.txt

# 学習させる。
# 細かいコマンドライン引数のイミは把握してない。
python3 train.py --img 640 --batch 16 --epochs 10 --data coco128.yaml --weights yolov5s.pt

# data/images/*** の画像を detect する。
# レクタングルをつけた画像は runs/detect/exp/*** に格納される。
python3 detect.py --source data/images --weights yolov5s.pt --conf 0.50
```

## Until seeing images in the dataset

### Install labelimg

```bash
git clone https://github.com/tzutalin/labelImg
cd ./labelImg
brew install python3
pip3 install pipenv
pipenv --three
pipenv shell
pip install pyqt5 lxml
make qt5py3  # Displays... -> pyrcc5 -o libs/resources.py resources.qrc
rm -rf build dist
python setup.py py2app
cp -rf dist/labelImg.app /Applications
```

- Download dataset
    - https://github.com/ultralytics/yolov5/releases/download/v1.0/coco128.zip
- Put coco128 images and labels all in one folder
- Make classes.txt; Content are below ⬇️; You can see them in data/coco128.yaml
- Put classes.txt in the folder you made above.
- Open labelimg.
- "Open dir" > Select the folder you made.
    - You may need to set the folder at "Change Save Dir" too.

```plaintext
person
bicycle
car
motorcycle
airplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
couch
potted plant
bed
dining table
toilet
tv
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush
```
