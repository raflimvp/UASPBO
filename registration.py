import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QMenu, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc
from changedPass import *

class Registrasi(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi('form/form_register.ui', self)
    self.setWindowTitle('User Registration')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataRegister()
    
    # tombol
    self.btnSimpan.clicked.connect(self.simpan)
    self.btnEdit.clicked.connect(self.edit)
    self.btnHapus.clicked.connect(self.hapus)
    self.btnToggle.clicked.connect(self.toggle)
    self.btnUbahPass.clicked.connect(self.tampilDialogUbahPass)
    
    self.tblUser.clicked.connect(self.dataPilih)
    
  # fungsi menampilkan pesan
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowTitle('Data Perpustakaan')
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()
    
  # fungsi jendela konfirmasi
  def jendelaACC(self, pesan):
    msgbox = QMessageBox()
    msgbox.setIcon(QMessageBox.Question)
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setIconPixmap(QIcon('ICON/question.png').pixmap(40, 40))
    msgbox.setText(pesan)
    msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    
    return msgbox.exec()
  
  # fungsi menghapus teks saat login
  def hapusTeks(self):
    self.editID.setText('')
    self.editNamaDepan.setText('')
    self.editNamaTengah.setText('')
    self.editNamaBelakang.setText('')
    self.cmbTipeUser.setCurrentIndex(0)
    self.editUsername.setText('')
    self.editPassword.setText('')
    
  # fungsi menampilkan data register
  def tampilDataRegister(self):
    try:
      # konek ke mysql
      con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
      
      # akses data user pada tbl_user
      query = 'SELECT * FROM tbl_user'
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      # menutup koneksi 
      con.close()
      
      # menampilkan data user ke form tabel
      panjang = len(data)
      self.tblUser.setRowCount(panjang)
      baris = 0
      for i in data:
        self.tblUser.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblUser.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblUser.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblUser.setItem(baris, 3, QTableWidgetItem(i[3]))
        self.tblUser.setItem(baris, 4, QTableWidgetItem(i[4]))
        self.tblUser.setItem(baris, 5, QTableWidgetItem(i[5]))
        baris += 1
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data pengguna')
      
  # fungsi untuk tombol show hiden password  
  def toggle(self):
    if self.editPassword.echoMode() == QLineEdit.Password:
      self.editPassword.setEchoMode(QLineEdit.Normal)
      self.btnToggle.setIcon(QIcon('ICON/hide.png'))
    else:
      self.editPassword.setEchoMode(QLineEdit.Password)
      self.btnToggle.setIcon(QIcon('ICON/show.png'))
      
  # fungsi simpan data user
  def simpan(self):
    try:
      idUser = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      tipeUser = self.cmbTipeUser.currentText()
      username = self.editUsername.displayText()
      password = self.editPassword.text()
      
      if idUser != '' and nDepan != '' and tipeUser != '' and username != '' and password != '':
        # konek ke mysql
        con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
        
        # menyimpan data tabel form ke data tbl_user
        query = '''
                  INSERT INTO tbl_user(id_user, nama_depan, nama_tengah, nama_belakang, tipe_user, username, password) 
                  VALUES(%s, %s, %s, %s, %s, %s, MD5(%s))
                '''
        value = (idUser, nDepan, nTengah, nBelakang, tipeUser, username, password)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        # menutup koneksi
        con.close()
        
        # menampilkan pesan bila berhasil
        self.tampilPesan('Data berhasil di simpan')
        
        # hapus teks setelah disimpan
        self.hapusTeks()
        
        # menampilkan data user pada tabel dengan memanggil fungsi tampilDataRegister
        self.tampilDataRegister()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menyimpan data')
      
  # fungsi menampilkan data user bilsa di pilih
  def dataPilih(self):
    try:
      # mendapatkan data user
      items = self.tblUser.selectedItems()
      idUser = items[0].text()
      nDepan = items[1].text()
      nTengah = items[2].text()
      nBelakang = items[3].text()
      tipeUser = items[4].text()
      username = items[5].text()
      
      # menampilkan detail data ke form
      self.editID.setText(idUser)
      self.editNamaDepan.setText(nDepan)
      self.editNamaTengah.setText(nTengah)
      self.editNamaBelakang.setText(nBelakang)
      self.editUsername.setText(username)
      if tipeUser == 'Administrator':
        self.cmbTipeUser.setCurrentIndex(1)
      elif tipeUser == 'User':
        self.cmbTipeUser.setCurrentIndex(2)
      else:
        pass
      
    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
      
  # fungsi edit data user
  def edit(self):
    try:
      # mengambil data form
      idUser = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      tipeUser = self.cmbTipeUser.currentText()
      username = self.editUsername.displayText()
      
      if idUser != '' and nDepan != '' and tipeUser != '' and username != '':
        # konek ke mysql
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        # query edit data
        query = '''
                  UPDATE 
                    tbl_user 
                  SET 
                    nama_depan=%s, 
                    nama_tengah=%s, 
                    nama_belakang=%s, 
                    tipe_user=%s, 
                    username=%s 
                  WHERE 
                    id_user=%s
                '''
        value = (nDepan, nTengah, nBelakang, tipeUser, username, idUser)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        # menutup koneksi
        con.close()
        
        # menampilkan pesan bila berhasil
        self.tampilPesan('Data berhasil di edit')
        
        # memanggil fungsi menampilkan data pada tabel
        self.tampilDataRegister()
        
        # memanggil fungsi hapusTeks agar form kosong setelah dihapus
        self.hapusTeks()
          
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
    except:
      self.tampilPesan('Terjadi kesalahan saat mengedit data')
      
  # fungsi data user
  def hapus(self):
    try:
      # mengambil id user
      idUser = self.editID.displayText()
      
      if idUser != '':
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
          query = 'DELETE FROM tbl_user WHERE id_user=%s'
          value = (idUser,)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()
          
          # menutup koneksi
          con.close()
          
          self.tampilPesan('Data berhasil di hapus')
          
          self.tampilDataRegister()
          
          # memanggil fungsi hapusTeks agar form kosong setelah dihapus
          self.hapusTeks()
        else:
          pass
      
      else:
        self.tampilPesan('Data kosong, silahkan pilih data terlebih dahulu')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menghapus data')
      
  # fungsi menampilkan dialog ubah password
  def tampilDialogUbahPass(self):
    try:
      idUser = self.editID.displayText()
      if idUser != '':
        form = UbahPass(idUser)
        form.exec()
      else:
        self.tampilPesan('Silahkan pilih user yang ingin di ubah passwordnya')
    except:
      self.tampilPesan('Terjadi kesalahan saat mengganti password')
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Registrasi()
  window.show()
  sys.exit(app.exec_())