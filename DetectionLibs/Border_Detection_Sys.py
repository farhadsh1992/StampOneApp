import numpy as np
import cv2
from FarhadCV.Tools import tcolors, bcolors


#########################################################################################
#####                                                 #####
#########################################################################################
class add_purple_border():
    def __init__(self, bordersize:int=5):
        self.bordersize = bordersize
    def crop_face(image: np.array, bordersize:int=5)->np.float32:
        image_border = cv2.copyMakeBorder(
            image,
            top    = bordersize,
            bottom = bordersize,
            left   = bordersize,
            right  = bordersize,
            borderType = cv2.BORDER_CONSTANT,
            value = [255, 0, 255]
        )
        return image_border



#########################################################################################
#####                                                 #####
#########################################################################################
class code_detection():
    def __init__(self, method:str="border", debug:bool=True):
        self.method = method
        self.debug = debug

    def crop_face(self, frame: np.array, method:str="border", debug:bool=True)->np.float32:
        if method == "border":
            
            # Solid color border detection
            mat = np.array(frame)
            gray = cv2.cvtColor(mat, cv2.COLOR_RGBA2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            edged = cv2.Canny(gray, 70, 75)
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            boundary = None
            largestarea = 0
            for c in contours:
                # Approximate the contour
                peri = cv2.arcLength(c, True)
                area = cv2.contourArea(c)
                poly = cv2.approxPolyDP(c, 0.03 * peri, True)
                # If the polygon has 4 sides and its area occupies at least 10% of the image area
                if len(poly) == 4 and area > 0.1 * mat.shape[0] * mat.shape[1]:
                    if boundary is None or largestarea < area:
                        largestarea = area
                        boundary = poly
                    # print(peri, area, len(approx), ((peri / 4) ** 2) / area)

            border = boundary.reshape(-1, 2)
            minxy = border.min(axis=0)
            maxxy = border.max(axis=0)
            xlim = [minxy[0], maxxy[0]]
            ylim = [minxy[1], maxxy[1]]
            cropped = mat[ylim[0]:ylim[1], xlim[0]:xlim[1], :]
            
            
            # boxes = [contours[4]]
            boxes = contours
            
            boxes1 = [int(((xlim[1]-xlim[0])/2)), int(((ylim[1]- ylim[0])/2)+ylim[0])]
            # boxes1 = [int(((ylim[1]- ylim[0])/2)), int(((xlim[1]-xlim[0])/2))]

            if debug:
                # Draw debug information onto frame before outputting it
                cv2.drawContours(frame, boxes, -1, (60, 160, 102), 4)
                cv2.drawContours(frame, boxes[:2], -1, (0, 0, 255), 3)
            #     cv2.drawContours(output, east_corners, -1, (0, 255, 0), 3)
            #     cv2.drawContours(output, south_corners, -1, (255, 0, 0), 3)
            # #cv2.drawContours(output, tiny_squares, -1, (128, 128, 0), 2)
            return cropped, boxes #, boxes1
        
        elif method == "qr":
            # QR-Code finding pattern detector
            codes, debugout, squares = pattern_reader.extract(np.array(frame), True)
            Image.fromarray(debugout).save("debugout.jpg")
            # Image.fromarray(squares).save("squares.jpg")
            encoded_image = np.array(codes[0])
            return encoded_image