import cv2
import imutils
import pytesseract

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:\5_projects\python\python_projects\python\Tesseract data files\tesseract.exe'

# Load image
img = cv2.imread(r'D:\opencv\photos\new_large_cat\new_img\number_plate.webp')
cv2.imshow('normal image', img)

# # Convert to grayscale we will do this because reduce the complicaty of the image and reduce the dimensonalyt of the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscale', gray)

# Resize
resized = imutils.resize(gray, width=300)
cv2.imshow('resized', resized)

# Bilateral Filter ir reduse the noise fo the image

filtered_image = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
cv2.imshow('filtered image', filtered_image)

# Canny Edge Detection
#canny we find edges of the image
# Canny Edge Detection and canny and dmany algo only work for the grayscle images

canny = cv2.Canny(img, 125, 300)
cv2.imshow('canny edge', canny)

# Find contours
cnts, new = cv2.findContours(canny.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#Cv2 RETR_LIST ir retercies all the contious but does not creat any parent child redation ship
#cv3.chain_approx_simple it removes all the reduces points and compart the counter by saving the memory
#we will create a copy of our image to draw a countours

img1 = img.copy()
cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)
cv2.imshow('contours img1', img1)
#now we dont want all the counter we are intreseted in only number plate
#but cannot locat direct that so we sort bases of there area
#so we will sect thos area whcih are max we will select top 30 areas
#but it will give sort list in order of min to maximum
#so far that we will revers the order  the sorting 

# Sort contours by area
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCount = None

img2 = img.copy()
cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)
cv2.imshow('number plate img2', img2)

# Loop through contours
count = 0
name = 1
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    if len(approx) == 4:
        NumberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_img = img[y:y+h, x:x+w]
        cv2.imwrite(str(name) + '.png', crp_img)
        name += 1
    cv2.drawContours(img, [NumberPlateCount], -1, (0, 255, 0), 3)
    cv2.imshow('final image', img)
    
    crop_img_loc = '1.png'
    cv2.imshow('cropped img', cv2.imread(crop_img_loc))
    
    
text = pytesseract.image_to_string(crop_img_loc, lang='eng', config='--tessdata-dir "D:/5_projects/python/python_projects/python/tessdata"')
print('Text:', text)
    

key = cv2.waitKey(0)
if key == 27:
    cv2.destroyAllWindows()

