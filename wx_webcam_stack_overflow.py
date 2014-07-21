import wx
import cv2

#---------------------------------------------------------------------- 

class webcamPanel(wx.Panel):

    def __init__(self, parent, camera, fps=10):
        wx.Panel.__init__(self, parent)

        self.camera = camera

        ret_value, frame = self.camera.read()
        height, width = frame.shape[:2]

        # resize panel with camera image
        self.SetSize( (width, height) )

        # resize main window
        self.GetParent().GetParent().SetSize( (width, height+75) )

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

#---------------------------------------------------------------------- 

class webcamWindow(wx.Frame):

    def __init__(self, camera, fps=10):
        wx.Frame.__init__(self, None)

        self.panel = wx.Panel(self, -1)

        # add panel with webcam image
        self.webcampanel = webcamPanel(self.panel, camera)

        # get size of webcam panel
        webcampanelsize = self.webcampanel.GetSize()

        # put button below webcam panel
        self.but = wx.Button(self.panel, label="Capture", pos=(0, webcampanelsize.height), size=(webcampanelsize.width,75))

#----------------------------------------------------------------------

camera = cv2.VideoCapture(0)

app = wx.App()
cap = webcamWindow(camera)
cap.Show()
app.MainLoop()