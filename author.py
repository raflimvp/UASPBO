import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class Penulis(QDialog):
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_author.ui', self)
    
    self.setWindowTitle('Author Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataPenulis()
    
    self.btnSimpan.clicked.connect(self.simpan)
    self.btnEdit.clicked.connect(self.edit)
    self.btnHapus.clicked.connect(self.hapus)
    self.btnSearch.clicked.connect(self.cari)
    
    self.tblPenulis.clicked.connect(self.dataPilih)
    
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
    self.editID.setText('')
    self.editNamaDepan.setText('')
    self.editNamaTengah.setText('')
    self.editNamaBelakang.setText('')
    
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
      
      # menampilkan data penulis ke form tabel
      panjang = len(data)
      self.tblPenulis.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblPenulis.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblPenulis.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblPenulis.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblPenulis.setItem(baris, 3, QTableWidgetItem(i[3]))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data pengguna')
      
  def dataPilih(self):
    try:
      # mengambil data penulis
      items = self.tblPenulis.selectedItems()
      idPenulis = items[0].text()
      nDepan = items[1].text()
      nTengah = items[2].text()
      nBelakang = items[3].text()
      
      # menampilkan detail data ke form
      self.editID.setText(idPenulis)
      self.editNamaDepan.setText(nDepan)
      self.editNamaTengah.setText(nTengah)
      self.editNamaBelakang.setText(nBelakang)

    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
      
  def simpan(self):
    try:
      idPenulis = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      
      if idPenulis != '' and nDepan != '':
        con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')

        query = '''
                  INSERT INTO tbl_penulis(id_penulis, nama_depan, nama_tengah, nama_belakang) 
                  VALUES (%s, %s, %s, %s)
                '''
                
        value = (idPenulis, nDepan, nTengah, nBelakang)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()
        
        self.tampilPesan('Data berhasil di simpan')
        
        self.hapusTeks()
        
        self.tampilDataPenulis()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menyimpan data')
      
  def edit(self):
    try:
      # mengambil data form
      idPenulis = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      
      if idPenulis != '' and nDepan != '':
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')

        query = '''
                  UPDATE 
                    tbl_penulis 
                  SET 
                    nama_depan=%s, 
                    nama_tengah=%s, 
                    nama_belakang=%s 
                  WHERE 
                    id_penulis=%s
                '''
                
        value = (nDepan, nTengah, nBelakang, idPenulis)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()

        self.tampilPesan('Data berhasil di edit')

        self.tampilDataPenulis()

        self.hapusTeks()
          
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat mengedit data')
      
  def hapus(self):
    try:
      # mengambil id penulis
      idPenulis = self.editID.displayText()
      
      if idPenulis != '':
        msgbox = self.jendelaACC('Apakah anda yakin ingin menghapus data ini ?')
        
        if msgbox == QMessageBox.Ok:
          con = mc.connect(
            host='localhost',
            user='root',
            password='', 
            database='pboperpus',
            port='3306')

          query = 'DELETE FROM tbl_penulis WHERE id_penulis=%s'
          value = (idPenulis,)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()

          con.close()
          
          self.tampilPesan('Data berhasil di hapus')
          
          self.tampilDataPenulis()

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
      
      query = f''''
                  SELECT * 
                  FROM tbl_penulis 
                  WHERE 
                    id_penulis LIKE "%{search}%" OR 
                    nama_depan LIKE "%{search}%" OR 
                    nama_tengah LIKE "%{search}%" OR 
                    nama_belakang LIKE "%{search}%"
                '''
                
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblPenulis.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblPenulis.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblPenulis.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblPenulis.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblPenulis.setItem(baris, 3, QTableWidgetItem(i[3]))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat pencarian data')
    
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Penulis()
  window.show()
  sys.exit(app.exec_())