import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class CariAnggota(QDialog):
  id_member = ''
  name = ''
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_member.ui', self)
    
    self.setWindowTitle('Member Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataAnggota()
    self.btnSearch.clicked.connect(self.cari)
    self.tblAnggota.doubleClicked.connect(self.dataPilih)
    
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()   
    
  def tampilDataAnggota(self):
    try:
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')

      # akses data user pada tbl_anggota
      query = 'SELECT * FROM tbl_anggota'
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      # menutup koneksi 
      con.close()
      
      # menampilkan data anggota ke form tabel
      panjang = len(data)
      self.tblAnggota.setRowCount(panjang)
      baris = 0
      for i in data:
        self.tblAnggota.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblAnggota.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblAnggota.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblAnggota.setItem(baris, 3, QTableWidgetItem(i[3]))
        self.tblAnggota.setItem(baris, 4, QTableWidgetItem(i[4]))
        self.tblAnggota.setItem(baris, 5, QTableWidgetItem(i[5]))
        self.tblAnggota.setItem(baris, 6, QTableWidgetItem(i[6]))
        self.tblAnggota.setItem(baris, 7, QTableWidgetItem(i[7]))
        baris += 1
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data anggota')
      
  def cari(self):
    try:
      search = self.editSearch.displayText()
      con = mc.connect(
              host='localhost',
              user='root',
              password='', 
              database='pboperpus',
              port='3306')
      
      query = f'''
                SELECT 
                  * 
                FROM 
                  tbl_anggota 
                WHERE 
                  id_anggota LIKE "%{search}%" 
                  OR nama_depan LIKE "%{search}%" 
                  OR nama_tengah LIKE "%{search}%" 
                  OR nama_belakang LIKE "%{search}%"
              '''
              
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblAnggota.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblAnggota.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblAnggota.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblAnggota.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblAnggota.setItem(baris, 3, QTableWidgetItem(i[3]))
        self.tblAnggota.setItem(baris, 4, QTableWidgetItem(i[4]))
        self.tblAnggota.setItem(baris, 5, QTableWidgetItem(i[5]))
        self.tblAnggota.setItem(baris, 6, QTableWidgetItem(i[6]))
        self.tblAnggota.setItem(baris, 7, QTableWidgetItem(i[7]))
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat pencarian data')
      
  def dataPilih(self):
    items = self.tblAnggota.selectedItems()
    name = items[1].text()+' '+items[2].text()+' '+items[3].text()
    self.id_member = items[0].text()
    self.name = name
    
    self.close()
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = CariAnggota()
  window.show()
  sys.exit(app.exec_())