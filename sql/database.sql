CREATE DATABASE pboperpus;
USE pboperpus;

CREATE TABLE tbl_user(
  id_user VARCHAR(25) PRIMARY KEY NOT NULL,
  nama_depan VARCHAR(100),
  nama_tengah VARCHAR(100),
  nama_belakang VARCHAR(100),
  tipe_user VARCHAR(25),
  username VARCHAR(15),
  password VARCHAR(32)
);

-- username password admin
INSERT INTO tbl_user 
VALUE
  ('ADM001', 'Andrian', '', 'Maulana', 'Administrator', 'andrian', MD5('12345'));

CREATE TABLE tbl_anggota(
  id_anggota VARCHAR(25) PRIMARY KEY NOT NULL,
  nama_depan VARCHAR(100),
  nama_tengah VARCHAR(100),
  nama_belakang VARCHAR(100),
  jenis_kelamin VARCHAR(15),
  no_telp VARCHAR(20),
  alamat VARCHAR(200),
  email VARCHAR(200)
);

CREATE TABLE tbl_genre(
  id_genre VARCHAR(25) PRIMARY KEY NOT NULL,
  nama_genre VARCHAR(100)
);

CREATE TABLE tbl_penulis(
  id_penulis VARCHAR(25) PRIMARY KEY NOT NULL,
  nama_depan VARCHAR(100),
  nama_tengah VARCHAR(100),
  nama_belakang VARCHAR(100)
);

CREATE TABLE tbl_buku(
  isbn VARCHAR(25) PRIMARY KEY NOT NULL,
  id_genre VARCHAR(25),
  id_penulis VARCHAR(25),
  judul VARCHAR(100),
  penerbit VARCHAR(100),
  tanggal_publikasi DATE,
  jumlah_stok INT,
  Foreign Key (id_genre) REFERENCES tbl_genre(id_genre),
  Foreign Key (id_penulis) REFERENCES tbl_penulis(id_penulis)
);

CREATE TABLE tbl_peminjaman(
  id_peminjaman INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  isbn VARCHAR(25),
  id_anggota VARCHAR(25),
  tanggal_pinjam DATE,
  tanggal_tempo DATE,
  tanggal_kembali DATE,
  Foreign Key (isbn) REFERENCES tbl_buku(isbn),
  Foreign Key (id_anggota) REFERENCES tbl_anggota(id_anggota)
);

SHOW VARIABLES LIKE 'hostname';

SELECT USER();

SELECT @IDENTIFIED_BY_PASSWORD;

SELECT * FROM tbl_user;
SELECT * FROM tbl_peminjaman;
SELECT * FROM tbl_anggota;
SELECT * FROM tbl_genre;
SELECT * FROM tbl_penulis;
SELECT * FROM tbl_buku;

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
          DATEDIFF(tbl_peminjaman.tanggal_kembali, tbl_peminjaman.tanggal_tempo) * 2000
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

INSERT INTO tbl_anggota (id_anggota, nama_depan, nama_tengah, nama_belakang, jenis_kelamin, no_telp, alamat, email)
VALUES
('ANG001', 'Budi', 'Santoso', 'Wibowo', 'Laki-laki', '081234567890', 'Jl. Merdeka No. 123', 'budi@gmail.com'),
('ANG002', 'Citra', 'Rahayu', 'Utami', 'Perempuan', '085678901234', 'Jl. Raya Kencana No. 45', 'citra@yahoo.com'),
('ANG003', 'Dharma', 'Adi', 'Prabowo', 'Laki-laki', '081345678901', 'Jl. Mawar Indah No. 56', 'dharma@hotmail.com'),
('ANG004', 'Eka', 'Sari', 'Wijaya', 'Perempuan', '087890123456', 'Jl. Puri Sentosa No. 78', 'eka@gmail.com'),
('ANG005', 'Fajar', 'Wisnu', 'Saputra', 'Laki-laki', '081234567890', 'Jl. Kenanga No. 90', 'fajar@gmail.com'),
('ANG006', 'Gita', 'Ayunda', 'Kusuma', 'Perempuan', '085678901234', 'Jl. Anggrek No. 12', 'gita@yahoo.com'),
('ANG007', 'Hendra', 'Wijaya', 'Gunawan', 'Laki-laki', '081345678901', 'Jl. Dahlia No. 34', 'hendra@hotmail.com'),
('ANG008', 'Intan', 'Rahayu', 'Sari', 'Perempuan', '087890123456', 'Jl. Jambu Murni No. 67', 'intan@gmail.com'),
('ANG009', 'Joko', 'Susilo', 'Saputro', 'Laki-laki', '081234567890', 'Jl. Raya Cempaka No. 89', 'joko@gmail.com'),
('ANG010', 'Kartika', 'Dewi', 'Putri', 'Perempuan', '085678901234', 'Jl. Puspa Indah No. 23', 'kartika@yahoo.com'),
('ANG011', 'Lukman', 'Firmansyah', 'Raharjo', 'Laki-laki', '081345678901', 'Jl. Melati No. 45', 'lukman@hotmail.com'),
('ANG012', 'Maya', 'Fitri', 'Lestari', 'Perempuan', '087890123456', 'Jl. Raya Kebon Jati No. 56', 'maya@gmail.com'),
('ANG013', 'Nugroho', 'Surya', 'Wijaya', 'Laki-laki', '081234567890', 'Jl. Kenari No. 78', 'nugroho@gmail.com'),
('ANG014', 'Putri', 'Cahaya', 'Murni', 'Perempuan', '085678901234', 'Jl. Mawar Jingga No. 90', 'putri@yahoo.com'),
('ANG015', 'Rudi', 'Prabowo', 'Wicaksono', 'Laki-laki', '081345678901', 'Jl. Raya Merpati No. 12', 'rudi@hotmail.com'),
('ANG016', 'Siti', 'Nur', 'Hidayah', 'Perempuan', '087890123456', 'Jl. Dahlia Murni No. 34', 'siti@gmail.com'),
('ANG017', 'Taufik', 'Wibowo', 'Santoso', 'Laki-laki', '081234567890', 'Jl. Puspa No. 67', 'taufik@gmail.com'),
('ANG018', 'Umi', 'Suryani', 'Rahayu', 'Perempuan', '085678901234', 'Jl. Raya Cendana No. 23', 'umi@yahoo.com'),
('ANG019', 'Vino', 'Setiawan', 'Wijaya', 'Laki-laki', '081345678901', 'Jl. Jambu Muda No. 56', 'vino@hotmail.com'),
('ANG020', 'Wulan', 'Murni', 'Sari', 'Perempuan', '087890123456', 'Jl. Raya Kebon Jati No. 78', 'wulan@gmail.com');

-- Insertkan data genre buku dengan format ID GNR001 dan seterusnya
INSERT INTO tbl_genre (id_genre, nama_genre)
VALUES
('GNR001', 'Fiksi'),
('GNR002', 'Non-Fiksi'),
('GNR003', 'Sains'),
('GNR004', 'Sejarah'),
('GNR005', 'Biografi'),
('GNR006', 'Sastra'),
('GNR007', 'Seni'),
('GNR008', 'Pendidikan'),
('GNR009', 'Agama'),
('GNR010', 'Filosofi'),
('GNR011', 'Teknologi'),
('GNR012', 'Pemrograman'),
('GNR013', 'Psikologi'),
('GNR014', 'Self-Help'),
('GNR015', 'Kesehatan'),
('GNR016', 'Matematika'),
('GNR017', 'Hukum'),
('GNR018', 'Politik'),
('GNR019', 'Ekonomi'),
('GNR020', 'Gaya Hidup');

-- Insertkan data penulis dengan format ID PNL001 dan seterusnya
INSERT INTO tbl_penulis (id_penulis, nama_depan, nama_tengah, nama_belakang)
VALUES
('PNL001', 'Agatha', '', 'Christie'),
('PNL002', 'Ernest', 'Hemingway', ''),
('PNL003', 'J.K.', '', 'Rowling'),
('PNL004', 'George', 'Orwell', ''),
('PNL005', 'Haruki', '', 'Murakami'),
('PNL006', 'Jane', '', 'Austen'),
('PNL007', 'Leo', 'Tolstoy', ''),
('PNL008', 'Mark', '', 'Twain'),
('PNL009', 'Gabriel', 'García', 'Márquez'),
('PNL010', 'Virginia', '', 'Woolf'),
('PNL011', 'F. Scott', 'Fitzgerald', ''),
('PNL012', 'Toni', 'Morrison', ''),
('PNL013', 'Khaled', '', 'Hosseini'),
('PNL014', 'Agnes', 'Gonxha', 'Bojaxhiu'), -- Mother Teresa
('PNL015', 'Roald', '', 'Dahl'),
('PNL016', 'Arthur', 'Conan', 'Doyle'),
('PNL017', 'Maya', '', 'Angelou'),
('PNL018', 'Albert', '', 'Camus'),
('PNL019', 'Marianne', '', 'Williamson'),
('PNL020', 'J.R.R.', 'Tolkien', ''),
('PNL021', 'Andrea', '', 'Hirata'),
('PNL022', 'Tere', 'Liye', ''),
('PNL023', 'Dee', '', 'Lestari'),
('PNL024', 'Pramoedya', 'Ananta', 'Toer'),
('PNL025', 'Ayah', 'Arie', 'Wibowo'),
('PNL026', 'Mochtar', 'Lubis', ''),
('PNL027', 'Leila', 'Chudori', ''),
('PNL028', 'Eka', 'Kurniawan', ''),
('PNL029', 'Laksmi', '', 'Pamuntjak'),
('PNL030', 'Sapardi', '', 'Djoko Damono');



-- Insertkan data buku berdasarkan penulis dan genre yang sudah dibuat sebelumnya
INSERT INTO tbl_buku (isbn, id_genre, id_penulis, judul, penerbit, tanggal_publikasi, jumlah_stok)
VALUES
('9780061122415', 'GNR001', 'PNL001', 'Murder on the Orient Express', 'HarperCollins', '1934-01-01', 10),
('9780684801469', 'GNR002', 'PNL002', 'The Old Man and the Sea', 'Scribner', '1952-09-01', 15),
('9781408855669', 'GNR003', 'PNL003', 'Harry Potter and the Sorcerer''s Stone', 'Bloomsbury', '1997-06-26', 20),
('9780451524935', 'GNR004', 'PNL004', '1984', 'Signet Classic', '1949-06-08', 12),
('9780099582070', 'GNR005', 'PNL005', 'Norwegian Wood', 'Vintage', '1987-08-11', 18),
('9780141439556', 'GNR006', 'PNL006', 'Pride and Prejudice', 'Penguin Classics', '1813-01-28', 25),
('9781908538229', 'GNR007', 'PNL007', 'Anna Karenina', 'Barnes & Noble Classics', '1877-01-01', 14),
('9780486406510', 'GNR008', 'PNL008', 'The Adventures of Tom Sawyer', 'Dover Publications', '1876-01-01', 16),
('9780061120077', 'GNR009', 'PNL009', 'One Hundred Years of Solitude', 'Harper Perennial', '1967-05-30', 22),
('9780156881807', 'GNR010', 'PNL010', 'To Kill a Mockingbird', 'Harper Perennial', '1960-07-11', 30),
('9780743273565', 'GNR011', 'PNL011', 'The Great Gatsby', 'Scribner', '1925-04-10', 28),
('9781400032493', 'GNR012', 'PNL012', 'Beloved', 'Vintage', '1987-09-08', 24),
('9781594480003', 'GNR013', 'PNL013', 'The Kite Runner', 'Riverhead Books', '2003-05-29', 20),
('9780061577079', 'GNR014', 'PNL014', 'And Then There Were None', 'HarperCollins', '1939-01-01', 15),
('9780143105954', 'GNR015', 'PNL015', 'Matilda', 'Penguin Books', '1988-10-01', 18),
('9780553212455', 'GNR016', 'PNL016', 'Sherlock Holmes: The Complete Novels and Stories', 'Bantam Classics', '1887-01-01', 12),
('9780375706772', 'GNR017', 'PNL017', 'I Know Why the Caged Bird Sings', 'Random House', '1969-04-01', 16),
('9780679732761', 'GNR018', 'PNL018', 'The Stranger', 'Vintage', '1942-01-01', 20),
('9780062502179', 'GNR019', 'PNL019', 'A Return to Love', 'HarperOne', '1992-03-01', 14),
('9780618002214', 'GNR020', 'PNL020', 'The Hobbit', 'Houghton Mifflin', '1937-09-21', 25),
('9786029144979', 'GNR001', 'PNL021', 'Laskar Pelangi', 'Bentang Pustaka', '2005-08-30', 15),
('9786020301285', 'GNR002', 'PNL022', 'Hafalan Shalat Delisa', 'Republika', '2005-01-01', 20),
('9786024252527', 'GNR003', 'PNL023', 'Supernova: Akar', 'Bentang Pustaka', '2001-01-01', 18),
('9789792263228', 'GNR004', 'PNL024', 'Bumi Manusia', 'Hasta Mitra', '1980-01-01', 25),
('9786020301629', 'GNR005', 'PNL025', 'Ayah: Kisah Buya Hamka', 'Republika', '2012-01-01', 22),
('9789793451846', 'GNR006', 'PNL026', 'Senja di Jakarta', 'Balai Pustaka', '1951-01-01', 12),
('9789799959062', 'GNR007', 'PNL027', 'Pulang', 'Kepustakaan Populer Gramedia', '2015-01-01', 16),
('9786020303708', 'GNR008', 'PNL028', 'Manusia Setengah Salmon', 'Bentang Pustaka', '2011-01-01', 20),
('9786024241569', 'GNR009', 'PNL029', 'Amba', 'Gramedia Pustaka Utama', '2012-01-01', 14),
('9789792255261', 'GNR010', 'PNL030', 'Hujan Bulan Juni', 'Hasta Mitra', '1971-01-01', 18);

CREATE TABLE tbl_tgl_merah (
  id_tgl_merah INT PRIMARY KEY AUTO_INCREMENT,
  tgl_merah DATE NOT NULL
);

INSERT INTO tbl_tgl_merah (tgl_merah)
SELECT DISTINCT
  date_table.date_column
FROM
  (SELECT
    CURDATE() + INTERVAL n DAY AS date_column
   FROM
    (SELECT 
      a.N + b.N * 10 + c.N * 100 AS N
     FROM 
      (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
      (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b,
      (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c
    ) numbers_table
   WHERE
    CURDATE() + INTERVAL n DAY BETWEEN '2023-01-01' AND '2035-12-31'
  ) date_table
WHERE
  DAYOFWEEK(date_table.date_column) = 1; -- 1 corresponds to Sunday


-- tampilan denda pengecualian hari sabtu minggu
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
          -- Mengurangkan denda untuk hari Sabtu-Minggu
          (DATEDIFF(tbl_peminjaman.tanggal_kembali, tbl_peminjaman.tanggal_tempo) DIV 7) * 2000 * 2
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


