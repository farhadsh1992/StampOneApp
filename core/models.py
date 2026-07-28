





from django.http import HttpResponse
from django.shortcuts import render
from FarhadCV.Tools import tcolors, bcolors

def selector_detector(request):
    if request.method == 'POST':

        results = request.POST.get("detection")
        print(tcolors.BLUE, "results: ", results, tcolors.ENDC)
        if results == None:
            results = "FaceDetection"
        return results
    else:
        return "FaceDetection"

