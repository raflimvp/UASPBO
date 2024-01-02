CREATE DATABASE tgl_merah;
USE tgl_merah;

CREATE TABLE tbl_tgl_merah (
  id_tgl_merah INT PRIMARY KEY AUTO_INCREMENT,
  tgl_merah DATE NOT NULL
)

-- Insert tanggal di hari Minggu dari tahun 2023 sampai 2025
INSERT INTO tbl_tgl_merah (tgl_merah)
SELECT DISTINCT DATE_ADD('2023-01-01', INTERVAL n DAY) AS tgl_merah
FROM (
  SELECT t*1000 + u*100 + d*10 + s AS n
  FROM (SELECT 0 AS t UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t,
       (SELECT 0 AS u UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) u,
       (SELECT 0 AS d UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) d,
       (SELECT 0 AS s UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) s
) numbers
WHERE YEAR(DATE_ADD('2023-01-01', INTERVAL n DAY)) BETWEEN 2023 AND 2025
  AND DAYOFWEEK(DATE_ADD('2023-01-01', INTERVAL n DAY)) = 1;

SELECT * FROM tbl_tgl_merah;

-- Kueri untuk menghitung denda dengan mengabaikan tanggal merah
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
        WHEN tbl_peminjaman.tanggal_kembali IS NOT NULL 
             AND tbl_peminjaman.tanggal_kembali > tbl_peminjaman.tanggal_tempo
             AND NOT EXISTS (
               SELECT 1 
               FROM tbl_tgl_merah 
               WHERE tbl_tgl_merah.tanggal BETWEEN tbl_peminjaman.tanggal_tempo AND tbl_peminjaman.tanggal_kembali
             )
        THEN
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

-- Pilih dan urutkan tanggal pada tabel tbl_tgl_merah
SELECT id_tgl_merah , tgl_merah
FROM tbl_tgl_merah
ORDER BY tgl_merah;

DELETE FROM tbl_tgl_merah;

-- Insert tanggal di hari Minggu dari tahun 2023 hingga 2035 ke dalam tabel
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
