import cv2
cv2.namedWindow("Webcam")
camera_id = 0

camera = cv2.VideoCapture(camera_id)

if camera.isOpened(): #ensure opening
	return_value, image = camera.read()
else:
	return_value = False
	print "Cannot establish connection with camera!"

while return_value:
	cv2.imshow("Webcam",image)
	return_value, image = camera.read()
	key = cv2.waitKey(20)
	if key == 27:
		break
cv2.destroyAllWindows()