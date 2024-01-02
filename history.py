import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class Riwayat(QDialog):
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_history.ui', self)
    
    self.setWindowTitle('History Data')
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

      query = '''
                SELECT 
                  tbl_peminjaman.id_peminjaman,
                  tbl_buku.isbn, tbl_buku.judul, 
                  tbl_anggota.nama_depan, 
                  tbl_anggota.nama_tengah, 
                  tbl_anggota.nama_belakang, 
                  tbl_peminjaman.tanggal_pinjam, 
                  tbl_peminjaman.tanggal_tempo, 
                  tbl_peminjaman.tanggal_kembali,
                  CONCAT('Rp ',
                    FORMAT(
                      CASE
                        WHEN tbl_peminjaman.tanggal_kembali IS NOT NULL AND tbl_peminjaman.tanggal_kembali > tbl_peminjaman.tanggal_tempo THEN
                          -- Menghitung denda hanya untuk hari-hari kerja
                          DATEDIFF(tbl_peminjaman.tanggal_kembali, tbl_peminjaman.tanggal_tempo) * 2000
                          - 
                          -- Mengurangkan denda untuk hari Minggu
                          (DATEDIFF(tbl_peminjaman.tanggal_kembali, tbl_peminjaman.tanggal_tempo) DIV 7) * 2000
                          -
                          -- Mengurangkan denda untuk hari-hari libur
                          (SELECT COUNT(*) FROM tbl_tgl_merah 
                           WHERE tbl_tgl_merah.tgl_merah BETWEEN tbl_peminjaman.tanggal_tempo AND tbl_peminjaman.tanggal_kembali) * 2000
                        ELSE
                          0
                      END, 
                    0)
                  ) AS denda
                FROM 
                  ((tbl_peminjaman 
                    INNER JOIN tbl_buku ON tbl_peminjaman.isbn=tbl_buku.isbn) 
                    INNER JOIN tbl_anggota ON tbl_peminjaman.id_anggota=tbl_anggota.id_anggota)
                WHERE 
                  tbl_peminjaman.tanggal_kembali IS NOT NULL
                ORDER BY
                  tbl_peminjaman.tanggal_kembali;
              '''
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblHistory.setRowCount(panjang)
      baris = 0
      
      for i in data:
        nama = i[3]+' '+i[4]+' '+i[5]
        
        self.tblHistory.setItem(baris, 0, QTableWidgetItem(str(i[0])))
        self.tblHistory.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblHistory.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblHistory.setItem(baris, 3, QTableWidgetItem(nama))
        self.tblHistory.setItem(baris, 4, QTableWidgetItem(i[6].strftime('%d-%m-%Y')))
        self.tblHistory.setItem(baris, 5, QTableWidgetItem(i[7].strftime('%d-%m-%Y')))
        self.tblHistory.setItem(baris, 6, QTableWidgetItem(i[8].strftime('%d-%m-%Y')))
        self.tblHistory.setItem(baris, 7, QTableWidgetItem(str(i[9])))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data')
      
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Riwayat()
  window.show()
  sys.exit(app.exec_())