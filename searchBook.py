import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class CariBuku(QDialog):
  isbn = ''
  title = ''
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_book.ui', self)
    
    self.setWindowTitle('Book Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataBuku()
    self.btnSearch.clicked.connect(self.cari)
    self.tblBuku.doubleClicked.connect(self.dataPilih)

  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()
    
  def tampilDataBuku(self):
    try:
      con = mc.connect(
              host='localhost',
              user='root',
              password='', 
              database='pboperpus',
              port='3306')
      
      query = f'''
                SELECT 
                  tbl_buku.isbn, 
                  tbl_buku.judul, 
                  tbl_genre.nama_genre, 
                  tbl_penulis.nama_depan, 
                  tbl_penulis.nama_tengah, 
                  tbl_penulis.nama_belakang, 
                  tbl_buku.penerbit, 
                  tbl_buku.tanggal_publikasi, 
                  tbl_buku.jumlah_stok
                FROM 
                  ((tbl_buku 
                    INNER JOIN tbl_penulis ON tbl_buku.id_penulis = tbl_penulis.id_penulis) 
                    INNER JOIN tbl_genre ON tbl_buku.id_genre = tbl_genre.id_genre)
              '''
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblBuku.setRowCount(panjang)
      baris = 0
      
      for i in data:
        nama = i[3]+' '+i[4]+' '+i[5]
        
        self.tblBuku.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblBuku.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblBuku.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblBuku.setItem(baris, 3, QTableWidgetItem(nama))
        self.tblBuku.setItem(baris, 4, QTableWidgetItem(i[6]))
        self.tblBuku.setItem(baris, 5, QTableWidgetItem(i[7].strftime('%d-%m-%Y')))
        self.tblBuku.setItem(baris, 6, QTableWidgetItem(str(i[8])))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat pencarian data')
      
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
                  tbl_buku.isbn, 
                  tbl_buku.judul, 
                  tbl_genre.nama_genre, 
                  tbl_penulis.nama_depan, 
                  tbl_penulis.nama_tengah, 
                  tbl_penulis.nama_belakang, 
                  tbl_buku.penerbit, 
                  tbl_buku.tanggal_publikasi, 
                  tbl_buku.jumlah_stok
                FROM 
                  ((tbl_buku 
                    INNER JOIN tbl_penulis ON tbl_buku.id_penulis = tbl_penulis.id_penulis) 
                    INNER JOIN tbl_genre ON tbl_buku.id_genre = tbl_genre.id_genre)
                WHERE 
                  tbl_buku.judul LIKE "%{search}%" 
                  OR tbl_buku.isbn LIKE "%{search}%"
              '''
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblBuku.setRowCount(panjang)
      baris = 0
      
      for i in data:
        nama = i[3]+' '+i[4]+' '+i[5]
        
        self.tblBuku.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblBuku.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblBuku.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblBuku.setItem(baris, 3, QTableWidgetItem(nama))
        self.tblBuku.setItem(baris, 4, QTableWidgetItem(i[6]))
        self.tblBuku.setItem(baris, 5, QTableWidgetItem(i[7].strftime('%d-%m-%Y')))
        self.tblBuku.setItem(baris, 6, QTableWidgetItem(str(i[8])))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat pencarian data')
      
  def dataPilih(self):
    items = self.tblBuku.selectedItems()
    self.isbn = items[0].text()
    self.title = items[1].text()
    
    self.close()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = CariBuku()
  window.show()
  sys.exit(app.exec_())