**1. Import Modul:**

**_import threading, time, random_**

- threading: Digunakan untuk menjalankan beberapa thread secara bersamaan (multithreading).

- time: Digunakan untuk mengukur waktu eksekusi simulasi.

- random: Digunakan untuk menghasilkan angka acak yang diperlukan dalam simulasi (misalnya, untuk memilih alamat memori atau menentukan apakah operasi baca atau tulis yang dilakukan).

**2. Variabel Konstanta Global:**

**_THREADS = 4_**

**_BLOCKS = 10_**

**_ITER = 50_**

- THREADS: Menentukan jumlah thread yang digunakan dalam simulasi (dalam hal ini, 4 thread).

- BLOCKS: Menentukan jumlah blok memori yang tersedia (dalam hal ini, 10 blok).

- ITER: Menentukan jumlah iterasi atau operasi (baca/tulis) yang dilakukan oleh setiap thread.

**3.Fungsi simpan_hasil_ke_file:**

def simpan_hasil_ke_file(hasil):
    
    with open('output.txt', 'a') as f: 
        
        f.write(hasil + "\n")

- Fungsi ini digunakan untuk menyimpan hasil simulasi (seperti jumlah hits, misses, dan waktu yang diambil) ke dalam file teks bernama output.txt.

- Menggunakan mode 'a' agar data yang baru ditambahkan (append) ke file yang sudah ada tanpa menghapus data lama.        

**4. Kelas Simulasi:**

Kelas ini berfungsi untuk mensimulasikan perilaku cache dalam sistem dengan beberapa thread dan menguji dua kondisi:

- Dengan koherensi (cache coherence).

- Tanpa koherensi.

class Simulasi:    
    def __init__(self, koheren):        
       
        self.cache = [{} for _ in range(THREADS)]        
        self.memori = [0]*BLOCKS         
        self.traffic = 0     
        self.hit = [0]*THREADS  
        self.miss = [0]*THREADS  
        self.koheren = koheren 

- cache: Setiap thread memiliki cache-nya masing-masing (dalam bentuk list of dictionary). Cache berfungsi untuk menyimpan data yang diakses agar dapat diambil dengan cepat.

- memori: Daftar yang berisi blok-blok memori. Setiap blok memori diinisialisasi dengan nilai 0.

- traffic: Menghitung jumlah total akses memori (baik baca maupun tulis).

- hit: Menghitung jumlah hit cache (sukses mengambil data dari cache).

- miss: Menghitung jumlah miss cache (gagal mengambil data dari cache, sehingga data harus diambil dari memori).

- koheren: Menentukan apakah koherensi cache diaktifkan atau tidak.        

**Metode read (Membaca Memori):** 

def read(self, tid, addr):
    if addr in self.cache[tid]:
        
        self.hit[tid] += 1   
    else:
        self.miss[tid] += 1   
        self.cache[tid][addr] = self.memori[addr]  
        self.traffic += 1 

- Fungsi ini melakukan operasi baca pada memori. Jika data sudah ada di cache thread, maka disebut hit. Jika tidak ada, disebut miss, dan data akan dimuat ke cache serta trafik meningkat.        

**Metode write (Menulis ke Memori):**


def write(self, tid, addr, val):
    
    if self.koheren:        
        for i in range(THREADS):            
            if i != tid and addr in self.cache[i]:                
                del self.cache[i][addr]                  
                self.traffic += 1  
    self.cache[tid][addr] = val  
    self.memori[addr] = val  
    self.traffic += 1  

- Jika koherensi cache diaktifkan (self.koheren = True), saat satu thread menulis ke memori, cache pada thread lain yang memiliki data yang sama akan dihapus (invalidated).

- Kemudian data ditulis baik di cache thread yang bersangkutan maupun di memori utama.

**Metode tugas (Operasi yang Dilakukan oleh Setiap Thread):**

def tugas(self, tid):
    
    for _ in range(ITER):
        a = random.randint(0, BLOCKS-1)  
        if random.random() < 0.6:  
            self.read(tid, a)
        else:  
            self.write(tid, a, random.randint(1, 100))

- Fungsi ini adalah pekerjaan yang dijalankan oleh setiap thread. Setiap thread akan melakukan ITER kali operasi baca atau tulis secara acak.

- 60% dari waktu akan memilih operasi baca, dan 40% akan memilih operasi tulis.

**Metode jalankan (Menjalankan Simulasi):**

def jalankan(self):
    
    t0 = time.time()  
    ths = [threading.Thread(target=self.tugas, args=(i,)) for i in range(THREADS)]  # Membuat thread
    for t in ths: t.start()  
    for t in ths: t.join()  
    hasil = f"Koherensi: {self.koheren} | Traffic: {self.traffic} | Hits: {sum(self.hit)} | Misses: {sum(self.miss)} | Waktu: {time.time()-t0:.2f}s"
    
    simpan_hasil_ke_file(hasil)  
    print(hasil)  

- Fungsi ini akan menjalankan simulasi dengan membuat thread-thread yang masing-masing melakukan tugas (tugas) secara paralel.

- Setelah semua thread selesai, hasil simulasi (jumlah trafik, hits, misses, dan waktu eksekusi) akan disimpan ke dalam file dan dicetak di terminal.

**5. Bagian Main:**

if __name__ == "__main__":
    
    Simulasi(False).jalankan()  
    Simulasi(True).jalankan()   

- Bagian ini menjalankan dua simulasi secara berturut-turut: pertama tanpa koherensi cache (Simulasi(False)) dan kemudian dengan koherensi cache (Simulasi(True)).

**6.  Ringkasan Proses:**

- Simulasi ini menguji perilaku cache dalam sistem multi-threaded dengan dua kondisi: dengan koherensi dan tanpa koherensi.

- Koherensi cache berarti ketika satu thread menulis ke memori, cache pada thread lain yang memiliki data yang sama akan dihapus.

- Hasil simulasi mencakup jumlah trafik akses memori, jumlah hits (akses cache yang berhasil), jumlah misses (akses cache yang gagal), dan waktu eksekusi simulasi.
