/**
 * quests.js - Database 10 Quest Beragam: Coding + Minigame Arkade,
 * Scavenger Hunt (Cari Barang di Pulau), Lomba Lari Rintangan, dan Interaksi Desa Warga.
 */

const QUEST_DATA = [
  // -------------------------------------------------------------
  // QUEST 1: Pantai Hampa (Coding + Minigame Tembak-Tembakan Bug)
  // -------------------------------------------------------------
  {
    id: 1,
    type: "coding",
    minigame_type: "shooter",
    location: "Pantai Hampa (Pesisir Selatan)",
    npc_name: "Mori Si Kerang Surealis",
    npc_blip: "high",
    npc_title: "Penjaga Pesisir Sadar",
    story: "Ombak hitam ini membisikkan namamu... Tapi lidahmu membeku oleh air laut surealis.\nKeluarkan suaramu dengan fungsi print() dan basmi bug laut dengan tembakan blaster!",
    topic: "Fungsi print() & input()",
    lesson: `• <b>print(...)</b>: Menampilkan teks atau nilai ke layar.<br>
  Contoh: <code>print("Teks yang ingin dicetak")</code><br>
• String teks harus diapit tanda petik <code>"..."</code> atau <code>'...'</code>.<br>
• <b>input(...)</b>: Menerima masukan dari pengguna.<br>
  Contoh: <code>nama = input("Masukkan nama: ")</code>`,
    task: `ALGORITMA & PSEUDOCODE:
1. Panggil fungsi print
2. Masukkan parameter teks: "Halo Pantai Hampa"
3. Mainkan Minigame Tembak-Tembakan dan capai 100 Poin!`,
    initial_code: `# --- TANTANGAN QUEST 1: OUTPUT TEKS ---
# PSEUDOCODE:
# Panggil fungsi print dengan teks "Halo Pantai Hampa"

# TODO: Tulis kodemu di bawah:
`,
    hints: [
      "Gunakan fungsi print: print(\"Halo Pantai Hampa\")",
      "Buka tab '🎮 Mini-Game Aksi' dan tembak bug sintaks hingga 100 poin!"
    ],
    reward_item: "Kerang Suara & Sayap Kiri Pesawat",
    reward_desc: "Memperbaiki sayap kiri pesawat di alun-alun tengah pulau!",
    validator: (code) => {
      const clean = code.replace(/\r/g, '');
      const match = clean.match(/print\s*\(\s*["']Halo Pantai Hampa["']\s*\)/);
      if (match) return { success: true, msg: "Suaramu bergema di seluruh pesisir Pantai Hampa!" };
      if (!clean.includes("print")) return { success: false, msg: "Gunakan fungsi print(...) untuk mencetak sapaan." };
      return { success: false, msg: "Teks di dalam print harus persis \"Halo Pantai Hampa\"." };
    }
  },

  // -------------------------------------------------------------
  // QUEST 2: Hutan Bisikan (Scavenger Hunt: Cari 3 Kristal Data di Hutan)
  // -------------------------------------------------------------
  {
    id: 2,
    type: "scavenger",
    target_count: 3,
    item_target_name: "Kristal Data Jiwa",
    location: "Hutan Bisikan (Barat Laut)",
    npc_name: "Pohon Mata Bintang",
    npc_blip: "low",
    npc_title: "Entitas Kuno Berdaun Kristal",
    story: "Data eksistensimu terpecah menjadi 3 serpihan kristal dan tersembunyi di balik pepohonan hutan bisikan!\nJelajahi area hutan di sebelah barat laut, temukan ke-3 kristal data itu untuk menyatukan jiwamu!",
    topic: "Variabel & Tipe Data Dasar",
    lesson: `Konsep 4 Tipe Data Dasar Python yang tersimpan di dalam kristal:<br>
• <b>String (str)</b>: <code>"Sunny"</code> (Teks berpetik)<br>
• <b>Integer (int)</b>: <code>16</code> (Bilangan bulat)<br>
• <b>Float (float)</b>: <code>95.5</code> (Pecahan desimal)<br>
• <b>Boolean (bool)</b>: <code>True / False</code> (Nilai logika kebenaran)`,
    task: `MISI SCAVENGER HUNT:
1. Telusuri Hutan Bisikan di barat pulau.
2. Cari dan dekati 3 Kristal Berpijar yang tersebar di antara pohon.
3. Tekan [E] / [Spasi] pada kristal untuk memungutnya!`,
    initial_code: `# --- MISI PENCARIAN BARANG (SCAVENGER HUNT) ---
# Temukan 3 Kristal Data Jiwa di sekitar Hutan Bisikan!
# Dekati kristal yang bersinar dan tekan [E] untuk mengambilnya.
`,
    hints: [
      "Jalanlah ke arah barat laut pulau tempat pepohonan hijau lebat berada.",
      "Kristal berpijar dengan warna pastel mint dan ungu di dekat semak."
    ],
    reward_item: "Baling-Baling Depan Pesawat",
    reward_desc: "Baling-baling pesawat di tengah pulau kini telah terpasang!",
    validator: () => ({ success: true, msg: "Ketiga Kristal Data berhasil dikumpulkan!" })
  },

  // -------------------------------------------------------------
  // QUEST 3: Gua Gema (Coding + Minigame Lompat Rintangan Duri)
  // -------------------------------------------------------------
  {
    id: 3,
    type: "coding",
    minigame_type: "jumper",
    location: "Gua Gema (Tebing Utara)",
    npc_name: "Kelelawar Prisma",
    npc_blip: "mid",
    npc_title: "Penjaga Kristal Suara",
    story: "Kristal ungu gua ini memancarkan getaran aritmatika!\nHitung sisa kristal dengan modulo (%) lalu lompati jurang rintangan duri mimpi!",
    topic: "Operator Aritmatika & Modulo",
    lesson: `Operator Matematika di Python:<br>
• Penjumlahan (<code>+</code>), Pengurangan (<code>-</code>)<br>
• Perkalian (<code>*</code>), Pembagian desimal (<code>/</code>)<br>
• <b>Modulo (%)</b>: Menghitung sisa hasil pembagian.<br>
Contoh: <code>23 % 4</code> menghasilkan <code>3</code>.`,
    task: `ALGORITMA & PSEUDOCODE:
1. total_kristal = 23
2. sisa = total_kristal % 4
3. daya_kristal = sisa * 10
4. Mainkan Minigame Lompat Duri dan kumpulkan 100 Poin!`,
    initial_code: `# --- TANTANGAN QUEST 3: ARITMATIKA & MODULO ---
# PSEUDOCODE:
# total_kristal = 23
# sisa = total_kristal % 4
# daya_kristal = sisa * 10

total_kristal = ...
sisa = ... % 4
daya_kristal = sisa * ...
`,
    hints: [
      "total_kristal = 23",
      "sisa = total_kristal % 4",
      "daya_kristal = sisa * 10"
    ],
    reward_item: "Aki & Generator Listrik Pesawat",
    reward_desc: "Sistem kelistrikan pesawat di tengah pulau mulai berdengung!",
    validator: (code) => {
      const hasTot = /total_kristal\s*=\s*23/.test(code);
      const hasMod = /sisa\s*=\s*(total_kristal\s*%\s*4|23\s*%\s*4)/.test(code);
      const hasMul = /daya_kristal\s*=\s*(sisa\s*\*\s*10|3\s*\*\s*10)/.test(code);

      if (!hasTot) return { success: false, msg: "Variabel total_kristal harus bernilai 23." };
      if (!hasMod) return { success: false, msg: "Gunakan operator %: sisa = total_kristal % 4" };
      if (!hasMul) return { success: false, msg: "daya_kristal harus mengalikan sisa dengan 10 (sisa * 10)." };

      return { success: true, msg: "Kristal ungu beresonansi menghasilkan 30 daya magis!" };
    }
  },

  // -------------------------------------------------------------
  // QUEST 4: Rawa Keputusan (Action Minigame: Lomba Lari Sprint Dash)
  // -------------------------------------------------------------
  {
    id: 4,
    type: "race",
    minigame_type: "dash",
    location: "Rawa Keputusan (Danau Tengah)",
    npc_name: "Katak Mahkota Melayang",
    npc_blip: "low",
    npc_title: "Hakim Aliran Rawa",
    story: "Krook... air rawa akan segera pasang! Jika kamu bisa berlari lincah menghindari lumpur dan meraih 100 Poin booster kecepatan, jembatan teratai akan kubuka!",
    topic: "Percabangan if-else & Kecepatan",
    lesson: `Logika Percabangan Keputusan:<br>
<pre>if punya_kunci == True:
    print("Jembatan Terbuka")
else:
    print("Terkunci")</pre>`,
    task: `MISI LOMBA LARI SPRINT:
1. Buka Tab '🎮 Mini-Game Aksi'.
2. Kendalikan karakter menghindari lumpur pekat dan ambil booster kilat ⚡.
3. Kumpulkan minimal 100 Poin untuk memenangkan balapan!`,
    initial_code: `# --- TANTANGAN QUEST 4: BALAP SPRINT RAWA ---
# Selesaikan minigame lomba lari untuk melewati rawa keputusan!
`,
    hints: [
      "Gunakan tombol W / S atau Panah Atas/Bawah untuk menghindari lumpur dan mengambil booster kilat!"
    ],
    reward_item: "Sayap Kanan & Kemudi Pesawat",
    reward_desc: "Kedua sayap pesawat di alun-alun kini terpasang seimbang!",
    validator: () => ({ success: true, msg: "Kamu berhasil menyeberangi rawa dengan kecepatan kilat!" })
  },

  // -------------------------------------------------------------
  // QUEST 5: Taman Cabang (Coding + Minigame Tembak Kelopak)
  // -------------------------------------------------------------
  {
    id: 5,
    type: "coding",
    minigame_type: "shooter",
    location: "Taman Cabang (Timur Tengah)",
    npc_name: "Bunga Melankolis Raksasa",
    npc_blip: "high",
    npc_title: "Penjaga Kelopak Kelabu",
    story: "Kelopakkau layu oleh kabut keraguan...\nTentukan klasifikasi cabang mekar bungaku dan basmi hama bayangan dengan blaster!",
    topic: "Kondisional elif & Operator Logika",
    lesson: `Percabangan multi-kondisi bertingkat dengan <b>elif</b>:<br>
<pre>if skor >= 80:
    status_bunga = "Mekar Sempurna"
elif skor >= 50:
    status_bunga = "Mekar Sebagian"
else:
    status_bunga = "Kuncup"</pre>`,
    task: `ALGORITMA & PSEUDOCODE:
skor_cahaya = 85
JIKA skor_cahaya >= 80 -> status_bunga = "Mekar Sempurna"
JIKA LAIN (elif) skor_cahaya >= 50 -> status_bunga = "Mekar Sebagian"
SELAIN ITU (else) -> status_bunga = "Kuncup"`,
    initial_code: `# --- TANTANGAN QUEST 5: MULTI-KONDISI ELIF ---
skor_cahaya = 85

# TODO: Lengkapi percabangan di bawah ini:
if skor_cahaya >= 80:
    status_bunga = ...
elif skor_cahaya >= 50:
    status_bunga = ...
else:
    status_bunga = ...
`,
    hints: [
      "status_bunga = \"Mekar Sempurna\"",
      "status_bunga = \"Mekar Sebagian\"",
      "status_bunga = \"Kuncup\""
    ],
    reward_item: "Cat Pelangi Lambung Pesawat",
    reward_desc: "Badan pesawat kini dicat indah berkilau warna pastel!",
    validator: (code) => {
      if (!/if\s+skor_cahaya\s*>=\s*80/.test(code)) return { success: false, msg: "Gunakan 'if skor_cahaya >= 80:'" };
      if (!/status_bunga\s*=\s*["']Mekar Sempurna["']/.test(code)) return { success: false, msg: "Set status_bunga = 'Mekar Sempurna' pada kondisi >= 80." };
      if (!/elif\s+skor_cahaya\s*>=\s*50/.test(code)) return { success: false, msg: "Gunakan 'elif skor_cahaya >= 50:'" };
      return { success: true, msg: "Bunga melankolis memancarkan warna pelangi yang memukau!" };
    }
  },

  // -------------------------------------------------------------
  // QUEST 6: Lembah Berulang (Scavenger Hunt: 4 Sparepart Pesawat)
  // -------------------------------------------------------------
  {
    id: 6,
    type: "scavenger",
    target_count: 4,
    item_target_name: "Baut & Suku Cadang",
    location: "Lembah Berulang (Timur Laut)",
    npc_name: "Kucing Pita Pastel",
    npc_blip: "high",
    npc_title: "Kolektor Barang Surealis",
    story: "Meow~ Kotak peralatan pesawatmu tumpah berantakan di sepanjang lembah berkabut!\nKumpulkan 4 suku cadang berceceran di lembah agar bisa dirangkai ke dalam list inventaris!",
    topic: "List / Array Dinamis",
    lesson: `Konsep List (Koleksi Berurutan):<br>
• Membuat list: <code>tas = ["baut", "mur", "kabel"]</code><br>
• Menambah elemen: <code>tas.append("oli")</code><br>
• Mengakses elemen pertama: <code>tas[0]</code>`,
    task: `MISI PENCARIAN SUKU CADANG:
1. Jelajahi Lembah Berulang di area timur laut pulau.
2. Cari dan kumpulkan 4 Baut & Suku Cadang yang bersinar di tanah.
3. Tekan [E] saat berada di dekat benda tersebut!`,
    initial_code: `# --- MISI PENCARIAN 4 SUKU CADANG ---
# Cari 4 Baut & Suku Cadang yang tercecer di Lembah Berulang!
`,
    hints: [
      "Jelajahi area timur laut melewati jembatan kayu dan semak ungu.",
      "Dekati objek berbentuk roda gigi dan tekan [E]."
    ],
    reward_item: "Kotak Perkakas Mekanik Pesawat",
    reward_desc: "Kerangka dalam pesawat di tengah pulau selesai dirakit!",
    validator: () => ({ success: true, msg: "Semua 4 suku cadang berhasil dikumpulkan ke dalam list!" })
  },

  // -------------------------------------------------------------
  // QUEST 7: Pasar Misteri & Desa Warga (Interaksi Rumah & Barter)
  // -------------------------------------------------------------
  {
    id: 7,
    type: "coding",
    minigame_type: "dash",
    location: "Perkampungan Warga (Timur Pulau)",
    npc_name: "Pedagang Topeng Bulan",
    npc_blip: "mid",
    npc_title: "Saudagar Barang Memori",
    story: "Kiosku di desa menjual radar navigasi pesawat!\nCatat spesifikasi dictionary dan antarkan pesanan melintasi jalan desa warga!",
    topic: "Dictionary (Key-Value)",
    lesson: `Dictionary menyimpan data berpasangan <code>{kunci: nilai}</code>:<br>
• Membuat dict: <code>perahu = {"kayu": 5, "mesin": "rusak"}</code><br>
• Mengubah nilai: <code>perahu["mesin"] = "bagus"</code><br>
• Menambah kunci baru: <code>perahu["layar"] = 1</code>`,
    task: `ALGORITMA & PSEUDOCODE:
1. perahu = {"kayu": 5, "mesin": "rusak"}
2. perahu["mesin"] = "bagus"
3. perahu["layar"] = 1`,
    initial_code: `# --- TANTANGAN QUEST 7: DICTIONARY KEY-VALUE ---
# TODO: Lengkapi kamus data onderdil berikut:
perahu = {"kayu": 5, "mesin": ...}
perahu["mesin"] = ...
perahu[...] = 1
`,
    hints: [
      "perahu[\"mesin\"] = \"bagus\"",
      "perahu[\"layar\"] = 1"
    ],
    reward_item: "Kompas & Radar Navigasi Pesawat",
    reward_desc: "Kokpit pesawat di alun-alun pulau kini dilengkapi radar menyala!",
    validator: (code) => {
      if (!/perahu\s*\[\s*["']mesin["']\s*\]\s*=\s*["']bagus["']/.test(code)) return { success: false, msg: "Ubah nilai mesin dengan: perahu[\"mesin\"] = \"bagus\"" };
      if (!/perahu\s*\[\s*["']layar["']\s*\]\s*=\s*1/.test(code)) return { success: false, msg: "Tambah kunci layar dengan: perahu[\"layar\"] = 1" };
      return { success: true, msg: "Kamus suku cadang perahu & radar telah diperbarui!" };
    }
  },

  // -------------------------------------------------------------
  // QUEST 8: Menara Waktu (Coding + Minigame Jumper Waktu)
  // -------------------------------------------------------------
  {
    id: 8,
    type: "coding",
    minigame_type: "jumper",
    location: "Menara Waktu (Puncak Barat)",
    npc_name: "Jam Bandul Bersayap",
    npc_blip: "mid",
    npc_title: "Pengawas Putaran Detik",
    story: "Tik... tok... putaran waktu di menara terhenti!\nGunakan loop perulangan for dan lompati rintangan jarum detik untuk mengumpulkan 100 poin!",
    topic: "Perulangan for loop & range()",
    lesson: `Perulangan mengulang blok kode otomatis:<br>
<pre>total = 0
for i in range(1, 6): # mengulang 1, 2, 3, 4, 5
    total = total + i</pre>`,
    task: `ALGORITMA & PSEUDOCODE:
total_detik = 0
UNTUK i DALAM range(1, 6):
    total_detik = total_detik + i`,
    initial_code: `# --- TANTANGAN QUEST 8: PERULANGAN FOR LOOP ---
total_detik = 0

# TODO: Lengkapi perulangan for di bawah ini:
for i in range(..., ...):
    total_detik = total_detik + ...
`,
    hints: [
      "range(1, 6) menghasilkan angka 1 sampai 5.",
      "total_detik = total_detik + i"
    ],
    reward_item: "Gigi Roda Kronos & Spidometer",
    reward_desc: "Panel spidometer pesawat kini berdetak presisi!",
    validator: (code) => {
      if (!/for\s+\w+\s+in\s+range\s*\(\s*1\s*,\s*6\s*\)\s*:/.test(code)) return { success: false, msg: "Gunakan: for i in range(1, 6):" };
      if (!/total_detik\s*(\+=|=.*total_detik\s*\+\s*i)/.test(code)) return { success: false, msg: "Jumlahkan: total_detik = total_detik + i" };
      return { success: true, msg: "Putaran waktu berhasil disinkronkan kembali!" };
    }
  },

  // -------------------------------------------------------------
  // QUEST 9: Kuil Mantra (Coding + Minigame Blaster)
  // -------------------------------------------------------------
  {
    id: 9,
    type: "coding",
    minigame_type: "shooter",
    location: "Kuil Mantra (Altar Kuno)",
    npc_name: "Patung Pendeta Cahaya",
    npc_blip: "low",
    npc_title: "Arsitek Formula Kuno",
    story: "Mantra kuno pembangkit turbin membutuhkan formula fungsi def!\nBungkus rumusnya dan hancurkan penghalang kuil dengan tembakan magis!",
    topic: "Pembuatan Fungsi (def & return)",
    lesson: `Fungsi membungkus logika agar reusable:<br>
<pre>def hitung_daya(voltase, arus):
    return voltase * arus

daya_kapal = hitung_daya(12, 5)</pre>`,
    task: `ALGORITMA & PSEUDOCODE:
1. def hitung_daya(voltase, arus): return voltase * arus
2. daya_kapal = hitung_daya(12, 5)`,
    initial_code: `# --- TANTANGAN QUEST 9: FUNGSI DEF & RETURN ---
# TODO: Lengkapi deklarasi fungsi berikut:
def hitung_daya(..., ...):
    return ... * ...

daya_kapal = hitung_daya(12, 5)
`,
    hints: [
      "def hitung_daya(voltase, arus):",
      "return voltase * arus"
    ],
    reward_item: "Bahan Bakar Turbin Surealis",
    reward_desc: "Tangki bahan bakar pesawat telah terisi penuh!",
    validator: (code) => {
      if (!/def\s+hitung_daya\s*\(\s*voltase\s*,\s*arus\s*\)\s*:/.test(code)) return { success: false, msg: "Definisikan: def hitung_daya(voltase, arus):" };
      if (!/return\s+voltase\s*\*\s*arus/.test(code)) return { success: false, msg: "Kembalikan perkalian: return voltase * arus" };
      return { success: true, msg: "Mantra pembangkit daya berhasil dikristalisasi!" };
    }
  },

  // -------------------------------------------------------------
  // QUEST 10: Alun-Alun Tengah Pulau (Final Mesin Pesawat)
  // -------------------------------------------------------------
  {
    id: 10,
    type: "coding",
    minigame_type: "shooter",
    location: "Pesawat Rusak (Alun-Alun Tengah Pulau)",
    npc_name: "Kapten Boneka Beruang",
    npc_blip: "low",
    npc_title: "Nahkoda Penerbangan Mimpi",
    story: "Semua onderdil pesawat telah terpasang sempurna!\nKini saatnya menyalakan pengapian mesin pesawat dengan penanganan error (try - except) agar pesawat tidak meledak saat lepas landas!",
    topic: "Penanganan Error (try & except)",
    lesson: `try-except mengamankan runtime pengapian mesin:<br>
<pre>try:
    hasil = 100 / daya_input
    status_mesin = "Normal"
except ZeroDivisionError:
    status_mesin = "Pengaman Darurat Aktif"</pre>`,
    task: `ALGORITMA & PSEUDOCODE:
daya_input = 0
status_mesin = "Mati"

COBA (try):
    hasil = 100 / daya_input
    status_mesin = "Normal"
TANGKAP (except ZeroDivisionError):
    status_mesin = "Pengaman Darurat Aktif"`,
    initial_code: `# --- TANTANGAN FINAL QUEST 10: PENGAMANAN MESIN ---
daya_input = 0
status_mesin = "Mati"

# TODO: Lengkapi blok try-except di bawah:
try:
    hasil = 100 / daya_input
    status_mesin = ...
except ZeroDivisionError:
    status_mesin = ...
`,
    hints: [
      "status_mesin = \"Normal\" di blok try",
      "status_mesin = \"Pengaman Darurat Aktif\" di blok except ZeroDivisionError"
    ],
    reward_item: "Kunci Kontak Emas Pesawat",
    reward_desc: "MESIN PESAWAT MENYALA MENDERU! PESAWAT SIAP TERBANG!",
    validator: (code) => {
      if (!/try\s*:/.test(code)) return { success: false, msg: "Gunakan blok 'try:'" };
      if (!/except\s+ZeroDivisionError\s*:/.test(code)) return { success: false, msg: "Tangkap error: 'except ZeroDivisionError:'" };
      if (!/status_mesin\s*=\s*["']Pengaman Darurat Aktif["']/.test(code)) return { success: false, msg: "Set status_mesin = 'Pengaman Darurat Aktif' di dalam blok except." };
      return { success: true, msg: "MESIN PESAWAT MENYALA STABIL! PESAWAT SIAP LEPAS LANDAS!" };
    }
  }
];
