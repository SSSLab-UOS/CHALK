# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import json

import numpy as np

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

from PySide6.QtCore import *
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QFileDialog, QSizePolicy
)

from widgets import CustomGrip

from modules.app_settings import Settings
from modules.ui_functions import UIFunctions
from modules.ui_main import Ui_MainWindow
from modules.project_functions import ProjectFunctions
from modules.image_functions import ImageFunctions
from modules.utils import imwrite



class MainWindow(
    QMainWindow, UIFunctions, ProjectFunctions,
    ImageFunctions
    ):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        ProjectFunctions.__init__(self)
        ImageFunctions.__init__(self)
        

        widgets.appMargins.setContentsMargins(0, 0, 0, 0)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.settings = Settings()

        self.uiDefinitions()

        widgets.toggleButton.clicked.connect(lambda: self.toggleMenu(True))

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        
        widgets.btn_save.clicked.connect(self.buttonClick)        

        widgets.projectButton.clicked.connect(self.openProjectMenu)
        widgets.closeProjectButton.clicked.connect(self.openProjectMenu)

        widgets.imageButton.clicked.connect(self.openImageMenu)
        widgets.closeImageButton.clicked.connect(self.openImageMenu)

        widgets.openRightToolBox.clicked.connect(self.openRightToolBox)
    
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            self.toggleLeftBox(True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # WHEEL EVENT
        self.ui.scrollAreaImage.wheelEvent = self.wheelEventScroll

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            self.theme(themeFile, True)

            # SET HACKS
            # AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(self.selectMenu(widgets.btn_home.styleSheet()))

        widgets.imageLeftBox.grip = CustomGrip(widgets.imageLeftBox, Qt.RightEdge)
        widgets.projectLeftBox.grip = CustomGrip(widgets.projectLeftBox, Qt.RightEdge)
        
    def openProjectMenu(self):

        btn = self.sender()
        btnName = btn.objectName()

        self.resetStyle(btnName)
        btn.setStyleSheet(self.selectMenu(btn.styleSheet()))

        image_animation = self.toggleLeftBoxAnimation(widgets.imageLeftBox, to_standard=True)
        project_animation = self.toggleLeftBoxAnimation(widgets.projectLeftBox)
        
        widgets.stackedWidget.setCurrentWidget(widgets.imagePage)

        self.group = QParallelAnimationGroup()
        self.group.addAnimation(project_animation)
        self.group.addAnimation(image_animation)
        self.group.start()

    def openImageMenu(self):

        btn = self.sender()
        btnName = btn.objectName()

        self.resetStyle(btnName) # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(self.selectMenu(btn.styleSheet())) # SELECT MENU
        
        project_animation = self.toggleLeftBoxAnimation(widgets.projectLeftBox, to_standard=True)
        image_animation = self.toggleLeftBoxAnimation(widgets.imageLeftBox)

        widgets.stackedWidget.setCurrentWidget(widgets.imagePage) # SET PAGE

        self.group = QParallelAnimationGroup()
        self.group.addAnimation(image_animation)
        self.group.addAnimation(project_animation)
        self.group.start()


    def openRightToolBox(self):

        btn = self.sender()
        btnName = btn.objectName()

        widgets.stackedWidget.setCurrentWidget(widgets.imagePage) # SET PAGE

        if widgets.rightToolBox.width() == 0: 
            btn.setStyleSheet(self.selectTopMenu(btn.styleSheet())) # SELECT MENU
        else: 
            btn.setStyleSheet(self.deselectTopMenu(btn.styleSheet()))

        right_animation = self.toggleRightBoxAnimation(widgets.rightToolBox)
        
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(right_animation)
        self.group.start()
        
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            self.resetStyle(btnName)
            btn.setStyleSheet(self.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            self.resetStyle(btnName)
            btn.setStyleSheet(self.selectMenu(btn.styleSheet()))

            project_animation = self.toggleLeftBoxAnimation(widgets.projectLeftBox)
            image_animation = self.toggleLeftBoxAnimation(widgets.imageLeftBox, to_standard=True)

            self.group = QParallelAnimationGroup()
            self.group.addAnimation(project_animation)
            self.group.addAnimation(image_animation)
            self.group.start()

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            self.resetStyle(btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(self.selectMenu(btn.styleSheet())) # SELECT MENU
            
            image_animation = self.toggleLeftBoxAnimation(widgets.imageLeftBox)
            project_animation = self.toggleLeftBoxAnimation(widgets.projectLeftBox, to_standard=True)

            self.group = QParallelAnimationGroup()
            self.group.addAnimation(project_animation)
            self.group.addAnimation(image_animation)
            self.group.start()

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

        


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        self.resize_grips()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


    def keyPressEvent(self, event):
            
        if event.key() == 16777249:
            self.ControlKey = True

        if event.key() == 83: # S key 
            if self.ControlKey:
                imwrite(self.labelPath, self.label) 
            

    def keyReleaseEvent(self, event):

        # zoom
        if event.key() == 16777249:
            self.ControlKey = False


    def wheelEventScroll(self, event):
        
        self.mouseWheelAngleDelta = event.angleDelta().y() # -> 1 (up), -1 (down)

        if self.ControlKey:

            if self.mouseWheelAngleDelta > 0: 
                self.scale *= 1.1
                width_future = int(self.ui.mainImageViewer.geometry().width() * 1.1)
                height_future = int(self.ui.mainImageViewer.geometry().height() * 1.1)
            else : 
                self.scale /= 1.1
                width_future = int(self.ui.mainImageViewer.geometry().width() / 1.1)
                height_future = int(self.ui.mainImageViewer.geometry().height() / 1.1)
            
            self.oldPos = self.ui.mainImageViewer.mapFromGlobal(QCursor.pos())
            cursor_x = self.oldPos.x()  
            cursor_y = self.oldPos.y()

            cursor_x = np.clip(cursor_x, 0, self.ui.mainImageViewer.geometry().width())
            cursor_y = np.clip(cursor_y, 0, self.ui.mainImageViewer.geometry().height())

            cursor_x = cursor_x / self.ui.mainImageViewer.geometry().width()
            cursor_y = cursor_y / self.ui.mainImageViewer.geometry().height()

            _width_diff = width_future - self.ui.scrollAreaImage.geometry().width()
            _height_diff = height_future - self.ui.scrollAreaImage.geometry().height() 

            set_hor_max = _width_diff + 18 if _width_diff > 0 else 0 # check padd value for scrollArea
            set_ver_max = _height_diff + 18 if _height_diff > 0 else 0 # 

            self.ui.scrollAreaImage.horizontalScrollBar().setRange(0, set_hor_max) 
            self.ui.scrollAreaImage.verticalScrollBar().setRange(0, set_ver_max) 
            
            if self.ui.scrollAreaImage.verticalScrollBar().maximum() > 0: 
                setvalueY = int(cursor_y*set_ver_max)
                self.ui.scrollAreaImage.verticalScrollBar().setValue(setvalueY)

            if self.ui.scrollAreaImage.horizontalScrollBar().maximum() > 0: 
                setvalueX = int(cursor_x*set_hor_max)
                self.ui.scrollAreaImage.horizontalScrollBar().setValue(setvalueX)

            self.ui.mainImageViewer.setFixedSize(self.scale * self.pixmap.size())
            self.ui.mainImageViewer.fitInView(self.pixmap_item)
            self.ui.mainImageViewer.setVisible(False)
            

            # self.rescaleLabelViewer()
            self.ui.mainImageViewer.setVisible(True)

            # self.ui.scrollAreaImage.update()
            # self.ui.mainImageViewer.update()
            

        else : 
            scroll_value = self.ui.scrollAreaImage.verticalScrollBar().value()
            self.ui.scrollAreaImage.verticalScrollBar().setValue(scroll_value - self.mouseWheelAngleDelta)

        
    
        

if __name__ == "__main__":

    os.system("pyside6-rcc -o resources_rc.py resources.qrc")  
    os.system("pyside6-uic designs/main.ui -o modules/ui_main.py")  
    os.system("pyside6-uic designs/project_name.ui -o modules/ui_project_name.py")  
    os.system("pyside6-uic designs/brush_menu.ui -o modules/ui_brush_menu.py")  
    os.system("pyside6-uic designs/project_class.ui -o modules/ui_project_class.py")  
    os.system("pyside6-uic designs/thumbnail_window.ui -o modules/ui_thumbnail_window.py")  
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    
    window = MainWindow()
    sys.exit(app.exec())




