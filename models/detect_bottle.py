import cv2 as cv

def detect_bottle(im, 
                  thresh_low=90, 
                  thresh_high=200,
                  contour_cutoff=300, 
                  thresh_label_size=100,
                  contours_to_check=10):
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
    def bottle_found(x, y, w, d):
        return x <= midline_x and x + w >= midline_x and w > thresh_label_size and h > thresh_label_size
    
    midline_x = im.shape[1] / 3
    im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(im, thresh_low, thresh_high, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    if len(contours) == 0:
        return False
    contours.sort(key=cv.contourArea)

    i = len(contours) - 1
    while i >= 0 and contours_to_check > 0:
        x, y, w, h = cv.boundingRect(contours[i])
        
        # cv.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        # cv.imwrite('temp.jpg', im)

        if w < im.shape[1] / 2:
            contours_to_check -= 1
            if bottle_found(x, y, w, h):
                return True
        i -= 1
    
    return False
    
    #==========================================================================
    # CODE FOR SHOWIMG IMAGE & CALIBRATNG
    # cv.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    # cv.imshow('image', im)
    # cv.imwrite('temp.jpg', im)
    #==========================================================================

if __name__ == "__main__":
    img_path = "..\\images\\WIN_20201028_21_21_28_Pro.jpg"
    image = cv.imread(img_path)
    print(detect_bottle(image))
