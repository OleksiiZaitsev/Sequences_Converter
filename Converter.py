from PIL import Image, ImageDraw
import os
from PyQt4 import QtCore, QtGui, QtDeclarative
import myUI
import sys
from PyQt4.QtNetwork import *
import threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import re
import time
import numpy
import cv2
from subprocess import Popen, PIPE




# MAIN UI
app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
UI = myUI.Ui_sequences_converter()
UI.setupUi(window)






# CONVERTER
class SequencesConverter():
   def __init__(self):
       self.images = []
       self.take_image_from = UI.lineEdit_fileName_from.text()
       self.save_folder = UI.lineEdit_fileName_to.text()
       self.color_left = "#ffffff"
       self.color_right = "#ffffff"
       def MAIN_UI():
           self.viewport_checking()
           self.setup_checking()
           self.create_variables()


           UI.label_image_Left.setStyleSheet("background-color:{}".format(self.color_left))
           UI.label_image_Right.setStyleSheet("background-color:{}".format(self.color_right))




           if len(threading._active) > 1:
               progress_percentage = (self.padding / len(self.FPS_reducer())) * 100
               print(progress_percentage)
               UI.progressBar.setProperty("value", progress_percentage)
               self.MAIN_UI_Timer.start(1000/float(UI.horizontalSlider_FPS.value()))
           else:
               UI.progressBar.setProperty("value", 0)
               self.MAIN_UI_Timer.start(1000)


       self.MAIN_UI_Timer = QTimer()
       self.MAIN_UI_Timer.timeout.connect(MAIN_UI)
       self.MAIN_UI_Timer.start(1000)




       self.Play_Current = self.current_body_play()
       self.Play_Timer_Current = QTimer()
       self.Play_Timer_Current.timeout.connect(lambda: next(self.Play_Current))


       self.Play_Output = self.output_body_play()
       self.Play_Timer_Output = QTimer()
       self.Play_Timer_Output.timeout.connect(lambda: next(self.Play_Output))
   ###################################################################################################
   def viewport_checking(self):


       if self.take_image_from:
           try:
               image = os.listdir(self.take_image_from)
               UI.label_image_Left.setPixmap(QtGui.QPixmap(self.take_image_from + "\\" + image[0]))


           except:
               print("libpng error: Read Error")
       if self.save_folder:
           try:
               image = os.listdir(self.save_folder)
               UI.label_image_Right.setPixmap(QtGui.QPixmap(self.save_folder + "\\" + image[0]))
           except:
               print("libpng error: Read Error")


   def setup_checking(self):
       variables_for_Apply = (UI.horizontalSlider_FPS.value(),
                              UI.lineEdit_Height.text(),
                              UI.lineEdit_Width.text(),
                              UI.lineEdit_Name.text(),
                              UI.comboBox_Type.currentText())


       if not any(i == "" for i in variables_for_Apply) and os.path.exists(
               self.take_image_from) and os.path.exists(self.save_folder):
           UI.pushButton_Apply.setEnabled(True)
       else:
           UI.pushButton_Apply.setEnabled(False)




       if os.path.exists(self.take_image_from) and UI.horizontalSlider_FPS.value():
           UI.pushButton_Play_Current.setEnabled(True)
       else:
           UI.pushButton_Play_Current.setEnabled(False)


       if os.path.exists(self.save_folder) and UI.horizontalSlider_FPS.value():
           UI.pushButton_Play_Output.setEnabled(True)
       else:
           UI.pushButton_Play_Output.setEnabled(False)




   def current_body_play(self):
       while True:
           image = os.listdir(self.take_image_from)
           for i, name in enumerate(image):
               self.Play_Timer_Current.start(1000 / float(UI.horizontalSlider_FPS_Current_Play.value()))
               yield UI.label_image_Left.setPixmap(QtGui.QPixmap(self.take_image_from + "\\" + name))


   def current_play_stop_button(self):
       if UI.pushButton_Play_Current.text() == "Play":
           self.create_variables()
           self.MAIN_UI_Timer.stop()
           self.Play_Timer_Current.start(1000 / float(UI.horizontalSlider_FPS_Current_Play.value()))
           UI.pushButton_Play_Current.setText("Stop")


       else:
           self.MAIN_UI_Timer.start(1000)
           UI.pushButton_Play_Current.setText("Play")
           self.Play_Timer_Current.stop()
   ###################################################################################################
   def output_body_play(self):
       while True:
           image = os.listdir(self.save_folder)
           for i, name in enumerate(image):
               self.Play_Timer_Output.start(1000 / float(UI.horizontalSlider_FPS_Output_Play.value()))
               yield UI.label_image_Right.setPixmap(QtGui.QPixmap(self.save_folder + "\\" + name))


   def output_play_stop_button(self):
       if UI.pushButton_Play_Output.text() == "Play":
           self.create_variables()
           self.MAIN_UI_Timer.stop()
           self.Play_Timer_Output.start(1000 / float(UI.horizontalSlider_FPS_Output_Play.value()))
           UI.pushButton_Play_Output.setText("Stop")


       else:
           self.MAIN_UI_Timer.start(1000)
           UI.pushButton_Play_Output.setText("Play")
           self.Play_Timer_Output.stop()
   ###################################################################################################
   def Color_Selector_Left(self):


       self.color_left = QtGui.QColorDialog.getColor().name()
       UI.label_Color_Selector_Left.setStyleSheet("background-color:{}".format(self.color_left))
       UI.label_Color_Selector_Left.setText(self.color_left)


   def Color_Selector_Right(self):


       self.color_right = QtGui.QColorDialog.getColor().name()
       UI.label_Color_Selector_Right.setStyleSheet("background-color:{}".format(self.color_right))
       UI.label_Color_Selector_Right.setText(self.color_right)


   def create_variables(self):
       self.take_image_from = UI.lineEdit_fileName_from.text()
       self.save_folder = UI.lineEdit_fileName_to.text()




       self.Quality = int(UI.horizontalSlider.value())
       self.FPS = int(UI.horizontalSlider_FPS.value())


       self.Height = int(UI.lineEdit_Height.text())
       self.Width = int(UI.lineEdit_Width.text())


       self.name = UI.lineEdit_Name.text()
       self.type = UI.comboBox_Type.currentText()




   def fileName_from(self):
       fileName = QtGui.QFileDialog.getExistingDirectory()
       UI.lineEdit_fileName_from.setText(fileName)
       self.take_image_from = fileName


   def fileName_to(self):
       fileName = QtGui.QFileDialog.getExistingDirectory()
       UI.lineEdit_fileName_to.setText(fileName)
       self.save_folder = fileName


   def list_of_images(self):
       images = []
       if UI.lineEdit_Current_PATH.text():
           path = os.path.abspath(UI.lineEdit_Current_PATH.text())
           files = [os.path.join(path, i) for i in os.listdir(path)]
           for i in files:
               if re.findall('\.jpg|\.png|\.tiff|\.psd|\.eps|\.gif|\.exr|\.tga|\.bmp', i):
                   images.append(i)
       return images




   def save_video(self):
       self.create_variables()


       images = [os.path.join(self.take_image_from, i) for i in os.listdir(self.take_image_from)]
       p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r',  str(self.FPS), '-i', '-', '-vcodec', 'mpeg4',
                  '-qscale', '5', '-r', str(self.FPS), self.save_folder + "/" + self.name + ".avi"], stdin=PIPE)


       for f, i in enumerate(images):
           summ = len(images)
           progress_percentage = (f / summ) * 100
           print(progress_percentage)
           UI.progressBar.setProperty("value", progress_percentage)


           try:
               im = Image.open(i).convert('RGBA')
               bg = Image.new("RGBA", im.size, (int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).red()),
                                                int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).green()),
                                                int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).blue()), 255))
               bg.paste(im, im)


               bg.resize((self.Width, self.Height), Image.ANTIALIAS).save(p.stdin, 'JPEG', dpi=(72, 72), compress_level=9, quality=self.Quality, progressive=True)
           except:
               print("pass: ", i)
               pass


       p.stdin.close()
       p.wait()


       UI.progressBar.setProperty("value", 100)


   def save_image(self, image: str, padding: str ):
       if os.path.exists(self.save_folder):
           if self.type == "jpg" or self.type == "gif" or self.type == "bmp":
               image = Image.open(image).convert('RGBA')
               bg = Image.new("RGBA", image.size, (int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).red()),
                                                   int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).green()),
                                                   int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).blue())))
               bg.paste(image, image)
               bg.resize((self.Width, self.Height), Image.ANTIALIAS).save(os.path.join(self.save_folder, self.name) + "." + padding + "." + self.type, dpi=(72, 72), compress_level=9, quality=self.Quality, progressive=True)
           else:


               image = Image.open(image).convert('RGBA')
               bg = Image.new("RGBA", image.size, (int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).red()),
                                                   int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).green()),
                                                   int(UI.label_image_Right.palette().color(QtGui.QPalette.Background).blue()), 0))
               bg.paste(image, image)
               bg.resize((self.Width, self.Height), Image.ANTIALIAS).save(os.path.join(self.save_folder, self.name) + "." + padding + "." + self.type, dpi=(72, 72), compress_level=9, quality=self.Quality, progressive=True)




   def FPS_reducer(self):
       reduced_frames = []
       images = self.list_of_images()
       reduced_ID = numpy.linspace(0, len(images), (len(images)/30)*self.FPS, endpoint=False, dtype=int)
       for i in reduced_ID:
           reduced_frames.append(images[i])
       return reduced_frames


   def Body(self):
       for padding, image in enumerate(self.FPS_reducer()):
           self.padding = padding
           self.save_image(image, str(padding).zfill(4))
           if not self.__running:
               break




   def Apply(self):
       self.create_variables()
       self.__running = True
       self.Thread = threading.Thread(target=lambda: self.Body())
       self.Thread.start()


   def Cancel(self):
       self.Thread.daemon
       self.__running = False




################################################################################
UI.label_Quality.setText("Quality: " + str(UI.horizontalSlider.value()))
#Quality
def setText_Quality():
   UI.label_Quality.setText("Quality: " + str(UI.horizontalSlider.value()))


UI.horizontalSlider.valueChanged.connect(setText_Quality)
################################################################################
UI.label_FPS.setText("FPS: " + str(UI.horizontalSlider_FPS.value()))
#FPS
def setText_FPS():
   UI.label_FPS.setText("FPS: " + str(UI.horizontalSlider_FPS.value()))


UI.horizontalSlider_FPS.valueChanged.connect(setText_FPS)
################################################################################
UI.label_FPS_Current_Play.setText("FPS: " + str(UI.horizontalSlider_FPS_Current_Play.value()))
#FPS Current
def setText_FPS_Current():
   UI.label_FPS_Current_Play.setText("FPS: " + str(UI.horizontalSlider_FPS_Current_Play.value()))


UI.horizontalSlider_FPS_Current_Play.valueChanged.connect(setText_FPS_Current)
################################################################################
UI.label_FPS_Output_Play.setText("FPS: " + str(UI.horizontalSlider_FPS_Output_Play.value()))
#FPS Current
def setText_FPS_Output():
   UI.label_FPS_Output_Play.setText("FPS: " + str(UI.horizontalSlider_FPS_Output_Play.value()))


UI.horizontalSlider_FPS_Output_Play.valueChanged.connect(setText_FPS_Output)
################################################################################


# THREADS
ConverterThread = SequencesConverter()




def func_choice():
   if "png" in UI.comboBox_Type.currentText() or "jpg" in UI.comboBox_Type.currentText():
       ConverterThread.Apply()
   elif "avi" in UI.comboBox_Type.currentText():
       ConverterThread.save_video()




# BUTTONS
UI.pushButton_Play_Current.clicked.connect(lambda: ConverterThread.current_play_stop_button())
UI.pushButton_Play_Output.clicked.connect(lambda: ConverterThread.output_play_stop_button())




UI.toolButton_fileName_from.clicked.connect(lambda: ConverterThread.fileName_from())
UI.toolButton_fileName_to.clicked.connect(lambda: ConverterThread.fileName_to())




UI.label_Color_Selector_Right.mousePressEvent = lambda event: ConverterThread.Color_Selector_Right()
UI.label_Color_Selector_Left.mousePressEvent = lambda event: ConverterThread.Color_Selector_Left()


UI.pushButton_Apply.clicked.connect(lambda: func_choice())
UI.pushButton_Cancel.clicked.connect(lambda: ConverterThread.Cancel())


if __name__ == '__main__':
   UI.progressBar.setProperty("value", 0)
   window.show()
   sys.exit(app.exec_())


