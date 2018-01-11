
### Intro

The purpose of this little project is to add object tracking to yolov2 and achieve real-time multiple object tracking.

The current architecture is set to only track one type of objects, but it should be easy to generalise over all objects.

Currently support people tracking (as the provided weights for deep_sort were trained on people tracking)


### Dependencies
python
numpy
opencv 3
tensorflow 1.0
Cython.
sklean.


for using sort :
scikit-learn
scikit-image
FilterPy


## RUN 
you just have to run python run.py, 
for example choice deepsort or sort.
> deep_sort is build upon sort , it uses deep encoders to build features for each detected box and match it with it's corresponding box in next frame, 
I've put links to both of them in the readme file , you can find more info there
---
Arguments:
--summary path to TensorBoard summaries directory

--momentum applicable for rmsprop and momentum optimizers

--load how to initialize the net? Either from .weights or a checkpoint, or even from scratch

--saveVideo Records video from input video or camera

--lr learning rate

--labels path to labels file

--verbalise say out loud while building graph

--imgdir path to testing directory with images

--help, --h, -h show this super helpful message and exit

--epoch number of epoch

--savepb save net and weight to a .pb file

--annotation path to annotation directory

--train train the whole net

--queue process demo in batch

--trainer training algorithm

--demo demo on webcam

--batch batch size

--gpu how much gpu (from 0.0 to 1.0)

--metaLoad path to .meta file generated during --savepb that corresponds to .pb file

--model configuration of choice

--gpuName GPU device name

--threshold detection threshold

--config path to .cfg directory

--save save checkpoint every ? training examples

--binary path to .weights directory

--pbLoad path to .pb protobuf file (metaLoad must also be specified)

--json Outputs bounding box information in json format.

--keep Number of most recent training results to save

--dataset path to dataset directory

--backup path to backup folder
