import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMdiArea, QMenuBar, QAction, QMdiSubWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from registration import *
from member import *
from book import *
from transaction import *

class FormMain(QMainWindow):
  def __init__(self, tipeUser):
    super().__init__()
    loadUi('form/form_main.ui', self)
    
    self.setWindowTitle('Aplikasi Perpustakaan Kelompok 12')
    self.setWindowIcon(QIcon('ICON/library_logo.png'))
    
    # membuat Mdi
    self.mdi = QMdiArea()
    self.setCentralWidget(self.mdi)
    
    # menu bar
    self.menu_bar = QMenuBar()
    
    administrator = self.menu_bar.addMenu('Administrator')
    data = self.menu_bar.addMenu('Data')
    transaksi = self.menu_bar.addMenu('Transaksi')
    user = self.menu_bar.addMenu('User')
    
    # sub menu
    dataUser = QAction(QIcon('ICON/account.png'), 'Registrasi Pengguna', self)
    administrator.addAction(dataUser)
    
    dataMember = QAction(QIcon('ICON/member.png'), 'Data Anggota', self)
    dataBook = QAction(QIcon('ICON/book.png'), 'Data Buku', self)
    data.addAction(dataMember)
    data.addAction(dataBook)
    
    dataLoan = QAction(QIcon('ICON/loan_transaction.png'), 'Transaksi Peminjaman Pengembalian', self)
    transaksi.addAction(dataLoan)
    
    logout = QAction(QIcon('ICON/logout.png'),'Logout', self)
    exitApp = QAction(QIcon('ICON/exit.png'),'Keluar', self)
    user.addAction(logout)
    user.addAction(exitApp)
    
    self.setMenuBar(self.menu_bar)
    
    # trigger
    dataUser.triggered.connect(self.tampilFormRegistrasi)
    dataMember.triggered.connect(self.tampilFormAnggota)
    dataBook.triggered.connect(self.tampilFormBuku)
    dataLoan.triggered.connect(self.tampilFormTransaksi)
    logout.triggered.connect(self.logoutUser)
    exitApp.triggered.connect(self.keluar)

    # pengecekan tipe user
    if tipeUser == 'User':
      dataUser.setEnabled(False)
      dataBook.setEnabled(False)
      dataMember.setEnabled(False)

    
  # fungsi tampilan dialog konfirmasi
  def jendelaACC(self, pesan):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Aplikasi Perpustakaan')
    msgbox.setIconPixmap(QIcon('ICON/question.png').pixmap(40, 40))
    msgbox.setWindowIcon(QIcon('ICON/library_logo.png'))
    msgbox.setText(pesan)
    msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    
    return msgbox.exec()
  
  # fungsi untuk menampilkan form data user
  def tampilFormRegistrasi(self):
    form = Registrasi()  
    sub_form = QMdiSubWindow()
    sub_form.setWidget(form)
    sub_form.setFixedSize(1080, 520)
    self.mdi.addSubWindow(sub_form)
    sub_form.show() 
    
  # fungsi menampilkan form data anggota  
  def tampilFormAnggota(self):
    form = Anggota()
    sub_form = QMdiSubWindow()
    sub_form.setWidget(form)
    sub_form.setFixedSize(1290, 550)
    self.mdi.addSubWindow(sub_form)
    sub_form.show() 
  
  # fungsi menampilkan form data buku
  def tampilFormBuku(self):
    form = Buku()
    sub_form = QMdiSubWindow()
    sub_form.setWidget(form)
    sub_form.setFixedSize(1140, 570)
    self.mdi.addSubWindow(sub_form)
    sub_form.show()
    
  def tampilFormTransaksi(self):
    form = Transaksi()
    sub_form = QMdiSubWindow()
    sub_form.setWidget(form)
    sub_form.setFixedSize(990, 600)
    self.mdi.addSubWindow(sub_form)
    sub_form.show()
    
  # fungsi untuk logout
  def logoutUser(self):
    msgbx = self.jendelaACC('Apakah anda yakin untuk logout ?')
    if msgbx == QMessageBox.Ok:
      widget = self.parentWidget()
      widget.setCurrentIndex(0)
      widget.showNormal()
    
  # fungsi keluar dari aplikasi
  def keluar(self):
    msgbx = self.jendelaACC('Apakah anda yakin untuk keluar dari aplikasi ?')
    if msgbx == QMessageBox.Ok:
      self.parentWidget().close()
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = FormMain('Administrator')
  window.show()
  sys.exit(app.exec_())