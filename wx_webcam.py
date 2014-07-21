import wx
import cv2

class webcamWindow(wx.Panel):

	def __init__(self, parent, camera, fps=10):
		wx.Panel.__init__(self, parent)
		panel = wx.Panel(self, -1)
		
		wx.Button(panel, -1, "Capture", (210,660))
		
		self.camera = camera
		ret_value, frame = self.camera.read()
		height, width = frame.shape[:2]
		parent.SetSize((width, (height+75)))
		
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = cv2.flip(frame, 1)
		self.bmp = wx.BitmapFromBuffer(width, height, frame)
		
		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)
		
	def OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)
	def NextFrame(self, e):
		ret_value, frame = self.camera.read()
		if ret_value:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame = cv2.flip(frame, 1)
			self.bmp.CopyFromBuffer(frame)
			self.Refresh()
			
camera = cv2.VideoCapture(0)

app = wx.App()
frame = wx.Frame(None, -1, "Webcam")
cap = webcamWindow(frame, camera)
frame.Show()
app.MainLoop()
