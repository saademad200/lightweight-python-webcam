import wx
import cv2
import numpy as np
import os

"""
requires wx, cv2, and numpy to run. the frozen exe is ~36MB

Help was obtained from the following urls:

http://stackoverflow.com/questions/14804741/opencv-integration-with-wxpython
http://stackoverflow.com/questions/24856687/wxpython-button-widget-wont-move

"""

current_directory = ''
iteration = 1
mirror = True

class webcamPanel(wx.Panel):
	
	def __init__(self, parent, camera, fps=10):
		global mirror
		
		wx.Panel.__init__(self, parent)
		
		self.camera = camera
		return_value, frame = self.camera.read()
		height, width = frame.shape[:2]
		
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		if mirror:
			frame = cv2.flip(frame, 1)
		self.bmp = wx.BitmapFromBuffer(width, height, frame)
		
		
		self.SetSize((width,height))
		self.GetParent().GetParent().SetSize((width,height+123))
		
		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)
		
	def OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)
		
	def NextFrame(self, e):
		return_value, frame = self.camera.read()
		if return_value:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			if mirror:
				frame = cv2.flip(frame, 1)
			self.bmp.CopyFromBuffer(frame)
			self.Refresh()
			
class mainWindow(wx.Frame):
	def __init__(self, camera):
		
		#set up directory to save photos
		global current_directory
		current_directory = os.getcwd()
		
		#inheritence
		wx.Frame.__init__(self, None)
		self.Title = "webcam"
		#menubar
		menubar = wx.MenuBar()
		
		filemenu = wx.Menu()
		change_dir = filemenu.Append(-1, 'Change Directory', "Change the directory to save Photos")
		menubar.Append(filemenu, '&File')
		
		optionsmenu = wx.Menu()
		self.mirrorcheckbox = optionsmenu.AppendCheckItem(-1, 'Mirror Image', "Mirror")
		optionsmenu.Check(self.mirrorcheckbox.GetId(), True)
		menubar.Append(optionsmenu,'&Options')
		
		self.SetMenuBar(menubar)
		
		
		#main ui
		self.panel = wx.Panel(self, -1)
		self.webcampanel = webcamPanel(self.panel, camera)
		webcampanelsize = self.webcampanel.GetSize()
		self.button = wx.Button(self.panel, label="Take Picture!", pos=(0,webcampanelsize.height), size=(webcampanelsize.width,75))
		

		
		self.Bind(wx.EVT_MENU, self.change_dir, change_dir)
		self.Bind(wx.EVT_MENU, self.mirror, self.mirrorcheckbox)
		self.Bind(wx.EVT_BUTTON, self.take_picture, self.button)
			
	def change_dir(self, e):
		#declare global variables
		global current_directory
		global iteration
		#open the choose folder directory
		dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
		#wait for the okay
		if dialog.ShowModal() == wx.ID_OK:
			#grab the new directory
			current_directory = dialog.GetPath()
		#close the window
		dialog.Destroy()
		#reset the count for files
		iteration = 1

	def mirror(self, e):
		global mirror
		mirror = self.mirrorcheckbox.IsChecked()
			
		
	def take_picture(self, e):
		#declare global variables
		global current_directory
		global iteration
		global mirror
		
		#get current frame from camera
		camera.set(3,1920)
		camera.set(4,1080)
		return_value, image = camera.read()
		#check to see if you should mirror image
		if mirror:
			image = cv2.flip(image, 1)
		#get the directory to save it in.
		filename = current_directory + "/000" + str(iteration) + ".png"
		#update the count
		iteration += 1
		#save the image
		cv2.imwrite(filename,image)
		#read the image (this is backwards isn't it?!
		saved_image = cv2.imread(filename)
		#show the image in a new window!
		cv2.imshow('Snapshot!',saved_image)
		camera.set(3, 640)
		camera.set(4,480)
		
		

camera = cv2.VideoCapture(0)

app = wx.App()
window = mainWindow(camera)
window.Show()
app.MainLoop()