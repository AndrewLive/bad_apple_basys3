# importing the necessary libraries
import cv2
import numpy as np

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('./bad_apple_32x32_7fps.mkv')

print(cap.isOpened())
# Loop until the end of the video
i = 0
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    print("frame "+str(i))

    if ret == False:
        break

    # save the resulting frame
    # cv2.imwrite('./bad_apple_32x32_8fps_frames/bad_apple_' + str(i) + '.png', frame)
    i += 1

    # conversion of BGR to grayscale is necessary to apply this operation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # adaptive thresholding to use different threshold
    # values on different regions of the frame.
    ThreshRet, Thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'./bad_apple_32x32_7fps_frames/bad_apple_thresh_{i:04}.png', Thresh)

    # cv2.imshow('Thresh', Thresh)
    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()