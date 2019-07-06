"""
LiMONTeCH, MNM, 2017
Desarrollado por: MNM
Andres Trujillo Mateus
Marco Jose Cortes Guzman
Nestor Alfonso Portela
"""

#-----------------------------------------------------------
import wx
import wx.calendar
import cv2
import numpy as np
import time
import os
import serial.tools.list_ports
import sys
import serial
import glob

#-----------------------------------------------------------

#Detectar si hay un Arduino conectado
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            arduino = serial.Serial(port,9600)
            arduino.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass    
    return result
#Seleccion del Arduino
def setArduino():
	if __name__ == '__main__':
	    global arser, strarser, arduinoconexion
	    arser=str(serial_ports())
	    temp=len(arser)    
	    strarser=arser.strip("[']")

	if not strarser:
		arduinoconexion=0
		strarser=str("No encontrado.")
	else:
		arduinoconexion=1
#Ejecute la funcion de escoger el arduino
setArduino()

#---------------------------------------------------------------------------
class MyFrame(wx.Frame):

	def onClickedAcerca(self, event):
		about=wx.MessageDialog(None, "LiMONTeCH. Detector para limones.\n2017, MNM\n\n"+
			"Desarrollado por:\nAndres Trujillo Mateus\nMarco Jose Cortes Guzman\n"+
			"Nestor Alfonso Portela Rincon\n\n"+"Contacto:\nhttps://www.facebook.com/MNM-138132210147377/",
			"Acerca de LiMONTeCH", wx.OK)
		respuestaabout=about.ShowModal()
		about.Destroy()

	def onClickedManual(self, event):
		os.startfile("manual.pdf")

	def onClickedSalir(self, event):
		self.Destroy()
	
	def onClickedRestart(self, event):
		self.Destroy()
		serial_ports()
		setArduino()
		app = MyApp(True)
		app.MainLoop()
		#self.Center()	

	def onClickedDetener(self, event):
	    self.botoniniciar.Enable(0)
	    self.menuiteminiciar.Enable(0)
	    appTotal = MyAppTotal(True)
	    appTotal.MainLoop()

	def onClickedIniciar(self, event):
	    #Seleccionar la camara
	    value = self.radiobutton0.GetValue()
	    if value == True:
	    	numcam=0
	    	self.radiobutton1.Enable(0)
	    	numerocamara=str("Camara seleccionada: Por defecto.")
	    else:
	    	numcam=1
	    	self.radiobutton0.Enable(0)
	    	numerocamara=str("Camara seleccionada: Externa.")
	    #Arduino
	    if arduinoconexion == 1:
	    	self.label8.SetLabel("#------------------------Dispositivos------------------------#\n"+
	    		numerocamara+"\n"+"Arduino en: "+"[ ' "+strarser+" ' ].")
	    else:
	    	self.label8.SetLabel("#------------------------Dispositivos------------------------#\n"+
	    		numerocamara+"\n"+"No hay Arduino. Considere conectar uno.")
	    #Ventana principal
	    self.botoniniciar.Enable(0)
	    self.botondetener.Enable(0)	    
	    self.menuiteminiciar.Enable(0)
	    self.menuitemguardar.Enable(0)
	    self.label5.SetLabel("Intensidad del color:")
	    self.labelvalor.SetLabel("0")    
	    #Iniciar la camara
	    captura = cv2.VideoCapture(numcam)    
	    contador=0
	    #Iniciar la deteccion
	    while(1):
	        #Capturamos una imagen y la convertimos de RGB -> HSV
	        _, imagen = captura.read()
	        #Se "verifica" si la camara esta conectada
	        try:
	        	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
	        except Exception as e:
	        	#raise e
	        	self.label5.SetLabel(":")
	        	self.label8.SetLabel("#---------------------------Estado---------------------------#\n"+
	        		"El programa se niega a arrancar.\nPor favor, escoja la camara correcta y pulse 'Iniciar'")
	        	global resultadocontador
	        	resultadocontador=str("Error de camara")
	        	self.botondetener.Enable(0)
	        	self.botoniniciar.Enable(1)
	        	self.menuitemguardar.Enable(0)
	        	self.menuiteminiciar.Enable(1)
	        	self.radiobutton0.Enable(1)
	        	self.radiobutton1.Enable(1)
	        	break
	        #Amarillos
	        amarillo_bajos = np.array([20, 113, 164], dtype=np.uint8)
	        amarillo_altos = np.array([30, 195, 255], dtype=np.uint8)
	        #Hongos
	        hbajos=np.array([17, 48, 108], dtype=np.uint8)
	        haltos=np.array([30, 195, 255], dtype=np.uint8)
	        #Detectar los pixeles de la imagen que esten dentro del rango de amarillos
	        mascara_amarillo = cv2.inRange(hsv, amarillo_bajos, amarillo_altos)
	        mask_hongos = cv2.inRange(hsv, hbajos, haltos)
	        kernel = np.ones((6,6),np.uint8)
	        #Anadimos las dos mascaras
	        mascara_amarillo=cv2.add(mascara_amarillo, mask_hongos)
	        mask = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_OPEN, kernel)
	        #Encontrar el area de los objetos que detecta la camara
	        moments = cv2.moments(mascara_amarillo)
	        area = moments['m00']
	        #Tolerancia
	        if (area > 100000):
	            #print area
	            x = int(moments['m10']/moments['m00'])
	            y = int(moments['m01']/moments['m00'])
	            #Intensidad cromatica
	            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	                cv2.CHAIN_APPROX_SIMPLE)[-2]
	            if len(cnts) > 0:
	                #print cnts
	            # find the largest contour in the mask, then use
	            # it to compute the minimum enclosing circle and
	                # centroid
	                c = max(cnts, key=cv2.contourArea)
	                ((x, y), radius) = cv2.minEnclosingCircle(c)
	                self.labelvalor.SetLabel(str(radius))
	                #print radius
	                M = cv2.moments(c)
	            #Tolerancia. only proceed if the radius meets a minimum size. Correct this value for your obect's size
	                if radius > 40:
	                # draw the circle and centroid on the frame,
	                # then update the list of tracked points
	                    cv2.drawContours(imagen, [c], 0, (0, 255, 0), 2, cv2.LINE_AA)
	                    cv2.putText(imagen, 'Amarillo'.format(int(x), int(y)), (int(x-2),int(y-2)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
	                    if arduinoconexion==1:
	                    	arduino=serial.Serial(strarser,9600)
	                    	arduino.write('1')
	                    	contador=contador+1	                    	
	                    	arduino.close()
	                    else:	                    	
	                    	contador=contador+1
	                    time.sleep(0.5)
	                    arduino.close()	                    	
	        #cv2.imshow('Amarillo y Hongos', mascara_amarillo)
	        cv2.imshow("Camara: (Presione 'Esc' para salir)", imagen)
	        cv2.moveWindow("Camara: (Presione 'Esc' para salir)", 237,17)
	        #cv2.resizeWindow("Camara: (Presione 'Esc' para salir)", 640,480)
	        #Cierre de la camara
	        tecla = cv2.waitKey(5) & 0xFF
	        if tecla == 27:
	        	#global resultadocontador
	        	intcontador=contador/2
	        	resultadocontador=str(intcontador)    
	        	#print ("Limones defectuosos encontrados: "+resultadocontador)
	        	#print ("Cierre esta ventana para continuar")
	        	cv2.destroyAllWindows()
	        	self.botondetener.Enable(1)
	        	self.botoniniciar.Enable(1)
	        	self.menuitemguardar.Enable(1)
	        	self.menuiteminiciar.Enable(1)
	        	self.radiobutton0.Enable(1)
	        	self.radiobutton1.Enable(1)
	        	self.label5.SetLabel("Limones encontrados:")
	        	break
	    self.labelvalor.SetLabel(resultadocontador)	        
	    #return resultado
			            
#----------------------------------------------------------
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'MNM LiMONTeCH', (11 ,16), (300,345), style=wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | 0 | 0 | 0)
		self.panel = wx.Panel(self, -1)
		#self.Center()

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.menuarchivo = wx.Menu()
		self.menuiteminiciar = wx.MenuItem( self.menuarchivo, wx.ID_ANY, u"Iniciar", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuarchivo.AppendItem( self.menuiteminiciar )
		
		self.menuitemguardar = wx.MenuItem( self.menuarchivo, wx.ID_ANY, u"Guardar", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuarchivo.AppendItem( self.menuitemguardar )
		self.menuitemguardar.Enable(0)
		
		self.menuarchivo.AppendSeparator()
		
		self.menuitemreiniciar = wx.MenuItem( self.menuarchivo, wx.ID_ANY, u"Reiniciar", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuarchivo.AppendItem( self.menuitemreiniciar )
		
		self.menuitemsalir = wx.MenuItem( self.menuarchivo, wx.ID_ANY, u"Salir", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuarchivo.AppendItem( self.menuitemsalir )
		#self.menuitemsalir.Bind(wx.EVT_BUTTON, self.onClickedSalir)		

		self.m_menubar1.Append( self.menuarchivo, u"Archivo" ) 
		
		self.menuayuda = wx.Menu()
		self.menuitemacercade = wx.MenuItem( self.menuayuda, wx.ID_ANY, u"Acerca de", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuayuda.AppendItem( self.menuitemacercade )
		
		self.menuayuda.AppendSeparator()
		
		self.menuitemmanual = wx.MenuItem( self.menuayuda, wx.ID_ANY, u"Manual", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuayuda.AppendItem( self.menuitemmanual )
		
		self.m_menubar1.Append( self.menuayuda, u"Ayuda" ) 
		
		self.SetMenuBar( self.m_menubar1 )

		#Eventos del Menubar
		self.Bind( wx.EVT_MENU, self.onClickedIniciar, id = self.menuiteminiciar.GetId() )
		self.Bind( wx.EVT_MENU, self.onClickedDetener, id = self.menuitemguardar.GetId() )
		self.Bind( wx.EVT_MENU, self.onClickedRestart, id = self.menuitemreiniciar.GetId() )
		self.Bind( wx.EVT_MENU, self.onClickedSalir, id = self.menuitemsalir.GetId() )		
		self.Bind( wx.EVT_MENU, self.onClickedAcerca, id = self.menuitemacercade.GetId() )
		self.Bind( wx.EVT_MENU, self.onClickedManual, id = self.menuitemmanual.GetId() )
		#---------------------------------------------------------

		self.botonsalir = wx.Button(self.panel, -1, 'Salir', (178,180), (65, 22))
		self.botonsalir.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botonsalir.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botonsalir.Bind(wx.EVT_BUTTON, self.onClickedSalir)

		self.botonrestart = wx.Button(self.panel, -1, 'Reiniciar', (178,158), (65, 22))
		self.botonrestart.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botonrestart.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botonrestart.Bind(wx.EVT_BUTTON, self.onClickedRestart)

		self.botondetener = wx.Button(self.panel, -1, 'GUARDAR', (168,128), (86, 25))
		self.botondetener.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botondetener.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botondetener.Bind(wx.EVT_BUTTON, self.onClickedDetener)
		self.botondetener.Enable(0)

		self.label1 = wx.StaticText(self.panel, -1, 'Tecnologia LiMONTeCH', (16,16), (110, 23))
		self.label1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.botoniniciar = wx.Button(self.panel, -1, 'INICIAR', (168,102), (86, 25))
		self.botoniniciar.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.botoniniciar.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.botoniniciar.Bind(wx.EVT_BUTTON, self.onClickedIniciar)

		self.label2 = wx.StaticText(self.panel, -1, 'Arduino encontrado en:', (152,16), (125, 17))
		self.label2.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label2.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labelcom = wx.StaticText(self.panel, -1, "[ ' "+strarser+" ' ]", (152,35), (100, 23))
		self.labelcom.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelcom.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labelvalor = wx.StaticText(self.panel, -1, '0', (16,177), (100, 23))
		self.labelvalor.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelvalor.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label5 = wx.StaticText(self.panel, -1, 'Intensidad del color:', (16,160), (100, 23))
		self.label5.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label5.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label6 = wx.StaticText(self.panel, -1, '(Se requiere el Arduino.\nEn caso de no encontrar,\nel programa no iniciara.)', (152,55), (100, 23))
		self.label6.SetFont(wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label6.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label7 = wx.StaticText(self.panel, -1, '(Se recomienda usar la\ncamara por defecto.\nEn caso de contar\ncon otra, seleccionela.)', (16,100), (100, 23))
		self.label7.SetFont(wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label7.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label8 = wx.StaticText(self.panel, -1, '#------------------------Dispositivos------------------------#', (16,220), (100, 23))
		self.label8.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label8.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))		

		self.radiobutton0 = wx.RadioButton(self.panel, -1, '0: Por defecto.', (16,55), (99, 24))
		self.radiobutton0.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.radiobutton0.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.radiobutton0.SetValue(1)

		self.radiobutton1 = wx.RadioButton(self.panel, -1, '1: Externa.', (16,75), (98, 24))
		self.radiobutton1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.radiobutton1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
		self.radiobutton1.SetValue(0)

		self.labelcam = wx.StaticText(self.panel, -1, 'Camara:', (16,40), (100, 23))
		self.labelcam.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.labelcam.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap("LiMONTeCH.ico", wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)		

#---------------------------------------------------------------------------
class MyFrameTotal(wx.Frame):

	def onClickedSalirTotal(self, event):
		self.Destroy()

	def onClickedGuardar(self, event):
		self.buttonge.Enable(0)
		#Recoge la hora actual
		current=str(time.strftime("%d-%m-%Y"+"_"+"%H-%M-%S"))
		namecurrent=str(time.strftime("%d/%m/%Y"+"_"+"%H:%M:%S"))
		#Ruta de guardado
		folderpath="C:/LiMONTeCHLogs/"
		directory=os.path.dirname(folderpath)
		#Verifica si el directorio existe, si no, lo crea
		if not os.path.exists(directory):
			os.makedirs(directory)
		#Crea el archivo de registro
		file = open("C:/LiMONTeCHLogs/reg_"+current+".txt","w")
		file.write("Registro realizado el: "+namecurrent+".\nLimones defectuosos encontrados: "+resultadocontador)
		file.close()
		#Notifica el exito del registro
		ward=wx.MessageDialog(None, "Archivo creado el: "+namecurrent+".\nRegistro realizado con exito.", "Guardado", wx.OK)
		respuesta=ward.ShowModal()
		ward.Destroy()

#------------------------------------------------
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'Total', (20, 365), (195, 150), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | 0 | 0 | 0)
		self.panel = wx.Panel(self, -1)

		self.label1 = wx.StaticText(self.panel, -1, 'Limones defectuosos\nencontrados en el analisis\nmas reciente:', (16,10), (128, 23))
		self.label1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.labeltotal = wx.StaticText(self.panel, -1, resultadocontador, (16,55), (100, 23))
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

		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap("LiMONTeCH.ico", wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

#---------------------------------------------------------------------------
class MyAppTotal(wx.App):
	def OnInit(self):
		frame = MyFrameTotal(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

#---------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

#---------------------------------------------------------------------------
#Ejecucion del wx
app = MyApp(True)
#Saludo
wx.MessageBox("Bienvenido a LiMONTeCH.\n\nPulse 'INICIAR' cuando este listo.\n\n"+
	"Terminado el proceso, dirijase a la ventana de la camara y presione 'Esc' (Escape) para terminar.\nSe recomienda este proceso para evitar errores.\n"+
    "\nSi la placa se encuentra conectada y desea cambiarla,\ndesconecte la placa y conecte la placa en reemplazo,\n"+
    "hecho esto, pulse 'Reiniciar' para conectar la segunda placa.\n\nLo mismo aplica si no hay placa y desea conectar una.\n"+
    "\nTenga en cuenta lo anterior para evitar errores y conflictos con el programa.\n\nAcceda al manual completo en el menu 'Ayuda'.\n"+
    "\n\n- MNM Team\n", "Bienvenido a LiMONTeCH", wx.OK)
#Abre el wx
app.MainLoop()

#LiMONTeCH, MNM, 2017