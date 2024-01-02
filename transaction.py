import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
import mysql.connector as mc
from datetime import datetime, timedelta
from searchMember import *
from searchBook import *
from notBackYet import *
from history import *

class Transaksi(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi('form/form_transaction.ui', self)
    
    self.setWindowTitle('Transaction Data')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    # mengatur tanggal saat ini
    self.datePinjam.setDate(QDate.currentDate())
    self.dateTempo.setDate(QDate.currentDate())
    self.dateKembali.setDate(QDate.currentDate())
    
    # mengatur tanggal 14 hari setelah hari ini
    self.dateTempo.setDate(datetime.today() + timedelta(days=14))
    self.dateKembali.setDate(datetime.today() + timedelta(days=14))
    
    self.tblPeminjaman.clicked.connect(self.dataPilih)
    
    # tombol-tombol
    self.btnBorrow.clicked.connect(self.pinjam)
    self.btnReturn.clicked.connect(self.kembali)
    self.btnCancel.clicked.connect(self.batal)
    self.btnSearchMember.clicked.connect(self.tampilDialogAnggota)
    self.btnSearchBook.clicked.connect(self.tampilDialogBuku)
    self.btnNotBackYet.clicked.connect(self.tampilDialogBukuBelumKembali)
    self.btnHistory.clicked.connect(self.tampilDialogRiwayat)
    
  def tampilDialogAnggota(self):
    form = CariAnggota()
    form.exec()
    self.editIDAnggota.setText(form.id_member)
    self.editNamaAnggota.setText(form.name)
    
    self.tampilDataPeminjaman(form.id_member)
    
  def tampilDialogBuku(self):
    form = CariBuku()
    form.exec()
    self.editISBN.setText(form.isbn)
    self.editJudul.setText(form.title)
    
  def tampilDialogBukuBelumKembali(self):
    form = BukuBelumKembali()
    form.exec()

  def tampilDialogRiwayat(self):
    form = Riwayat()
    form.exec()

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
    
  def hapusTeks(self):
    self.editISBN.setText('')
    self.editJudul.setText('')
    self.datePinjam.setDate(datetime.today())
    self.dateTempo.setDate(datetime.today() + timedelta(days=14))
    self.dateKembali.setDate(datetime.today() + timedelta(days=14))
    
  def tampilDataPeminjaman(self, idAnggota):
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
                  tbl_buku.isbn, tbl_buku.judul, 
                  tbl_peminjaman.tanggal_pinjam, 
                  tbl_peminjaman.tanggal_tempo, 
                  tbl_peminjaman.tanggal_kembali
                FROM 
                  (tbl_peminjaman 
                    INNER JOIN tbl_buku ON tbl_peminjaman.isbn=tbl_buku.isbn)
                WHERE 
                  tbl_peminjaman.id_anggota="{idAnggota}" AND tbl_peminjaman.tanggal_kembali IS NULL
              '''
      cursor = con.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      
      con.close()
      
      panjang = len(data)
      self.tblPeminjaman.setRowCount(panjang)
      baris = 0
      
      for i in data:
        self.tblPeminjaman.setItem(baris, 0, QTableWidgetItem(str(i[0])))
        self.tblPeminjaman.setItem(baris, 1, QTableWidgetItem(i[1]))
        self.tblPeminjaman.setItem(baris, 2, QTableWidgetItem(i[2]))
        self.tblPeminjaman.setItem(baris, 3, QTableWidgetItem(i[3].strftime('%d-%m-%Y')))
        self.tblPeminjaman.setItem(baris, 4, QTableWidgetItem(i[4].strftime('%d-%m-%Y')))
        
        baris += 1
        
    except:
      self.tampilPesan('Terjadi kesalahan saat menampilkan data')
      
  def dataPilih(self):
    try:
      items = self.tblPeminjaman.selectedItems()
      self.idPeminjaman = items[0].text()
      isbn = items[1].text()
      judul = items[2].text()
      tglPinjam = items[3].text()
      tglTempo = items[4].text()
      
      self.editISBN.setText(isbn)
      self.editJudul.setText(judul)
      self.datePinjam.setDate(datetime.strptime(tglPinjam, '%d-%m-%Y'))
      self.dateTempo.setDate(datetime.strptime(tglTempo, '%d-%m-%Y'))
      
    except:
      self.tampilPesan('Terjadi kesalahan saat memilih data')
      
  def pinjam(self):
    try:
      idAnggota = self.editIDAnggota.displayText()
      namaAnggota = self.editNamaAnggota.displayText()
      isbn = self.editISBN.displayText()
      tglPinjam = self.datePinjam.date()
      tglTempo = self.dateTempo.date()
      pinjam = -1  # mengurangi stok saat dipinjam 
      
      if idAnggota!='' and isbn!='':
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        # mengurangi stok buku
        query = 'SELECT jumlah_stok from tbl_buku WHERE isbn=%s'
        value = (isbn,)
        cursor = con.cursor()
        cursor.execute(query, value)
        stok = cursor.fetchone()[0]
        
        # validasi jika stok buku habis
        if stok > 0:
          query = '''
                    INSERT INTO tbl_peminjaman(isbn, id_anggota, tanggal_pinjam, tanggal_tempo) 
                    VALUES(%s, %s, %s, %s)
                  '''

          value = (isbn, idAnggota, tglPinjam.toString('yyyy-MM-dd'), tglTempo.toString('yyyy-MM-dd'))
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()
          
          # update stok buku
          query = 'UPDATE tbl_buku SET jumlah_stok = jumlah_stok + %s WHERE isbn=%s'
          value = (pinjam, isbn)
          cursor = con.cursor()
          cursor.execute(query, value)
          con.commit()

          self.tampilPesan('Peminjaman buku berhasil')
        else:
          self.tampilPesan('Maaf, stok buku yang ingin di pinjam sudah habis')
          
        con.close()
        
        self.tampilDataPeminjaman(idAnggota)
        
        self.hapusTeks()
        
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat melakukan peminjaman')
      
  def kembali(self):
    try:
      idPeminjaman = self.idPeminjaman
      idAnggota = self.editIDAnggota.displayText()
      isbn = self.editISBN.displayText()
      tglKembali = self.dateKembali.date()
      kembali = 1  # menambahkan stok saat dikembalikan
      
      if idPeminjaman!='' and idAnggota!='' and isbn!='':
        con = mc.connect(
          host='localhost',
          user='root',
          password='', 
          database='pboperpus',
          port='3306')
        
        query = 'UPDATE tbl_peminjaman SET tanggal_kembali=%s WHERE id_peminjaman=%s'
        value = (tglKembali.toString('yyyy-MM-dd'), int(idPeminjaman))
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        # update stok buku
        query = 'UPDATE tbl_buku SET jumlah_stok = jumlah_stok + %s WHERE isbn=%s'
        value = (kembali, isbn)
        cursor = con.cursor()
        cursor.execute(query, value)
        con.commit()
        
        con.close()

        self.tampilPesan('Pengembalian buku berhasil')
        
        self.tampilDataPeminjaman(idAnggota)
        
        self.hapusTeks()
      else:
        self.tampilPesan('Data tidak boleh kosong, silahkan lengkapi !')
        
    except:
      self.tampilPesan('Terjadi kesalahan saat melakukan pengembalian')

  def batal(self):
    try:
      idPeminjaman = self.idPeminjaman
      idAnggota = self.editIDAnggota.displayText()
      isbn = self.editISBN.displayText()
      kembali = 1
      
      if idPeminjaman!='' and idAnggota!='' and isbn!='':
        msgbox = self.jendelaACC('Apakah anda yakin ingin membatalkan pinjaman ?')
        
        if msgbox == QMessageBox.Ok:
          con = mc.connect(
            host='localhost',
            user='root',
            password='', 
            database='pboperpus',
            port='3306')

          query = 'DELETE FROM tbl_peminjaman WHERE id_peminjaman=%s'
          value = (int(idPeminjaman),)
          cursor = con.cursor()
          cursor.execute(query, value)
          
          # update stok buku
          query = 'UPDATE tbl_buku SET jumlah_stok = jumlah_stok + %s WHERE isbn=%s'
          value = (kembali, isbn)
          cursor = con.cursor()
          cursor.execute(query, value)

          con.commit()
                    
          con.close()
          
          self.tampilDataPeminjaman(idAnggota)
          
          self.hapusTeks()
        
    except:
      self.tampilPesan('Terjadi kesalahan saat membatalkan peminjaman')

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Transaksi()
  window.show()
  sys.exit(app.exec_())