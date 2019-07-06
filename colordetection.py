# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import serial.tools.list_ports

import sys
import glob
import serial

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
            #s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
    return arduino
    return port

if __name__ == '__main__':
    arser=str(serial_ports())  
    strarser=arser.strip("[']")
    arduinoencontrado=str('Arduino encontrado en: '+strarser)
    print(arduinoencontrado)

def onClickedIniciar():
        
        #Iniciar la camara
        captura = cv2.VideoCapture(0)
        contador=0
        print("Presione 'Esc' (Escape) para terminar\n")
        while(1):
            #Capturamos una imagen y la convertimos de RGB -> HSV
            _, imagen = captura.read()
            hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

            #Amarillos 23
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

            if (area > 100000):
                #print area

                x = int(moments['m10']/moments['m00'])
                y = int(moments['m01']/moments['m00'])

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]
                if len(cnts) > 0:
                    #print cnts
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    print radius
                    M = cv2.moments(c)

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                    if radius > 10.5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                        cv2.drawContours(imagen, [c], 0, (0, 255, 0), 2, cv2.LINE_AA)
                        cv2.putText(imagen, 'Amarillo'.format(int(x), int(y)), (int(x-2),int(y-2)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                        arduino=serial.Serial(strarser,9600)
                        arduino.write('1')
                        time.sleep(0.05)
                        arduino.close()
                        contador=contador+1

            #cv2.imshow('amarillo y hongos', mascara_amarillo)
            cv2.imshow('Camara', imagen)

            tecla = cv2.waitKey(5) & 0xFF
            if tecla == 27:
                global resultadocontador
                resultadocontador=str(contador)  
                print ("\n#----------------------#------------------#\n")  
                print ("Limones defectuosos encontrados: "+resultadocontador)
                print ("Cierre esta ventana para continuar")
                cv2.destroyAllWindows()
                break

onClickedIniciar()