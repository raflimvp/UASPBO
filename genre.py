import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class Genre(QDialog):
  
  def __init__(self):
    super().__init__()
    loadUi('dialog/dialog_genre.ui', self)
    
    self.setWindowTitle('Genre Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataGenre()
    
    self.btnSimpan.clicked.connect(self.simpan)
    self.btnEdit.clicked.connect(self.edit)
    self.btnHapus.clicked.connect(self.hapus)
    
    self.tblGenre.clicked.connect(self.dataPilih)
    
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
    self.editNamaGenre.setText('')
    
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
      
      panjang = len(data)
      self.tblGenre.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblGenre.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblGenre.setItem(baris, 1, QTableWidgetItem(i[1]))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data genre')
      
  def dataPilih(self):
    try:
      items = self.tblGenre.selectedItems()
      idGenre = items[0].text()
      nGenre = items[1].text()
      
      self.editID.setText(idGenre)
      self.editNamaGenre.setText(nGenre)

    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
      
  def simpan(self):
    try:
      idGenre = self.editID.displayText()
      nGenre = self.editNamaGenre.displayText()
      
      if idGenre != '' and nGenre != '':
        con = mc.connect(
        host='localhost',
        user='root',
        password='', 
        database='pboperpus',
        port='3306')
        
        query = '''
                  INSERT INTO tbl_genre(id_genre, nama_genre) 
                  VALUES (%s, %s)
                '''
                
        value = (idGenre, nGenre)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()
        
        self.tampilPesan('Data berhasil di simpan')
        
        self.hapusTeks()

        self.tampilDataGenre()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menyimpan data')
      
  def edit(self):
    try:
      idGenre = self.editID.displayText()
      nGenre = self.editNamaGenre.displayText()
      
      if idGenre != '' and nGenre != '':
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')

        query = '''
                  UPDATE 
                    tbl_genre 
                  SET 
                    nama_genre=%s 
                  WHERE 
                    id_genre=%s
                '''
                
        value = (nGenre, idGenre)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()
        
        self.tampilPesan('Data berhasil di edit')
        
        self.tampilDataGenre()

        self.hapusTeks()
          
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat mengedit data')
      
  def hapus(self):
    try:
      idGenre = self.editID.displayText()
      
      if idGenre != '':
        msgbox = self.jendelaACC('Apakah anda yakin ingin menghapus data ini ?')
        
        if msgbox == QMessageBox.Ok:
          con = mc.connect(
            host='localhost',
            user='root',
            password='', 
            database='pboperpus',
            port='3306')
          
          query = 'DELETE FROM tbl_genre WHERE id_genre=%s'
          value = (idGenre,)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()
          
          con.close()
          
          self.tampilPesan('Data berhasil di hapus')
          
          self.tampilDataGenre()

          self.hapusTeks()
        else:
          pass
      
      else:
        self.tampilPesan('Data kosong, silahkan pilih data terlebih dahulu')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menghapus data')
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Genre()
  window.show()
  sys.exit(app.exec_())