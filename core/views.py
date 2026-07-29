"""

"""

###################################
## Django file:
from base64 import b64encode
from django.conf import settings ## give access to vraibles and models that we uploaded settings.py file. 
from django.core.files.storage import default_storage ##
from django.core.files.storage import  FileSystemStorage
from django.shortcuts import render ##  
###################################
##
import numpy as np
import cv2 
##############################################
## deep pakages
import tensorflow as tf
import keras 
##############################################
from Tools_stega89_de1.tools_TFLite_decoder import read_message
###################################
from FarhadCV.Tools import tcolors, bcolors
# from django.db import models 
# from .model import selector1
from core import models

from django import forms


#######################################################
######                                       ######
#######################################################
def splash(request):
    return render(request, 'splash.html')


#######################################################
######                                       ######
#######################################################
def index(request):
    
    name_detector  = models.selector_detector(request)
    # results  = selector1(request)
    if request.method == 'POST':

        
        ##########################################
        ## Django image API
        ## upload the file
        
        message_reuslts = ""
        try:
            request_file = request.FILES['imageFile']  ## imagesFile is name that choose in html file to input data
            # field_name = forms.ImageField['imageFile']
            # print(tcolors.BLUE,"request_file:", request_file, tcolors.ENDC)
            ##########################################
            fs = FileSystemStorage()
            file_name = fs.save(request_file.name, request_file)
            file_path = fs.path(file_name)

            # image = request.FILES["imageFile"].read()
            # imgtest = b64encode(image)
            # form = ImageUploadForm(request.POST, request.FILES)
            # image = form.cleaned_data['image']

            # imgResp = urllib.request.urlopen(self.url)
            # imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
            # imgtest= cv2.imdecode(imgNp,-1)
            ##########################################
            # print(tcolors.RED,"field_name:", field_name,tcolors.ENDC)
            print(tcolors.RED,"name_detector: ", name_detector,tcolors.ENDC)
            

            #########################################
            ## Read Image:
            try:
                imgtest = cv2.imread(file_path)
                imgtest = cv2.cvtColor(imgtest, cv2.COLOR_BGR2RGB)
            except:
                cap = cv2.VideoCapture(file_path)
                ret, imgtest = cap.read()
                print(tcolors.BLUE, imgtest.shape, tcolors.ENDC)

            size_img = (imgtest.shape[0], imgtest.shape[1])
            #########################################
            ## Detect the encoded part of the image:

            name_decector = settings.DETECT_ROUTER.choose_model(name_detector)
            try:
                croped_face, points = settings.DETECT_ROUTER(imgtest)
                message_reuslts += f"Detector: {name_decector}"
            except Exception as e: 
                message_reuslts += f"Can not use {name_decector} - {e}"
                croped_face = imgtest.copy()
            
            croped_face2 = cv2.cvtColor(croped_face, cv2.COLOR_RGB2BGR)
            croped_face2 = cv2.resize(croped_face2, (size_img[1], size_img[0]))
            cv2.imwrite(f"./media/Encoded_faces/{file_name}", croped_face2)

          
            ##########################################
            ## Run StampOne Decoder
            binery_message = settings.STAMPONE_DECODER(croped_face)
            message, message_error = read_message(Message=binery_message, 
                        BCH_BITS= 25, # 13, 7, 21, 44 
                        BCH_POLYNOMIAL=487, #487#137#8219, 20023, 
                        bits= 256, 
                        size=16, 
                        pad=0)
            message_reuslts += f"- {message_error}"
            if message== "None":
                color = "red"
            else:
                color = "green"
            file_root = "Croped_encoded_Image.jpg" #f"media/{file_name}"
        except Exception as e: 
            print("you Do not upload a pic!!")
            message = ""
            file_name = "ZNo-Image.png"
            color = "red"
            name_decector = "None"
            message_reuslts = f"you Do not upload a pic!! - L101 - {e}" 
        ##########################################
        # print(tcolors.RED, 'Predicted:', label, tcolors.ENDC)
        return render(request, "index.html", {"predictions": message, 
                                              "Image":file_name, 
                                              'answer':name_decector, 
                                              "color":color,
                                              "message_reuslts":message_reuslts,
                                              })
    else:
        message = ""
        file_name = "ZNo-Image.png"
        color = "red"
        name_decector = "None"
        message_reuslts = "StampOne Decoder"
        return render(request, 'index.html',{"predictions": message, 
                                              "Image":file_name, 
                                              'answer':name_decector, 
                                              "color":color,
                                              "message_reuslts":message_reuslts,
                                              })
   


# def about(request):
#     if request.method == 'GET':
#         print(tcolors.GREEN, "It is ok!!: ", tcolors.ENDC)
#         print(tcolors.GREEN, "request: ", request, tcolors.ENDC)


#         form = request.get('Detection')#(request.POST)
#         print(tcolors.GREEN, "form: ", form, tcolors.ENDC)

#         answer = "None"
#         if form.is_valid():
#             answer = form.cleaned_data['value']
            
#         print(tcolors.GREEN, "answer: ", answer, tcolors.ENDC)

#     return render(request, {"answer":answer})