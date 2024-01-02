import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc
from datetime import datetime
from author import *
from genre import *

class Buku(QMainWindow):
  
  def __init__(self):
    super().__init__()
    loadUi('form/form_book.ui', self)
    
    self.setWindowTitle('Book Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataGenre()
    self.tampilDataPenulis()
    self.tampilDataBuku()
    
    self.tblBuku.clicked.connect(self.dataPilih)

    self.btnAddGenre.clicked.connect(self.tampilDialogGenre)
    self.btnAddPenulis.clicked.connect(self.tampilDialogPenulis)
    self.btnSimpan.clicked.connect(self.simpan)
    self.btnEdit.clicked.connect(self.edit)
    self.btnHapus.clicked.connect(self.hapus)
    self.btnSearch.clicked.connect(self.cari)
    
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()

  def jendelaACC(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/question.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    
    return msgbox.exec()
  
  def hapusTeks(self):
    self.editISBN.setText('')
    self.editJudul.setText('')
    self.cmbGenre.setCurrentIndex(0)
    self.cmbPenulis.setCurrentIndex(0)
    self.editPenerbit.setText('')
    self.dateTerbit.setDate(datetime.today())
    self.editStok.setText('')
  
  def tampilDataGenre(self):
    try:
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      query = 'SELECT * FROM tbl_genre'
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      self.cmbGenre.clear()
      self.cmbGenre.addItem('')
      
      for i in data:
        self.cmbGenre.addItem(i[1])
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data genre')
      
  def tampilDialogGenre(self):
    form = Genre()
    form.exec()
    self.tampilDataGenre()
    
  def tampilDataPenulis(self):
    try:
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      query = 'SELECT * FROM tbl_penulis'
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      self.cmbPenulis.clear()
      self.cmbPenulis.addItem('')
      
      for i in data:
        self.cmbPenulis.addItem(i[1] + ' ' + i[2] + ' ' + i[3])
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data penulis')    
      
  def tampilDialogPenulis(self):
    form = Penulis()
    form.exec()
    self.tampilDataPenulis()
    
  # fungsi untuk mendapatkan semua data dari penulis
  def getDataPenulis(self, flag, key):
    try:
      nDepan = ''
      nTengah = ''
      nBelakang = ''
      query = ''
      
      # flag 1 untuk mendapatkan nama penulis dan flag 2 untuk mendapatkan id penulis
      if flag == 1:
        query = f'''
                    SELECT 
                      nama_depan, 
                      nama_tengah, 
                      nama_belakang 
                    FROM 
                      tbl_penulis 
                    WHERE 
                      id_penulis="{key}" 
                '''
      elif flag == 2:
        nLengkap = key.split()
        
        if len(nLengkap) == 3:
          nDepan = nLengkap[0]
          nTengah = nLengkap[1]
          nBelakang = nLengkap[2]
        elif len(nLengkap) == 2:
          nDepan = nLengkap[0]
          nTengah = nLengkap[1]
          nBelakang = nLengkap[1]
        elif len(nLengkap) == 1:
          nDepan = nLengkap[0]
          
        query = f'''
                    SELECT 
                      id_penulis 
                    FROM 
                      tbl_penulis 
                    WHERE 
                      nama_depan LIKE "%{nDepan}%" 
                      OR nama_tengah LIKE "%{nTengah}%" 
                      OR nama_belakang LIKE "%{nBelakang}%"
                '''

      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      # menyimpan nilai balik fungsi
      x = ''
      if flag == 1:
        x = data[0][0]+' '+data[0][1]+' '+data[0][2]
      elif flag == 2:
        x = data[0][0]
        
      return x
    
    except:
      self.tampilPesan('Terjadi kesalahan saat mengakses data penulis')
    
  # fungsi untuk mendapatkan semua data dari penulis
  def getDataGenre(self, flag, key):  
    try:
      query = ''
      if flag == 1:
        query = f'SELECT nama_genre FROM tbl_genre WHERE id_genre="{key}"'
      elif flag == 2:
        query = f'SELECT id_genre FROM tbl_genre WHERE nama_genre LIKE "%{key}%"'
        
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      x = data[0][0]
      
      return x
    
    except:
      self.tampilPesan('Terjadi kesalahan saat mengakses data genre')
      
  def tampilDataBuku(self):
    try:
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        query = 'SELECT * FROM tbl_buku'
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        
        con.close()
        
        panjang = len(data)
        self.tblBuku.setRowCount(panjang)
        baris = 0
        
        for i in data:
          genre = self.getDataGenre(1, i[1])
          penulis = self.getDataPenulis(1, i[2])
          
          self.tblBuku.setItem(baris, 0, QTableWidgetItem(i[0]))
          self.tblBuku.setItem(baris, 1, QTableWidgetItem(i[3]))
          self.tblBuku.setItem(baris, 2, QTableWidgetItem(genre))
          self.tblBuku.setItem(baris, 3, QTableWidgetItem(penulis))
          self.tblBuku.setItem(baris, 4, QTableWidgetItem(i[4]))
          self.tblBuku.setItem(baris, 5, QTableWidgetItem(i[5].strftime('%d-%m-%Y')))
          self.tblBuku.setItem(baris, 6, QTableWidgetItem(str(i[6])))
          
          baris += 1
          
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data buku')
      
  def dataPilih(self):
    try:
      items = self.tblBuku.selectedItems()
      isbn = items[0].text()
      judul = items[1].text()
      genre = items[2].text()
      penulis = items[3].text()
      penerbit = items[4].text()
      terbit = items[5].text()
      stok = items[6].text()
      
      self.editISBN.setText(isbn)
      self.editJudul.setText(judul)
      self.cmbGenre.setCurrentText(genre)
      self.cmbPenulis.setCurrentText(penulis)
      self.editPenerbit.setText(penerbit)
      self.dateTerbit.setDate(datetime.strptime(terbit,'%d-%m-%Y'))
      self.editStok.setText(stok)
    
    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
      
  def simpan(self):
    try:
      isbn = self.editISBN.displayText()
      judul = self.editJudul.toPlainText()
      genre = self.cmbGenre.currentText()
      penulis = self.cmbPenulis.currentText()
      penerbit = self.editPenerbit.displayText()
      terbit = self.dateTerbit.date()
      stok = self.editStok.displayText()
      
      if isbn!='' and judul!='' and genre!='' and penulis!='' and penerbit!='' and terbit!='' and stok!='':
        idGenre = self.getDataGenre(2, genre)
        idPenulis = self.getDataPenulis(2, penulis)
        
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        query = '''
                  INSERT INTO tbl_buku (isbn, judul, id_genre, id_penulis, penerbit, tanggal_publikasi, jumlah_stok) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                
        value = (isbn, judul, idGenre, idPenulis, penerbit, terbit.toString('yyyy-MM-dd'), int(stok))
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()
        
        self.tampilPesan('Data berhasil di simpan')
        
        self.hapusTeks()
        
        self.tampilDataBuku()
        
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
    except:
      self.tampilPesan('Terjadi kesalahan saat menyimpan data')
      
  def edit(self):
    try:
      isbn = self.editISBN.displayText()
      judul = self.editJudul.toPlainText()
      genre = self.cmbGenre.currentText()
      penulis = self.cmbPenulis.currentText()
      penerbit = self.editPenerbit.displayText()
      terbit = self.dateTerbit.date()
      stok = self.editStok.displayText()

      if isbn!= '' and judul!= '' and genre!= '' and penulis!= '' and penerbit!= '' and stok!= '':
        # konek ke mysql
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')

        # mendapatkan id genre dan penulis
        idGenre = self.getDataGenre(2, genre)
        idPenulis = self.getDataPenulis(2, penulis)

        # query edit data
        query = 'UPDATE tbl_buku SET judul=%s, id_genre=%s, id_penulis=%s, penerbit=%s, tanggal_publikasi=%s, jumlah_stok=%s WHERE isbn=%s'
        value = (judul, idGenre, idPenulis, penerbit, terbit.toString('yyyy-MM-dd'), stok, isbn)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()

        # menutup koneksi
        con.close()

        # menampilkan pesan bila berhasil
        self.tampilPesan('Data berhasil di edit')

        # memanggil fungsi menampilkan data pada tabel
        self.tampilDataBuku()

        # memanggil fungsi hapusTeks agar form kosong setelah dihapus
        self.hapusTeks()  
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat mengedit data')
      
  def hapus(self):
    try:
      isbn = self.editISBN.displayText()
      
      if isbn != '':
        msgbox = self.jendelaACC('Apakah anda yakin ingin menghapus data ini ?')
        
        if msgbox == QMessageBox.Ok:
          # konek ke mysql
          con = mc.connect(
            host='localhost',
            user='root',
            password='', 
            database='pboperpus',
            port='3306')
          
          # query hapus data
          query = 'DELETE FROM tbl_buku WHERE isbn=%s'
          value = (isbn,)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()
          
          con.close()
          
          self.tampilPesan('Data berhasil di hapus')
          
          self.tampilDataBuku()
          
          self.hapusTeks()
        else:
          pass
      
      else:
        self.tampilPesan('Data kosong, silahkan pilih data terlebih dahulu')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menghapus data')
      
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
                    OR tbl_penulis.nama_depan LIKE "%{search}%"
                    OR tbl_penulis.nama_tengah LIKE "%{search}%"
                    OR tbl_penulis.nama_belakang LIKE "%{search}%"
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
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Buku()
  window.show()
  sys.exit(app.exec_())