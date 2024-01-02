import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class BukuBelumKembali(QDialog):
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_notYetBack.ui', self)
    
    self.setWindowTitle('Book Data That Has Not Been Returned')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilData()
    
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()

  def tampilData(self):
    try:
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      query = f'''
                SELECT 
                  tbl_peminjaman.id_peminjaman, 
                  tbl_buku.judul, 
                  tbl_anggota.nama_depan, 
                  tbl_anggota.nama_tengah, 
                  tbl_anggota.nama_belakang, 
                  tbl_peminjaman.tanggal_pinjam, 
                  tbl_peminjaman.tanggal_tempo, 
                  tbl_peminjaman.tanggal_kembali
                FROM 
                  ((tbl_peminjaman 
                    INNER JOIN tbl_buku ON tbl_peminjaman.isbn=tbl_buku.isbn) 
                    INNER JOIN tbl_anggota ON tbl_peminjaman.id_anggota=tbl_anggota.id_anggota)
                WHERE 
                  tbl_peminjaman.tanggal_kembali IS NULL
              '''
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblBookNotYetBack.setRowCount(panjang)
      baris = 0
      
      for i in data:
        nama = i[2]+' '+i[3]+' '+i[4]
        
        self.tblBookNotYetBack.setItem(baris, 0, QTableWidgetItem(str(i[0])))
        self.tblBookNotYetBack.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblBookNotYetBack.setItem(baris, 2, QTableWidgetItem(nama))
        self.tblBookNotYetBack.setItem(baris, 3, QTableWidgetItem(i[5].strftime('%d-%m-%Y')))
        self.tblBookNotYetBack.setItem(baris, 4, QTableWidgetItem(i[6].strftime('%d-%m-%Y')))
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data')
      
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = BukuBelumKembali()
  window.show()
  sys.exit(app.exec_())