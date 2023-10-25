import cv2
import time
from emailing import send_email, clean_folder
import glob
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    # check returns True, image is captured
    # frame contains the array object
    check, frame = video.read()
    # The frame is converted to gray scale to speed up the process.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # GaussianBlur is done to improve speed. (21,21) amount of blur and 0 is stnd deviation
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
    # difference between first frame and current frame is depicted by white color on the screen
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # assignment of pixel above 30 with 255 ( white) so the image diff is show in white
    # Return a list, second value in the list is the array object with max value applied
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contour of the image
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # All contours resulting are looped depending on its size
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        # x,y Coordinate and the width and height of the contours are obtained
        x, y, w, h = cv2.boundingRect(contour)
    # Rectangular frame on frame array, x,y coordinate, opposite end of the rectangle, color of the line and its width
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, ), 3)
        if rectangle.any():
            status = 1
            # writing the captured frame into images folder
            cv2.imwrite(f'images/{count}.png', rectangle)
            count = count + 1
            all_images = glob.glob('images/*.png')
            print(all_images)
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)
    # checks for the status 1 (when the image appears on screen) and status 0 (when the img goes out.)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args= (image_with_object,))
        email_thread.daemon = True

        email_thread.start()


    cv2.imshow('my_video', frame)
    # user input key is recorded
    key = cv2.waitKey(1)
    # if the input key 'q' is pressed, then it loops out
    if key == ord('q'):
        break

video.release()
clean_folder()

