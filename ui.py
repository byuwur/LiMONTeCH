
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar


class MyFrame(wx.Frame):

	def onClickedSalir(self, event):
		exit()

	def onClickedIniciar(self, event):
		numcam = int(self.textboxcam.GetValue())
		print (numcam)

	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'LiMONTECH', wx.DefaultPosition, (300, 225), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | 0 | 0 | 0)
		self.panel = wx.Panel(self, -1)

		self.botonsalir = wx.Button(self.panel, -1, 'Salir', (178,158), (65, 22))
		self.botonsalir.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botonsalir.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botonsalir.Bind(wx.EVT_BUTTON, self.onClickedSalir)


		self.botondetener = wx.Button(self.panel, -1, 'DETENER', (168,130), (86, 25))
		self.botondetener.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botondetener.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label1 = wx.StaticText(self.panel, -1, 'Tecnologia LiMONTECH', (16,16), (75, 23))
		self.label1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.botoniniciar = wx.Button(self.panel, -1, 'INICIAR', (168,104), (86, 25))
		self.botoniniciar.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botoniniciar.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botoniniciar.Bind(wx.EVT_BUTTON, self.onClickedIniciar)

		self.label2 = wx.StaticText(self.panel, -1, 'Arduino encontrado en:', (152,16), (125, 17))
		self.label2.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label2.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labelcom = wx.StaticText(self.panel, -1, 'COM', (152,35), (100, 23))
		self.labelcom.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelcom.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labelvalor = wx.StaticText(self.panel, -1, 'VALOR', (16,130), (100, 23))
		self.labelvalor.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelvalor.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label5 = wx.StaticText(self.panel, -1, 'Valor del color', (16,112), (100, 23))
		self.label5.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label5.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label6 = wx.StaticText(self.panel, -1, '(Se requiere el Arduino.\nEn caso de no encontrar,\nel programa no iniciara.)', (152,57), (100, 23))
		self.label6.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label6.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.textboxcam = wx.TextCtrl(self.panel, -1, '', (16,64), size=(100, 20))
		self.textboxcam.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.textboxcam.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.textboxcam.SetCursor(wx.StockCursor(wx.CURSOR_IBEAM))


		self.labelcam = wx.StaticText(self.panel, -1, 'Camara:', (16,48), (100, 23))
		self.labelcam.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelcam.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label7 = wx.StaticText(self.panel, -1, '0: Defecto. 1: Externa.', (16,88), (100, 25))
		self.label7.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label7.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		
#---------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(True)
app.MainLoop()
