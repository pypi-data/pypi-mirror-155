import streamlit as st
from PIL import Image
import cv2 
import numpy as np
import cv2
from  PIL import Image, ImageEnhance
#image = Image.open(r't12.png') #Brand logo image (optional)
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline

import albumentations as A
import random 
import numpy as np
import matplotlib.pyplot as plt  
#%matplotlib inline
from PIL import Image
from IPython.display import display

# Loading pre-trained parameters for the cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 






class image_preprcessing():
    
    #get image properties
    def image_properties(self,img):
        print("Image Properties")
        print("- Number of Pixels: " + str(img.size))
        print("- Shape/Dimensions: " + str(img.shape))
        return img.size,img.shape
    
    
    #resize image
    def resize_imge(self,img,image_size1,image_size2):
        resized_pic = cv2.resize(img,(image_size1,image_size2))
        plt.imshow(resized_pic)  
        return resized_pic
    #rotate image
    def roatate_image(self,img):
        rotate = cv2.flip(img,-1) #you also can pass value like--> 0,1,-1 etc.
        #plt.imshow(rotate)
        return rotate
    
    def crop_image(self,img,x,y,w,h):
        #print(img.shape)
        # x=int(input("Enter Start point on x axis:"))
        # y=int(input("Enter Start point on y axis:"))

        # w=int(input("Enter width of cropped image:"))
        # h=int(input("Enter height of cropped image:"))

        cropped_image = img[y:y+h, x:x+w] # Cropping using Slicing
        #plt.axis("off")
        #cropped_image  = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        #plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        #plt.show() # Display the original image
        #print(cropped_image.shape)
        return cropped_image
    #thersolding
    def  thresholding(self,img,t1,t2): 
        # Perform binary thresholding on the image with T = 125
        r, threshold = cv2.threshold(img,t1,t2 ,cv2.THRESH_BINARY)
        #cv2_imshow(threshold)

        plt.figure(figsize=(10,18))

        plt. imshow(threshold)
        plt. title('my picture')
        return threshold
        
    #gray scale
    def gray_scale(self,img):
        # Grayscale version of the input:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Display grayscale version
        plt.figure(figsize=(10,18))

        plt. imshow(gray)
        plt. title('my picture')
        return gray
    
    #extract bit plane
    def extract_bit_plane(self,cd):
        #  extracting all bit one by one 
        # from 1st to 8th in variable 
        # from c1 to c8 respectively 
        c1 = np.mod(cd, 2)
        c2 = np.mod(np.floor(cd/2), 2)
        c3 = np.mod(np.floor(cd/4), 2)
        c4 = np.mod(np.floor(cd/8), 2)
        c5 = np.mod(np.floor(cd/16), 2)
        c6 = np.mod(np.floor(cd/32), 2)
        c7 = np.mod(np.floor(cd/64), 2)
        c8 = np.mod(np.floor(cd/128), 2)
        # combining image again to form equivalent to original grayscale image 
        cc = 2 * (2 * (2 * c8 + c7) + c6) # reconstructing image  with 3 most significant bit planes
        to_plot = [cd, c1, c2, c3, c4, c5, c6, c7, c8, cc]
        fig, axes = plt.subplots(nrows=2, ncols=5,figsize=(10, 8), subplot_kw={'xticks': [], 'yticks': []})
        fig.subplots_adjust(hspace=0.05, wspace=0.05)
        for ax, i in zip(axes.flat, to_plot):
            ax.imshow(i, cmap='gray')
        plt.tight_layout()
        plt.show()
        return cc
    
    #edge detection
    def edge_detect(self,image):
         #Edge Detection and Image Gradients
        #image= cv2.imread('t1.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hgt, wdt,_ = image.shape
        # Sobel Edges
        x_sobel = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
        y_sobel = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        plt.figure(figsize=(20, 20))
        plt.subplot(3, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        plt.subplot(3, 2, 2)
        plt.title("Sobel X")
        plt.imshow(x_sobel)
        plt.subplot(3, 2, 3)
        plt.title("Sobel Y")
        plt.imshow(y_sobel)
        sobel_or = cv2.bitwise_or(x_sobel, y_sobel)
        plt.subplot(3, 2, 4)
        plt.imshow(sobel_or)
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        plt.subplot(3, 2, 5)
        plt.title("Laplacian")
        plt.imshow(laplacian)
        ## There are two values: threshold1 and threshold2.
        ## Those gradients that are greater than threshold2 => considered as an edge
        ## Those gradients that are below threshold1 => considered not to be an edge.
        ## Those gradients Values that are in between threshold1 and threshold2 => either classiﬁed as edges or non-edges
        # The first threshold gradient
        cat = cv2.Canny(image, 50, 120)
        plt.subplot(3, 2, 6)
        plt.imshow(cat)
        return x_sobel,y_sobel,sobel_or,laplacian,cat 
    #Dilation, Opening, Closing And Erosion---used to removing noises, finding an intensity hole or bump in an image 
    def dilation(self,image):
                
        #image = cv2.imread('t1.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(3, 2, 1)
        plt.title("Original")
        plt.imshow(image)

        kernel = np.ones((5,5), np.uint8)

        erosion = cv2.erode(image, kernel, iterations = 1)
        plt.subplot(3, 2, 2)
        plt.title("Erosion")
        plt.imshow(erosion)
        dilation = cv2.dilate(image, kernel, iterations = 1)
        plt.subplot(3, 2, 3)
        plt.title("Dilation")
        plt.imshow(dilation)

        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        plt.subplot(3, 2, 4)
        plt.title("Opening")
        plt.imshow(opening)

        closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        plt.subplot(3, 2, 5)
        plt.title("Closing")
        plt.imshow(closing)
        return erosion,opening,closing,

    #image Sharpening
    def image_sharpening(self,image):
        #image sharpening
        #image = cv2.imread('t1.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(1, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        kernel_sharpening = np.array([[-1,-1,-1], 
                                      [-1,9,-1], 
                                      [-1,-1,-1]])
        sharpened = cv2.filter2D(image, -1, kernel_sharpening)
        plt.subplot(1, 2, 2)
        plt.title("Image Sharpening")
        plt.imshow(sharpened)
        plt.show()
        return sharpened
    
    def brighten_image(self,image, amount):
        img_bright = cv2.convertScaleAbs(image, beta=amount)
        return img_bright


    def blur_image(self,image, amount):
        blur_img = cv2.GaussianBlur(image, (11, 11), amount)
        return blur_img


    def enhance_details(self,img):
        hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
        return hdr
    
    #image blurring
    def image_blurring(self,image):
        #blurring
        #image = cv2.imread('t1.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(2, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        kernel_3x3 = np.ones((4, 4), np.float32) / 9
        blurred = cv2.filter2D(image, -1, kernel_3x3)
        plt.subplot(2, 2, 2)
        plt.title("4x4 Kernel Blurring")
        plt.imshow(blurred)
        kernel_7x7 = np.ones((7, 7), np.float32) / 49
        blurred2 = cv2.filter2D(image, -1, kernel_7x7)
        plt.subplot(2, 2, 3)
        plt.title("7x7 Kernel Blurring")
        plt.imshow(blurred2)
        
    def blackandwhite(self,image):
        image = np.array(image.convert('RGB'))
        
        
        gray_scale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        #slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, 127, 255, cv2.THRESH_BINARY)
        return blackAndWhiteImage
                    
    #skew correction
    #Masking
    def apply_filter(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((5, 5), np.float32) / 15
        filtered = cv2.filter2D(gray, -1, kernel)
        plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        plt.title('Filtered Image')
        plt.show()
        return filtered
    # Thresholding 
    def apply_threshold(self,filtered):
        ret, thresh = cv2.threshold(filtered, 250, 255, cv2.THRESH_OTSU)
        plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
        plt.title('After applying OTSU threshold')
        plt.show()
        return thresh
    
    #to detect_contour
    def detect_contour(self,img, image_shape):
        canvas = np.zeros(image_shape, np.uint8)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
        plt.title('Largest Contour')
        plt.imshow(canvas)
        plt.show()

        return canvas, cnt
    #detech corners
    def detect_corners_from_contour(self,canvas, cnt):


        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx_corners = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
        approx_corners = sorted(np.concatenate(approx_corners).tolist())
        print('\nThe corner points are ...\n')
        for index, c in enumerate(approx_corners):
            character = chr(65 + index)
            print(character, ':', c)
            cv2.putText(canvas, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Rearranging the order of the corner points
        approx_corners = [approx_corners[i] for i in [0, 2, 1, 3]]

        plt.imshow(canvas)
        plt.title('Corner Points: Douglas-Peucker')
        plt.show()
        return approx_corners
    
    
    def get_destination_points(self,corners):
        """
        -Get destination points from corners of warped images
        -Approximating height and width of the rectangle: we take maximum of the 2 widths and 2 heights
        Args:
            corners: list
        Returns:
            destination_corners: list
            height: int
            width: int
        """

        w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
        w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
        w = max(int(w1), int(w2))

        h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
        h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
        h = max(int(h1), int(h2))

        destination_corners = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

        print('\nThe destination points are: \n')
        for index, c in enumerate(destination_corners):
            character = chr(65 + index) + "'"
            print(character, ':', c)

        print('\nThe approximated height and width of the original image is: \n', (h, w))
        return destination_corners, h, w
    
    #unwarp
    def unwarp(self,img, src, dst):
   
        h, w = img.shape[:2]
        H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
        print('\nThe homography matrix is: \n', H)
        un_warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)

        # plot

        f, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(img)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax1.plot(x, y, color='yellow', linewidth=3)
        ax1.set_ylim([h, 0])
        ax1.set_xlim([0, w])
        ax1.set_title('Targeted Area in Original Image')
        ax2.imshow(un_warped)
        ax2.set_title('Unwarped Image')
        plt.show()
        return un_warped

    #call skew coreection Function 
    def skew_croeection(self,image):

        #image = cv2.imread('notebook.jpeg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #plt.imshow(image)
        #plt.title('Original Image')
        #plt.show()

        filtered_image = aug.apply_filter(image)
        threshold_image = aug.apply_threshold(filtered_image)

        cnv, largest_contour = aug.detect_contour(threshold_image, image.shape)
        corners = aug.detect_corners_from_contour(cnv, largest_contour)

        destination_points, h, w = aug.get_destination_points(corners)
        un_warped = aug.unwarp(image, np.float32(corners), destination_points)

        cropped = un_warped[0:h, 0:w]
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        # f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(un_warped)
        ax2.imshow(cropped)

        plt.show()
        return cropped
    
    #resize image
    def resize_imge(self,img,image_size1=224,image_size2=224):
        resized_pic = cv2.resize(img,(image_size1,image_size2))
        plt.imshow(resized_pic)  
        return resized_pic
    #sepia effect
    def sepia(self,img):
        #img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
        img_sepia = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                        [0.349, 0.686, 0.168],
                                        [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        return img_sepia
        
    #Perspective transformation  
    def perspective_transformation(self,image):
        #image = cv2.imread('scan.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(1, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        points_A = np.float32([[320,15], [700,215], [85,610], [530,780]])
        points_B = np.float32([[0,0], [420,0], [0,594], [420,594]])
        M = cv2.getPerspectiveTransform(points_A, points_B)
        warped = cv2.warpPerspective(image, M, (420,594))
        plt.subplot(1, 2, 2)
        plt.title("warpPerspective")
        plt.imshow(warped)
     #Image Pyramids
    def image_pyramids(self,image):
        #image = cv2.imread('butterfly.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(2, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        smaller = cv2.pyrDown(image)
        larger = cv2.pyrUp(smaller)
        plt.subplot(2, 2, 2)
        plt.title("Smaller")
        plt.imshow(smaller)
        plt.subplot(2, 2, 3)
        plt.title("Larger")
        plt.imshow(larger)
   
    def find_conturs(self,image):
        # Load the data
        #image = cv2.imread('pic.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        plt.subplot(2, 2, 1)
        plt.title("Original")
        plt.imshow(image)
        # Grayscale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # Canny edges
        edged = cv2.Canny(gray, 30, 200)
        plt.subplot(2, 2, 2)
        plt.title("Canny Edges")
        plt.imshow(edged)
        # Finding Contours
        contour, hier = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        plt.subplot(2, 2, 3)
        plt.imshow(edged)
        print("Count of Contours  = " + str(len(contour)))
        # All contours
        all_contors = cv2.drawContours(image, contour, -1, (0,255,0), 3)
        plt.subplot(2, 2, 4)
        plt.title("Contours")
        plt.imshow(image)
        return all_contors
    




      


    
    #Line Detection Using Hough Lines    
    def line_detection(self, image):
        
        # Load the image
        #image = cv2.imread('sudoku.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        # Grayscale 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Canny Edges
        edges = cv2.Canny(gray, 100, 170, apertureSize = 3)
        # plt.subplot(2, 2, 1)
        # plt.title("edges")
        # plt.imshow(edges)
        # Run HoughLines Fucntion 
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        # Run for loop through each line
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x_1 = int(x0 + 1000 * (-b))
            y_1 = int(y0 + 1000 * (a))
            x_2 = int(x0 - 1000 * (-b))
            y_2 = int(y0 - 1000 * (a))
            image = cv2.line(image, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2)
        # Show Final output
        plt.subplot(2, 2, 2)
        plt.imshow(image)
        return image
    #Finding Corners  
    def finding_corners(self, image):
                # Load image 
        #image = cv2.imread('chessboard.png')
        # Grayscaling
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(10, 10))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # CornerHarris function  want input to be float
        gray = np.float32(gray)
        h_corners = cv2.cornerHarris(gray, 3, 3, 0.05)
        kernel = np.ones((7,7),np.uint8)
        h_corners = cv2.dilate(h_corners, kernel, iterations = 10)
        image[h_corners > 0.024 * h_corners.max() ] = [256, 128, 128]
        plt.subplot(1, 1, 1)
        # Final Output
        plt.imshow(image)
        return image
        
    #finding circles
    def counting_circles(self,image):
        # Load image
        #image = cv2.imread('blobs.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 20))
        detector = cv2.SimpleBlobDetector_create()
        # Detect blobs
        points = detector.detect(image)

        blank = np.zeros((1,1)) 
        blobs = cv2.drawKeypoints(image, points, blank, (0,0,255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        keypoints = detector.detect(image)
        number_of_blobs = len(keypoints)
        text = "Total Blobs: " + str(len(keypoints))
        cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 0, 255), 2)

        plt.subplot(2, 2, 1)

        plt.imshow(blobs)
        # Filtering parameters
        # Initialize parameter settiing using cv2.SimpleBlobDetector
        params = cv2.SimpleBlobDetector_Params()
        # Area filtering parameters
        params.filterByArea = True
        params.minArea = 100
        # Circularity filtering parameters
        params.filterByCircularity = True 
        params.minCircularity = 0.9
        # Convexity filtering parameters
        params.filterByConvexity = False
        params.minConvexity = 0.2
        #  inertia filtering parameters
        params.filterByInertia = True
        params.minInertiaRatio = 0.01
        # detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs
        keypoints = detector.detect(image)
        # Draw blobs on our image as red circles
        blank = np.zeros((1,1)) 
        blobs = cv2.drawKeypoints(image, keypoints, blank, (0,255,0),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        number_of_blobs = len(keypoints)
        text = "No.  Circular Blobs: " + str(len(keypoints))
        image = cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
        # Show blobs
        plt.subplot(2, 2, 2)
        plt.title("Filtering Circular Blobs Only")
        plt.imshow(blobs)
        return image

    #colour pencil sketch effect
    def pencil_sketch_col(self,img):
        #inbuilt function to create sketch effect in colour and greyscale
        sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
        return  sk_color

    #HDR effect
    def HDR(self,img):
        hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
        return  hdr

    # invert filter
    def invert(self,img):
        inv = cv2.bitwise_not(img)
        return inv
    #defining a function
    from scipy.interpolate import UnivariateSpline
    def LookupTable(self,x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))

    #summer effect
    def Summer(self,img):
        increaseLookupTable = aug.LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = aug.LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel  = cv2.split(img)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        sum= cv2.merge((blue_channel, green_channel, red_channel ))
        return sum
    #winter effect
    def Winter(self,img):
        increaseLookupTable = aug.LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = aug.LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel = cv2.split(img)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        win= cv2.merge((blue_channel, green_channel, red_channel))
        return win
    
    #carttoon image
    def cartoon_image(self,img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey = cv2.medianBlur(grey, 5)
        edges = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        #cartoonize
        color = cv2.bilateralFilter(img, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask = edges)
        
        return cartoon
    
    def water_color_art(self,image):
        image_resized = cv2.resize(image, None, fx=0.5, fy=0.5)
        image_cleared = cv2.medianBlur(image_resized, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)

        image_cleared = cv2.edgePreservingFilter(image_cleared, sigma_s=5)
        image_filtered = cv2.bilateralFilter(image_cleared, 3, 10, 5)

        for i in range(2):
            image_filtered = cv2.bilateralFilter(image_filtered, 3, 20, 10)

        for i in range(3):
            image_filtered = cv2.bilateralFilter(image_filtered, 5, 30, 10)
        gaussian_mask= cv2.GaussianBlur(image_filtered, (7,7), 2)
        image_sharp = cv2.addWeighted(image_filtered, 1.5, gaussian_mask, -0.5, 0)
        image_sharp = cv2.addWeighted(image_sharp, 1.4, gaussian_mask, -0.2, 10)
        return image_sharp
    def zoom(self,img, zoom_factor):
        zoom =  cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)
        return zoom
    def detect_faces_eyes(self,image):
        '''
        Function to detect faces/eyes and smiles in the image passed to this function
        '''

        
        #image = np.array(image.convert('RGB'))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Next two lines are for converting the image from 3 channel image (RGB) into 1 channel image
        # img = cv2.cvtColor(new_img, 1)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Passing grayscale image to perform detection
        # We pass grayscaled image because opencv expects image with one channel
        # Even if you don't convert the image into one channel, open-cv does it automatically.
        # So, you can just comment line number 26 and 27.
        # If you do, make sure that you change the variables name at appropriate places in the code below
        # Don't blame me if you run into errors while doing that :P
        
        faces = face_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=5)
        # The face_cascade classifier returns coordinates of the area in which the face might be located in the image
        # These coordinates are (x,y,w,h)
        # We will be looking for eyes and smile within this area instead of looking for them in the entire image
        # This makes sense when you're looking for smiles and eyes in a face, if that is not your use case then
        # you can pull the code segment out and make a different function for doing just that, specifically.


        # Draw rectangle around faces
        for (x, y, w, h) in faces:
            
            # The following are the parameters of cv2.rectangle()
            # cv2.rectangle(image_to_draw_on, start_point, end_point, color, line_width)
            cv2.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
            
            roi = image[y:y+h, x:x+w]
            
            # Detecting eyes in the face(s) detected
            eyes = eye_cascade.detectMultiScale(roi)
            
            # Detecting smiles in the face(s) detected
            smile = smile_cascade.detectMultiScale(roi, minNeighbors = 25)
            
            # Drawing rectangle around eyes
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
                
            # Drawing rectangle around smile
            for (sx,sy,sw,sh) in smile:
                cv2.rectangle(roi, (sx, sy), (sx+sw, sy+sh), (0,0,255), 2)

        # Returning the image with bounding boxes drawn on it (in case of detected objects), and faces array
        return image, faces
    def detect_faces(self,our_image):
        new_img = np.array(our_image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 5)
        return img, faces


aug  =  image_preprcessing()










