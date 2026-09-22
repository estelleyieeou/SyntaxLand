"""
player.py - Kelas Karakter Pemain dengan Animasi Prosedural Pixel-Art ala OMORI,
Sistem Pergerakan Grid/Smooth, Collision Detection, dan Manajemen Inventaris.
"""

import math
import pygame
from config import (
    TILE_SIZE, COLOR_WHITE, COLOR_BLACK, COLOR_DARK_PURPLE,
    COLOR_PASTEL_PINK, COLOR_PASTEL_PURPLE, COLOR_PASTEL_MINT, COLOR_PASTEL_YELLOW
)

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = 36
        self.height = 44
        self.speed = 220.0  # Kecepatan gerak (piksel per detik)
        
        # Orientasi & Animasi
        self.direction = "down"  # "down", "up", "left", "right"
        self.is_moving = False
        self.anim_timer = 0.0
        self.anim_frame = 0  # 0, 1, 2, 3
        
        # State Progres & Inventaris
        self.current_quest_index = 0  # 0 sampai 9 (Quest 1 - 10)
        self.inventory = []           # List item yang didapat dari quest
        self.interact_target = None   # NPC terdekat yang bisa diajak bicara
        
        # Cache permukaan sprite prosedural
        self._sprite_cache = {}
        self._generate_sprites()

    def _generate_sprites(self):
        """Membuat sprite pixel-art karakter bergaya OMORI secara prosedural untuk 4 arah dan animasi langkah."""
        directions = ["down", "up", "left", "right"]
        for d in directions:
            for frame in range(4):
                surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                self._draw_procedural_omori(surf, d, frame)
                self._sprite_cache[(d, frame)] = surf

    def _draw_procedural_omori(self, surf, direction, frame):
        """Menggambar karakter OMORI (Rambut hitam, kulit pucat, rompi, celana pendek) dengan animasi langkah."""
        w, h = self.width, self.height
        
        # Offset langkah kaki
        bob = int(math.sin(frame * math.pi / 2) * 2) if self.is_moving or frame > 0 else 0
        leg_offset = int(math.sin(frame * math.pi / 2) * 3) if self.is_moving or frame > 0 else 0
        
        # 1. Bayangan bawah kaki (Soft oval shadow)
        shadow_rect = pygame.Rect(4, h - 8, w - 8, 7)
        pygame.draw.ellipse(surf, (15, 12, 25, 120), shadow_rect)
        
        # 2. Kaki & Sepatu
        leg_color = (235, 235, 245)  # Kaos kaki putih
        shoe_color = (30, 25, 40)    # Sepatu hitam
        
        if direction in ["down", "up"]:
            # Kaki kiri
            pygame.draw.rect(surf, leg_color, (10, h - 14 + bob - leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (9, h - 7 + bob - leg_offset, 7, 5))
            # Kaki kanan
            pygame.draw.rect(surf, leg_color, (21, h - 14 + bob + leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (20, h - 7 + bob + leg_offset, 7, 5))
        elif direction == "left":
            pygame.draw.rect(surf, leg_color, (12, h - 14 + bob + leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (9, h - 7 + bob + leg_offset, 8, 5))
            pygame.draw.rect(surf, leg_color, (18, h - 14 + bob - leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (15, h - 7 + bob - leg_offset, 8, 5))
        elif direction == "right":
            pygame.draw.rect(surf, leg_color, (13, h - 14 + bob - leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (13, h - 7 + bob - leg_offset, 8, 5))
            pygame.draw.rect(surf, leg_color, (19, h - 14 + bob + leg_offset, 5, 8))
            pygame.draw.rect(surf, shoe_color, (19, h - 7 + bob + leg_offset, 8, 5))

        # 3. Celana Pendek Hitam
        pygame.draw.rect(surf, (25, 22, 38), (9, h - 22 + bob, 18, 9), border_radius=2)

        # 4. Baju / Rompi Bergaris Putih & Hitam khas OMORI
        # Badan dasar
        pygame.draw.rect(surf, (245, 245, 250), (8, 14 + bob, 20, 15), border_radius=3)
        # Rompi / Garis vest
        pygame.draw.rect(surf, (35, 30, 50), (10, 15 + bob, 16, 13), 2)
        pygame.draw.line(surf, (35, 30, 50), (18, 15 + bob), (18, 27 + bob), 1)

        # 5. Kepala & Wajah
        skin_color = (252, 248, 242) # Pale skin
        face_rect = pygame.Rect(9, 3 + bob, 18, 16)
        pygame.draw.rect(surf, skin_color, face_rect, border_radius=4)
        
        # 6. Rambut Hitam Berantakan Khas Headspace
        hair_color = (22, 18, 32)
        # Bagian atas rambut
        pygame.draw.rect(surf, hair_color, (7, 0 + bob, 22, 9), border_radius=5)
        # Ponikiri & kanan
        pygame.draw.rect(surf, hair_color, (6, 4 + bob, 4, 10))
        pygame.draw.rect(surf, hair_color, (26, 4 + bob, 4, 10))
        # Poni depan segitiga
        if direction == "down":
            pygame.draw.polygon(surf, hair_color, [(12, 9 + bob), (15, 12 + bob), (17, 9 + bob)])
            pygame.draw.polygon(surf, hair_color, [(18, 9 + bob), (20, 11 + bob), (23, 9 + bob)])
            # Mata Hitam Besar Melankolis
            pygame.draw.rect(surf, (20, 15, 30), (12, 10 + bob, 3, 4))
            pygame.draw.rect(surf, (20, 15, 30), (21, 10 + bob, 3, 4))
            # Titik putih pantulan cahaya di mata
            pygame.draw.rect(surf, (255, 255, 255), (12, 10 + bob, 1, 1))
            pygame.draw.rect(surf, (255, 255, 255), (21, 10 + bob, 1, 1))
            # Pipi semburat pastel pink
            pygame.draw.rect(surf, (255, 190, 210), (10, 14 + bob, 3, 2))
            pygame.draw.rect(surf, (255, 190, 210), (23, 14 + bob, 3, 2))
        elif direction == "up":
            # Rambut penuh belakang kepala
            pygame.draw.rect(surf, hair_color, (7, 2 + bob, 22, 16), border_radius=4)
        elif direction == "left":
            pygame.draw.polygon(surf, hair_color, [(10, 8 + bob), (13, 12 + bob), (16, 8 + bob)])
            # Satu mata samping
            pygame.draw.rect(surf, (20, 15, 30), (11, 10 + bob, 3, 4))
            pygame.draw.rect(surf, (255, 255, 255), (11, 10 + bob, 1, 1))
            pygame.draw.rect(surf, (255, 190, 210), (10, 14 + bob, 3, 2))
        elif direction == "right":
            pygame.draw.polygon(surf, hair_color, [(20, 8 + bob), (23, 12 + bob), (26, 8 + bob)])
            # Satu mata samping
            pygame.draw.rect(surf, (20, 15, 30), (22, 10 + bob, 3, 4))
            pygame.draw.rect(surf, (255, 255, 255), (23, 10 + bob, 1, 1))
            pygame.draw.rect(surf, (255, 190, 210), (23, 14 + bob, 3, 2))

    def get_hitbox(self):
        """Hitbox kecil di area kaki untuk collision detection yang presisi dan nyaman."""
        return pygame.Rect(self.x + 6, self.y + self.height - 18, self.width - 12, 16)

    def handle_input(self, dt, keys, collision_rects):
        """Memproses pergerakan pemain dengan keyboard dan sliding collision."""
        dx = 0.0
        dy = 0.0

        def is_pressed(k):
            try:
                return bool(keys[k])
            except (IndexError, KeyError, TypeError):
                return False

        if is_pressed(pygame.K_w) or is_pressed(pygame.K_UP):
            dy -= 1.0
            self.direction = "up"
        if is_pressed(pygame.K_s) or is_pressed(pygame.K_DOWN):
            dy += 1.0
            self.direction = "down"
        if is_pressed(pygame.K_a) or is_pressed(pygame.K_LEFT):
            dx -= 1.0
            self.direction = "left"
        if is_pressed(pygame.K_d) or is_pressed(pygame.K_RIGHT):
            dx += 1.0
            self.direction = "right"

        # Normalisasi vektor gerak diagonal
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.is_moving = True
            self.anim_timer += dt * 8.0
            if self.anim_timer >= 1.0:
                self.anim_timer = 0.0
                self.anim_frame = (self.anim_frame + 1) % 4
        else:
            self.is_moving = False
            self.anim_frame = 0

        # Gerak Sumbu X dengan Collision
        old_x = self.x
        self.x += dx * self.speed * dt
        hitbox_x = self.get_hitbox()
        for r in collision_rects:
            if hitbox_x.colliderect(r):
                self.x = old_x
                break

        # Gerak Sumbu Y dengan Collision
        old_y = self.y
        self.y += dy * self.speed * dt
        hitbox_y = self.get_hitbox()
        for r in collision_rects:
            if hitbox_y.colliderect(r):
                self.y = old_y
                break

    def check_npc_interaction(self, npcs):
        """Memeriksa apakah pemain berada di dekat NPC yang bisa diajak berinteraksi."""
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        nearest_npc = None
        min_dist = 64.0  # Jarak interaksi
        
        for npc in npcs:
            d = math.hypot(center_x - npc.center_x, center_y - npc.center_y)
            if d <= min_dist:
                min_dist = d
                nearest_npc = npc
                
        self.interact_target = nearest_npc
        return nearest_npc

    def add_reward_item(self, item_name):
        """Menambahkan item ke inventaris pemain jika belum ada."""
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            self.current_quest_index += 1

    def draw(self, surface, camera):
        """Menggambar pemain ke layar dengan memperhitungkan posisi kamera offset."""
        screen_x = int(self.x - camera.x)
        screen_y = int(self.y - camera.y)
        
        frame_key = (self.direction, self.anim_frame)
        sprite = self._sprite_cache.get(frame_key)
        if sprite:
            surface.blit(sprite, (screen_x, screen_y))
        else:
            # Fallback jika cache hilang
            pygame.draw.rect(surface, COLOR_PASTEL_PURPLE, (screen_x, screen_y, self.width, self.height))

        # Tampilkan prompt interaksi jika dekat NPC
        if self.interact_target:
            prompt_surf = pygame.Surface((120, 24), pygame.SRCALPHA)
            pygame.draw.rect(prompt_surf, (15, 12, 25, 210), (0, 0, 120, 24), border_radius=6)
            pygame.draw.rect(prompt_surf, COLOR_PASTEL_MINT, (0, 0, 120, 24), 2, border_radius=6)
            
            font = pygame.font.SysFont("consolas", 12, bold=True)
            text = font.render("[E] Bicara", True, COLOR_WHITE)
            prompt_surf.blit(text, (20, 4))
            
            # Animasi melayang atas kepala
            float_y = int(math.sin(pygame.time.get_ticks() * 0.006) * 3)
            surface.blit(prompt_surf, (screen_x + self.width // 2 - 60, screen_y - 28 + float_y))
