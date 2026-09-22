/**
 * game.js - Engine Game 2D Open-World Island RPG (OMORI x Google Doodle Champion Island Style)
 * Menampilkan Peta Pulau Terbuka 2400x1920, Pesawat Rusak di Tengah Pulau yang Berevolusi,
 * Perkampungan Desa dengan Rumah Interaktif, NPC Warga Biasa, Scavenger Hunt, dan Minigame Arkade.
 */

const TILE_SIZE = 48;
const MAP_COLS = 50;
const MAP_ROWS = 40;
const MAP_WIDTH = MAP_COLS * TILE_SIZE;
const MAP_HEIGHT = MAP_ROWS * TILE_SIZE;

// --- KAMERA SCROLLING 2D HALUS ---
class Camera {
  constructor(viewportW, viewportH) {
    this.x = 0;
    this.y = 0;
    this.w = viewportW;
    this.h = viewportH;
  }

  update(targetX, targetY) {
    const desiredX = targetX - this.w / 2;
    const desiredY = targetY - this.h / 2;
    this.x += (desiredX - this.x) * 0.12;
    this.y += (desiredY - this.y) * 0.12;
    this.x = Math.max(0, Math.min(this.x, MAP_WIDTH - this.w));
    this.y = Math.max(0, Math.min(this.y, MAP_HEIGHT - this.h));
  }
}

// --- KARAKTER PEMAIN (OMORI SPRITE) ---
class Player {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.w = 34;
    this.h = 42;
    this.speed = 220;
    this.direction = 'down';
    this.isMoving = false;
    this.animTimer = 0;
    this.animFrame = 0;
    this.inventory = [];
    this.currentQuestIndex = 0; // 0..9
    this.interactTarget = null;
    this.scavengerItemsCollected = 0;
  }

  getHitbox() {
    return { x: this.x + 4, y: this.y + this.h - 16, w: this.w - 8, h: 14 };
  }

  handleInput(dt, keys, obstacles) {
    let dx = 0;
    let dy = 0;

    if (keys['KeyW'] || keys['ArrowUp']) { dy -= 1; this.direction = 'up'; }
    if (keys['KeyS'] || keys['ArrowDown']) { dy += 1; this.direction = 'down'; }
    if (keys['KeyA'] || keys['ArrowLeft']) { dx -= 1; this.direction = 'left'; }
    if (keys['KeyD'] || keys['ArrowRight']) { dx += 1; this.direction = 'right'; }

    const dist = Math.hypot(dx, dy);
    if (dist > 0) {
      dx /= dist;
      dy /= dist;
      this.isMoving = true;
      this.animTimer += dt * 8;
      if (this.animTimer >= 1) {
        this.animTimer = 0;
        this.animFrame = (this.animFrame + 1) % 4;
      }
    } else {
      this.isMoving = false;
      this.animFrame = 0;
    }

    const oldX = this.x;
    this.x += dx * this.speed * dt;
    if (this._checkCollision(obstacles)) {
      this.x = oldX;
    }

    const oldY = this.y;
    this.y += dy * this.speed * dt;
    if (this._checkCollision(obstacles)) {
      this.y = oldY;
    }
  }

  _checkCollision(obstacles) {
    const hb = this.getHitbox();
    // Batas Luar Peta
    if (hb.x < 3 * TILE_SIZE || hb.x + hb.w > MAP_WIDTH - 3 * TILE_SIZE) return true;
    if (hb.y < 3 * TILE_SIZE || hb.y + hb.h > MAP_HEIGHT - 3 * TILE_SIZE) return true;

    // Rintangan (Rumah, Danau dalam, tebing)
    for (const ob of obstacles) {
      if (hb.x < ob.x + ob.w && hb.x + hb.w > ob.x && hb.y < ob.y + ob.h && hb.y + hb.h > ob.y) {
        return true;
      }
    }
    return false;
  }

  draw(ctx, cam) {
    const sx = Math.floor(this.x - cam.x);
    const sy = Math.floor(this.y - cam.y);
    const bob = (this.isMoving || this.animFrame > 0) ? Math.sin(this.animFrame * Math.PI / 2) * 2 : 0;
    const legOffset = (this.isMoving || this.animFrame > 0) ? Math.sin(this.animFrame * Math.PI / 2) * 3 : 0;

    // Bayangan
    ctx.fillStyle = "rgba(12, 10, 22, 0.4)";
    ctx.beginPath();
    ctx.ellipse(sx + this.w / 2, sy + this.h - 4, this.w / 2 - 2, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Kaki & Sepatu
    ctx.fillStyle = "#ebebf5";
    ctx.fillRect(sx + 9, sy + this.h - 12 + bob - legOffset, 5, 7);
    ctx.fillRect(sx + 20, sy + this.h - 12 + bob + legOffset, 5, 7);

    ctx.fillStyle = "#1e1928";
    ctx.fillRect(sx + 8, sy + this.h - 6 + bob - legOffset, 7, 4);
    ctx.fillRect(sx + 19, sy + this.h - 6 + bob + legOffset, 7, 4);

    // Celana Pendek Hitam
    ctx.fillStyle = "#1a1626";
    ctx.fillRect(sx + 8, sy + this.h - 20 + bob, 18, 9);

    // Baju Putih & Rompi
    ctx.fillStyle = "#f5f5fa";
    ctx.fillRect(sx + 7, sy + 13 + bob, 20, 14);
    ctx.strokeStyle = "#251e34";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(sx + 9, sy + 14 + bob, 16, 12);
    ctx.beginPath();
    ctx.moveTo(sx + 17, sy + 14 + bob);
    ctx.lineTo(sx + 17, sy + 26 + bob);
    ctx.stroke();

    // Wajah
    ctx.fillStyle = "#fcf8f2";
    ctx.fillRect(sx + 8, sy + 3 + bob, 18, 14);

    // Rambut Hitam khas OMORI
    ctx.fillStyle = "#141020";
    ctx.fillRect(sx + 6, sy + 0 + bob, 22, 8);
    ctx.fillRect(sx + 5, sy + 4 + bob, 4, 9);
    ctx.fillRect(sx + 25, sy + 4 + bob, 4, 9);

    if (this.direction === 'down') {
      ctx.beginPath();
      ctx.moveTo(sx + 11, sy + 8 + bob); ctx.lineTo(sx + 14, sy + 11 + bob); ctx.lineTo(sx + 16, sy + 8 + bob);
      ctx.fill();
      ctx.fillStyle = "#140e20";
      ctx.fillRect(sx + 11, sy + 9 + bob, 3, 4); ctx.fillRect(sx + 20, sy + 9 + bob, 3, 4);
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(sx + 11, sy + 9 + bob, 1, 1); ctx.fillRect(sx + 20, sy + 9 + bob, 1, 1);
      ctx.fillStyle = "#ffa8cb";
      ctx.fillRect(sx + 9, sy + 13 + bob, 3, 2); ctx.fillRect(sx + 22, sy + 13 + bob, 3, 2);
    } else if (this.direction === 'left') {
      ctx.fillStyle = "#140e20"; ctx.fillRect(sx + 10, sy + 9 + bob, 3, 4);
      ctx.fillStyle = "#ffffff"; ctx.fillRect(sx + 10, sy + 9 + bob, 1, 1);
      ctx.fillStyle = "#ffa8cb"; ctx.fillRect(sx + 9, sy + 13 + bob, 3, 2);
    } else if (this.direction === 'right') {
      ctx.fillStyle = "#140e20"; ctx.fillRect(sx + 21, sy + 9 + bob, 3, 4);
      ctx.fillStyle = "#ffffff"; ctx.fillRect(sx + 22, sy + 9 + bob, 1, 1);
      ctx.fillStyle = "#ffa8cb"; ctx.fillRect(sx + 22, sy + 13 + bob, 3, 2);
    }

    // Prompt Interaksi
    if (this.interactTarget) {
      const floatY = Math.sin(performance.now() * 0.006) * 3;
      ctx.fillStyle = "rgba(16, 12, 28, 0.9)";
      ctx.strokeStyle = "#91f0d7";
      ctx.lineWidth = 1.5;
      
      const px = sx + this.w / 2 - 45;
      const py = sy - 26 + floatY;
      ctx.fillRect(px, py, 90, 20);
      ctx.strokeRect(px, py, 90, 20);

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 11px Space Mono, monospace";
      ctx.textAlign = "center";
      ctx.fillText(this.interactTarget.prompt || "[E] Interaksi", sx + this.w / 2, py + 14);
    }
  }
}

// --- RUMAH WARGA DESA INTERAKTIF ---
class VillageHouse {
  constructor(gridX, gridY, name, message, color = "#af91e1") {
    this.x = gridX * TILE_SIZE;
    this.y = gridY * TILE_SIZE;
    this.w = 4 * TILE_SIZE;
    this.h = 3 * TILE_SIZE;
    this.cx = this.x + this.w / 2;
    this.cy = this.y + this.h / 2;
    this.name = name;
    this.message = message;
    this.color = color;
    this.prompt = "[E] Ketuk Pintu";
  }

  draw(ctx, cam) {
    const sx = Math.floor(this.x - cam.x);
    const sy = Math.floor(this.y - cam.y);

    // Badan Rumah
    ctx.fillStyle = "#251e38";
    ctx.fillRect(sx, sy + TILE_SIZE, this.w, this.h - TILE_SIZE);
    ctx.strokeStyle = "#4a3c6b";
    ctx.lineWidth = 2;
    ctx.strokeRect(sx, sy + TILE_SIZE, this.w, this.h - TILE_SIZE);

    // Atap Segitiga Bergaya Pastel
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(sx - 10, sy + TILE_SIZE);
    ctx.lineTo(sx + this.w / 2, sy - 10);
    ctx.lineTo(sx + this.w + 10, sy + TILE_SIZE);
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.stroke();

    // Pintu Kayu
    ctx.fillStyle = "#6e4b32";
    const doorX = sx + this.w / 2 - 16;
    const doorY = sy + this.h - 36;
    ctx.fillRect(doorX, doorY, 32, 36);
    ctx.fillStyle = "#ffd75a";
    ctx.fillRect(doorX + 22, doorY + 16, 4, 4); // Gagang pintu

    // Jendela Bercahaya
    ctx.fillStyle = "#fff0b4";
    ctx.fillRect(sx + 20, sy + TILE_SIZE + 16, 24, 24);
    ctx.fillRect(sx + this.w - 44, sy + TILE_SIZE + 16, 24, 24);
    ctx.strokeStyle = "#322346";
    ctx.strokeRect(sx + 20, sy + TILE_SIZE + 16, 24, 24);
    ctx.strokeRect(sx + this.w - 44, sy + TILE_SIZE + 16, 24, 24);

    // Plang Nama Rumah
    ctx.fillStyle = "rgba(18, 14, 30, 0.85)";
    ctx.fillRect(sx + 10, sy + TILE_SIZE - 24, this.w - 20, 18);
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 10px Space Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(this.name, sx + this.w / 2, sy + TILE_SIZE - 11);
  }
}

// --- ITEM SCAVENGER (BARANG TERSEMBUNYI DI PULAU) ---
class ScavengerItem {
  constructor(id, x, y, name, color = "#91f0d7") {
    this.id = id;
    this.x = x;
    this.y = y;
    this.w = 24;
    this.h = 24;
    this.cx = x + 12;
    this.cy = y + 12;
    this.name = name;
    this.color = color;
    this.isCollected = false;
    this.prompt = "[E] Ambil " + name;
  }

  draw(ctx, cam) {
    if (this.isCollected) return;

    const sx = Math.floor(this.x - cam.x);
    const floatY = Math.sin(performance.now() * 0.006 + this.id) * 4;
    const sy = Math.floor(this.y - cam.y + floatY);

    // Pijaran Cahaya
    ctx.fillStyle = "rgba(145, 240, 215, 0.3)";
    ctx.beginPath();
    ctx.arc(sx + 12, sy + 12, 16, 0, Math.PI * 2);
    ctx.fill();

    // Kristal / Roda Gigi
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(sx + 12, sy + 2);
    ctx.lineTo(sx + 22, sy + 12);
    ctx.lineTo(sx + 12, sy + 22);
    ctx.lineTo(sx + 2, sy + 12);
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }
}

// --- NPC WARGA DESA BIASA (AMBIENT DIALOGUE) ---
class AmbientNPC {
  constructor(gridX, gridY, name, role, dialog, color = "#ffa8cb") {
    this.x = gridX * TILE_SIZE;
    this.y = gridY * TILE_SIZE;
    this.w = 36;
    this.h = 42;
    this.cx = this.x + 18;
    this.cy = this.y + 21;
    this.name = name;
    this.role = role;
    this.dialog = dialog;
    this.color = color;
    this.prompt = "[E] Bicara";
  }

  draw(ctx, cam) {
    const sx = Math.floor(this.x - cam.x);
    const sy = Math.floor(this.y - cam.y);

    // Bayangan
    ctx.fillStyle = "rgba(10, 8, 20, 0.4)";
    ctx.beginPath();
    ctx.ellipse(sx + 18, sy + 38, 14, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Badan & Pakaian Pastel
    ctx.fillStyle = this.color;
    ctx.fillRect(sx + 8, sy + 14, 20, 24);

    // Wajah
    ctx.fillStyle = "#fcf8f2";
    ctx.fillRect(sx + 10, sy + 4, 16, 12);

    // Mata
    ctx.fillStyle = "#140e20";
    ctx.fillRect(sx + 13, sy + 9, 2, 3);
    ctx.fillRect(sx + 21, sy + 9, 2, 3);
  }
}

// --- NPC MASTER QUEST ---
class QuestNPC {
  constructor(questId, gridX, gridY, name, title, blipPitch) {
    this.questId = questId;
    this.x = gridX * TILE_SIZE;
    this.y = gridY * TILE_SIZE;
    this.w = 40;
    this.h = 46;
    this.cx = this.x + 20;
    this.cy = this.y + 23;
    this.name = name;
    this.title = title;
    this.blipPitch = blipPitch;
    this.prompt = "[E] Quest " + questId;
  }

  draw(ctx, cam) {
    const sx = Math.floor(this.x - cam.x);
    const floatY = Math.sin(performance.now() * 0.004 + this.questId) * 3;
    const sy = Math.floor(this.y - cam.y + floatY);

    // Pijaran Simbol Quest
    ctx.fillStyle = "rgba(255, 240, 180, 0.3)";
    ctx.beginPath();
    ctx.arc(sx + 20, sy + 20, 24, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ffa8cb";
    ctx.beginPath();
    ctx.arc(sx + 20, sy + 20, 15, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Simbol Seru Emas di Atas Kepala
    ctx.fillStyle = "#ffd75a";
    ctx.font = "bold 16px Space Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText("!", sx + 20, sy - 8);
  }
}

// --- GAME APP UTAMA ---
class GameApp {
  constructor() {
    this.canvas = document.getElementById("game-canvas");
    this.ctx = this.canvas.getContext("2d");
    this.camera = new Camera(960, 640);
    this.player = new Player(24 * TILE_SIZE, 22 * TILE_SIZE); // Mulai dekat pesawat di alun-alun tengah

    this.keys = {};
    this.questNPCs = [];
    this.ambientNPCs = [];
    this.houses = [];
    this.scavengerItems = [];
    this.obstacles = [];

    this.minigameManager = new MiniGameManager("minigame-canvas");
    this.activeQuest = null;

    this.introTexts = [
      "Badai petir menyambar pesawatmu dan kamu terdampar di Pulau Sintaksis!",
      "Pesawatmu yang rusak tergeletak di tengah alun-alun pulau...",
      "Jelajahi pantai, hutan lebat, tebing gua, dan desa perkampungan warga.",
      "Kumpulkan suku cadang, selesaikan quest Python & mini-game aksi untuk memperbaiki pesawat!",
      "Ayo perbaiki pesawat sedikit demi sedikit dan terbang bebas pulang!"
    ];
    this.introStep = 0;

    this._buildWorld();
    this._bindEvents();
    this._startLoop();
  }

  _buildWorld() {
    // 1. Tempatkan Pesawat Rusak di Tengah Pulau (Col 23-26, Row 18-21)
    this.planeX = 23 * TILE_SIZE;
    this.planeY = 18 * TILE_SIZE;
    this.obstacles.push({ x: this.planeX, y: this.planeY + 20, w: 4 * TILE_SIZE, h: 2 * TILE_SIZE });

    // 2. Buat 5 Rumah Warga di Desa (Area Timur Pulau)
    const villageHouses = [
      { gx: 34, gy: 14, name: "Kios Pedagang Topeng Bulan", msg: "Selamat datang di Kios Memori! Kami menjual onderdil dan radar pesawat.", col: "#ffd78c" },
      { gx: 40, gy: 14, name: "Rumah Mori Si Kerang", msg: "Mori: 'Pantai di selatan sangat tenang... Jangan lupa berlatih fungsi print!'", col: "#ffa8cb" },
      { gx: 34, gy: 22, name: "Perpustakaan Mantra Kuno", msg: "Buku catatan kuno: 'Fungsi def adalah cara para tetua membungkus keajaiban.'", col: "#91f0d7" },
      { gx: 40, gy: 22, name: "Bengkel Mekanik Lavender", msg: "Bengkel: 'Baut dan generator siap dipasang ke sayap pesawat!'", col: "#af91e1" },
      { gx: 37, gy: 28, name: "Kincir Angin Waktu", msg: "Penjaga Kincir: 'Putaran waktu di pulau ini mengikuti ritme for loop.'", col: "#ffbedc" }
    ];

    villageHouses.forEach(h => {
      const house = new VillageHouse(h.gx, h.gy, h.name, h.msg, h.col);
      this.houses.push(house);
      this.obstacles.push({ x: house.x, y: house.y + TILE_SIZE, w: house.w, h: house.h - TILE_SIZE });
    });

    // 3. Buat 10 NPC Quest Master di Lokasi Alami
    const qLocations = [
      { qid: 1, gx: 10, gy: 32 }, // Pantai Selatan Barat
      { qid: 2, gx: 8, gy: 12 },  // Hutan Barat Laut
      { qid: 3, gx: 24, gy: 6 },  // Tebing Gua Utara
      { qid: 4, gx: 14, gy: 20 }, // Danau Rawa Tengah
      { qid: 5, gx: 28, gy: 28 }, // Taman Bunga Selatan
      { qid: 6, gx: 38, gy: 8 },  // Lembah Timur Laut
      { qid: 7, gx: 36, gy: 18 }, // Desa Pasar Timur
      { qid: 8, gx: 6, gy: 24 },  // Menara Waktu Barat
      { qid: 9, gx: 18, gy: 8 },  // Kuil Mantra Kuno
      { qid: 10, gx: 24, gy: 17 } // Dekat Pesawat Tengah
    ];

    qLocations.forEach(loc => {
      const q = QUEST_DATA[loc.qid - 1];
      this.questNPCs.push(new QuestNPC(loc.qid, loc.gx, loc.gy, q.npc_name, q.npc_title, q.npc_blip));
    });

    // 4. Buat 6 NPC Warga Biasa (Ambient Dialogues)
    this.ambientNPCs.push(new AmbientNPC(36, 17, "Bocah Topi Jerami", "Warga", "Aku suka melihat pesawat di tengah pulau! Kalau sudah selesai diperbaiki, ajak aku terbang ya!"));
    this.ambientNPCs.push(new AmbientNPC(12, 30, "Gadis Payung Pastel", "Warga", "Hari ini ombak pantainya berbusa ungu. Rasanya sangat menyejukkan!"));
    this.ambientNPCs.push(new AmbientNPC(28, 35, "Kakek Pemancing Bulan", "Warga", "Dermaga kayu di tenggara adalah tempat terbaik memandang langit sore."));
    this.ambientNPCs.push(new AmbientNPC(10, 16, "Sprout Mole Surealis", "Warga", "Toge... toge... Hutan di utara menyimpan kristal data yang berkilau!"));
    this.ambientNPCs.push(new AmbientNPC(38, 25, "Kucing Pita Penjaga", "Warga", "Meow! Kamu bisa mengetuk pintu rumah-rumah warga di desa untuk menyapa!"));

    // 5. Buat Item Scavenger (Quest 2 & Quest 6)
    // 3 Kristal di Hutan Barat
    this.scavengerItems.push(new ScavengerItem(1, 6 * TILE_SIZE, 10 * TILE_SIZE, "Kristal Data String", "#91f0d7"));
    this.scavengerItems.push(new ScavengerItem(2, 11 * TILE_SIZE, 8 * TILE_SIZE, "Kristal Data Integer", "#ffa8cb"));
    this.scavengerItems.push(new ScavengerItem(3, 8 * TILE_SIZE, 15 * TILE_SIZE, "Kristal Data Boolean", "#fff0b4"));

    // 4 Sparepart di Lembah & Sekitar
    this.scavengerItems.push(new ScavengerItem(4, 35 * TILE_SIZE, 6 * TILE_SIZE, "Roda Gigi Kronos", "#ffd75a"));
    this.scavengerItems.push(new ScavengerItem(5, 42 * TILE_SIZE, 10 * TILE_SIZE, "Baut Sayap Baja", "#af91e1"));
    this.scavengerItems.push(new ScavengerItem(6, 30 * TILE_SIZE, 10 * TILE_SIZE, "Kabel Turbin Emas", "#ffa8cb"));
    this.scavengerItems.push(new ScavengerItem(7, 44 * TILE_SIZE, 16 * TILE_SIZE, "Mur Pengunci Kemudi", "#91f0d7"));
  }

  _bindEvents() {
    window.addEventListener("keydown", (e) => {
      this.keys[e.code] = true;

      if (e.code === "Enter" && !document.getElementById("title-screen").classList.contains("hidden")) {
        this._startGameFromTitle();
      }

      if ((e.code === "Space" || e.code === "Enter") && !document.getElementById("intro-screen").classList.contains("hidden")) {
        this._nextIntroStep();
      }

      if (e.code === "KeyE" || e.code === "Space") {
        if (this._isOverworldActive()) {
          this._handleOverworldInteraction();
        }
      }

      if (e.code === "KeyI" || e.code === "Tab") {
        if (this._isOverworldActive() || !document.getElementById("inventory-modal").classList.contains("hidden")) {
          e.preventDefault();
          this._toggleInventory();
        }
      }

      if (e.code === "Escape") {
        this._closeAllModals();
      }
    });

    window.addEventListener("keyup", (e) => {
      this.keys[e.code] = false;
    });

    // Button Bindings
    document.getElementById("btn-start-game").onclick = () => this._startGameFromTitle();
    document.getElementById("btn-next-intro").onclick = () => this._nextIntroStep();
    document.getElementById("btn-close-quest").onclick = () => this._closeAllModals();
    document.getElementById("btn-reset-code").onclick = () => this._resetQuestCode();
    document.getElementById("btn-quest-hint").onclick = () => this._showQuestHint();
    document.getElementById("btn-submit-code").onclick = () => this._submitQuestCode();

    document.getElementById("hud-inventory-btn").onclick = () => this._toggleInventory();
    document.getElementById("btn-close-inventory").onclick = () => this._closeAllModals();
    document.getElementById("btn-close-inv-bottom").onclick = () => this._closeAllModals();
    document.getElementById("btn-restart-game").onclick = () => location.reload();

    document.getElementById("tab-btn-lesson").onclick = () => this._switchTab("lesson");
    document.getElementById("tab-btn-code").onclick = () => this._switchTab("code");
    document.getElementById("tab-btn-minigame").onclick = () => this._switchTab("minigame");
  }

  _isOverworldActive() {
    return document.getElementById("title-screen").classList.contains("hidden") &&
           document.getElementById("intro-screen").classList.contains("hidden") &&
           document.getElementById("quest-modal").classList.contains("hidden") &&
           document.getElementById("inventory-modal").classList.contains("hidden") &&
           document.getElementById("ending-screen").classList.contains("hidden");
  }

  _startGameFromTitle() {
    audioSys.playSuccess();
    document.getElementById("title-screen").classList.add("hidden");
    document.getElementById("intro-screen").classList.remove("hidden");
    this.introStep = 0;
    this._showIntroText();
  }

  _showIntroText() {
    const header = document.getElementById("intro-header-text");
    const body = document.getElementById("intro-body-text");
    header.innerText = `PROLOGUE : Terdampar di Pulau Sintaksis (${this.introStep + 1}/${this.introTexts.length})`;
    body.innerText = this.introTexts[this.introStep];
    audioSys.playBlip("mid");
  }

  _nextIntroStep() {
    this.introStep++;
    if (this.introStep < this.introTexts.length) {
      this._showIntroText();
      audioSys.playClick();
    } else {
      document.getElementById("intro-screen").classList.add("hidden");
      this._showToast("Selamat Datang di Pulau Sintaksis! Temui Mori di Pantai Selatan.");
      audioSys.playPickup();
    }
  }

  _handleOverworldInteraction() {
    const target = this.player.interactTarget;
    if (!target) return;

    if (target instanceof QuestNPC) {
      this._openQuestModal(target.questId - 1);
    } else if (target instanceof VillageHouse) {
      this._showToast(`🚪 [${target.name}]: "${target.message}"`);
      audioSys.playClick();
    } else if (target instanceof AmbientNPC) {
      this._showToast(`💬 [${target.name}]: "${target.dialog}"`);
      audioSys.playBlip("high");
    } else if (target instanceof ScavengerItem) {
      target.isCollected = true;
      this.player.scavengerItemsCollected++;
      audioSys.playPickup();
      this._showToast(`★ Berhasil Memungut: ${target.name}!`);
    }
  }

  _openQuestModal(qIndex) {
    this.activeQuest = QUEST_DATA[qIndex];
    const q = this.activeQuest;

    document.getElementById("modal-quest-badge").innerText = `[ QUEST ${q.id}/10 : ${q.location.toUpperCase()} ]`;
    document.getElementById("modal-npc-name").innerText = q.npc_name;
    document.getElementById("modal-quest-topic").innerText = `Topik: ${q.topic}`;
    document.getElementById("modal-npc-story").innerText = `"${q.story}"`;

    document.getElementById("modal-lesson-content").innerHTML = `
      <h4>Materi: ${q.topic}</h4>
      <p>${q.lesson}</p>
      <hr style="border: 0; border-top: 1px solid #483c64; margin: 12px 0;">
      <h4 style="color: var(--pastel-yellow);">Tantangan / Panduan Pseudocode:</h4>
      <pre>${q.task}</pre>
    `;

    document.getElementById("modal-task-prompt").innerText = q.task.split("\n")[1] || q.task;
    document.getElementById("code-input").value = q.initial_code;
    
    // Feedback Reset
    const fb = document.getElementById("modal-feedback-box");
    fb.className = "feedback-box hidden";

    // Setup Minigame jika ada
    const minigameType = q.minigame_type || "shooter";
    document.getElementById("tab-score-badge").innerText = `0/100 Poin`;

    this._switchTab(q.type === "scavenger" ? "lesson" : "code");
    document.getElementById("quest-modal").classList.remove("hidden");
    audioSys.playPickup();
  }

  _switchTab(tab) {
    const btnL = document.getElementById("tab-btn-lesson");
    const btnC = document.getElementById("tab-btn-code");
    const btnM = document.getElementById("tab-btn-minigame");
    const paneL = document.getElementById("tab-pane-lesson");
    const paneC = document.getElementById("tab-pane-code");
    const paneM = document.getElementById("tab-pane-minigame");

    [btnL, btnC, btnM].forEach(b => b.classList.remove("active"));
    [paneL, paneC, paneM].forEach(p => p.classList.remove("active"));

    if (tab === "lesson") {
      btnL.classList.add("active"); paneL.classList.add("active");
      this.minigameManager.stop();
    } else if (tab === "code") {
      btnC.classList.add("active"); paneC.classList.add("active");
      this.minigameManager.stop();
    } else if (tab === "minigame") {
      btnM.classList.add("active"); paneM.classList.add("active");
      const mgType = this.activeQuest ? (this.activeQuest.minigame_type || "shooter") : "shooter";
      this.minigameManager.start(mgType, 100, (finalScore) => {
        document.getElementById("tab-score-badge").innerText = `${finalScore}/100 Poin (SELESAI)`;
        this._showToast("★ Tantangan Mini-Game Berhasil! Nilai 100 Poin!");
      });
    }
    audioSys.playClick();
  }

  _resetQuestCode() {
    if (this.activeQuest) {
      document.getElementById("code-input").value = this.activeQuest.initial_code;
      this._setFeedback("Kode direset ke pseudocode template.", "hint");
    }
  }

  _showQuestHint() {
    if (this.activeQuest && this.activeQuest.hints) {
      this._setFeedback(`💡 Petunjuk: ${this.activeQuest.hints[0]}`, "hint");
      audioSys.playBlip("high");
    }
  }

  _submitQuestCode() {
    if (!this.activeQuest) return;

    // 1. Jika tipe scavenger
    if (this.activeQuest.type === "scavenger") {
      if (this.player.scavengerItemsCollected < this.activeQuest.target_count) {
        this._setFeedback(`✗ Belum selesai! Kamu baru memungut ${this.player.scavengerItemsCollected}/${this.activeQuest.target_count} ${this.activeQuest.item_target_name}. Cari di pulau!`, "error");
        audioSys.playError();
        return;
      }
    }

    // 2. Jika tipe coding, verifikasi kode
    if (this.activeQuest.type === "coding") {
      const userCode = document.getElementById("code-input").value;
      const result = this.activeQuest.validator(userCode);
      if (!result.success) {
        this._setFeedback(`✗ ${result.msg}`, "error");
        audioSys.playError();
        return;
      }

      // Cek apakah mini-game arkade sudah dimainkan
      if (this.minigameManager.score < 100) {
        this._setFeedback(`✓ Kodemu BENAR! Sekarang buka Tab '🎮 Mini-Game Aksi' dan raih minimal 100 Poin untuk menuntaskan quest!`, "hint");
        this._switchTab("minigame");
        return;
      }
    }

    // 3. Quest Selesai!
    this._setFeedback(`★ LULUS! ${this.activeQuest.reward_desc}`, "success");
    audioSys.playSuccess();

    if (!this.player.inventory.includes(this.activeQuest.reward_item)) {
      this.player.inventory.push(this.activeQuest.reward_item);
      this.player.currentQuestIndex = Math.max(this.player.currentQuestIndex, this.activeQuest.id);
      this.player.scavengerItemsCollected = 0;
      this._updateHUD();
      this._showToast(`★ Quest ${this.activeQuest.id} Selesai! Pesawat di alun-alun semakin terpasang!`);
    }

    // Jika quest 10 selesai -> Tamat & Pesawat Terbang!
    if (this.activeQuest.id >= 10) {
      setTimeout(() => {
        this._closeAllModals();
        document.getElementById("ending-screen").classList.remove("hidden");
      }, 1500);
    }
  }

  _setFeedback(text, type) {
    const fb = document.getElementById("modal-feedback-box");
    const txt = document.getElementById("modal-feedback-text");
    fb.className = `feedback-box ${type}`;
    txt.innerText = text;
  }

  _toggleInventory() {
    const invModal = document.getElementById("inventory-modal");
    if (invModal.classList.contains("hidden")) {
      this._renderInventoryList();
      invModal.classList.remove("hidden");
      audioSys.playClick();
    } else {
      invModal.classList.add("hidden");
    }
  }

  _renderInventoryList() {
    const container = document.getElementById("inv-grid-container");
    container.innerHTML = "";

    QUEST_DATA.forEach((q, idx) => {
      const unlocked = idx < this.player.currentQuestIndex;
      const card = document.createElement("div");
      card.className = `inv-card ${unlocked ? 'unlocked' : ''}`;
      card.innerHTML = `
        <div class="inv-card-title">${unlocked ? '★' : '🔒'} Q${q.id}: ${q.topic}</div>
        <div style="color: ${unlocked ? '#91f0d7' : '#a098b8'}; margin: 2px 0;">Progres Pesawat: ${unlocked ? q.reward_item : '(Belum selesai)'}</div>
        <div style="color: #786e8c;">Lokasi: ${q.location}</div>
      `;
      container.appendChild(card);
    });
  }

  _showToast(msg) {
    const toast = document.getElementById("toast-banner");
    toast.innerText = msg;
    toast.classList.remove("hidden");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 4000);
  }

  _updateHUD() {
    const qIndex = Math.min(this.player.currentQuestIndex, 9);
    const q = QUEST_DATA[qIndex];
    document.getElementById("hud-location").innerText = `Quest ${Math.min(this.player.currentQuestIndex + 1, 10)}/10: ${q.location.split('(')[0]}`;
    document.getElementById("hud-inventory-btn").innerText = `🎒 Pesawat: ${this.player.inventory.length}/10 Bagian [TAB]`;
  }

  _closeAllModals() {
    document.getElementById("quest-modal").classList.add("hidden");
    document.getElementById("inventory-modal").classList.add("hidden");
    this.minigameManager.stop();
  }

  _startLoop() {
    let lastTime = performance.now();
    const loop = (now) => {
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;
      this._update(dt);
      this._render();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  _update(dt) {
    if (this._isOverworldActive()) {
      this.player.handleInput(dt, this.keys, this.obstacles);

      // Cek interaksi terdekat
      const allInteractables = [
        ...this.questNPCs,
        ...this.houses,
        ...this.ambientNPCs,
        ...this.scavengerItems.filter(it => !it.isCollected)
      ];

      let nearest = null;
      let minD = 72;
      for (const obj of allInteractables) {
        const d = Math.hypot(this.player.x + 17 - obj.cx, this.player.y + 21 - obj.cy);
        if (d < minD) {
          minD = d;
          nearest = obj;
        }
      }
      this.player.interactTarget = nearest;
      this.camera.update(this.player.x + 17, this.player.y + 21);
    }
  }

  _render() {
    const ctx = this.ctx;
    const cam = this.camera;

    ctx.clearRect(0, 0, 960, 640);

    // 1. Render Peta Open World Pulau (Laut, Pasir Pantai, Rumput, Tebing)
    this._renderTerrain(ctx, cam);

    // 2. Render Rumah-Rumah Warga Desa
    this.houses.forEach(h => h.draw(ctx, cam));

    // 3. Render Pesawat di Alun-Alun Tengah Pulau (Berevolusi!)
    this._renderEvolvingPlane(ctx, cam);

    // 4. Render Item Scavenger Tersebar
    this.scavengerItems.forEach(it => it.draw(ctx, cam));

    // 5. Render NPC Warga Biasa & Master Quest
    this.ambientNPCs.forEach(npc => npc.draw(ctx, cam));
    this.questNPCs.forEach(npc => npc.draw(ctx, cam));

    // 6. Render Karakter Pemain
    this.player.draw(ctx, cam);
  }

  _renderTerrain(ctx, cam) {
    const startCol = Math.max(0, Math.floor(cam.x / TILE_SIZE));
    const endCol = Math.min(MAP_COLS, Math.ceil((cam.x + 960) / TILE_SIZE) + 1);
    const startRow = Math.max(0, Math.floor(cam.y / TILE_SIZE));
    const endRow = Math.min(MAP_ROWS, Math.ceil((cam.y + 640) / TILE_SIZE) + 1);

    const ticks = performance.now();

    for (let c = startCol; c < endCol; c++) {
      for (let r = startRow; r < endRow; r++) {
        const sx = Math.floor(c * TILE_SIZE - cam.x);
        const sy = Math.floor(r * TILE_SIZE - cam.y);

        // Zona Laut Pesisir Luar
        if (c < 3 || c > MAP_COLS - 4 || r < 3 || r > MAP_ROWS - 4) {
          ctx.fillStyle = "#1e2246";
          ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
          // Ombak laut animasi
          if ((c + r) % 3 === 0) {
            const waveY = Math.sin(ticks * 0.003 + c) * 3;
            ctx.fillStyle = "#2d3568";
            ctx.fillRect(sx + 8, sy + 18 + waveY, 28, 4);
          }
        }
        // Pantai Berpasir (Selatan & Barat)
        else if (r > MAP_ROWS - 10 || c < 8) {
          ctx.fillStyle = "#f5e4be";
          ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
          if ((c * 3 + r * 7) % 4 === 0) {
            ctx.fillStyle = "#e6d2a5";
            ctx.fillRect(sx + 10, sy + 10, 4, 4);
          }
        }
        // Tebing Gunung / Gua (Utara)
        else if (r < 10) {
          ctx.fillStyle = "#2d263e";
          ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
          if ((c + r) % 2 === 0) {
            ctx.fillStyle = "#3e3556";
            ctx.fillRect(sx + 12, sy + 12, 10, 10);
          }
        }
        // Danau Teratai Tengah-Utara
        else if (c >= 12 && c <= 18 && r >= 16 && r <= 22) {
          ctx.fillStyle = "#2a4a48";
          ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
          // Teratai
          if (c % 2 === 0 && r % 2 === 0) {
            ctx.fillStyle = "#ffa8cb";
            ctx.beginPath(); ctx.arc(sx + 24, sy + 24, 6, 0, Math.PI * 2); ctx.fill();
          }
        }
        // Desa & Daratan Rumput Pastel
        else {
          ctx.fillStyle = "#3a5548";
          ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
          // Jalan Setapak Batu Menuju Alun-Alun
          if (r === 20 || c === 25 || (c >= 30 && r >= 14 && r <= 28)) {
            ctx.fillStyle = "#4a3c30";
            ctx.fillRect(sx, sy, TILE_SIZE, TILE_SIZE);
            ctx.fillStyle = "#5c4a3c";
            ctx.fillRect(sx + 8, sy + 8, 14, 14);
            ctx.fillRect(sx + 26, sy + 26, 12, 12);
          }
        }
      }
    }
  }

  _renderEvolvingPlane(ctx, cam) {
    const px = Math.floor(this.planeX - cam.x);
    const py = Math.floor(this.planeY - cam.y);
    const stage = Math.min(this.player.currentQuestIndex, 10);

    // Alun-Alun Lantai Batu Pesawat
    ctx.fillStyle = "rgba(45, 38, 62, 0.7)";
    ctx.fillRect(px - 20, py - 10, 5 * TILE_SIZE, 4 * TILE_SIZE);
    ctx.strokeStyle = "#91f0d7";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(px - 20, py - 10, 5 * TILE_SIZE, 4 * TILE_SIZE);

    // 1. Badan Dasar Pesawat
    ctx.fillStyle = stage >= 5 ? "#f5f5fa" : "#8c8296";
    ctx.beginPath();
    ctx.ellipse(px + 90, py + 70, 70, 24, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#1e162d";
    ctx.lineWidth = 2;
    ctx.stroke();

    // 2. Sayap Kiri (Quest >= 1)
    if (stage >= 1) {
      ctx.fillStyle = stage >= 5 ? "#ffa8cb" : "#6e6478";
      ctx.beginPath();
      ctx.moveTo(px + 70, py + 55); ctx.lineTo(px + 40, py + 10); ctx.lineTo(px + 80, py + 55);
      ctx.fill(); ctx.stroke();
    }

    // 3. Baling-Baling Depan (Quest >= 2)
    if (stage >= 2) {
      const propAngle = performance.now() * 0.01;
      ctx.fillStyle = "#ffd75a";
      ctx.beginPath();
      ctx.arc(px + 160, py + 70, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.beginPath();
      ctx.moveTo(px + 160 + Math.cos(propAngle) * 18, py + 70 + Math.sin(propAngle) * 18);
      ctx.lineTo(px + 160 - Math.cos(propAngle) * 18, py + 70 - Math.sin(propAngle) * 18);
      ctx.stroke();
    }

    // 4. Sayap Kanan & Kemudi (Quest >= 4)
    if (stage >= 4) {
      ctx.fillStyle = stage >= 5 ? "#91f0d7" : "#6e6478";
      ctx.beginPath();
      ctx.moveTo(px + 70, py + 85); ctx.lineTo(px + 40, py + 130); ctx.lineTo(px + 80, py + 85);
      ctx.fill(); ctx.stroke();

      // Ekor Kemudi Belakang
      ctx.fillStyle = "#c83246";
      ctx.fillRect(px + 20, py + 52, 18, 20);
    }

    // 5. Radar Kokpit Bercahaya (Quest >= 7)
    if (stage >= 7) {
      ctx.fillStyle = "#64f0a0";
      ctx.beginPath(); ctx.arc(px + 120, py + 66, 7, 0, Math.PI * 2); ctx.fill();
    }

    // 6. Mesin Menyala Bercahaya Penuh (Quest >= 10)
    if (stage >= 10) {
      const glow = Math.sin(performance.now() * 0.008) * 8 + 24;
      ctx.fillStyle = "rgba(100, 240, 160, 0.4)";
      ctx.beginPath(); ctx.arc(px + 90, py + 70, glow + 50, 0, Math.PI * 2); ctx.fill();
    }

    // Papan Status Pesawat
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 11px Space Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(`✈️ PESAWAT ALUN-ALUN (PROGRES: ${stage}/10 BAGIAN)`, px + 90, py + 120);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.gameApp = new GameApp();
});
