import sys
import serial
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "PROGRAMAFINAL.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Area de los Signals
        self.btn_accion.clicked.connect(self.accion)
        self.btn_activarLuz.clicked.connect(self.activar_luz)  # Nuevo botón
        self.btn_ActivarPuerta.clicked.connect(self.activar_puerta)  # Nuevo botón

        self.arduino = None
        self.luz_activada = False
        self.puerta_activada = False

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturaArduino)
        self.segundoPlano.start(100)

    # Area de los Slots
    def accion(self):
        texto_boton = self.btn_accion.text()
        com = self.txt_com.text()
        if texto_boton == "CONECTAR" and self.arduino is None:
            self.arduino = serial.Serial(port=com, baudrate=9600, timeout=1)
            self.btn_accion.setText("DESCONECTAR")
        elif texto_boton == "DESCONECTAR" and self.arduino.isOpen():
            self.arduino.close()
            self.btn_accion.setText("RECONECTAR")
        else:
            self.arduino.open()
            self.btn_accion.setText("DESCONECTAR")

    def lecturaArduino(self):
        if self.arduino is not None and self.arduino.isOpen():
            if self.arduino.inWaiting():
                cadena = self.arduino.readline()
                cadena = cadena.decode().strip()

                if cadena != "":
                    # Si el dato es de distancia e intensidad de luz, lo mostramos
                    if "Distancia" in cadena and "Intensidad de luz" in cadena:
                        self.datos.addItem(cadena)  # Agrega los datos a la lista
                        self.datos.setCurrentRow(self.datos.count())  # Desplaza la lista hacia abajo

    def activar_luz(self):
        if self.arduino is not None and self.arduino.isOpen():
            if self.luz_activada:
                self.arduino.write(b"DESACTIVAR_LUZ\n")
                self.btn_activarLuz.setText("Activar Luz")  # Cambia el texto del botón
            else:
                self.arduino.write(b"ACTIVAR_LUZ\n")
                self.btn_activarLuz.setText("Desactivar Luz")
            self.luz_activada = not self.luz_activada

    def activar_puerta(self):
        if self.arduino is not None and self.arduino.isOpen():
            if self.puerta_activada:
                self.arduino.write(b"DESACTIVAR_PUERTA\n")
                self.btn_ActivarPuerta.setText("Activar Puerta")
            else:
                self.arduino.write(b"ACTIVAR_PUERTA\n")
                self.btn_ActivarPuerta.setText("Desactivar Puerta")
            self.puerta_activada = not self.puerta_activada

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
