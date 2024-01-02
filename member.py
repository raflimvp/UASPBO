import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import mysql.connector as mc

class Anggota(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi('form/form_member.ui', self)
    
    self.setWindowTitle('Member Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    self.tampilDataAnggota()
    
    self.btnSimpan.clicked.connect(self.simpan)
    self.btnEdit.clicked.connect(self.edit)
    self.btnHapus.clicked.connect(self.hapus)
    self.btnSearch.clicked.connect(self.cari)
    
    self.tblDataAnggota.clicked.connect(self.dataPilih)
    
  # fungsi menampilkan pesan
  def tampilPesan(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/info.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.exec()

  # fungsi tampilan dialog konfirmasi
  def jendelaACC(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/question.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    
    return msgbox.exec()
  
  # fungsi menampilkan data anggota
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
      self.tblDataAnggota.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblDataAnggota.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblDataAnggota.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblDataAnggota.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblDataAnggota.setItem(baris, 3, QTableWidgetItem(i[3]))
        self.tblDataAnggota.setItem(baris, 4, QTableWidgetItem(i[4]))
        self.tblDataAnggota.setItem(baris, 5, QTableWidgetItem(i[5]))
        self.tblDataAnggota.setItem(baris, 6, QTableWidgetItem(i[6]))
        self.tblDataAnggota.setItem(baris, 7, QTableWidgetItem(i[7]))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data anggota')
  
  # fungsi menghapus teks line edit    
  def hapusTeks(self):
    self.editID.setText('')
    self.editNamaDepan.setText('')
    self.editNamaTengah.setText('')
    self.editNamaBelakang.setText('')
    self.cmbJenisKel.setCurrentIndex(0)
    self.editNoTlp.setText('')
    self.editAlamat.setText('')
    self.editEmail.setText('')
  
  # fungsi untuk memilih data   
  def dataPilih(self):
    try:
      # mendapatkan data user
      items = self.tblDataAnggota.selectedItems()
      idAnggota = items[0].text()
      nDepan = items[1].text()
      nTengah = items[2].text()
      nBelakang = items[3].text()
      jenisKel = items[4].text()
      noTlp = items[5].text()
      alamat = items[6].text()
      email = items[7].text()
      
      # menampilkan detail data ke form
      self.editID.setText(idAnggota)
      self.editNamaDepan.setText(nDepan)
      self.editNamaTengah.setText(nTengah)
      self.editNamaBelakang.setText(nBelakang)
      self.editNoTlp.setText(noTlp)
      self.editAlamat.setText(alamat)
      self.editEmail.setText(email)
      
      if jenisKel == 'Laki-laki':
        self.cmbJenisKel.setCurrentIndex(1)
      elif jenisKel == 'Perempuan':
        self.cmbJenisKel.setCurrentIndex(2)
      else:
        pass
      
    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
  
  # fungsi untuk menyimpan data  
  def simpan(self):
    try:
      # mengambil data form
      idAnggota = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      jenisKel = self.cmbJenisKel.currentText()
      noTlp = self.editNoTlp.displayText()
      alamat = self.editAlamat.displayText()
      email = self.editEmail.displayText()
      
      if idAnggota!='' and nDepan!='' and jenisKel!='' and noTlp!='' and alamat!='' and email!='':
        # konek ke mysql
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        # query untuk memasukkan data
        query = '''
                  INSERT INTO tbl_anggota (id_anggota, nama_depan, nama_tengah, nama_belakang, jenis_kelamin, no_telp, alamat, email) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
        value = (idAnggota, nDepan, nTengah, nBelakang, jenisKel, noTlp, alamat, email)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        # menutup koneksi
        con.close()
        
        self.tampilPesan('Data berhasil di simpan')
        
        # menampilkan data setelah penyimpanan
        self.tampilDataAnggota()
        
        # memanggil hapus agar form kosong setelah disimpan
        self.hapusTeks()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menyimpan data anggota')    

  # fungsi edit data
  def edit(self):
    try:
      # mengambil data form
      idAnggota = self.editID.displayText()
      nDepan = self.editNamaDepan.displayText()
      nTengah = self.editNamaTengah.displayText()
      nBelakang = self.editNamaBelakang.displayText()
      jenisKel = self.cmbJenisKel.currentText()
      noTlp = self.editNoTlp.displayText()
      alamat = self.editAlamat.displayText()
      email = self.editEmail.displayText()
      
      if idAnggota != '' and nDepan != '' and jenisKel != '' and noTlp != '' and alamat != '' and email != '':
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
                    tbl_anggota 
                  SET 
                    nama_depan=%s,
                    nama_tengah=%s,
                    nama_belakang=%s,
                    jenis_kelamin=%s,
                    alamat=%s,
                    email=%s 
                  WHERE 
                    id_anggota=%s
                '''
                    
        value = (nDepan, nTengah, nBelakang, jenisKel, alamat, email, idAnggota)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        # menutup koneksi
        con.close()
        
        # menampilkan pesan bila berhasil
        self.tampilPesan('Data berhasil di edit')
        
        # memanggil fungsi menampilkan data pada tabel
        self.tampilDataAnggota()
        
        # memanggil fungsi hapusTeks agar form kosong setelah dihapus
        self.hapusTeks()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat mengedit data')
      
  # fungsi menghapus data
  def hapus(self):
    try:
      # mengambil id anggota
      idAnggota = self.editID.displayText()
      
      if idAnggota != '':
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
          query = '''
                    DELETE FROM tbl_anggota 
                    WHERE id_anggota=%s
                  '''
                    
          value = (idAnggota,)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()
          
          # menutup koneksi
          con.close()
          
          self.tampilPesan('Data berhasil di hapus')
          
          self.tampilDataAnggota()
          
          # memanggil fungsi hapus agar form kosong setelah dihapus
          self.hapusTeks()
        else:
          pass
      
      else:
        self.tampilPesan('Data kosong, silahkan pilih data terlebih dahulu')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menghapus data')
  
  # fungsi pencarian data    
  def cari(self):
    try:
      search = self.editSearch.displayText()
      con = mc.connect(
              host='localhost',
              user='root',
              password='', 
              database='pboperpus',
              port='3306')
      
      query =f'''
                SELECT * FROM tbl_anggota
                WHERE 
                  id_anggota LIKE "%{search}%" OR 
                  nama_depan LIKE "%{search}%" OR 
                  nama_tengah LIKE "%{search}%" OR 
                  nama_belakang LIKE "%{search}%"
              '''
              
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblDataAnggota.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblDataAnggota.setItem(baris, 0, QTableWidgetItem(i[0]))
        self.tblDataAnggota.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblDataAnggota.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblDataAnggota.setItem(baris, 3, QTableWidgetItem(i[3]))
        self.tblDataAnggota.setItem(baris, 4, QTableWidgetItem(i[4]))
        self.tblDataAnggota.setItem(baris, 5, QTableWidgetItem(i[5]))
        self.tblDataAnggota.setItem(baris, 6, QTableWidgetItem(i[6]))
        self.tblDataAnggota.setItem(baris, 7, QTableWidgetItem(i[7]))
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat pencarian data')

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Anggota()
  window.show()
  sys.exit(app.exec_())