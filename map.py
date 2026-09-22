"""
map.py - Sistem Peta 2D (10 Zona Tematik Terhubung), Procedural Pixel-Art Generator,
NPC Entitas & Portrait, Barrier Gerbang Magis, dan Kamera Scrolling.
"""

import math
import random
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE,
    ZONE_COLORS, COLOR_WHITE, COLOR_BLACK, COLOR_DARK_PURPLE,
    COLOR_PASTEL_PURPLE, COLOR_PASTEL_PINK, COLOR_PASTEL_MINT,
    COLOR_PASTEL_YELLOW, COLOR_PASTEL_BLUE, COLOR_BARRIER_GLOW
)
from quests import QUEST_DATA


class Camera:
    """Kamera scrolling halus mengikuti pergerakan pemain."""
    def __init__(self, map_width, map_height):
        self.x = 0.0
        self.y = 0.0
        self.map_width = map_width
        self.map_height = map_height

    def update(self, target_rect):
        """Memusatkan kamera ke target pemain dengan batas peta."""
        target_x = target_rect.centerx - SCREEN_WIDTH / 2
        target_y = target_rect.centery - SCREEN_HEIGHT / 2
        
        # Smooth interpolation (lerp)
        self.x += (target_x - self.x) * 0.12
        self.y += (target_y - self.y) * 0.12
        
        # Clamp batas peta
        self.x = max(0, min(self.x, self.map_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.map_height - SCREEN_HEIGHT))


class NPC:
    """Entitas NPC di overworld lengkap dengan sprite dan portrait dialog OMORI."""
    def __init__(self, zone_id, quest_id, grid_x, grid_y, name, title, blip_pitch="mid"):
        self.zone_id = zone_id
        self.quest_id = quest_id
        self.x = grid_x * TILE_SIZE
        self.y = grid_y * TILE_SIZE
        self.width = 40
        self.height = 46
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2
        self.name = name
        self.title = title
        self.blip_pitch = blip_pitch
        
        self.sprite_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.portrait_surf = pygame.Surface((84, 84), pygame.SRCALPHA)
        self._generate_visuals()

    def _generate_visuals(self):
        """Menghasilkan visual sprite overworld dan portrait 84x84 unik untuk setiap NPC."""
        # 1. Gambar Portrait Bergaya OMORI (Frame Hitam/Putih Sketsa & Karakter Unik)
        p = self.portrait_surf
        p.fill((20, 16, 32))
        pygame.draw.rect(p, COLOR_WHITE, (2, 2, 80, 80), 2)
        
        # 2. Karakteristik khusus berdasarkan quest_id (1 - 10)
        qid = self.quest_id
        if qid == 1:
            # Mori Si Kerang
            self._draw_shell_npc(self.sprite_surf, p)
        elif qid == 2:
            # Pohon Mata Bintang
            self._draw_tree_npc(self.sprite_surf, p)
        elif qid == 3:
            # Kelelawar Prisma
            self._draw_bat_npc(self.sprite_surf, p)
        elif qid == 4:
            # Katak Mahkota
            self._draw_frog_npc(self.sprite_surf, p)
        elif qid == 5:
            # Bunga Melankolis
            self._draw_flower_npc(self.sprite_surf, p)
        elif qid == 6:
            # Kucing Pita Pastel
            self._draw_cat_npc(self.sprite_surf, p)
        elif qid == 7:
            # Pedagang Topeng Bulan
            self._draw_merchant_npc(self.sprite_surf, p)
        elif qid == 8:
            # Jam Bandul Bersayap
            self._draw_clock_npc(self.sprite_surf, p)
        elif qid == 9:
            # Patung Pendeta Cahaya
            self._draw_statue_npc(self.sprite_surf, p)
        elif qid == 10:
            # Kapten Boneka Beruang
            self._draw_captain_npc(self.sprite_surf, p)

    def _draw_shell_npc(self, s, p):
        # Overworld
        pygame.draw.ellipse(s, (245, 210, 220), (4, 10, 32, 28))
        pygame.draw.ellipse(s, (255, 160, 190), (8, 14, 24, 20), 2)
        pygame.draw.circle(s, (20, 20, 30), (16, 22), 3) # Mata
        pygame.draw.circle(s, (20, 20, 30), (24, 22), 3)
        # Portrait
        pygame.draw.ellipse(p, (250, 220, 230), (14, 20, 56, 48))
        pygame.draw.ellipse(p, (255, 140, 180), (18, 24, 48, 40), 3)
        pygame.draw.circle(p, (20, 15, 30), (32, 42), 4)
        pygame.draw.circle(p, (20, 15, 30), (52, 42), 4)
        pygame.draw.circle(p, (255, 255, 255), (31, 41), 1)
        pygame.draw.circle(p, (255, 255, 255), (51, 41), 1)

    def _draw_tree_npc(self, s, p):
        # Overworld
        pygame.draw.rect(s, (70, 50, 40), (15, 18, 10, 24))
        pygame.draw.circle(s, (90, 180, 140), (20, 16), 16)
        pygame.draw.circle(s, (255, 255, 255), (20, 16), 6) # Mata tengah
        pygame.draw.circle(s, (30, 20, 40), (20, 16), 3)
        # Portrait
        pygame.draw.circle(p, (80, 160, 130), (42, 38), 28)
        pygame.draw.circle(p, (255, 255, 255), (42, 36), 10)
        pygame.draw.circle(p, (255, 230, 100), (42, 36), 6)
        pygame.draw.circle(p, (30, 20, 40), (42, 36), 3)

    def _draw_bat_npc(self, s, p):
        # Overworld
        pygame.draw.circle(s, (140, 110, 190), (20, 20), 12)
        pygame.draw.polygon(s, (110, 80, 160), [(2, 18), (14, 12), (12, 28)])
        pygame.draw.polygon(s, (110, 80, 160), [(38, 18), (26, 12), (28, 28)])
        pygame.draw.circle(s, (255, 230, 130), (16, 18), 3)
        pygame.draw.circle(s, (255, 230, 130), (24, 18), 3)
        # Portrait
        pygame.draw.polygon(p, (90, 60, 140), [(4, 30), (30, 20), (22, 55)])
        pygame.draw.polygon(p, (90, 60, 140), [(80, 30), (54, 20), (62, 55)])
        pygame.draw.circle(p, (140, 110, 190), (42, 40), 22)
        pygame.draw.circle(p, (255, 240, 150), (34, 36), 5)
        pygame.draw.circle(p, (255, 240, 150), (50, 36), 5)

    def _draw_frog_npc(self, s, p):
        # Overworld
        pygame.draw.ellipse(s, (110, 190, 120), (6, 16, 28, 24))
        pygame.draw.circle(s, (140, 230, 150), (12, 12), 6)
        pygame.draw.circle(s, (140, 230, 150), (28, 12), 6)
        pygame.draw.polygon(s, (255, 220, 90), [(15, 6), (20, 2), (25, 6)]) # Mahkota
        # Portrait
        pygame.draw.ellipse(p, (110, 190, 120), (14, 28, 56, 44))
        pygame.draw.circle(p, (140, 230, 150), (26, 24), 12)
        pygame.draw.circle(p, (140, 230, 150), (58, 24), 12)
        pygame.draw.circle(p, (20, 30, 20), (26, 24), 5)
        pygame.draw.circle(p, (20, 30, 20), (58, 24), 5)
        pygame.draw.polygon(p, (255, 225, 90), [(32, 16), (42, 6), (52, 16)])

    def _draw_flower_npc(self, s, p):
        # Overworld
        pygame.draw.circle(s, (240, 130, 170), (20, 18), 14)
        pygame.draw.circle(s, (40, 30, 50), (20, 18), 8)
        pygame.draw.rect(s, (60, 140, 90), (18, 30, 4, 14))
        # Portrait
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            cx = int(42 + math.cos(rad) * 22)
            cy = int(42 + math.sin(rad) * 22)
            pygame.draw.circle(p, (245, 150, 190), (cx, cy), 12)
        pygame.draw.circle(p, (35, 28, 48), (42, 42), 16)
        pygame.draw.circle(p, (255, 200, 220), (38, 40), 3) # Mata sedih
        pygame.draw.circle(p, (255, 200, 220), (46, 40), 3)

    def _draw_cat_npc(self, s, p):
        # Overworld
        pygame.draw.ellipse(s, (230, 215, 245), (6, 16, 28, 22))
        pygame.draw.polygon(s, (200, 180, 230), [(8, 16), (12, 6), (18, 14)])
        pygame.draw.polygon(s, (200, 180, 230), [(32, 16), (28, 6), (22, 14)])
        pygame.draw.circle(s, (255, 140, 180), (20, 24), 4) # Pita
        # Portrait
        pygame.draw.circle(p, (235, 220, 250), (42, 45), 24)
        pygame.draw.polygon(p, (210, 190, 240), [(22, 35), (26, 12), (38, 28)])
        pygame.draw.polygon(p, (210, 190, 240), [(62, 35), (58, 12), (46, 28)])
        pygame.draw.circle(p, (30, 25, 45), (34, 42), 4)
        pygame.draw.circle(p, (30, 25, 45), (50, 42), 4)
        pygame.draw.circle(p, (255, 130, 180), (42, 56), 6) # Pita leher

    def _draw_merchant_npc(self, s, p):
        # Overworld
        pygame.draw.circle(s, (240, 235, 210), (20, 18), 12)
        pygame.draw.arc(s, (30, 25, 40), (10, 8, 20, 20), 0, math.pi, 3) # Mask
        pygame.draw.rect(s, (140, 90, 50), (8, 28, 24, 16), border_radius=3)
        # Portrait
        pygame.draw.circle(p, (245, 240, 220), (42, 38), 24)
        pygame.draw.arc(p, (40, 30, 60), (24, 22, 36, 36), 0.2, math.pi - 0.2, 5)
        pygame.draw.circle(p, (255, 210, 90), (42, 30), 4) # Simbol bulan

    def _draw_clock_npc(self, s, p):
        # Overworld
        pygame.draw.circle(s, (245, 210, 130), (20, 18), 14)
        pygame.draw.circle(s, (30, 25, 40), (20, 18), 14, 2)
        pygame.draw.line(s, (30, 25, 40), (20, 18), (20, 10), 2)
        pygame.draw.line(s, (30, 25, 40), (20, 18), (26, 18), 2)
        # Portrait
        pygame.draw.circle(p, (250, 220, 140), (42, 42), 26)
        pygame.draw.circle(p, (35, 25, 45), (42, 42), 26, 3)
        pygame.draw.line(p, (35, 25, 45), (42, 42), (42, 24), 3)
        pygame.draw.line(p, (35, 25, 45), (42, 42), (54, 42), 3)
        pygame.draw.polygon(p, (255, 255, 255), [(12, 30), (6, 16), (22, 26)]) # Sayap

    def _draw_statue_npc(self, s, p):
        # Overworld
        pygame.draw.rect(s, (170, 195, 225), (10, 12, 20, 30), border_radius=4)
        pygame.draw.circle(s, (210, 230, 255), (20, 10), 8) # Halo cahaya
        # Portrait
        pygame.draw.circle(p, (220, 240, 255), (42, 22), 16, 3) # Halo
        pygame.draw.rect(p, (160, 190, 230), (24, 26, 36, 46), border_radius=6)
        pygame.draw.circle(p, (255, 255, 255), (36, 40), 3) # Mata bersinar
        pygame.draw.circle(p, (255, 255, 255), (48, 40), 3)

    def _draw_captain_npc(self, s, p):
        # Overworld
        pygame.draw.circle(s, (160, 110, 80), (20, 18), 12)
        pygame.draw.rect(s, (30, 45, 90), (12, 6, 16, 6)) # Topi kapten
        pygame.draw.rect(s, (30, 45, 90), (8, 28, 24, 16), border_radius=3)
        # Portrait
        pygame.draw.circle(p, (160, 110, 80), (42, 42), 24)
        pygame.draw.circle(p, (120, 80, 50), (24, 24), 8) # Telinga beruang
        pygame.draw.circle(p, (120, 80, 50), (60, 24), 8)
        pygame.draw.rect(p, (35, 55, 110), (22, 12, 40, 12), border_radius=3) # Topi kapten
        pygame.draw.circle(p, (255, 220, 100), (42, 18), 3) # Jangkar emas

    def draw(self, surface, camera):
        """Menggambar NPC dengan efek animasi mengambang lembut."""
        screen_x = int(self.x - camera.x)
        float_y = int(math.sin(pygame.time.get_ticks() * 0.004 + self.quest_id) * 3)
        screen_y = int(self.y - camera.y + float_y)
        
        # Bayangan
        shadow_rect = pygame.Rect(screen_x + 6, int(self.y - camera.y) + self.height - 6, self.width - 12, 6)
        pygame.draw.ellipse(surface, (15, 12, 25, 100), shadow_rect)
        
        surface.blit(self.sprite_surf, (screen_x, screen_y))


class ZoneBarrier:
    """Gerbang magis antar-zona yang terbuka saat quest zona sebelumnya selesai."""
    def __init__(self, zone_id, grid_x, grid_y, rows=7):
        self.zone_id = zone_id
        self.x = grid_x * TILE_SIZE
        self.y = grid_y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = rows * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def is_locked(self, player_quest_index):
        """Terkunci jika indeks quest pemain masih di bawah atau sama dengan zona ini."""
        return player_quest_index <= self.zone_id

    def draw(self, surface, camera, player_quest_index):
        if not self.is_locked(player_quest_index):
            return  # Gerbang sudah terbuka, jangan digambar

        screen_x = int(self.x - camera.x)
        screen_y = int(self.y - camera.y)
        
        # Efek medan energi bergetar magis
        ticks = pygame.time.get_ticks()
        alpha = int(180 + 60 * math.sin(ticks * 0.008 + self.zone_id))
        
        barrier_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        barrier_surf.fill((160, 90, 220, int(alpha * 0.35)))
        
        # Garis rune
        pygame.draw.rect(barrier_surf, (240, 200, 255, alpha), (4, 0, self.width - 8, self.height), 2)
        
        # Simbol Gembok Rune di tengah
        mid_y = self.height // 2
        pygame.draw.circle(barrier_surf, (255, 255, 255, alpha), (self.width // 2, mid_y), 14, 2)
        pygame.draw.rect(barrier_surf, (255, 210, 230, alpha), (self.width // 2 - 8, mid_y - 2, 16, 14), border_radius=2)
        
        surface.blit(barrier_surf, (screen_x, screen_y))


class WorldMap:
    """Peta dunia 10 Zona terhubung dengan dekorasi dan lingkungan surealis."""
    def __init__(self):
        self.zones_count = 10
        self.zone_width_tiles = 15
        self.total_cols = self.zones_count * self.zone_width_tiles
        self.total_rows = 14
        self.pixel_width = self.total_cols * TILE_SIZE
        self.pixel_height = self.total_rows * TILE_SIZE
        
        self.npcs = []
        self.barriers = []
        self.decorations = []
        self._build_world()

    def _build_world(self):
        """Membangun 10 zona, menempatkan NPC di tengah zona, dan memasang gerbang magis."""
        for zid in range(self.zones_count):
            q_info = QUEST_DATA[zid]
            zone_start_col = zid * self.zone_width_tiles
            
            # Posisi NPC di tengah zona
            npc_x = zone_start_col + 7
            npc_y = 6
            npc = NPC(
                zone_id=zid,
                quest_id=q_info["id"],
                grid_x=npc_x,
                grid_y=npc_y,
                name=q_info["npc_name"],
                title=q_info["npc_title"],
                blip_pitch=q_info["npc_blip"]
            )
            self.npcs.append(npc)
            
            # Gerbang di akhir zona (kecuali zona terakhir 9)
            if zid < self.zones_count - 1:
                barrier_col = zone_start_col + self.zone_width_tiles - 1
                self.barriers.append(ZoneBarrier(zone_id=zid, grid_x=barrier_col, grid_y=3, rows=8))
                
            # Tambahkan dekorasi prosedural per zona
            self._generate_zone_decorations(zid, zone_start_col)

    def _generate_zone_decorations(self, zid, start_col):
        """Menambahkan objek visual atmosfer surealis sesuai tema zona."""
        random.seed(zid * 997 + 42)
        for _ in range(12):
            rx = (start_col + random.randint(1, self.zone_width_tiles - 2)) * TILE_SIZE + random.randint(0, 16)
            ry = random.choice([random.randint(1, 2), random.randint(10, 12)]) * TILE_SIZE + random.randint(0, 16)
            self.decorations.append({
                "zone_id": zid,
                "x": rx,
                "y": ry,
                "type": random.choice(["flower", "crystal", "cloud", "star", "lamp"])
            })

    def get_collision_rects(self, player_quest_index):
        """Menghasilkan semua boundary solid dan gerbang yang masih terkunci."""
        rects = []
        # Batas dinding atas dan bawah dunia
        rects.append(pygame.Rect(0, 0, self.pixel_width, 2 * TILE_SIZE))
        rects.append(pygame.Rect(0, (self.total_rows - 2) * TILE_SIZE, self.pixel_width, 2 * TILE_SIZE))
        # Batas kiri & kanan dunia
        rects.append(pygame.Rect(-32, 0, 32, self.pixel_height))
        rects.append(pygame.Rect(self.pixel_width, 0, 32, self.pixel_height))
        
        # Gerbang aktif
        for b in self.barriers:
            if b.is_locked(player_quest_index):
                rects.append(b.rect)
                
        return rects

    def draw(self, surface, camera, player_quest_index):
        """Menggambar lantai zona, jalur setapak, dekorasi, NPC, dan gerbang."""
        # Rentang tile yang terlihat di layar
        start_col = max(0, int(camera.x // TILE_SIZE))
        end_col = min(self.total_cols, int((camera.x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        start_row = max(0, int(camera.y // TILE_SIZE))
        end_row = min(self.total_rows, int((camera.y + SCREEN_HEIGHT) // TILE_SIZE) + 2)

        # 1. Gambar Lantai Grid & Jalur Setapak
        for c in range(start_col, end_col):
            zid = min(self.zones_count - 1, c // self.zone_width_tiles)
            z_style = ZONE_COLORS[zid]
            
            for r in range(start_row, end_row):
                screen_x = int(c * TILE_SIZE - camera.x)
                screen_y = int(r * TILE_SIZE - camera.y)
                tile_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                
                # Dinding atas/bawah
                if r < 2 or r >= self.total_rows - 2:
                    pygame.draw.rect(surface, COLOR_DARK_PURPLE, tile_rect)
                    # Pola grid gelap
                    pygame.draw.rect(surface, (20, 14, 38), tile_rect, 1)
                elif 5 <= r <= 8:
                    # Jalur utama (Path)
                    pygame.draw.rect(surface, z_style["path"], tile_rect)
                    # Titik tekstur
                    if (c + r) % 2 == 0:
                        pygame.draw.rect(surface, z_style["ground"], (screen_x + 10, screen_y + 10, 6, 6))
                else:
                    # Area samping (Ground)
                    pygame.draw.rect(surface, z_style["ground"], tile_rect)
                    if (c * 3 + r * 7) % 5 == 0:
                        pygame.draw.circle(surface, z_style["accent"], (screen_x + 24, screen_y + 24), 3)

        # 2. Gambar Efek Khusus Zona (Pesawat Jatuh di Pantai & Perahu di Dermaga)
        self._draw_special_landmarks(surface, camera, player_quest_index)

        # 3. Gambar Dekorasi
        ticks = pygame.time.get_ticks()
        for d in self.decorations:
            dx = d["x"] - camera.x
            dy = d["y"] - camera.y
            if -30 <= dx <= SCREEN_WIDTH + 30 and -30 <= dy <= SCREEN_HEIGHT + 30:
                self._draw_decor_item(surface, int(dx), int(dy), d["type"], d["zone_id"], ticks)

        # 4. Gambar NPC
        for npc in self.npcs:
            if -60 <= npc.x - camera.x <= SCREEN_WIDTH + 60:
                npc.draw(surface, camera)

        # 5. Gambar Gerbang Antar-Zona
        for b in self.barriers:
            if -60 <= b.x - camera.x <= SCREEN_WIDTH + 60:
                b.draw(surface, camera, player_quest_index)

    def _draw_special_landmarks(self, surface, camera, player_quest_index):
        # 1. Pesawat Jatuh di Pantai (Zona 0, dekat awal permainan)
        plane_x = int(3 * TILE_SIZE - camera.x)
        plane_y = int(2 * TILE_SIZE - camera.y)
        if -100 <= plane_x <= SCREEN_WIDTH + 100:
            # Sayap & Badan Pesawat Putih Bergaya Kartun Surealis
            pygame.draw.polygon(surface, (230, 230, 245), [(plane_x - 40, plane_y + 30), (plane_x + 60, plane_y + 10), (plane_x + 30, plane_y + 50)])
            pygame.draw.polygon(surface, (200, 70, 90), [(plane_x + 40, plane_y + 5), (plane_x + 60, plane_y + 10), (plane_x + 45, plane_y + 25)]) # Ekor merah
            # Asap kartun pelangi
            smoke_y = int(math.sin(pygame.time.get_ticks() * 0.005) * 4)
            pygame.draw.circle(surface, (245, 200, 220, 180), (plane_x - 10, plane_y + 15 + smoke_y), 8)
            pygame.draw.circle(surface, (200, 240, 230, 150), (plane_x - 25, plane_y + 5 + smoke_y), 12)

        # 2. Perahu Pelarian di Dermaga Tua (Zona 9)
        dock_start_x = 9 * self.zone_width_tiles * TILE_SIZE
        boat_x = int(dock_start_x + 10 * TILE_SIZE - camera.x)
        boat_y = int(6 * TILE_SIZE - camera.y)
        if -120 <= boat_x <= SCREEN_WIDTH + 120:
            # Dermaga Kayu
            pier_rect = pygame.Rect(boat_x - 50, boat_y + 20, 60, 20)
            pygame.draw.rect(surface, (90, 60, 45), pier_rect)
            
            # Perahu
            boat_bob = int(math.sin(pygame.time.get_ticks() * 0.004) * 3)
            # Lambung kapal
            pygame.draw.polygon(surface, (140, 95, 60), [
                (boat_x, boat_y + 10 + boat_bob),
                (boat_x + 70, boat_y + 10 + boat_bob),
                (boat_x + 58, boat_y + 36 + boat_bob),
                (boat_x + 12, boat_y + 36 + boat_bob)
            ])
            # Tiang Layar
            pygame.draw.line(surface, (80, 50, 30), (boat_x + 35, boat_y + 10 + boat_bob), (boat_x + 35, boat_y - 30 + boat_bob), 3)
            
            # Layar: Jika quest 10 belum selesai -> Layar robek/mati; Jika selesai -> Layar putih megah
            if player_quest_index >= 10:
                # Layar Berkibar Sempurna
                pygame.draw.polygon(surface, (255, 248, 235), [
                    (boat_x + 37, boat_y - 28 + boat_bob),
                    (boat_x + 65, boat_y - 8 + boat_bob),
                    (boat_x + 37, boat_y + 4 + boat_bob)
                ])
                # Efek Cahaya Mesin Berputar
                pygame.draw.circle(surface, (100, 255, 200), (boat_x + 12, boat_y + 16 + boat_bob), 6)
            else:
                # Layar compang-camping
                pygame.draw.polygon(surface, (180, 160, 160), [
                    (boat_x + 37, boat_y - 20 + boat_bob),
                    (boat_x + 55, boat_y - 12 + boat_bob),
                    (boat_x + 37, boat_y + 2 + boat_bob)
                ])

    def _draw_decor_item(self, surface, x, y, decor_type, zone_id, ticks):
        if decor_type == "flower":
            pygame.draw.circle(surface, COLOR_PASTEL_PINK, (x, y), 5)
            pygame.draw.circle(surface, COLOR_PASTEL_YELLOW, (x, y), 2)
        elif decor_type == "crystal":
            float_c = int(math.sin(ticks * 0.005 + x) * 2)
            pygame.draw.polygon(surface, COLOR_PASTEL_PURPLE, [(x, y - 6 + float_c), (x + 4, y + float_c), (x, y + 6 + float_c), (x - 4, y + float_c)])
        elif decor_type == "cloud":
            pygame.draw.ellipse(surface, (245, 245, 255, 140), (x, y, 18, 10))
        elif decor_type == "star":
            sparkle = int(math.sin(ticks * 0.008 + y) * 2) + 3
            pygame.draw.circle(surface, COLOR_PASTEL_YELLOW, (x, y), sparkle)
        elif decor_type == "lamp":
            pygame.draw.rect(surface, (40, 30, 50), (x, y, 4, 12))
            pygame.draw.circle(surface, (255, 240, 160), (x + 2, y - 2), 4)
