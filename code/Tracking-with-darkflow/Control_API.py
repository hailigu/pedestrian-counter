__author__ = 'gongjia'

EXCLUDE_SIGN = '~'
EXCLUDE = lambda x: EXCLUDE_SIGN + str(x)

from darkflow.darkflow.defaults import argHandler  # Import the default arguments
from darkflow.darkflow.net.build import TFNet
from threading import Thread
import os

class control_p(object):
    '''api for flask'''
    def __init__(self, filename, list_xy):

        self.FLAGS = argHandler()
        self.FLAGS.setDefaults()

        self.FLAGS.demo = filename  # video file to use, or if camera just put "camera"
        self.FLAGS.model = "darkflow/cfg/yolo.cfg"  # tensorflow model
        self.FLAGS.load = "darkflow/bin/yolo.weights"  # tensorflow weights
        self.FLAGS.threshold = 0.25  # threshold of decetion confidance (detection if confidance > threshold )
        self.FLAGS.gpu = 0.9  # how much of the GPU to use (between 0 and 1) 0 means use cpu
        self.FLAGS.track = True  # wheither to activate tracking or not
        self.FLAGS.trackObj = "person"  # the object to be tracked
        self.FLAGS.saveVideo = True  # whether to save the video or not
        self.FLAGS.BK_MOG = False  # activate background substraction using cv2 MOG substraction,
        # to help in worst case scenarion when YOLO cannor predict(able to detect mouvement, it's not ideal but well)
        # helps only when number of detection < 5, as it is still better than no detection.
        self.FLAGS.tracker = "deep_sort"  # wich algorithm to use for tracking deep_sort/sort (NOTE : dffpl   eep_sort only trained for people detection )
        self.FLAGS.skip = 2  # how many frames to skipp between each detection to speed up the network
        self.FLAGS.csv = False  # whether to write csv file or not(only when tracking is set to True)
        self.FLAGS.display = False  # display the tracking or not
        # FLAGS.queue = 10
        self.FLAGS.list_xy = list_xy
        self.FLAGS.counter = True
        self.tfnet = TFNet(self.FLAGS)

    def setcoo_p(self, list_xy):
        self.tfnet.camera_set(list_xy)
    
    def start_p(self):
        self.pstart = Thread(target=self.tfnet.camera)
        self.pstart.setDaemon(True)
        self.pstart.start()

    def stop_p(self):
        self.tfnet.camera_stop()

    def pause_p(self):
        self.tfnet.camera_pause()

    def resume_p(self):
        self.tfnet.camera_resume()

    def get_p(self):
        return self.tfnet.camera_get()

# test demo
# status:  strat  resume: 0    stop: 1   pause:2
if __name__ == '__main__':
    list_xy = [(32,32), (100, 100), (140, 140), (200,200), (100,50),(100,300), (200,58),(200,300)]
    list_xy2 = [(32,32), (180, 180), (140, 140), (250,250), (100,50),(100,300), (200,58),(200,300)]
    handle_p = control_p("test.avi", list_xy)
    handle_p.start_p()
    count = 0
    test = 0
    while True:
        count += 1

        # spend about 0.5s
        if count == 999999:
            test += 1
            count = 0
            #print (test)

        if test == 300:
            test += 1
            #handle_p.pause_p()
            #status = handle_p.get_p()
            handle_p.setcoo_p(list_xy2)
            #break

