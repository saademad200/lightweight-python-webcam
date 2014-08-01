import cv2
import time
cv2.namedWindow("Webcam")
camera_id = 0

camera = cv2.VideoCapture(camera_id)
camera.set(3, 1920)
camera.set(4,1080)
if camera.isOpened(): #ensure opening
	return_value, image = camera.read()
else:
	return_value = False
	print "Cannot establish connection with camera!"

stop = time.time() + 10
frame = 0
while time.time() < stop:
	cv2.imshow("Webcam",image)
	return_value, image = camera.read()
	frame += 1
	print frame
	key = cv2.waitKey(20)
	if key == 27:
		break
cv2.destroyAllWindows()
camera.release()
print float(frame/10)