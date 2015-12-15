import sys

from PySide.QtGui import *
from PySide import QtCore
from PySide.QtCore import *
import re
import datetime as dt
import random
class TextCorrectionGUI(QWidget):
    
    
    
    def __init__(self,sec):
        app=QApplication(sys.argv)
        app.aboutToQuit.connect(app.deleteLater)
        self.sec=sec
        
        super(TextCorrectionGUI, self).__init__()
        self.buttons()
        
        self.display()
        app.exec_()
    def tablefill(self):
        column=0
        keys=['Mond','Tues','Wedn','Thur','Frid']
        for i in keys:
            row=0
            for j in self.sec[i]:
                newitem=QTableWidgetItem(j)
                newitem.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row,column,newitem)
                row=row+1
            column=column+1
    def buttons(self):
        self.confirm=QPushButton('Confirm')
        self.confirm.clicked.connect(self.confirmbuttonslot)
        self.reset=QPushButton('Reset')
        self.reset.clicked.connect(self.resetbuttonslot)
    def keyPressEvent(self, e):
        
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
    def resetbuttonslot(self):
        self.table.clearContents()
       
        self.tablefill()
        
        
        
        
        
        
    def confirmbuttonslot(self):
        self.new=[]
        msgBox=QMessageBox(self)
        msgBox.setText("The table has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        se=msgBox.addButton("Save and Exit",QMessageBox.AcceptRole)
        msgBox.setStandardButtons(QMessageBox.Cancel)
        msgBox.setIcon(QMessageBox.Question)
        
        msgBox.setDefaultButton(se)
        msgBox.exec_()
        self.sec1={}
        if msgBox.clickedButton()==se:
            
            
            for i in xrange(self.table.columnCount()):
                self.new1=[]
                
                self.new.append(self.table.horizontalHeaderItem(i).text().encode('utf-8'))
                for j in xrange(self.table.rowCount()):
                    p=self.table.item(j,i)
                    
                    if type(p)==QTableWidgetItem:
                        
                        self.new.append(p.text().encode('utf-8'))
                        self.new1.append(p.text().encode('utf-8'))
                    else:
                        pass
                self.sec1[self.table.horizontalHeaderItem(i).text().encode('utf-8')]=self.new1
                
            
            
            self.close()
        
                    
                    

        #elif msgBox.clickedButton()==QMessageBox.Cancel:w
    def sec11(self):
        return self.sec1
    def display(self):
        self.setWindowTitle('Display')
        self.showMaximized()
        
        self.table=QTableWidget()
        
        lrow=[]
        for i in self.sec:
            length=0
            for j in self.sec[i]:
                if j.isspace() or j=='':
                    pass
                else:
                    length=length+1
            lrow.append(length)

       
        
        
        self.table.setColumnCount(len(self.sec.keys()))
        self.table.setRowCount(max(lrow))
        key=['Monday','Tuesday','Wednesday','Thursday','Friday']
        self.table.setHorizontalHeaderLabels(key)
        
        self.tablefill()
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(False)
        
        
        #table.setSpan(0,2, 2, 1)
        self.vbox=QVBoxLayout()
        self.hbox=QHBoxLayout()
        
        self.tableoriginal=self.table
        self.vbox.addWidget(self.table)
        
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.confirm)
        self.hbox.addWidget(self.reset)
        
        self.vbox.addLayout(self.hbox)
        
        
        
        self.setLayout(self.vbox)


timecolumn=[]
for i in xrange(7,24):#creates a time column full of time slots such as 7:00 and 7:30
    timecolumn.append(dt.time(i).strftime('%I %M %p'))
    timecolumn.append(dt.time(i,30).strftime('%I %M %p'))
    if i==23:
        
            
        timecolumn.append(dt.time(0).strftime('%I %M %p'))
dytw=['Time','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
rowfinal=[]
data=[]

for i in xrange(1,len(timecolumn)):
    
    rowfinal=[timecolumn[i]]
    for j in dytw:
        rowfinal.append('')
    data.append(rowfinal)
class tableitemprototype(QTableWidgetItem):
    def __init__(self):
        super(tableitemprototype,self).__init__()
        self.setTextAlignment(Qt.AlignCenter)
        
    
class usertable(QTableWidget):
    def __init__(self):
        super(usertable,self).__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.verticalHeader().setVisible(False)
        self.setDragDropMode(QTableWidget.DragDrop)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setItemPrototype(tableitemprototype())
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)  
    def dragMoveEvent(self,event):
        if event.mimeData().hasFormat('application/x-qt-mime-type-name') or event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            self.oldcoords=[]
            for item in self.selectedItems():
                self.oldcoords.append((item.row(),item.column()))
            
                
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def dragEnterEvent(self, event):
    
        event.accept()
    def dropEvent(self,event):
        
        if event.mimeData().hasFormat('application/x-qt-mime-type-name') or event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            
            event.setDropAction(Qt.CopyAction)
            currentitems=self.selectedItems()
            point=event.pos()
            itematpos=self.itemAt(event.pos())
            count=0
            
            for citem in currentitems:
                #citem=self.currentItem()
                #prescoord=[self.indexAt(event.pos()).column(),self.indexAt(event.pos()).row()]
                #print self.itemAt(event.pos()).text()
                
                if count==0:
                    
                    
                    citemtext=citem.text()
                    citemzero=citem
                    citem.setText(self.itemAt(event.pos()).text())
                    self.itemAt(event.pos()).setText(citemtext)
                else:
                    citemtext=citem.text()
                    try:
                        diff=[citem.row()-citemzero.row(),citem.column()-citemzero.column()]
                        citem.setText(self.item(itematpos.row()+diff[0],itematpos.column()+diff[1]).text())
                        self.item(itematpos.row()+diff[0],itematpos.column()+diff[1]).setText(citemtext)
                        
                    except:
                        pass
                    
                    
                count=count+1
                
            
            
            
            event.accept()
        else:
            event.ignore()

            
            
        
       
        
        
class UserGUI(QWidget):
    def __init__(self,data):
        
        app=QApplication(sys.argv)
        app.aboutToQuit.connect(app.deleteLater)
        super(UserGUI,self).__init__()
        self.data=data
        self.buttons()
        self.UGUI()
        
        app.exec_()
    def tablefill(self):
        
        row=0
       
        for i in self.data:
            column=0
            
            
            
            for j in i:
                
                
            
                newitem=tableitemprototype()
                if j=='place':
                    j=''
                newitem.setText(j)
                
                self.table.setItem(row,column,newitem)
                column=column+1
            row=row+1
    def resetbuttonslot(self):
        self.table.clearContents()
       
                       
                
        self.tablefill()
        self.colorcode()
        self.spanner()
    def fixbuttonslot(self):
        self.table.clearSpans()
        self.spanner()
        self.colorcode()
    
    def spanner(self):
        pattern=re.compile(r'(\d+):?\s?(\d+)\s?([AP]M)')
    
        
        for i in xrange(1,self.table.columnCount()):
            for j in xrange(1,self.table.rowCount()):
                
                item=self.table.item(j,i)
                if re.findall(pattern,item.text()):
                    
                    if len(re.findall(pattern,item.text())[1][0])==1:
                        time='0%s %s %s'%(re.findall(pattern,item.text())[1][0],re.findall(pattern,item.text())[1][1],re.findall(pattern,item.text())[1][2])
                    else:
                        time='%s %s %s'%(re.findall(pattern,item.text())[1][0],re.findall(pattern,item.text())[1][1],re.findall(pattern,item.text())[1][2])
                        
                    
                    for k in xrange(1,self.table.rowCount()):
                        
                        if time.split(' ')[0]==self.table.item(k,0).text().split(' ')[0] and time.split(' ')[1]==self.table.item(k,0).text().split(' ')[1] and self.table.item(k,0).text().split(' ')[2]==time.split(' ')[2]:
                            self.table.setSpan(j,i,k-j+1,1) 
                        elif time.split(' ')[0]==self.table.item(k,0).text().split(' ')[0] and time.split(' ')[1]>self.table.item(k,0).text().split(' ')[1] and self.table.item(k,0).text().split(' ')[2]==time.split(' ')[2]:
                            self.table.setSpan(j,i,k-j+1,1)
                        

        
        
    def colorcode(self):
        
        pattern2=re.compile(r'\d\w+')
        listtext=[]
        point=[]
        codesandcolors={}
        chosen=[]
        cNames=QColor.colorNames()
        del cNames[cNames.index(u'white')]
        del cNames[cNames.index(u'transparent')]
        for i in xrange(1,self.table.columnCount()):
            
        


            for j in xrange(1,self.table.rowCount()):
                
                item=self.table.item(j,i)
                if 'Lecture' in item.text() and 'Review' not in item.text():
                    
                    
                    text=re.findall(pattern2,item.text())[0]
                    
                    try:
                        
                        listtext.index(text)

                    except:
                        if len(text)==4 or len(text)==5:
                            listtext.append(text)
        
        while len(listtext)>0:
            
            point.append(listtext.pop(random.randint(0,len(listtext)-1)))
        
        for code in point:
  
            color=cNames.pop(random.randint(0,len(cNames)-1))
            

                    
                
                         
                
                
                
            
            codesandcolors[code]=color
            chosen.append(color)

        
        for i in xrange(1,self.table.columnCount()):
            
        
    


            for j in xrange(1,self.table.rowCount()):
                item=self.table.item(j,i)
                for code in point:
                    if code in item.text():
                        
                        self.table.item(j,i).setBackground(QColor(codesandcolors[code]))
                    elif item.text()=='':
                        self.table.item(j,i).setBackground(QColor(u'white'))
                           
            
            
        

                    
        
        
        
    def confirmbuttonslot(self):
        self.new=[]
        msgBox=QMessageBox(self)
        msgBox.setText("The table has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        se=msgBox.addButton("Save and Exit",QMessageBox.AcceptRole)
        msgBox.setStandardButtons(QMessageBox.Cancel)
        msgBox.setIcon(QMessageBox.Question)
        
        msgBox.setDefaultButton(se)
        msgBox.exec_()
        self.sec1={}
        if msgBox.clickedButton()==se:
            
            
            for i in xrange(self.table.columnCount()):
                self.new1=[]
                
                self.new.append(self.table.horizontalHeaderItem(i).text().encode('utf-8'))
                for j in xrange(self.table.rowCount()):
                    p=self.table.item(j,i)
                    
                    if type(p)==QTableWidgetItem:
                        
                        self.new.append(p.text().encode('utf-8'))
                        self.new1.append(p.text().encode('utf-8'))
                    else:
                        pass
                self.sec1[self.table.horizontalHeaderItem(i).text().encode('utf-8')]=self.new1
                
            
            
            self.close()
    def buttons(self):
        self.confirm=QPushButton('Confirm')
        self.confirm.clicked.connect(self.confirmbuttonslot)
        self.reset=QPushButton('Reset')
        self.reset.clicked.connect(self.resetbuttonslot)
        self.fixbutton=QPushButton('Fix')
        self.fixbutton.clicked.connect(self.fixbuttonslot)

    
    def UGUI(self):
        
        self.setWindowTitle('Display')
        self.showMaximized()
        self.table=usertable()
        lrow=len(timecolumn)
        self.table.setColumnCount(len(dytw))
        self.table.setRowCount(lrow-1)
        self.table.setHorizontalHeaderLabels(dytw)
        self.tablefill()
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.spanner()
        for column in (0,self.table.rowCount()):
            self.table.resizeRowToContents(column)
            
        
        self.table.horizontalHeader().setVisible(False)
        #table.setSpan(0,2, 2, 1)
        self.vbox=QVBoxLayout()
        self.hbox=QHBoxLayout()
        
        
        self.colorcode()
        
        
        self.tableoriginal=self.table
        self.vbox.addWidget(self.table)
        
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.confirm)
        self.hbox.addWidget(self.reset)
        self.hbox.addWidget(self.fixbutton)
        
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)
        

        

    
    
        
"""
def main():
    app=QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    test=TextCorrectionGUI()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()
"""
