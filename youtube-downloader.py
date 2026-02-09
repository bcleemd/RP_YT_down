"""
개선  : 
1. 다운중. 또는 나머지. 진생상태를 TextBrowser_Status 창에 보여주기
2. 다운된 파일은 리스트에 [V] 표시해주기.. 

"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile
from ui_Dialog_Downloader import Ui_Dialog_Main
from Basic_utils import ic
import clipboard 
from ytdlp_audiodown import audiodown
from ytdlp_videodown import videodown

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        #################
        self.ui = Ui_Dialog_Main() 
        self.ui.setupUi(self)
        ##################
        
        # Connects
        # [List_Links]
        # ListWidget_Links = self.ui.ListWidget_Links

        # [Paste Button]
        self.ui.Btn_Paste.clicked.connect(self.Btn_Paste_Clicked)

        # [Delete Button] 
        self.ui.Btn_Delete.clicked.connect(self.Btn_Delete_Clicked)

        # [Select File Button]
        self.ui.Btn_Select_File.clicked.connect(self.Btn_Select_File_Clicked)
        
        # [Link : Line Edit]
        self.ui.LineEdit_Link.returnPressed.connect(self.add_to_list_links_from_line_text)

        # [Add Button]
        self.ui.Btn_Add.clicked.connect(self.add_to_list_links_from_line_text)

        # [List File Path : Line Edit]
        self.ui.LineEdit_ListFile_Path.returnPressed.connect(self.add_to_list_links_from_file)

        # LineEdit_ListFile_Path.textChanged.connect(self.add_list_from_file)
        # LineEdit_ListFile_Path.textEdited.connect(self.add_list_from_file)

        # [Video Down Button]
        # Btn_Video_Down = self.ui.Btn_Video_Down
        self.ui.Btn_Video_Down.clicked.connect(self.Btn_Video_Down_Clicked)

        # [Audio Down Button]
        # Btn_Audio_Down = self.ui.Btn_Audio_Down
        self.ui.Btn_Audio_Down.clicked.connect(self.Btn_Audio_Down_Clicked)

        # [Close Button]
        # app.quit  
        Btn_Close = self.ui.Btn_Close_App
        Btn_Close.clicked.connect(app.quit)

    def Btn_Paste_Clicked(self) :
        # print("Paste Button Clicked ! ")
        text = clipboard.paste()
        # text = self.ui.LineEdit_Link.text()
        if text:
            self.ui.ListWidget_Links.addItem(text)        
        # self.log_text(text)
    
    def Btn_Delete_Clicked(self) :
        # print("Delete Button Clicked ! ")
        selected_items = self.ui.ListWidget_Links.selectedItems()
        # selected_items = self.ui.ListWidget_Links.items()
        # text = f'"{selected_items}" was deleted.' 
        # self.log_text(text)
        if selected_items:
            for item in selected_items:
                self.ui.ListWidget_Links.takeItem(self.ui.ListWidget_Links.row(item))
        

    def Btn_Select_File_Clicked(self) : 
        filename = QFileDialog.getOpenFileName(self,
		   ("Open List"), 
		   "", 
		   ("Text FIles (*.txt)")
           )
        # https://newbie-developer.tistory.com/122

        text= f'File "{filename[0]}" was selected.' 
        self.log_text(text)
        self.add_to_list_links_from_file(filename[0])

    def Btn_Video_Down_Clicked(self) :
        print("Video_Down Button Clicked ! ")
        urls = self.get_list_from_list_links()

        # generator = self.asterisk_generator()
        # text = next(generator)
        # self.log_text(text)
        videodown(urls)
        
        text = f'Vidoe Downloading is completed'
        self.log_text(text)
        
        

    def Btn_Audio_Down_Clicked(self) :
        print("Audio_Down Button Clicked ! ")
        urls = self.get_list_from_list_links()
        # text = 'Audio Download Starts'
        # self.log_text(text)
        audiodown(urls)
        text = 'Audio Downloading is completed'
        self.log_text(text)
        
        pass
    
    def add_to_list_links_from_line_text(self):
        # text = self.LineEdit_Link.text()
        text = self.ui.LineEdit_Link.text()
        if text:
            self.ui.ListWidget_Links.addItem(text)
            self.ui.LineEdit_Link.clear()
        
    def read_lines_to_list(self,filename) : 
        with open(filename, "r") as f:
        # Read all lines from the file
            lines = f.readlines()
        ic(lines)    
        return_list =[]
        for item in lines :
            if not item.strip() == "" :
                return_list.append(item.strip())
        return return_list        

    def add_to_list_links_from_file(self,filename) :
        ic(self,filename)
        # with open(filename, "r") as f:
        # # Read all lines from the file
        #     lines = f.readlines()
        # ic(lines)    
        items = self.read_lines_to_list(filename)
        for item in items : 
            self.ui.ListWidget_Links.addItem(item)

    def get_list_from_list_links(self) :
        list_items = [self.ui.ListWidget_Links.item(i).text() for i in range(self.ui.ListWidget_Links.count())]
        ic(list_items)
        return list_items 
    
    def log_text(self,text) : 
        self.ui.TextBrowser_Status.append(text)
    
    def show_asterisk(self,generator) : 
        self.ui.TextBrowser_Status.append(next(generator))

    def asterisk_generator(self):
        count = 0
        while True:
            count += 1
            yield "*" * count

    # def add_list_from_linedit(self) :
    #      filename = self.ui.LineEdit_ListFile_Path.text()
    #      self.add_list_from_file(self,filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())