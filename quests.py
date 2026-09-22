"""
quests.py - Definisi 10 Quest Kurikulum Python Lengkap, Materi Edukatif, dan Evaluator Kode Interaktif.
"""

import sys
import io
import ast

class QuestValidator:
    """Validator cerdas untuk mengevaluasi kode Python yang diketik pemain secara aman."""

    @staticmethod
    def run_sandbox_code(code_str, mock_inputs=None):
        """Menjalankan kode pemain dengan intercept stdout dan stdin mock secara aman."""
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        inputs_queue = list(mock_inputs) if mock_inputs else ["Pemain", "10", "5", "True"]
        
        def custom_input(prompt=""):
            if prompt:
                redirected_output.write(str(prompt))
            if inputs_queue:
                val = str(inputs_queue.pop(0))
                redirected_output.write(val + "\n")
                return val
            return "test"

        safe_builtins = {
            'print': print,
            'input': custom_input,
            'range': range,
            'len': len,
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'type': type,
            'abs': abs,
            'sum': sum,
            'min': min,
            'max': max,
            'ZeroDivisionError': ZeroDivisionError,
            'ValueError': ValueError,
            'TypeError': TypeError,
            'Exception': Exception,
            'True': True,
            'False': False,
            'None': None
        }

        local_vars = {}
        error_msg = None
        
        try:
            # Parse syntax first
            ast.parse(code_str)
            exec(code_str, {"__builtins__": safe_builtins}, local_vars)
        except SyntaxError as se:
            error_msg = f"Sintaks Error (Baris {se.lineno}): {se.msg}"
        except Exception as ex:
            error_msg = f"Runtime Error ({type(ex).__name__}): {str(ex)}"
        finally:
            sys.stdout = old_stdout

        output_str = redirected_output.getvalue()
        return output_str, local_vars, error_msg


# ==========================================
# 10 DEFINISI QUEST & VALIDATOR
# ==========================================

QUEST_DATA = [
    # -------------------------------------------------------------
    # QUEST 1: print() dan input()
    # -------------------------------------------------------------
    {
        "id": 1,
        "zone_id": 0,
        "location": "Pantai Hampa",
        "npc_name": "Mori Si Kerang Surealis",
        "npc_blip": "high",
        "npc_title": "Penjaga Pesisir Sadar",
        "story": (
            "\"Ombak hitam ini membisikkan namamu... Tapi lidahmu membeku oleh air laut surealis.\n"
            "Keluarkan suaramu dengan sintaks pembuka dunia!\""
        ),
        "topic": "Fungsi print() & input()",
        "lesson": (
            "• print(...): Digunakan untuk mencetak teks atau nilai ke layar.\n"
            "  Contoh: print(\"Halo Dunia!\")\n"
            "• Teks (String) harus diapit tanda petik satu ('...') atau dua (\"...\").\n"
            "• input(...): Digunakan untuk menerima masukan teks dari pengguna.\n"
            "  Contoh: nama = input(\"Masukkan nama: \")"
        ),
        "task": (
            "ALGORITMA & PSEUDOCODE:\n"
            "1. Panggil fungsi print\n"
            "2. Berikan argumen teks: \"Halo Pantai Hampa\"\n"
            "3. Pastikan penulisan persis sama"
        ),
        "initial_code": "# PSEUDOCODE: Panggil fungsi print(\"Halo Pantai Hampa\")\n# TODO: Tulis kodemu di bawah:\n",
        "hints": [
            "Pastikan kamu menulis fungsi print dengan huruf kecil.",
            "Teks harus diapit petik: print(\"Halo Pantai Hampa\")",
            "Perhatikan spasi dan huruf besar kecil pada 'Halo Pantai Hampa'."
        ],
        "reward_item": "Kerang Gema Suara",
        "reward_desc": "Membuka jalan menembus kabut Hutan Bisikan.",
        "validator": lambda code: _validate_q1(code)
    },

    # -------------------------------------------------------------
    # QUEST 2: Variabel dan Tipe Data
    # -------------------------------------------------------------
    {
        "id": 2,
        "zone_id": 1,
        "location": "Hutan Bisikan",
        "npc_name": "Pohon Mata Bintang",
        "npc_blip": "low",
        "npc_title": "Entitas Kuno Berdaun Kristal",
        "story": (
            "\"Kamu bukan sekadar bayangan... kamu memiliki wujud dan angka eksistensi.\n"
            "Daftarkan data jiwamu ke dalam empat wadah variabel agar hutan mengenalimu!\""
        ),
        "topic": "Variabel & Tipe Data Dasar",
        "lesson": (
            "Di Python, variabel dibuat langsung saat diberi nilai:\n"
            "• String (str): teks diapit tanda petik. Contoh: nama = \"Omori\"\n"
            "• Integer (int): bilangan bulat tanpa koma. Contoh: umur = 16\n"
            "• Float (float): bilangan desimal dengan titik. Contoh: energi = 95.5\n"
            "• Boolean (bool): nilai kebenaran True atau False (huruf depan besar)."
        ),
        "task": (
            "ALGORITMA & PSEUDOCODE:\n"
            "1. nama    <- String (contoh: \"Sunny\")\n"
            "2. umur    <- Integer (contoh: 16)\n"
            "3. energi  <- Float (contoh: 95.5)\n"
            "4. siap    <- Boolean (True)"
        ),
        "initial_code": (
            "# PSEUDOCODE: Lengkapi variabel berikut\n"
            "nama = ...\n"
            "umur = ...\n"
            "energi = ...\n"
            "siap = ...\n"
        ),
        "hints": [
            "nama harus string (gunakan tanda petik).",
            "umur harus int (angka bulat tanpa titik).",
            "energi harus float (angka desimal dengan tanda titik, misal 95.5).",
            "siap harus True (T besar, tanpa tanda petik)."
        ],
        "reward_item": "Lensa Data Murni",
        "reward_desc": "Menghilangkan ilusi dinding Gua Gema.",
        "validator": lambda code: _validate_q2(code)
    },

    # -------------------------------------------------------------
    # QUEST 3: Operasi Aritmatika
    # -------------------------------------------------------------
    {
        "id": 3,
        "zone_id": 2,
        "location": "Gua Gema",
        "npc_name": "Kelelawar Prisma",
        "npc_blip": "mid",
        "npc_title": "Penjaga Kristal Suara",
        "story": (
            "\"Ada 23 kristal ungu yang bergetar. Jika dibagi rata ke 4 altar gua,\n"
            "berapa kristal yang tersisa sebagai persembahan pintu keluar?\""
        ),
        "topic": "Operator Aritmatika",
        "lesson": (
            "Operator Matematika di Python:\n"
            "• Penjumlahan (+), Pengurangan (-)\n"
            "• Perkalian (*), Pembagian desimal (/)\n"
            "• Pembagian bulat (//), Modulo/Sisa bagi (%)\n"
            "• Perpangkatan (**)\n"
            "Contoh modulo: 10 % 3 hasilnya 1 (karena 10 dibagi 3 sisa 1)."
        ),
        "task": (
            "TUGAS:\n"
            "1. Buat variabel total_kristal bernilai 23\n"
            "2. Buat variabel sisa yang menghitung sisa bagi total_kristal dengan 4 menggunakan operator %\n"
            "3. Buat variabel daya_kristal yang mengalikan sisa dengan 10 menggunakan *"
        ),
        "initial_code": (
            "total_kristal = 23\n"
            "sisa = total_kristal % 4\n"
            "daya_kristal = sisa * 10\n"
        ),
        "hints": [
            "Gunakan operator % untuk modulo: sisa = total_kristal % 4",
            "Gunakan operator * untuk perkalian: daya_kristal = sisa * 10",
            "23 % 4 akan menghasilkan nilai 3, sehingga daya_kristal menjadi 30."
        ],
        "reward_item": "Palu Resonansi Ungu",
        "reward_desc": "Membuka gerbang batu menuju Rawa Keputusan.",
        "validator": lambda code: _validate_q3(code)
    },

    # -------------------------------------------------------------
    # QUEST 4: Kondisional Sederhana (if & else)
    # -------------------------------------------------------------
    {
        "id": 4,
        "zone_id": 3,
        "location": "Rawa Keputusan",
        "npc_name": "Katak Mahkota Melayang",
        "npc_blip": "low",
        "npc_title": "Hakim Aliran Rawa",
        "story": (
            "\"Krook... jalan di depan bercabang dua. Hanya jiwa yang memegang\n"
            "kunci kejujuran yang boleh melangkah melewati jembatan teratai!\""
        ),
        "topic": "Percabangan if dan else",
        "lesson": (
            "Struktur percabangan memilih jalur eksekusi:\n"
            "if kondisi:\n"
            "    # Dijalankan jika kondisi bernilai True (perhatikan 4 spasi / indentasi!)\n"
            "    print(\"Benar\")\n"
            "else:\n"
            "    # Dijalankan jika kondisi False\n"
            "    print(\"Salah\")\n"
            "Operator pembanding: == (sama dengan), != (tidak sama), >, <, >=, <="
        ),
        "task": (
            "TUGAS:\n"
            "Diberikan variabel punya_kunci = True.\n"
            "Tulis struktur if-else:\n"
            "• Jika punya_kunci bernilai True, print: \"Jembatan Terbuka\"\n"
            "• Jika tidak (else), print: \"Terkunci\""
        ),
        "initial_code": (
            "punya_kunci = True\n\n"
            "if punya_kunci == True:\n"
            "    print(\"Jembatan Terbuka\")\n"
            "else:\n"
            "    print(\"Terkunci\")\n"
        ),
        "hints": [
            "Gunakan titik dua (:) di akhir baris if dan else.",
            "Pastikan ada indentasi (spasi/tab) di dalam blok if dan else.",
            "Cetak persis string: \"Jembatan Terbuka\" dan \"Terkunci\"."
        ],
        "reward_item": "Kunci Mahkota Teratai",
        "reward_desc": "Membuka jalur rawa menuju Taman Cabang.",
        "validator": lambda code: _validate_q4(code)
    },

    # -------------------------------------------------------------
    # QUEST 5: Kondisional Lanjutan (elif & Logika and/or)
    # -------------------------------------------------------------
    {
        "id": 5,
        "zone_id": 4,
        "location": "Taman Cabang",
        "npc_name": "Bunga Melankolis Raksasa",
        "npc_blip": "high",
        "npc_title": "Penjaga Kelopak Kelabu",
        "story": (
            "\"Kelopakkau layu... warnaku ditentukan oleh kadar cahaya dan air.\n"
            "Tentukan tingkat mekar bungaku dengan klasifikasi percabangan multi-kondisi!\""
        ),
        "topic": "Kondisional elif & Operator Logika",
        "lesson": (
            "Gunakan 'elif' untuk memeriksa banyak kemungkinan secara berurutan:\n"
            "• and: Bernilai True hanya jika KEDUA kondisi benar.\n"
            "• or: Bernilai True jika SALAH SATU kondisi benar.\n"
            "Contoh:\n"
            "if skor >= 85:\n"
            "    grade = \"A\"\n"
            "elif skor >= 70:\n"
            "    grade = \"B\"\n"
            "else:\n"
            "    grade = \"C\""
        ),
        "task": (
            "TUGAS:\n"
            "Buat variabel skor_cahaya = 85.\n"
            "Buat variabel status_bunga menggunakan percabangan:\n"
            "• Jika skor_cahaya >= 80, isi status_bunga = \"Mekar Sempurna\"\n"
            "• elif skor_cahaya >= 50, isi status_bunga = \"Mekar Sebagian\"\n"
            "• else, isi status_bunga = \"Kuncup\""
        ),
        "initial_code": (
            "skor_cahaya = 85\n\n"
            "if skor_cahaya >= 80:\n"
            "    status_bunga = \"Mekar Sempurna\"\n"
            "elif skor_cahaya >= 50:\n"
            "    status_bunga = \"Mekar Sebagian\"\n"
            "else:\n"
            "    status_bunga = \"Kuncup\"\n"
        ),
        "hints": [
            "Periksa kondisi pertama dengan: if skor_cahaya >= 80:",
            "Lanjutkan dengan elif skor_cahaya >= 50:",
            "Tutup dengan else: dan pastikan string huruf besar kecilnya persis."
        ],
        "reward_item": "Kelopak Spektrum Pelangi",
        "reward_desc": "Menghidupkan angin di Lembah Berulang.",
        "validator": lambda code: _validate_q5(code)
    },

    # -------------------------------------------------------------
    # QUEST 6: List / Array
    # -------------------------------------------------------------
    {
        "id": 6,
        "zone_id": 5,
        "location": "Lembah Berulang",
        "npc_name": "Kucing Pita Pastel",
        "npc_blip": "high",
        "npc_title": "Kolektor Barang Surealis",
        "story": (
            "\"Meow~ Kantong petualangmu masih kosong berantakan!\n"
            "Susun barang-barangmu ke dalam sebuah List terurut agar tidak hilang di lembah mimpi!\""
        ),
        "topic": "List (Array Dinamis)",
        "lesson": (
            "List adalah kumpulan item berurutan yang bisa diubah (mutable):\n"
            "• Membuat list: barang = [\"peta\", \"kompas\"]\n"
            "• Mengakses index (dimulai dari 0): barang[0] -> \"peta\"\n"
            "• Menambah item di akhir: barang.append(\"senter\")\n"
            "• Menghitung jumlah item: len(barang)"
        ),
        "task": (
            "TUGAS:\n"
            "1. Buat list tas = [\"peta\", \"kompas\"]\n"
            "2. Tambahkan string \"dayung\" ke dalam tas menggunakan .append()\n"
            "3. Buat variabel item_pertama yang mengambil elemen index 0 dari tas (tas[0])"
        ),
        "initial_code": (
            "tas = [\"peta\", \"kompas\"]\n"
            "tas.append(\"dayung\")\n"
            "item_pertama = tas[0]\n"
        ),
        "hints": [
            "Gunakan tanda kurung siku [] untuk membuat list.",
            "Gunakan method tas.append(\"dayung\") untuk menambah item baru.",
            "Ambil item index ke-0 dengan tas[0]."
        ],
        "reward_item": "Kantong Dimensi Pastel",
        "reward_desc": "Membuka gerbang masuk ke Pasar Misteri.",
        "validator": lambda code: _validate_q6(code)
    },

    # -------------------------------------------------------------
    # QUEST 7: Dictionary (Key-Value)
    # -------------------------------------------------------------
    {
        "id": 7,
        "zone_id": 6,
        "location": "Pasar Misteri",
        "npc_name": "Pedagang Topeng Bulan",
        "npc_blip": "mid",
        "npc_title": "Saudagar Barang Memori",
        "story": (
            "\"Selamat datang di kios antara tidur dan sadar.\n"
            "Struktur kapal pelarianmu membutuhkan catatan suku cadang berbasis Pasangan Kunci & Nilai!\""
        ),
        "topic": "Dictionary (Kamus Data)",
        "lesson": (
            "Dictionary menyimpan data dalam format pasangan {kunci: nilai}:\n"
            "• Membuat dict: stats = {\"kayu\": 4, \"mesin\": \"rusak\"}\n"
            "• Membaca nilai: stats[\"kayu\"] -> 4\n"
            "• Mengubah nilai: stats[\"mesin\"] = \"bagus\"\n"
            "• Menambah kunci baru: stats[\"layar\"] = 1"
        ),
        "task": (
            "TUGAS:\n"
            "1. Buat dictionary perahu = {\"kayu\": 5, \"mesin\": \"rusak\"}\n"
            "2. Ubah nilai kunci \"mesin\" menjadi \"bagus\"\n"
            "3. Tambahkan kunci baru \"layar\" dengan nilai 1"
        ),
        "initial_code": (
            "perahu = {\"kayu\": 5, \"mesin\": \"rusak\"}\n"
            "perahu[\"mesin\"] = \"bagus\"\n"
            "perahu[\"layar\"] = 1\n"
        ),
        "hints": [
            "Gunakan kurung kurawal {} untuk membuat dictionary.",
            "Ubah mesin dengan: perahu[\"mesin\"] = \"bagus\"",
            "Tambah layar dengan: perahu[\"layar\"] = 1"
        ],
        "reward_item": "Buku Catatan Onderdil",
        "reward_desc": "Membuka pintu tangga Menara Waktu.",
        "validator": lambda code: _validate_q7(code)
    },

    # -------------------------------------------------------------
    # QUEST 8: Perulangan (Loops)
    # -------------------------------------------------------------
    {
        "id": 8,
        "zone_id": 7,
        "location": "Menara Waktu",
        "npc_name": "Jam Bandul Bersayap",
        "npc_blip": "mid",
        "npc_title": "Pengawas Putaran Detik",
        "story": (
            "\"Tik... tok... waktu di menara ini terperangkap dalam spiral tak terhingga.\n"
            "Gunakan mantra perulangan untuk mengumpulkan 5 serpihan detik yang berhamburan!\""
        ),
        "topic": "Perulangan for loop & range()",
        "lesson": (
            "Perulangan (Loop) mengulang blok kode berkali-kali:\n"
            "• for i in range(n): mengulang dari 0 sampai n-1.\n"
            "• for i in range(1, 6): mengulang dari angka 1 sampai 5.\n"
            "Contoh mengakumulasi total:\n"
            "total = 0\n"
            "for i in range(1, 4):\n"
            "    total = total + i  # total menjadi 1+2+3 = 6"
        ),
        "task": (
            "TUGAS:\n"
            "1. Buat variabel total_detik = 0\n"
            "2. Gunakan for loop dengan range(1, 6) untuk menjumlahkan angka 1 sampai 5 ke dalam total_detik:\n"
            "   (total_detik = total_detik + i)\n"
            "Hasil akhir total_detik harus 15 (1+2+3+4+5)."
        ),
        "initial_code": (
            "total_detik = 0\n"
            "for i in range(1, 6):\n"
            "    total_detik = total_detik + i\n"
        ),
        "hints": [
            "range(1, 6) menghasilkan urutan angka: 1, 2, 3, 4, 5.",
            "Pastikan ada indentasi di dalam blok for.",
            "Gunakan total_detik = total_detik + i atau total_detik += i."
        ],
        "reward_item": "Gigi Roda Kronos",
        "reward_desc": "Menyetel ulang waktu dan membuka Kuil Mantra.",
        "validator": lambda code: _validate_q8(code)
    },

    # -------------------------------------------------------------
    # QUEST 9: Fungsi (def & return)
    # -------------------------------------------------------------
    {
        "id": 9,
        "zone_id": 8,
        "location": "Kuil Mantra",
        "npc_name": "Patung Pendeta Cahaya",
        "npc_blip": "low",
        "npc_title": "Arsitek Formula Kuno",
        "story": (
            "\"Mantra kuno tidak ditulis berulang-ulang, melainkan dibungkus dalam sebuah Fungsi.\n"
            "Ciptakan formula pembangkit daya yang dapat dipanggil kapan saja!\""
        ),
        "topic": "Membuat Fungsi (def, parameter, return)",
        "lesson": (
            "Fungsi adalah blok kode terorganisir yang dapat digunakan kembali:\n"
            "• def nama_fungsi(parameter1, parameter2):\n"
            "      hasil = parameter1 * parameter2\n"
            "      return hasil  # Mengembalikan nilai ke pemanggil\n"
            "• Memanggil fungsi: output = nama_fungsi(10, 2)"
        ),
        "task": (
            "TUGAS:\n"
            "1. Buat fungsi bernama hitung_daya yang menerima 2 parameter: voltase dan arus\n"
            "2. Di dalam fungsi, kembalikan hasil perkalian: voltase * arus\n"
            "3. Panggil fungsi tersebut dengan nilai (12, 5) dan simpan ke variabel daya_kapal"
        ),
        "initial_code": (
            "def hitung_daya(voltase, arus):\n"
            "    return voltase * arus\n\n"
            "daya_kapal = hitung_daya(12, 5)\n"
        ),
        "hints": [
            "Gunakan kata kunci def untuk membuat fungsi: def hitung_daya(voltase, arus):",
            "Gunakan return untuk mengembalikan nilai: return voltase * arus",
            "Panggil fungsi: daya_kapal = hitung_daya(12, 5) sehingga bernilai 60."
        ],
        "reward_item": "Segel Mantra Pembangkit",
        "reward_desc": "Membuka jalan ke Dermaga Tua untuk perbaikan perahu final!",
        "validator": lambda code: _validate_q9(code)
    },

    # -------------------------------------------------------------
    # QUEST 10: Error Handling (try / except) - FINAL QUEST
    # -------------------------------------------------------------
    {
        "id": 10,
        "zone_id": 9,
        "location": "Dermaga Tua",
        "npc_name": "Kapten Boneka Beruang",
        "npc_blip": "low",
        "npc_title": "Nahkoda Perahu Harapan",
        "story": (
            "\"Mesin perahu ini sudah lama mati... Saat dinyalakan, ada kemungkinan arus pembagi nol (crash)!\n"
            "Lindungi sistem pengapian dengan penanganan error (try - except) agar perahu kita bisa berlayar!\""
        ),
        "topic": "Penanganan Error (try & except)",
        "lesson": (
            "try-except mencegah program berhenti mendadak saat terjadi error runtime:\n"
            "try:\n"
            "    # Blok kode yang berisiko error (misal pembagian dengan 0)\n"
            "    hasil = 100 / angka_pembagi\n"
            "    status_mesin = \"Berhasil Nyala\"\n"
            "except ZeroDivisionError:\n"
            "    # Dijalankan HANYA jika terjadi ZeroDivisionError\n"
            "    status_mesin = \"Pengaman Aktif: Pembagian Nol\"\n"
            "except Exception as e:\n"
            "    # Menangkap error umum lainnya\n"
            "    status_mesin = \"Error Lain Terdeteksi\""
        ),
        "task": (
            "TUGAS:\n"
            "Diberikan variabel daya_input = 0.\n"
            "Buat blok try-except:\n"
            "• Di dalam try: lakukan pembagian hasil = 100 / daya_input dan set status_mesin = \"Normal\"\n"
            "• Di dalam except ZeroDivisionError: set status_mesin = \"Pengaman Darurat Aktif\""
        ),
        "initial_code": (
            "daya_input = 0\n"
            "status_mesin = \"Mati\"\n\n"
            "try:\n"
            "    hasil = 100 / daya_input\n"
            "    status_mesin = \"Normal\"\n"
            "except ZeroDivisionError:\n"
            "    status_mesin = \"Pengaman Darurat Aktif\"\n"
        ),
        "hints": [
            "Tulis blok try: lalu lakukan pembagian 100 / daya_input di dalamnya.",
            "Tulis except ZeroDivisionError: di bawah blok try.",
            "Di dalam except, ubah nilai status_mesin menjadi \"Pengaman Darurat Aktif\"."
        ],
        "reward_item": "Kunci Kontak Perahu Emas",
        "reward_desc": "Mesin perahu hidup menderu! Kamu siap berlayar menembus batas Headspace!",
        "validator": lambda code: _validate_q10(code)
    }
]


# ==========================================
# LOGIKA VALIDASI KHUSUS PER QUEST
# ==========================================

def _validate_q1(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    if "Halo Pantai Hampa" in output:
        return True, "Luar biasa! Suaramu bergema di seluruh pesisir Pantai Hampa."
    return False, "Output belum memuat teks 'Halo Pantai Hampa'. Pastikan penulisan huruf persis."


def _validate_q2(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    if "nama" not in locals_dict or not isinstance(locals_dict["nama"], str):
        return False, "Variabel 'nama' harus bertipe string (str) dengan tanda petik."
    if "umur" not in locals_dict or not isinstance(locals_dict["umur"], int):
        return False, "Variabel 'umur' harus bertipe integer (int) bilangan bulat."
    if "energi" not in locals_dict or not isinstance(locals_dict["energi"], (int, float)):
        return False, "Variabel 'energi' harus bertipe float (contoh: 95.5)."
    if "siap" not in locals_dict or locals_dict["siap"] is not True:
        return False, "Variabel 'siap' harus bertipe bool dan bernilai True."
    
    return True, "Sempurna! Jiwamu kini terdaftar dengan 4 tipe data fundamental Python."


def _validate_q3(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    if "total_kristal" not in locals_dict or locals_dict["total_kristal"] != 23:
        return False, "Variabel 'total_kristal' harus bernilai 23."
    if "sisa" not in locals_dict or locals_dict["sisa"] != (23 % 4):
        return False, "Variabel 'sisa' belum benar. Gunakan operator modulo % (23 % 4 = 3)."
    if "daya_kristal" not in locals_dict or locals_dict["daya_kristal"] != 30:
        return False, "Variabel 'daya_kristal' harus bernilai 30 (sisa * 10)."
    
    return True, "Hebat! Kristal ungu beresonansi menghasilkan 30 daya magis."


def _validate_q4(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    # Test with True
    if "Jembatan Terbuka" not in output:
        return False, "Saat punya_kunci = True, program harus mencetak 'Jembatan Terbuka'."
    
    # Test with False to verify logic
    test_code = "punya_kunci = False\n" + code[code.find("if"):] if "if" in code else code
    out2, _, _ = QuestValidator.run_sandbox_code(test_code)
    if "Terkunci" not in out2:
        return False, "Saat punya_kunci = False, blok else harus mencetak 'Terkunci'."
    
    return True, "Tepat sekali! Gerbang rawa membuka jalurnya untukmu."


def _validate_q5(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    if "status_bunga" not in locals_dict:
        return False, "Variabel 'status_bunga' belum ditemukan."
    if locals_dict.get("status_bunga") != "Mekar Sempurna":
        return False, "Untuk skor 85, status_bunga harus bernilai 'Mekar Sempurna'."
    
    # Cek cabang elif
    test_code_mid = "skor_cahaya = 60\n" + code[code.find("if"):] if "if" in code else code
    _, locals_mid, _ = QuestValidator.run_sandbox_code(test_code_mid)
    if locals_mid.get("status_bunga") != "Mekar Sebagian":
        return False, "Cabang elif untuk skor 60 harus menghasilkan 'Mekar Sebagian'."

    return True, "Bunga melankolis kini memancarkan warna pelangi yang memukau!"


def _validate_q6(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    tas = locals_dict.get("tas")
    if not isinstance(tas, list):
        return False, "'tas' harus berupa tipe data List [ ... ]."
    if "dayung" not in tas:
        return False, "Jangan lupa menambahkan 'dayung' ke dalam list tas menggunakan .append(\"dayung\")."
    if locals_dict.get("item_pertama") != "peta":
        return False, "'item_pertama' harus mengambil elemen index 0 dari tas (tas[0])."
    
    return True, "Barang-barangmu tersusun rapi di dalam tas dimensi!"


def _validate_q7(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    perahu = locals_dict.get("perahu")
    if not isinstance(perahu, dict):
        return False, "'perahu' harus bertipe data Dictionary { ... }."
    if perahu.get("mesin") != "bagus":
        return False, "Nilai kunci 'mesin' harus diubah menjadi 'bagus'."
    if perahu.get("layar") != 1:
        return False, "Kunci 'layar' harus bernilai 1."
    
    return True, "Inventaris suku cadang perahu telah diperbarui dengan sukses!"


def _validate_q8(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    if locals_dict.get("total_detik") != 15:
        return False, "Nilai total_detik harus 15 (hasil dari 1 + 2 + 3 + 4 + 5)."
    if "for " not in code:
        return False, "Gunakan perulangan 'for i in range(1, 6):' untuk menjumlahkannya."

    return True, "Putaran waktu berhasil disinkronkan kembali!"


def _validate_q9(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    hitung_fn = locals_dict.get("hitung_daya")
    if not callable(hitung_fn):
        return False, "Fungsi 'hitung_daya' belum dibuat dengan sintaks def hitung_daya(voltase, arus):"
    
    try:
        test_val = hitung_fn(10, 4)
        if test_val != 40:
            return False, "Fungsi hitung_daya(10, 4) seharusnya mengembalikan nilai 40."
    except Exception as e:
        return False, f"Terjadi error saat menguji fungsi: {e}"

    if locals_dict.get("daya_kapal") != 60:
        return False, "Variabel daya_kapal harus memanggil hitung_daya(12, 5) dan bernilai 60."

    return True, "Mantra pembangkit daya berhasil dikristalisasi ke dalam fungsi!"


def _validate_q10(code):
    output, locals_dict, error = QuestValidator.run_sandbox_code(code)
    if error:
        return False, error
    
    if "try:" not in code or "except" not in code:
        return False, "Gunakan blok 'try:' dan 'except ZeroDivisionError:' untuk mengamankan kode."
    
    if locals_dict.get("status_mesin") != "Pengaman Darurat Aktif":
        return False, "Saat terjadi pembagian dengan nol, status_mesin harus bernilai 'Pengaman Darurat Aktif'."
    
    return True, "MESIN PERAHU MENYALA DENGAN STABIL! Semua quest terselesaikan!"
