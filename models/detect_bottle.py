import cv2 as cv

def detect_bottle(url, 
                  thresh_low=90, 
                  thresh_high=200, 
                  contour_cutoff=300, 
                  midline_x=500):
    """
    Detects whether a bottle is present.
    Parameters:
        - url: image link
        - thresh_low: lower bound for theresholding, defaulted at 90
        - thresh_higher: higher bound for theresholding, defaulted at 200
        - contour_cutoff: number of contours to cut off, defaulted at 300
        - midline_x: x coordinate of an imaginary vertical line by which a bottle 
        must pass to be considered present on the screen. Defaulted at 500.
    Return:
        - True if a bottle is detected, False otherwise.
    """
    im = cv.imread(url, cv.IMREAD_GRAYSCALE)
    _, thresh = cv.threshold(im, thresh_low, thresh_high, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    try: #handle edge cases where there are fewer than 300 contours.
        contours = contours[contour_cutoff:0:-1]
    except:
        pass

    cmax = max(contours, key = cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cmax)
    
    #==========================================================================
    # CODE FOR SHOWIMG IMAGE & CALIBRATNG
    # cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    # cv2.imshow(im)
    #==========================================================================

    if x + w > midline_x and w > 280 and h > 280:
        return True
    else:
        return False
