
# from core.model import selector1
from DetectionLibs.Face_Detection_System import Face_Detection_System_v23
from DetectionLibs.Border_Detection_Sys import code_detection
import tensorflow as tf
from FarhadCV.Tools import tcolors, bcolors

class Detection_Models():
    def __init__(self,):

        ## use select the model
        ## 0 = face-detection,# 1=object-detcetion,# 2=pink-border
        pass

    def choose_model(self, num_model):
        # num_model  = selector1(request)
        print(tcolors.RED,"num_model",num_model, tcolors.ENDC)

        if num_model == "FaceDetection" or num_model==None:
            name_decector = "PRNet-FaceDetection"
            self.detector_router = Face_Detection_System_v23(Kind_Model="kpt")
        elif num_model == "ObjectDetection":
            name_decector = "Alexa-ObjectDetection"
            pass
        elif num_model == "PinkBorder":
            name_decector = "OpenCV-BorderDetection"
            self.detector_router = code_detection()
            print(tcolors.GREEN, "name_decector: ", name_decector, tcolors.ENDC)
        elif num_model == "QRCode":
            name_decector = "QRCode-Pattern"
        else:
            raise NotImplementedError()
        return name_decector
    def __call__(self, encoded_img:tf.Tensor):
        croped_image = self.detector_router.crop_face(encoded_img)
        return croped_image