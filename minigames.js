/**
 * minigames.js - Engine Mini-Game Aksi Arkade Nyata (Tembak-Tembakan, Lompat Rintangan, dan Lomba Lari)
 */

class MiniGameManager {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.w = this.canvas.width;
    this.h = this.canvas.height;

    this.activeType = null; // 'shooter', 'jumper', 'dash'
    this.isRunning = false;
    this.score = 0;
    this.targetScore = 100;
    this.onCompleteCallback = null;

    this.keys = {};
    this._bindControls();

    // Entitas game internal
    this.entities = {
      player: null,
      bullets: [],
      enemies: [],
      particles: [],
      items: [],
      obstacles: []
    };

    this.spawnTimer = 0;
    this.gameTimer = 0;
  }

  _bindControls() {
    window.addEventListener('keydown', (e) => {
      this.keys[e.code] = true;
    });
    window.addEventListener('keyup', (e) => {
      this.keys[e.code] = false;
    });
  }

  start(gameType, targetScore = 100, onComplete = null) {
    this.activeType = gameType;
    this.targetScore = targetScore;
    this.score = 0;
    this.onCompleteCallback = onComplete;
    this.isRunning = true;
    this.spawnTimer = 0;
    this.gameTimer = 0;

    this.entities = {
      player: { x: this.w / 2, y: this.h - 50, vx: 0, vy: 0, isJumping: false },
      bullets: [],
      enemies: [],
      particles: [],
      items: [],
      obstacles: []
    };

    if (gameType === 'jumper') {
      this.entities.player.x = 80;
      this.entities.player.y = this.h - 60;
      this.entities.player.groundY = this.h - 60;
    } else if (gameType === 'dash') {
      this.entities.player.x = 100;
      this.entities.player.y = this.h / 2;
    }

    this._loop();
  }

  stop() {
    this.isRunning = false;
  }

  _loop() {
    if (!this.isRunning) return;

    this._update(1 / 60);
    this._render();

    requestAnimationFrame(() => this._loop());
  }

  _update(dt) {
    this.gameTimer += dt;
    this.spawnTimer += dt;

    if (this.activeType === 'shooter') {
      this._updateShooter(dt);
    } else if (this.activeType === 'jumper') {
      this._updateJumper(dt);
    } else if (this.activeType === 'dash') {
      this._updateDash(dt);
    }

    // Update partikel ledakan/sparkle
    this.entities.particles = this.entities.particles.filter(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt * 2.0;
      return p.life > 0;
    });

    // Cek Kemenangan Skor
    if (this.score >= this.targetScore && this.isRunning) {
      audioSys.playSuccess();
      this.isRunning = false;
      if (this.onCompleteCallback) {
        this.onCompleteCallback(this.score);
      }
    }
  }

  _addParticles(x, y, color, count = 12) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 60 + Math.random() * 120;
      this.entities.particles.push({
        x: x,
        y: y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 1.0,
        color: color,
        r: 2 + Math.random() * 3
      });
    }
  }

  // -------------------------------------------------------------
  // 1. MINIGAME: BUG BLASTER (TEMBAK-TEMBAKAN ARKADE)
  // -------------------------------------------------------------
  _updateShooter(dt) {
    const p = this.entities.player;
    const spd = 260;

    // Gerak Kiri / Kanan
    if (this.keys['KeyA'] || this.keys['ArrowLeft']) p.x -= spd * dt;
    if (this.keys['KeyD'] || this.keys['ArrowRight']) p.x += spd * dt;
    p.x = Math.max(30, Math.min(p.x, this.w - 30));

    // Menembak Laser (Spasi / Panah Atas)
    if ((this.keys['Space'] || this.keys['ArrowUp'] || this.keys['KeyW']) && (!p.lastShoot || performance.now() - p.lastShoot > 220)) {
      p.lastShoot = performance.now();
      this.entities.bullets.push({ x: p.x - 8, y: p.y - 12, vy: -450 });
      this.entities.bullets.push({ x: p.x + 8, y: p.y - 12, vy: -450 });
      audioSys.playLaser();
    }

    // Update Peluru
    this.entities.bullets.forEach(b => b.y += b.vy * dt);
    this.entities.bullets = this.entities.bullets.filter(b => b.y > -20);

    // Spawn Musuh Bug Sintaks
    if (this.spawnTimer >= 0.7) {
      this.spawnTimer = 0;
      const ex = 40 + Math.random() * (this.w - 80);
      const bugType = Math.random() > 0.4 ? 'basic' : 'fast';
      this.entities.enemies.push({
        x: ex,
        y: -30,
        vy: bugType === 'fast' ? 140 : 85,
        type: bugType,
        hp: bugType === 'fast' ? 1 : 2,
        r: 16
      });
    }

    // Update Musuh & Deteksi Tabrakan Peluru
    this.entities.enemies.forEach(e => e.y += e.vy * dt);

    for (let bi = this.entities.bullets.length - 1; bi >= 0; bi--) {
      const b = this.entities.bullets[bi];
      for (let ei = this.entities.enemies.length - 1; ei >= 0; ei--) {
        const e = this.entities.enemies[ei];
        if (Math.hypot(b.x - e.x, b.y - e.y) < e.r + 6) {
          e.hp--;
          this.entities.bullets.splice(bi, 1);
          if (e.hp <= 0) {
            this.entities.enemies.splice(ei, 1);
            this.score += 20;
            this._addParticles(e.x, e.y, '#91f0d7', 16);
            audioSys.playExplosion();
          } else {
            this._addParticles(b.x, b.y, '#ffa8cb', 6);
          }
          break;
        }
      }
    }

    this.entities.enemies = this.entities.enemies.filter(e => e.y < this.h + 40);
  }

  // -------------------------------------------------------------
  // 2. MINIGAME: DREAM JUMPER (LOMPAT RINTANGAN PLATFORMER)
  // -------------------------------------------------------------
  _updateJumper(dt) {
    const p = this.entities.player;
    const gravity = 880;

    // Tombol Lompat
    if ((this.keys['Space'] || this.keys['ArrowUp'] || this.keys['KeyW']) && !p.isJumping) {
      p.vy = -420;
      p.isJumping = true;
      audioSys.playJump();
    }

    // Gravitasi
    p.vy += gravity * dt;
    p.y += p.vy * dt;

    // Mendarat di Tanah
    if (p.y >= p.groundY) {
      p.y = p.groundY;
      p.vy = 0;
      p.isJumping = false;
    }

    // Spawn Rintangan Duri & Kristal Bintang
    if (this.spawnTimer >= 1.2) {
      this.spawnTimer = 0;
      // Tambah rintangan
      this.entities.obstacles.push({
        x: this.w + 40,
        y: this.h - 60,
        w: 24,
        h: 30,
        vx: -220
      });

      // Tambah bintang kristal di udara
      this.entities.items.push({
        x: this.w + 90,
        y: this.h - 130 - Math.random() * 40,
        r: 10,
        vx: -220
      });
    }

    // Gerakkan Rintangan & Item
    this.entities.obstacles.forEach(ob => ob.x += ob.vx * dt);
    this.entities.items.forEach(it => it.x += it.vx * dt);

    // Deteksi Ambil Kristal
    for (let ii = this.entities.items.length - 1; ii >= 0; ii--) {
      const it = this.entities.items[ii];
      if (Math.hypot(p.x - it.x, (p.y - 15) - it.y) < it.r + 20) {
        this.score += 25;
        this._addParticles(it.x, it.y, '#fff0b4', 12);
        this.entities.items.splice(ii, 1);
        audioSys.playPickup();
      }
    }

    // Deteksi Terkena Duri (Kurangi sedikit skor tapi lanjut bermain)
    for (const ob of this.entities.obstacles) {
      if (p.x > ob.x && p.x < ob.x + ob.w && p.y > ob.y - ob.h) {
        if (!p.invincibleTimer || performance.now() - p.invincibleTimer > 1000) {
          p.invincibleTimer = performance.now();
          this.score = Math.max(0, this.score - 10);
          this._addParticles(p.x, p.y, '#ff6e82', 15);
          audioSys.playError();
        }
      }
    }

    this.entities.obstacles = this.entities.obstacles.filter(ob => ob.x > -50);
    this.entities.items = this.entities.items.filter(it => it.x > -50);
  }

  // -------------------------------------------------------------
  // 3. MINIGAME: ISLAND DASH (LOMBA LARI SPRINT OBSTACLE)
  // -------------------------------------------------------------
  _updateDash(dt) {
    const p = this.entities.player;
    const spd = 240;

    if (this.keys['KeyW'] || this.keys['ArrowUp']) p.y -= spd * dt;
    if (this.keys['KeyS'] || this.keys['ArrowDown']) p.y += spd * dt;
    p.y = Math.max(40, Math.min(p.y, this.h - 60));

    // Spawn Booster Energi & Lumpur
    if (this.spawnTimer >= 0.8) {
      this.spawnTimer = 0;
      const isBooster = Math.random() > 0.4;
      if (isBooster) {
        this.entities.items.push({
          x: this.w + 30,
          y: 60 + Math.random() * (this.h - 120),
          r: 12,
          vx: -260,
          type: 'booster'
        });
      } else {
        this.entities.obstacles.push({
          x: this.w + 30,
          y: 60 + Math.random() * (this.h - 120),
          w: 30,
          h: 30,
          vx: -260
        });
      }
    }

    this.entities.items.forEach(it => it.x += it.vx * dt);
    this.entities.obstacles.forEach(ob => ob.x += ob.vx * dt);

    // Ambil booster
    for (let ii = this.entities.items.length - 1; ii >= 0; ii--) {
      const it = this.entities.items[ii];
      if (Math.hypot(p.x - it.x, p.y - it.y) < it.r + 18) {
        this.score += 25;
        this._addParticles(it.x, it.y, '#91f0d7', 14);
        this.entities.items.splice(ii, 1);
        audioSys.playPickup();
      }
    }

    this.entities.items = this.entities.items.filter(it => it.x > -40);
    this.entities.obstacles = this.entities.obstacles.filter(ob => ob.x > -40);
  }

  // -------------------------------------------------------------
  // RENDER GRAPHICS
  // -------------------------------------------------------------
  _render() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.w, this.h);

    // Background Arena
    ctx.fillStyle = '#100c1e';
    ctx.fillRect(0, 0, this.w, this.h);

    // Grid Garis Retrowave
    ctx.strokeStyle = 'rgba(75, 62, 105, 0.3)';
    ctx.lineWidth = 1;
    for (let x = 0; x < this.w; x += 32) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, this.h); ctx.stroke();
    }
    for (let y = 0; y < this.h; y += 32) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(this.w, y); ctx.stroke();
    }

    // 1. Render Spesifik Game
    if (this.activeType === 'shooter') {
      this._renderShooter(ctx);
    } else if (this.activeType === 'jumper') {
      this._renderJumper(ctx);
    } else if (this.activeType === 'dash') {
      this._renderDash(ctx);
    }

    // 2. Render Partikel
    for (const p of this.entities.particles) {
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.life;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1.0;

    // 3. Render Top HUD Bar Arkade
    ctx.fillStyle = 'rgba(24, 18, 40, 0.9)';
    ctx.fillRect(10, 10, this.w - 20, 36);
    ctx.strokeStyle = '#af91e1';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(10, 10, this.w - 20, 36);

    ctx.fillStyle = '#fff0b4';
    ctx.font = 'bold 14px Space Mono, monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`🎯 TARGET SKOR: ${this.targetScore} POIN`, 24, 33);

    ctx.fillStyle = this.score >= this.targetScore ? '#64f0a0' : '#91f0d7';
    ctx.textAlign = 'right';
    ctx.fillText(`SKOR ANDA: ${this.score} POIN`, this.w - 24, 33);
  }

  _renderShooter(ctx) {
    const p = this.entities.player;

    // Render Kapal Pemain
    ctx.fillStyle = '#f8f8fc';
    ctx.beginPath();
    ctx.moveTo(p.x, p.y - 18);
    ctx.lineTo(p.x - 18, p.y + 14);
    ctx.lineTo(p.x, p.y + 6);
    ctx.lineTo(p.x + 18, p.y + 14);
    ctx.fill();

    ctx.fillStyle = '#ffa8cb';
    ctx.fillRect(p.x - 4, p.y - 6, 8, 12);

    // Render Peluru Laser
    ctx.fillStyle = '#91f0d7';
    for (const b of this.entities.bullets) {
      ctx.fillRect(b.x - 2, b.y, 4, 14);
    }

    // Render Musuh Bug Sintaks
    for (const e of this.entities.enemies) {
      ctx.fillStyle = e.type === 'fast' ? '#ff6e82' : '#af91e1';
      ctx.beginPath();
      ctx.arc(e.x, e.y, e.r, 0, Math.PI * 2);
      ctx.fill();

      // Mata Bug
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(e.x - 6, e.y - 4, 4, 4);
      ctx.fillRect(e.x + 2, e.y - 4, 4, 4);
      ctx.fillStyle = '#140e24';
      ctx.fillRect(e.x - 5, e.y - 3, 2, 2);
      ctx.fillRect(e.x + 3, e.y - 3, 2, 2);
    }
  }

  _renderJumper(ctx) {
    const p = this.entities.player;

    // Lantai
    ctx.fillStyle = '#3a5548';
    ctx.fillRect(0, this.h - 40, this.w, 40);
    ctx.fillStyle = '#91e1b9';
    ctx.fillRect(0, this.h - 40, this.w, 4);

    // Karakter Omori Jumper
    ctx.fillStyle = '#f8f8fc';
    ctx.fillRect(p.x - 12, p.y - 30, 24, 30);
    ctx.fillStyle = '#141020';
    ctx.fillRect(p.x - 14, p.y - 32, 28, 10);
    ctx.fillStyle = '#141020';
    ctx.fillRect(p.x - 6, p.y - 22, 4, 4);
    ctx.fillRect(p.x + 2, p.y - 22, 4, 4);

    // Rintangan Duri
    ctx.fillStyle = '#ff6e82';
    for (const ob of this.entities.obstacles) {
      ctx.beginPath();
      ctx.moveTo(ob.x, ob.y + 20);
      ctx.lineTo(ob.x + ob.w / 2, ob.y - ob.h + 20);
      ctx.lineTo(ob.x + ob.w, ob.y + 20);
      ctx.fill();
    }

    // Kristal Bintang
    for (const it of this.entities.items) {
      ctx.fillStyle = '#fff0b4';
      ctx.beginPath();
      ctx.arc(it.x, it.y, it.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#ffa8cb';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  _renderDash(ctx) {
    const p = this.entities.player;

    // Karakter Dash
    ctx.fillStyle = '#91f0d7';
    ctx.beginPath();
    ctx.arc(p.x, p.y, 16, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#140e24';
    ctx.fillRect(p.x + 4, p.y - 4, 4, 4);

    // Booster
    for (const it of this.entities.items) {
      ctx.fillStyle = '#ffa8cb';
      ctx.beginPath();
      ctx.arc(it.x, it.y, it.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.fillText('⚡', it.x - 5, it.y + 4);
    }

    // Lumpur Rintangan
    ctx.fillStyle = '#553c28';
    for (const ob of this.entities.obstacles) {
      ctx.beginPath();
      ctx.ellipse(ob.x + ob.w / 2, ob.y + ob.h / 2, ob.w / 2, ob.h / 2, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
