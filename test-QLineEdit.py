import sys 
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit 

from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("My App") 
        
        widget = QLineEdit() 
        widget.setMaxLength(10) 
        widget.setPlaceholderText("Enter your text") 
        widget.returnPressed.connect(self.return_pressed) 
        widget.selectionChanged.connect(self.selection_changed) 
        widget.textChanged.connect(self.text_changed) 
        widget.textEdited.connect(self.text_edited) 
        # self.setCentralWidget(widget) 
        
    def return_pressed(self): 
        print("Return pressed!") 
        # self.centralWidget().setText("Boom!") 
        

    def selection_changed(self): 
        print("Selection changed") 
        print(self.centralWidget().selectedText()) 
    
    def addItemToList(self):
        text = self.textEdit.toPlainText()
        if text:  # 빈 문자열이 아닐 때만 추가
            self.listWidget.addItem(text)
            self.textEdit.clear()

    def text_changed(self, s): 
        print("Text changed...") 
        print(s) 
        
    def text_edited(self, s): 
        print("Text edited...") 
        print(s) 


    
app = QApplication(sys.argv) 
window = MainWindow() 
window.show() 
app.exec_()
