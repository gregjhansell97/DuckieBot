import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
    horizontal_img = cv2.flip( img, 0 )
    vertical_img = cv2.flip( img, 1 )
    both_img = cv2.flip( img, -1 )

    cv2.imshow( "Original", img )
    cv2.imshow( "Horizontal flip", horizontal_img )
    cv2.imshow( "Vertical flip", vertical_img )
    cv2.imshow( "Both flip", both_img )
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()