/**
 * game3d.js - Engine 3D WebGL Open-World Island RPG (Three.js)
 * Menghadirkan Peta Pulau 3D Luas, Karakter & Kamera 3D Third-Person, Pesawat 3D Berevolusi di Tengah Pulau,
 * Rumah 3D Interaktif, NPC 3D, Hutan & Tebing 3D, serta Integrasi 10 Quest Python & Minigame Arkade.
 */

class GameApp3D {
  constructor() {
    this.canvas = document.getElementById("game-canvas");
    this.scene = null;
    this.camera = null;
    this.renderer = null;

    // Entitas 3D
    this.player = null;
    this.playerMesh = null;
    this.airplaneGroup = null;
    this.airplaneParts = {};
    this.houses = [];
    this.questNPCs = [];
    this.ambientNPCs = [];
    this.scavengerItems = [];
    this.colliders = [];

    // State Game
    this.keys = {};
    this.currentQuestIndex = 0;
    this.activeQuest = null;
    this.inventory = [];
    this.scavengerCollected = 0;
    this.nearestInteractable = null;

    this.minigameManager = new MiniGameManager("minigame-canvas");

    this.introTexts = [
      "Badai petir menyambar pesawatmu dan kamu terdampar di Pulau Sintaksis 3D!",
      "Pesawatmu yang rusak tergeletak di tengah alun-alun pulau...",
      "Jelajahi pantai pasir, danau, hutan lebat, tebing gua, dan desa perkampungan warga 3D.",
      "Kumpulkan suku cadang, selesaikan quest Python & mini-game aksi untuk memperbaiki pesawat!",
      "Ayo perbaiki pesawat sedikit demi sedikit dan terbang bebas pulang!"
    ];
    this.introStep = 0;

    this._initThree();
    this._build3DWorld();
    this._bindEvents();
    this._animate();
  }

  _initThree() {
    // 1. Scene dengan Kabut Senja OMORI
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x181228);
    this.scene.fog = new THREE.FogExp2(0x181228, 0.008);

    // 2. Kamera 3D Perspektif
    const aspect = this.canvas.clientWidth / this.canvas.clientHeight || 960 / 640;
    this.camera = new THREE.PerspectiveCamera(55, aspect, 0.1, 1000);
    this.camera.position.set(0, 25, 35);

    // 3. WebGL Renderer dengan Shadow Mapping
    this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
    this.renderer.setSize(960, 640);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // 4. Pencahayaan Dinamis
    const ambientLight = new THREE.AmbientLight(0x786095, 0.9);
    this.scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xffecd0, 1.3);
    sunLight.position.set(60, 100, 50);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 250;
    sunLight.shadow.camera.left = -90;
    sunLight.shadow.camera.right = 90;
    sunLight.shadow.camera.top = 90;
    sunLight.shadow.camera.bottom = -90;
    this.scene.add(sunLight);

    // Lampu Aksen Alun-Alun Tengah
    const plazaLight = new THREE.PointLight(0x91f0d7, 1.2, 45);
    plazaLight.position.set(0, 8, 0);
    this.scene.add(plazaLight);
  }

  _build3DWorld() {
    // 1. Daratan Pulau 3D (Island Mesh)
    const islandGeo = new THREE.CylinderGeometry(85, 95, 6, 32);
    const islandMat = new THREE.MeshLambertMaterial({ color: 0x3a5548 }); // Rumput hijau pastel
    const islandMesh = new THREE.Mesh(islandGeo, islandMat);
    islandMesh.position.y = -3;
    islandMesh.receiveShadow = true;
    this.scene.add(islandMesh);

    // Pesisir Pantai Pasir 3D di Luar
    const beachGeo = new THREE.RingGeometry(80, 115, 32);
    const beachMat = new THREE.MeshLambertMaterial({ color: 0xf5e4be, side: THREE.DoubleSide });
    const beachMesh = new THREE.Mesh(beachGeo, beachMat);
    beachMesh.rotation.x = -Math.PI / 2;
    beachMesh.position.y = 0.05;
    beachMesh.receiveShadow = true;
    this.scene.add(beachMesh);

    // Lautan Samudra 3D
    const oceanGeo = new THREE.PlaneGeometry(500, 500);
    const oceanMat = new THREE.MeshLambertMaterial({ color: 0x1a2046, transparent: true, opacity: 0.85 });
    const oceanMesh = new THREE.Mesh(oceanGeo, oceanMat);
    oceanMesh.rotation.x = -Math.PI / 2;
    oceanMesh.position.y = -1;
    this.scene.add(oceanMesh);

    // Tebing Pegunungan 3D di Utara
    for (let i = 0; i < 8; i++) {
      const rockGeo = new THREE.DodecahedronGeometry(8 + Math.random() * 6);
      const rockMat = new THREE.MeshLambertMaterial({ color: 0x2d263e });
      const rock = new THREE.Mesh(rockGeo, rockMat);
      rock.position.set(-35 + i * 10, 4 + Math.random() * 3, -55 + (i % 2) * 8);
      rock.castShadow = true;
      rock.receiveShadow = true;
      this.scene.add(rock);
      this.colliders.push({ x: rock.position.x, z: rock.position.z, r: 8 });
    }

    // Danau Teratai 3D di Barat Laut
    const lakeGeo = new THREE.CircleGeometry(14, 24);
    const lakeMat = new THREE.MeshLambertMaterial({ color: 0x2a4e55, transparent: true, opacity: 0.9 });
    const lakeMesh = new THREE.Mesh(lakeGeo, lakeMat);
    lakeMesh.rotation.x = -Math.PI / 2;
    lakeMesh.position.set(-35, 0.08, -15);
    this.scene.add(lakeMesh);

    // 2. Bangun Pesawat Rusak 3D di Tengah Alun-Alun (Berevolusi!)
    this._build3DPlane();

    // 3. Bangun 5 Rumah Warga Desa 3D di Area Timur
    this._build3DVillage();

    // 4. Bangun Pepohonan 3D & Bunga Surealis
    this._build3DVegetation();

    // 5. Bangun Karakter Pemain 3D (OMORI)
    this._build3DPlayer();

    // 6. Tempatkan 10 NPC Quest Masters 3D & 5 Ambient NPCs 3D
    this._build3DNPCs();

    // 7. Tempatkan Item Scavenger 3D
    this._build3DScavengerItems();
  }

  // --- MODEL PESAWAT 3D BEREVOLUSI ---
  _build3DPlane() {
    this.airplaneGroup = new THREE.Group();
    this.airplaneGroup.position.set(0, 1.8, 0);

    // Badan Utama Pesawat (Fuselage)
    const bodyGeo = new THREE.CylinderGeometry(2.2, 2.5, 14, 16);
    bodyGeo.rotateZ(Math.PI / 2);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0x888095 });
    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
    bodyMesh.castShadow = true;
    this.airplaneGroup.add(bodyMesh);
    this.airplaneParts.body = bodyMesh;

    // Kokpit Kaca Transparan
    const glassGeo = new THREE.SphereGeometry(2, 16, 16);
    const glassMat = new THREE.MeshLambertMaterial({ color: 0x91f0d7, transparent: true, opacity: 0.7 });
    const glassMesh = new THREE.Mesh(glassGeo, glassMat);
    glassMesh.position.set(2, 1.2, 0);
    glassMesh.scale.set(1.5, 0.8, 0.9);
    this.airplaneGroup.add(glassMesh);

    // Sayap Kiri 3D (Quest >= 1)
    const wingGeo = new THREE.BoxGeometry(4, 0.3, 12);
    const wingMat = new THREE.MeshLambertMaterial({ color: 0xffa8cb });
    const leftWing = new THREE.Mesh(wingGeo, wingMat);
    leftWing.position.set(0, 0.2, 7);
    leftWing.castShadow = true;
    leftWing.visible = false;
    this.airplaneGroup.add(leftWing);
    this.airplaneParts.leftWing = leftWing;

    // Baling-Baling Depan 3D (Quest >= 2)
    const propGroup = new THREE.Group();
    propGroup.position.set(7.2, 0, 0);
    const propHubGeo = new THREE.SphereGeometry(0.8, 12, 12);
    const propHubMat = new THREE.MeshLambertMaterial({ color: 0xffd75a });
    const propHub = new THREE.Mesh(propHubGeo, propHubMat);
    propGroup.add(propHub);

    const bladeGeo = new THREE.BoxGeometry(0.1, 4.5, 0.6);
    const bladeMat = new THREE.MeshLambertMaterial({ color: 0xf8f8fc });
    const blade1 = new THREE.Mesh(bladeGeo, bladeMat);
    const blade2 = new THREE.Mesh(bladeGeo, bladeMat);
    blade2.rotation.x = Math.PI / 2;
    propGroup.add(blade1);
    propGroup.add(blade2);
    propGroup.visible = false;
    this.airplaneGroup.add(propGroup);
    this.airplaneParts.propeller = propGroup;

    // Sayap Kanan & Ekor 3D (Quest >= 4)
    const rightWing = new THREE.Mesh(wingGeo, wingMat);
    rightWing.position.set(0, 0.2, -7);
    rightWing.castShadow = true;
    rightWing.visible = false;
    this.airplaneGroup.add(rightWing);
    this.airplaneParts.rightWing = rightWing;

    const tailGeo = new THREE.BoxGeometry(2.5, 3.5, 0.4);
    const tailMat = new THREE.MeshLambertMaterial({ color: 0xc83246 });
    const tailMesh = new THREE.Mesh(tailGeo, tailMat);
    tailMesh.position.set(-6, 2.5, 0);
    tailMesh.castShadow = true;
    tailMesh.visible = false;
    this.airplaneGroup.add(tailMesh);
    this.airplaneParts.tail = tailMesh;

    // Radar Kokpit Bercahaya (Quest >= 7)
    const radarGeo = new THREE.CylinderGeometry(0.8, 0.8, 0.4, 12);
    const radarMat = new THREE.MeshLambertMaterial({ color: 0x64f0a0 });
    const radarMesh = new THREE.Mesh(radarGeo, radarMat);
    radarMesh.position.set(3.5, 2.2, 0);
    radarMesh.visible = false;
    this.airplaneGroup.add(radarMesh);
    this.airplaneParts.radar = radarMesh;

    // Mesin Turbo Bercahaya (Quest >= 10)
    const engineGlowGeo = new THREE.SphereGeometry(3.5, 16, 16);
    const engineGlowMat = new THREE.MeshBasicMaterial({ color: 0x91f0d7, transparent: true, opacity: 0.4 });
    const engineGlow = new THREE.Mesh(engineGlowGeo, engineGlowMat);
    engineGlow.position.set(-3, 0, 0);
    engineGlow.visible = false;
    this.airplaneGroup.add(engineGlow);
    this.airplaneParts.engineGlow = engineGlow;

    this.scene.add(this.airplaneGroup);
    this.colliders.push({ x: 0, z: 0, r: 8 });
  }

  // --- RUMAH WARGA DESA 3D ---
  _build3DVillage() {
    const houseConfigs = [
      { x: 35, z: -15, name: "Kios Pedagang Topeng Bulan", msg: "Selamat datang di Kios Memori! Onderdil radar tersedia di sini.", col: 0xffd78c },
      { x: 50, z: -15, name: "Rumah Mori Si Kerang", msg: "Mori: 'Pantai di selatan sangat damai. Jangan lupa fungsi print!'", col: 0xffa8cb },
      { x: 35, z: 15, name: "Perpustakaan Mantra Kuno", msg: "Buku: 'Fungsi def adalah formula membungkus logika sakti.'", col: 0x91f0d7 },
      { x: 50, z: 15, name: "Bengkel Mekanik Lavender", msg: "Pandai Besi: 'Semua sayap dan baut pesawat siap dipasang!'", col: 0xaf91e1 },
      { x: 42, z: 32, name: "Kincir Angin Waktu", msg: "Penjaga: 'Putaran waktu di pulau ini mengikuti ritme for loop.'", col: 0xffbedc }
    ];

    houseConfigs.forEach(h => {
      const group = new THREE.Group();
      group.position.set(h.x, 0, h.z);

      // Dinding Rumah 3D
      const wallGeo = new THREE.BoxGeometry(9, 6, 8);
      const wallMat = new THREE.MeshLambertMaterial({ color: 0x251e38 });
      const wall = new THREE.Mesh(wallGeo, wallMat);
      wall.position.y = 3;
      wall.castShadow = true;
      wall.receiveShadow = true;
      group.add(wall);

      // Atap Segitiga 3D
      const roofGeo = new THREE.ConeGeometry(7.5, 4.5, 4);
      roofGeo.rotateY(Math.PI / 4);
      const roofMat = new THREE.MeshLambertMaterial({ color: h.col });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.y = 8.2;
      roof.castShadow = true;
      group.add(roof);

      // Pintu Kayu 3D
      const doorGeo = new THREE.BoxGeometry(2, 3.5, 0.3);
      const doorMat = new THREE.MeshLambertMaterial({ color: 0x6e4b32 });
      const door = new THREE.Mesh(doorGeo, doorMat);
      door.position.set(0, 1.75, 4.1);
      group.add(door);

      this.scene.add(group);
      this.houses.push({ x: h.x, z: h.z, name: h.name, msg: h.msg, prompt: "[E] Ketuk " + h.name });
      this.colliders.push({ x: h.x, z: h.z, r: 6 });
    });
  }

  // --- PEPOHONAN & VEGETASI 3D ---
  _build3DVegetation() {
    // 30+ Pohon Pastel di Hutan Barat Laut
    for (let i = 0; i < 35; i++) {
      const tx = -20 - Math.random() * 45;
      const tz = 25 - Math.random() * 65;

      const treeGroup = new THREE.Group();
      treeGroup.position.set(tx, 0, tz);

      // Batang Cokelat
      const trunkGeo = new THREE.CylinderGeometry(0.8, 1.1, 4, 8);
      const trunkMat = new THREE.MeshLambertMaterial({ color: 0x463228 });
      const trunk = new THREE.Mesh(trunkGeo, trunkMat);
      trunk.position.y = 2;
      trunk.castShadow = true;
      treeGroup.add(trunk);

      // Dedaunan Berlapis (Pastel Mint & Purple)
      const leafColor = Math.random() > 0.5 ? 0x5ab48c : 0x8c6ebe;
      const leavesGeo = new THREE.ConeGeometry(3.5, 6, 8);
      const leavesMat = new THREE.MeshLambertMaterial({ color: leafColor });
      const leaves = new THREE.Mesh(leavesGeo, leavesMat);
      leaves.position.y = 6;
      leaves.castShadow = true;
      treeGroup.add(leaves);

      this.scene.add(treeGroup);
      this.colliders.push({ x: tx, z: tz, r: 2.5 });
    }

    // Dermaga Kayu 3D di Selatan-Timur
    const pierGeo = new THREE.BoxGeometry(8, 0.6, 32);
    const pierMat = new THREE.MeshLambertMaterial({ color: 0x6e4b32 });
    const pier = new THREE.Mesh(pierGeo, pierMat);
    pier.position.set(25, 0.4, 65);
    pier.receiveShadow = true;
    this.scene.add(pier);
  }

  // --- MODEL KARAKTER PEMAIN 3D (OMORI) ---
  _build3DPlayer() {
    this.playerMesh = new THREE.Group();
    this.playerMesh.position.set(0, 0, 18);

    // Badan & Baju Rompi
    const bodyGeo = new THREE.CylinderGeometry(0.9, 0.8, 2.2, 12);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0xf5f5fa });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 2;
    body.castShadow = true;
    this.playerMesh.add(body);

    // Kepala Kulit Pucat
    const headGeo = new THREE.SphereGeometry(1.2, 16, 16);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xfcf8f2 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 3.8;
    head.castShadow = true;
    this.playerMesh.add(head);

    // Rambut Hitam Berantakan khas OMORI
    const hairGeo = new THREE.SphereGeometry(1.3, 16, 16);
    const hairMat = new THREE.MeshLambertMaterial({ color: 0x141020 });
    const hair = new THREE.Mesh(hairGeo, hairMat);
    hair.position.set(0, 4.1, -0.2);
    hair.scale.set(1.05, 1.05, 1.05);
    this.playerMesh.add(hair);

    // Mata Hitam Melankolis
    const eyeGeo = new THREE.SphereGeometry(0.18, 8, 8);
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0x140e20 });
    const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
    leftEye.position.set(-0.4, 3.8, 1.1);
    const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
    rightEye.position.set(0.4, 3.8, 1.1);
    this.playerMesh.add(leftEye);
    this.playerMesh.add(rightEye);

    // Kaki
    const legGeo = new THREE.CylinderGeometry(0.3, 0.3, 1.4, 8);
    const legMat = new THREE.MeshLambertMaterial({ color: 0x1a1626 });
    this.leftLeg = new THREE.Mesh(legGeo, legMat);
    this.leftLeg.position.set(-0.45, 0.7, 0);
    this.rightLeg = new THREE.Mesh(legGeo, legMat);
    this.rightLeg.position.set(0.45, 0.7, 0);
    this.playerMesh.add(this.leftLeg);
    this.playerMesh.add(this.rightLeg);

    this.scene.add(this.playerMesh);
  }

  // --- NPC 3D QUEST MASTERS & WARGA DESA ---
  _build3DNPCs() {
    const qPositions = [
      { qid: 1, x: -15, z: 45, col: 0xffa8cb },  // Pantai Selatan
      { qid: 2, x: -45, z: -25, col: 0x5ab48c }, // Hutan Barat Laut
      { qid: 3, x: 0, z: -48, col: 0x8c6ebe },   // Tebing Gua Utara
      { qid: 4, x: -35, z: -5, col: 0x6ebe78 },  // Danau Teratai
      { qid: 5, x: 15, z: 42, col: 0xf082aa },   // Taman Bunga
      { qid: 6, x: 42, z: -35, col: 0xe6d7f5 },  // Lembah Timur Laut
      { qid: 7, x: 32, z: 0, col: 0xffd75a },    // Pasar Desa
      { qid: 8, x: -55, z: 15, col: 0xffd782 },  // Menara Waktu Barat
      { qid: 9, x: -18, z: -38, col: 0xd2e6ff }, // Kuil Mantra Kuno
      { qid: 10, x: 0, z: 10, col: 0xa06e50 }    // Alun-Alun Pesawat
    ];

    qPositions.forEach(p => {
      const q = QUEST_DATA[p.qid - 1];
      const npcGroup = new THREE.Group();
      npcGroup.position.set(p.x, 0, p.z);

      // Tubuh NPC 3D
      const bodyGeo = new THREE.SphereGeometry(1.6, 16, 16);
      const bodyMat = new THREE.MeshLambertMaterial({ color: p.col });
      const body = new THREE.Mesh(bodyGeo, bodyMat);
      body.position.y = 2.4;
      body.castShadow = true;
      npcGroup.add(body);

      // Simbol Seru Bercahaya di Atas Kepala NPC
      const markerGeo = new THREE.OctahedronGeometry(0.8);
      const markerMat = new THREE.MeshBasicMaterial({ color: 0xffd75a });
      const marker = new THREE.Mesh(markerGeo, markerMat);
      marker.position.y = 5.2;
      npcGroup.add(marker);

      this.scene.add(npcGroup);
      this.questNPCs.push({
        questId: p.qid,
        x: p.x,
        z: p.z,
        name: q.npc_name,
        prompt: `[E] Bicara ke ${q.npc_name} (Quest ${p.qid})`,
        mesh: npcGroup
      });
      this.colliders.push({ x: p.x, z: p.z, r: 3 });
    });

    // Warga Desa Biasa 3D
    const townsfolk = [
      { x: 30, z: 8, name: "Bocah Topi Jerami", dialog: "Pesawat di tengah alun-alun itu semakin keren setiap hari!", col: 0xffa8cb },
      { x: -5, z: 42, name: "Gadis Payung Pastel", dialog: "Ombak pantai berbusa ungu hari ini sangat menenangkan hati.", col: 0x91f0d7 },
      { x: 25, z: 62, name: "Kakek Pemancing Bulan", dialog: "Dermaga kayu adalah tempat terbaik memandang matahari terbenam.", col: 0xffd78c },
      { x: -28, z: 10, name: "Sprout Mole Surealis", dialog: "Toge... toge... Hutan barat menyimpan kristal data yang bersinar!", col: 0x8ce696 }
    ];

    townsfolk.forEach(t => {
      const g = new THREE.Group();
      g.position.set(t.x, 0, t.z);
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 2.2, 10), new THREE.MeshLambertMaterial({ color: t.col }));
      m.position.y = 1.4;
      m.castShadow = true;
      g.add(m);

      this.scene.add(g);
      this.ambientNPCs.push({ x: t.x, z: t.z, name: t.name, dialog: t.dialog, prompt: `[E] Sapa ${t.name}` });
      this.colliders.push({ x: t.x, z: t.z, r: 2 });
    });
  }

  // --- ITEM SCAVENGER 3D MELAYANG & BERPUTAR ---
  _build3DScavengerItems() {
    const itemCoords = [
      { id: 1, x: -32, z: -20, name: "Kristal Data String", col: 0x91f0d7 },
      { id: 2, x: -48, z: -35, name: "Kristal Data Integer", col: 0xffa8cb },
      { id: 3, x: -25, z: -40, name: "Kristal Data Boolean", col: 0xfff0b4 },
      { id: 4, x: 38, z: -28, name: "Roda Gigi Kronos", col: 0xffd75a },
      { id: 5, x: 45, z: -42, name: "Baut Sayap Baja", col: 0xaf91e1 },
      { id: 6, x: 28, z: -35, name: "Kabel Turbin Emas", col: 0xffa8cb },
      { id: 7, x: 48, z: 8, name: "Mur Pengunci Kemudi", col: 0x91f0d7 }
    ];

    itemCoords.forEach(it => {
      const mesh = new THREE.Mesh(
        new THREE.OctahedronGeometry(1.2),
        new THREE.MeshBasicMaterial({ color: it.col, wireframe: false })
      );
      mesh.position.set(it.x, 2, it.z);
      this.scene.add(mesh);
      this.scavengerItems.push({
        id: it.id,
        x: it.x,
        z: it.z,
        name: it.name,
        mesh: mesh,
        collected: false,
        prompt: `[E] Ambil ${it.name}`
      });
    });
  }

  _bindEvents() {
    window.addEventListener("keydown", (e) => {
      this.keys[e.code] = true;

      if (e.code === "Enter" && !document.getElementById("title-screen").classList.contains("hidden")) {
        this._startGame();
      }
      if ((e.code === "Space" || e.code === "Enter") && !document.getElementById("intro-screen").classList.contains("hidden")) {
        this._nextIntro();
      }
      if (e.code === "KeyE" || e.code === "Space") {
        if (this._isOverworldActive()) {
          this._handleInteraction();
        }
      }
      if (e.code === "KeyI" || e.code === "Tab") {
        if (this._isOverworldActive() || !document.getElementById("inventory-modal").classList.contains("hidden")) {
          e.preventDefault();
          this._toggleInventory();
        }
      }
      if (e.code === "Escape") {
        this._closeModals();
      }
    });

    window.addEventListener("keyup", (e) => {
      this.keys[e.code] = false;
    });

    // Buttons
    document.getElementById("btn-start-game").onclick = () => this._startGame();
    document.getElementById("btn-next-intro").onclick = () => this._nextIntro();
    document.getElementById("btn-close-quest").onclick = () => this._closeModals();
    document.getElementById("btn-reset-code").onclick = () => this._resetCode();
    document.getElementById("btn-quest-hint").onclick = () => this._showHint();
    document.getElementById("btn-submit-code").onclick = () => this._submitQuest();

    document.getElementById("hud-inventory-btn").onclick = () => this._toggleInventory();
    document.getElementById("btn-close-inventory").onclick = () => this._closeModals();
    document.getElementById("btn-close-inv-bottom").onclick = () => this._closeModals();
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

  _startGame() {
    audioSys.playSuccess();
    document.getElementById("title-screen").classList.add("hidden");
    document.getElementById("intro-screen").classList.remove("hidden");
    this.introStep = 0;
    this._showIntroText();
  }

  _showIntroText() {
    document.getElementById("intro-header-text").innerText = `PROLOGUE : Terdampar di Pulau Sintaksis (${this.introStep + 1}/${this.introTexts.length})`;
    document.getElementById("intro-body-text").innerText = this.introTexts[this.introStep];
    audioSys.playBlip("mid");
  }

  _nextIntro() {
    this.introStep++;
    if (this.introStep < this.introTexts.length) {
      this._showIntroText();
      audioSys.playClick();
    } else {
      document.getElementById("intro-screen").classList.add("hidden");
      this._showToast("Jelajahi Pulau 3D! Temui Mori di Pantai Selatan atau periksa Pesawat di tengah.");
      audioSys.playPickup();
    }
  }

  _handleInteraction() {
    const target = this.nearestInteractable;
    if (!target) return;

    if (target.questId) {
      this._openQuestModal(target.questId - 1);
    } else if (target.msg) {
      this._showToast(`🚪 [${target.name}]: "${target.msg}"`);
      audioSys.playClick();
    } else if (target.dialog) {
      this._showToast(`💬 [${target.name}]: "${target.dialog}"`);
      audioSys.playBlip("high");
    } else if (target.collected === false) {
      target.collected = true;
      target.mesh.visible = false;
      this.scavengerCollected++;
      audioSys.playPickup();
      this._showToast(`★ Memungut: ${target.name}!`);
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
    document.getElementById("modal-feedback-box").className = "feedback-box hidden";
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
      this.minigameManager.start(mgType, 100, (score) => {
        document.getElementById("tab-score-badge").innerText = `${score}/100 Poin (SELESAI)`;
        this._showToast("★ Mini-Game Berhasil! Nilai 100 Poin!");
      });
    }
    audioSys.playClick();
  }

  _resetCode() {
    if (this.activeQuest) {
      document.getElementById("code-input").value = this.activeQuest.initial_code;
      this._setFeedback("Kode direset ke template awal.", "hint");
    }
  }

  _showHint() {
    if (this.activeQuest && this.activeQuest.hints) {
      this._setFeedback(`💡 Petunjuk: ${this.activeQuest.hints[0]}`, "hint");
      audioSys.playBlip("high");
    }
  }

  _submitQuest() {
    if (!this.activeQuest) return;

    if (this.activeQuest.type === "scavenger") {
      if (this.scavengerCollected < this.activeQuest.target_count) {
        this._setFeedback(`✗ Baru memungut ${this.scavengerCollected}/${this.activeQuest.target_count} ${this.activeQuest.item_target_name}!`, "error");
        audioSys.playError();
        return;
      }
    }

    if (this.activeQuest.type === "coding") {
      const code = document.getElementById("code-input").value;
      const res = this.activeQuest.validator(code);
      if (!res.success) {
        this._setFeedback(`✗ ${res.msg}`, "error");
        audioSys.playError();
        return;
      }

      if (this.minigameManager.score < 100) {
        this._setFeedback(`✓ Kodemu BENAR! Buka Tab '🎮 Mini-Game Aksi' dan raih minimal 100 Poin!`, "hint");
        this._switchTab("minigame");
        return;
      }
    }

    // Berhasil Quest!
    this._setFeedback(`★ LULUS! ${this.activeQuest.reward_desc}`, "success");
    audioSys.playSuccess();

    if (!this.inventory.includes(this.activeQuest.reward_item)) {
      this.inventory.push(this.activeQuest.reward_item);
      this.currentQuestIndex = Math.max(this.currentQuestIndex, this.activeQuest.id);
      this.scavengerCollected = 0;
      this._updateEvolvingPlane3D();
      this._updateHUD();
      this._showToast(`★ Quest ${this.activeQuest.id} Selesai! Pesawat 3D di tengah pulau semakin utuh!`);
    }

    if (this.activeQuest.id >= 10) {
      setTimeout(() => {
        this._closeModals();
        document.getElementById("ending-screen").classList.remove("hidden");
      }, 1500);
    }
  }

  _updateEvolvingPlane3D() {
    const stage = this.currentQuestIndex;
    if (stage >= 1 && this.airplaneParts.leftWing) this.airplaneParts.leftWing.visible = true;
    if (stage >= 2 && this.airplaneParts.propeller) this.airplaneParts.propeller.visible = true;
    if (stage >= 4 && this.airplaneParts.rightWing) {
      this.airplaneParts.rightWing.visible = true;
      this.airplaneParts.tail.visible = true;
    }
    if (stage >= 5 && this.airplaneParts.body) {
      this.airplaneParts.body.material.color.setHex(0xf5f5fa);
    }
    if (stage >= 7 && this.airplaneParts.radar) this.airplaneParts.radar.visible = true;
    if (stage >= 10 && this.airplaneParts.engineGlow) this.airplaneParts.engineGlow.visible = true;
  }

  _setFeedback(text, type) {
    const fb = document.getElementById("modal-feedback-box");
    const txt = document.getElementById("modal-feedback-text");
    fb.className = `feedback-box ${type}`;
    txt.innerText = text;
  }

  _toggleInventory() {
    const inv = document.getElementById("inventory-modal");
    if (inv.classList.contains("hidden")) {
      this._renderInventoryList();
      inv.classList.remove("hidden");
      audioSys.playClick();
    } else {
      inv.classList.add("hidden");
    }
  }

  _renderInventoryList() {
    const c = document.getElementById("inv-grid-container");
    c.innerHTML = "";
    QUEST_DATA.forEach((q, idx) => {
      const unlocked = idx < this.currentQuestIndex;
      const card = document.createElement("div");
      card.className = `inv-card ${unlocked ? 'unlocked' : ''}`;
      card.innerHTML = `
        <div class="inv-card-title">${unlocked ? '★' : '🔒'} Q${q.id}: ${q.topic}</div>
        <div style="color: ${unlocked ? '#91f0d7' : '#a098b8'}; margin: 2px 0;">Pesawat 3D: ${unlocked ? q.reward_item : '(Belum selesai)'}</div>
        <div style="color: #786e8c;">Lokasi: ${q.location}</div>
      `;
      c.appendChild(card);
    });
  }

  _showToast(msg) {
    const toast = document.getElementById("toast-banner");
    toast.innerText = msg;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 4000);
  }

  _updateHUD() {
    const qIndex = Math.min(this.currentQuestIndex, 9);
    const q = QUEST_DATA[qIndex];
    document.getElementById("hud-location").innerText = `Quest ${Math.min(this.currentQuestIndex + 1, 10)}/10: ${q.location.split('(')[0]}`;
    document.getElementById("hud-inventory-btn").innerText = `🎒 Pesawat 3D: ${this.inventory.length}/10 Bagian [TAB]`;
  }

  _closeModals() {
    document.getElementById("quest-modal").classList.add("hidden");
    document.getElementById("inventory-modal").classList.add("hidden");
    this.minigameManager.stop();
  }

  // --- LOOP ANIMASI 3D (60 FPS) ---
  _animate() {
    requestAnimationFrame(() => this._animate());

    const dt = 1 / 60;
    const ticks = performance.now();

    // 1. Putar Baling-Baling Pesawat jika aktif
    if (this.airplaneParts.propeller && this.airplaneParts.propeller.visible) {
      this.airplaneParts.propeller.rotation.x += 0.35;
    }

    // 2. Rotasi Item Scavenger 3D di Udara
    this.scavengerItems.forEach(it => {
      if (it.mesh && !it.collected) {
        it.mesh.rotation.y += 0.03;
        it.mesh.position.y = 2 + Math.sin(ticks * 0.005 + it.id) * 0.5;
      }
    });

    // 3. Gerak Pemain 3D & Kamera Third Person
    if (this._isOverworldActive() && this.playerMesh) {
      let moveX = 0;
      let moveZ = 0;
      const speed = 26;

      if (this.keys['KeyW'] || this.keys['ArrowUp']) moveZ -= 1;
      if (this.keys['KeyS'] || this.keys['ArrowDown']) moveZ += 1;
      if (this.keys['KeyA'] || this.keys['ArrowLeft']) moveX -= 1;
      if (this.keys['KeyD'] || this.keys['ArrowRight']) moveX += 1;

      const len = Math.hypot(moveX, moveZ);
      if (len > 0) {
        moveX /= len;
        moveZ /= len;

        const targetAngle = Math.atan2(moveX, moveZ);
        this.playerMesh.rotation.y = targetAngle;

        const newX = this.playerMesh.position.x + moveX * speed * dt;
        const newZ = this.playerMesh.position.z + moveZ * speed * dt;

        // Cek Collision
        let collided = false;
        if (Math.hypot(newX, newZ) > 78) collided = true; // Batas luar pulau
        for (const col of this.colliders) {
          if (Math.hypot(newX - col.x, newZ - col.z) < col.r) {
            collided = true;
            break;
          }
        }

        if (!collided) {
          this.playerMesh.position.x = newX;
          this.playerMesh.position.z = newZ;
        }

        // Animasi Kaki Berjalan
        if (this.leftLeg && this.rightLeg) {
          const legSwing = Math.sin(ticks * 0.012) * 0.6;
          this.leftLeg.rotation.x = legSwing;
          this.rightLeg.rotation.x = -legSwing;
        }
      } else {
        if (this.leftLeg && this.rightLeg) {
          this.leftLeg.rotation.x = 0;
          this.rightLeg.rotation.x = 0;
        }
      }

      // Deteksi Interaksi Terdekat
      const allTargets = [
        ...this.questNPCs,
        ...this.houses,
        ...this.ambientNPCs,
        ...this.scavengerItems.filter(it => !it.collected)
      ];

      let nearest = null;
      let minD = 7.5;
      for (const t of allTargets) {
        const d = Math.hypot(this.playerMesh.position.x - t.x, this.playerMesh.position.z - t.z);
        if (d < minD) {
          minD = d;
          nearest = t;
        }
      }
      this.nearestInteractable = nearest;

      // Update Teks Prompt di Layar
      const bottomBar = document.querySelector(".hud-bottom-bar");
      if (bottomBar) {
        bottomBar.innerText = nearest ? nearest.prompt : "WASD: Gerak 3D  |  [E]: Interaksi  |  [TAB]: Buku Progres Pesawat";
      }

      // Kamera Third Person Mengikuti Pemain
      const camTargetX = this.playerMesh.position.x;
      const camTargetZ = this.playerMesh.position.z + 24;
      const camTargetY = this.playerMesh.position.y + 18;

      this.camera.position.x += (camTargetX - this.camera.position.x) * 0.08;
      this.camera.position.z += (camTargetZ - this.camera.position.z) * 0.08;
      this.camera.position.y += (camTargetY - this.camera.position.y) * 0.08;
      this.camera.lookAt(this.playerMesh.position.x, this.playerMesh.position.y + 2, this.playerMesh.position.z);
    }

    // 4. Render Scene 3D
    this.renderer.render(this.scene, this.camera);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.gameApp3D = new GameApp3D();
});
