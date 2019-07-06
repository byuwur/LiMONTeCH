
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar
import time
import os

class MyFrameTotal(wx.Frame):

	def onClickedSalirTotal(self, event):
		exit()

	def onClickedGuardar(self, event):
		current=str(time.strftime("%d-%m-%Y"+"_"+"%H-%M-%S"))
		namecurrent=str(time.strftime("%d/%m/%Y"+"_"+"%H:%M:%S"))

		folderpath="C:/LiMONTECHLogs/"
		directory=os.path.dirname(folderpath)

		if not os.path.exists(directory):
			os.makedirs(directory)

		file = open("C:/LiMONTECHLogs/file_"+current+".txt","w")
		file.write("Registro realizado el: "+namecurrent+".")
		file.close()

		ward=wx.MessageDialog(None, "Archivo creado el: "+namecurrent+".\nRegistro realizado con exito.", "Guardado", wx.OK)
		respuesta=ward.ShowModal()
		ward.Destroy()


	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'Total', wx.DefaultPosition, (195, 150), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | 0 | 0 | 0)
		self.panel = wx.Panel(self, -1)
		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap("limontech.ico", wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

		self.label1 = wx.StaticText(self.panel, -1, 'Limones defectuosos\nencontrados en el analisis\nmas reciente:', (16,8), (128, 23))
		self.label1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labeltotal = wx.StaticText(self.panel, -1, 'TOTAL', (16,50), (100, 23))
		self.labeltotal.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labeltotal.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.buttonge = wx.Button(self.panel, -1, 'Guardar', (16,80), (75, 23))
		self.buttonge.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.buttonge.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.buttonge.Bind(wx.EVT_BUTTON, self.onClickedGuardar)

		self.buttonsalir = wx.Button(self.panel, -1, 'Salir', (96,80), (75, 23))
		self.buttonsalir.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.buttonsalir.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.buttonsalir.Bind(wx.EVT_BUTTON, self.onClickedSalirTotal)

		
#---------------------------------------------------------------------------
class MyAppTotal(wx.App):
	def OnInit(self):
		frame = MyFrameTotal(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

appTotal = MyAppTotal(True)
appTotal.MainLoop()