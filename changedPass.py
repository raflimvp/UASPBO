import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class UbahPass(QDialog):
  def __init__(self, idUser):
    super().__init__()
    loadUi('dialog/dialog_changedPass.ui', self)
    
    self.idUser = idUser
    
    self.setWindowTitle('Changed Password')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.accepted.connect(self.tombolOk)
    self.rejected.connect(self.tombolCancel)
    self.btnToggle.clicked.connect(self.toggle)
    
  # fungsi menampilkan pesan
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowTitle('Data Perpustakaan')
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()

  def tombolOk(self):
    try:
      passBaru = self.editPassBaru.text()
      idUser = self.idUser
      # konek ke mysql
      con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
      
      # mengubah pass pada tbl_user di database
      query = 'UPDATE tbl_user SET password = MD5(%s) WHERE id_user = %s'
      data = (passBaru, idUser)
      cursor = con.cursor()
      cursor.execute(query, data)
      con.commit()
      
      con.close()
      
      self.tampilPesan('Password berhasil di ubah')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat mengubah password')
      
  # fungsi untuk tombol show hiden password  
  def toggle(self):
    if self.editPassBaru.echoMode() == QLineEdit.Password:
      self.editPassBaru.setEchoMode(QLineEdit.Normal)
      self.btnToggle.setIcon(QIcon('ICON/hide.png'))
    else:
      self.editPassBaru.setEchoMode(QLineEdit.Password)
      self.btnToggle.setIcon(QIcon('ICON/show.png'))
      
  def tombolCancel(self):
    self.close()
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = UbahPass('ADM001')
  window.show()
  sys.exit(app.exec_())