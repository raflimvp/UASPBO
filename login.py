import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc
from main import *

class Login(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi('form/form_login.ui', self)
    
    self.btnLogin.clicked.connect(self.userLogin)
    self.btnCancel.clicked.connect(self.userCancel)
    self.btnToggle.clicked.connect(self.toggle)
    
  # fungsi menampilkan pesan
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()
    
  # fungsi menghapus teks saat login
  def hapusTeks(self):
    self.editUsername.setText('')
    self.editPassword.setText('')

  # fungsi melakukan login
  def userLogin(self):
    try:
      username = self.editUsername.displayText()
      password = self.editPassword.text()
      
      if username != '' and password != '':
        # konek ke mysql
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        # login berdasarkan data yang tersimpan di database
        query = 'SELECT * FROM tbl_user WHERE username=%s AND password=MD5(%s)'
        value = (username, password)
        cursor = con.cursor()
        cursor.execute(query, value)
        data_user = cursor.fetchall()
        
        if len(data_user) == 1:
          self.hapusTeks()
          tipe_user = data_user[0][4] # pengecekan tipe user
          form = FormMain(tipe_user)
          widget.addWidget(form)
          widget.showMaximized()
          widget.setWindowTitle('Aplikasi Perpustakaan')
          widget.setWindowIcon(QIcon('ICON/library_logo.png'))
          widget.setCurrentIndex(1)
        else:
          self.tampilPesan('Login gagal, silahkan masukkan ulang username dan password anda')
          self.hapusTeks()
          
      else:
        self.tampilPesan('Username dan Password tidak boleh kosong, silahkan masukkan terlebih dahulu')
    
    except:
      self.tampilPesan('Terjadi kesalahan saat login')
  
  # fungsi untuk tombol show hiden password  
  def toggle(self):
    if self.editPassword.echoMode() == QLineEdit.Password:
      self.editPassword.setEchoMode(QLineEdit.Normal)
      self.btnToggle.setIcon(QIcon('ICON/hide.png'))
    else:
      self.editPassword.setEchoMode(QLineEdit.Password)
      self.btnToggle.setIcon(QIcon('ICON/show.png'))
  
  # fungsi tombol cancel untuk keluar dari aplikasi    
  def userCancel(self):
    widget.close()
      
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Login()
  widget = QStackedWidget()
  widget.addWidget(window)
  widget.setMinimumWidth(490)
  widget.setMinimumHeight(250)
  widget.setWindowTitle('Aplikasi Perpustakaan Kelompok 12')
  widget.setWindowIcon(QIcon('ICON/library_logo.png'))
  widget.show()
  sys.exit(app.exec_())