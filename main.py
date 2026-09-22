"""
main.py - Game Loop Utama, Pengelola State (Title, Intro, Overworld, Quest, Inventory, Ending),
Render HUD, dan Integrasi Seluruh Modul RPG Belajar Python OMORI.
"""

import sys
import math
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    COLOR_WHITE, COLOR_BLACK, COLOR_DARK_PURPLE, COLOR_DEEP_NAVY,
    COLOR_PASTEL_PURPLE, COLOR_PASTEL_PINK, COLOR_PASTEL_MINT,
    COLOR_PASTEL_YELLOW, COLOR_PASTEL_BLUE, COLOR_SUCCESS_GREEN,
    STATE_TITLE, STATE_INTRO, STATE_OVERWORLD, STATE_QUEST, STATE_INVENTORY, STATE_ENDING
)
from sound_gen import audio_sys
from quests import QUEST_DATA
from player import Player
from map import WorldMap, Camera
from ui import UIHelper, QuestModal, ToastNotification, ParticleManager, Button


class OmoriPythonGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # State Game
        self.state = STATE_TITLE
        
        # Objek Dunia & Pemain
        self.world_map = WorldMap()
        self.camera = Camera(self.world_map.pixel_width, self.world_map.pixel_height)
        self.player = Player(x=200, y=300)
        
        # UI & Partikel
        self.quest_modal = QuestModal()
        self.toast = ToastNotification()
        self.particles = ParticleManager()
        
        # Intro Cutscene State
        self.intro_step = 0
        self.intro_texts = [
            "Badai petir menyambar pesawatmu di atas Samudra Pikiran...",
            "Kamu terlempar dan jatuh ke pantai sebuah pulau surealis yang asing...",
            "Semua jalan terkunci oleh kabut dan gerbang teka-teki logika.",
            "Di ujung dermaga pulau, terdapat perahu kayu tua yang rusak...",
            "Temui penghuni pulau, kuasai 10 materi dasar Python, dan berlayarlah kembali!"
        ]
        self.intro_char_count = 0
        self.intro_timer = 0.0
        
        # Ending Animation State
        self.ending_boat_x = 0.0
        self.ending_timer = 0.0

    def run(self):
        """Game loop utama 60 FPS."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time dalam detik
            mouse_pos = pygame.mouse.get_pos()
            
            # 1. Event Handling
            self._handle_events(mouse_pos)
            
            # 2. Update Logika
            self._update(dt, mouse_pos)
            
            # 3. Render Gambar
            self._render()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == STATE_TITLE:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        audio_sys.play("success")
                        self.state = STATE_INTRO
                        self.intro_step = 0
                        self.intro_char_count = 0
                        self.intro_timer = 0.0

            elif self.state == STATE_INTRO:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
                    if self.intro_char_count < len(self.intro_texts[self.intro_step]):
                        # Tampilkan langsung seluruh teks jika ditekan cepat
                        self.intro_char_count = len(self.intro_texts[self.intro_step])
                    else:
                        self.intro_step += 1
                        self.intro_char_count = 0
                        if self.intro_step >= len(self.intro_texts):
                            self.state = STATE_OVERWORLD
                            self.toast.show("Selamat Datang di Pantai Hampa! Cari Mori Si Kerang.", COLOR_PASTEL_MINT)
                        else:
                            audio_sys.play("click")

            elif self.state == STATE_OVERWORLD:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_e, pygame.K_SPACE):
                        # Interaksi dengan NPC terdekat
                        nearest_npc = self.player.check_npc_interaction(self.world_map.npcs)
                        if nearest_npc:
                            q_idx = nearest_npc.quest_id - 1
                            if q_idx < len(QUEST_DATA):
                                q_data = QUEST_DATA[q_idx]
                                self.quest_modal.open(q_data, self.player, self._on_quest_solved)
                                self.state = STATE_QUEST
                    elif event.key in (pygame.K_i, pygame.K_TAB):
                        self.state = STATE_INVENTORY
                        audio_sys.play("click")

            elif self.state == STATE_QUEST:
                self.quest_modal.handle_event(event, mouse_pos)
                if not self.quest_modal.is_active:
                    self.state = STATE_OVERWORLD

            elif self.state == STATE_INVENTORY:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_i, pygame.K_TAB, pygame.K_SPACE):
                    self.state = STATE_OVERWORLD
                    audio_sys.play("click")

            elif self.state == STATE_ENDING:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Reset game ke menu awal
                    self.__init__()
                    self.state = STATE_TITLE

    def _on_quest_solved(self, quest_data):
        """Callback ketika sebuah quest berhasil diselesaikan."""
        self.particles.burst(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, count=60)
        self.toast.show(f"★ Quest {quest_data['id']} Selesai! Item Didapat: {quest_data['reward_item']}", COLOR_SUCCESS_GREEN)
        audio_sys.play("barrier")
        
        # Jika menyelesaikan Quest 10 (Final), buka cutscene Ending
        if quest_data["id"] >= 10:
            self.state = STATE_ENDING
            self.ending_boat_x = 0.0
            self.ending_timer = 0.0

    def _update(self, dt, mouse_pos):
        self.toast.update(dt)
        self.particles.update(dt)

        if self.state == STATE_INTRO:
            if self.intro_step < len(self.intro_texts):
                cur_text = self.intro_texts[self.intro_step]
                if self.intro_char_count < len(cur_text):
                    self.intro_timer += dt
                    if self.intro_timer >= 0.03:
                        self.intro_timer = 0.0
                        self.intro_char_count += 1
                        audio_sys.play_blip("mid")

        elif self.state == STATE_OVERWORLD:
            keys = pygame.key.get_pressed()
            collision_rects = self.world_map.get_collision_rects(self.player.current_quest_index)
            self.player.handle_input(dt, keys, collision_rects)
            self.player.check_npc_interaction(self.world_map.npcs)
            self.camera.update(self.player.get_hitbox())

        elif self.state == STATE_QUEST:
            self.quest_modal.update(dt, mouse_pos)
            if not self.quest_modal.is_active:
                self.state = STATE_OVERWORLD

        elif self.state == STATE_ENDING:
            self.ending_timer += dt
            self.ending_boat_x += dt * 45.0  # Perahu berlayar perlahan ke kanan

    def _render(self):
        self.screen.fill(COLOR_BLACK)

        if self.state == STATE_TITLE:
            self._render_title_screen()

        elif self.state == STATE_INTRO:
            self._render_intro_screen()

        elif self.state in (STATE_OVERWORLD, STATE_QUEST, STATE_INVENTORY):
            # 1. Render Dunia 2D & Pemain
            self.world_map.draw(self.screen, self.camera, self.player.current_quest_index)
            self.player.draw(self.screen, self.camera)
            
            # 2. Render Partikel Efek
            self.particles.draw(self.screen)
            
            # 3. Render HUD Atas & Bawah
            self._render_hud()

            # 4. Render Overlay Modal jika aktif
            if self.state == STATE_QUEST:
                # Cari portrait NPC yang sedang aktif
                active_npc = self.player.interact_target
                portrait = active_npc.portrait_surf if active_npc else None
                self.quest_modal.draw(self.screen, portrait)
            elif self.state == STATE_INVENTORY:
                self._render_inventory_modal()

        elif self.state == STATE_ENDING:
            self._render_ending_screen()

        # Render Toast Notifikasi (selalu di atas)
        self.toast.draw(self.screen)

    def _render_title_screen(self):
        """Layar judul minimalis surealis khas White Space / OMORI."""
        # Pola grid samar di background
        for x in range(0, SCREEN_WIDTH, 48):
            pygame.draw.line(self.screen, (22, 18, 38), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 48):
            pygame.draw.line(self.screen, (22, 18, 38), (0, y), (SCREEN_WIDTH, y), 1)

        # Lampu Gantung Hitam Khas OMORI di Atas
        lamp_x = SCREEN_WIDTH // 2
        lamp_y = 70
        pygame.draw.line(self.screen, (100, 90, 120), (lamp_x, 0), (lamp_x, lamp_y), 2)
        # Bohlam berpijar
        ticks = pygame.time.get_ticks()
        glow = int(math.sin(ticks * 0.005) * 4) + 12
        pygame.draw.circle(self.screen, (255, 245, 180, 80), (lamp_x, lamp_y), glow + 8)
        pygame.draw.circle(self.screen, (255, 240, 150), (lamp_x, lamp_y), 8)

        # Judul Utama
        title_font = UIHelper.get_font(42, bold=True)
        sub_font = UIHelper.get_font(16, bold=False)
        prompt_font = UIHelper.get_font(14, bold=True)

        t_surf = title_font.render("PULAU SINTAKSIS", True, COLOR_WHITE)
        t_shadow = title_font.render("PULAU SINTAKSIS", True, COLOR_DARK_PURPLE)
        self.screen.blit(t_shadow, (SCREEN_WIDTH // 2 - t_surf.get_width() // 2 + 3, 203))
        self.screen.blit(t_surf, (SCREEN_WIDTH // 2 - t_surf.get_width() // 2, 200))

        s_surf = sub_font.render("Petualangan 2D RPG Belajar Dasar Pemrograman Python", True, COLOR_PASTEL_PINK)
        self.screen.blit(s_surf, (SCREEN_WIDTH // 2 - s_surf.get_width() // 2, 260))

        # Kotak Karakter & Ilustrasi Mini di Tengah
        box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 160, 310, 320, 170)
        UIHelper.draw_omori_box(self.screen, box_rect, bg_color=(20, 16, 36, 230), border_color=COLOR_PASTEL_PURPLE)
        
        info_lines = [
            "• 10 Quest Materi Dasar Python Lengkap",
            "• Editor Kode Interaktif & Validator Cerdas",
            "• Eksplorasi 10 Zona Surealis Bergaya OMORI",
            "• Kontrol: WASD / Panah + [E] Bicara"
        ]
        info_font = UIHelper.get_font(12, bold=False)
        for idx, line in enumerate(info_lines):
            l_surf = info_font.render(line, True, (220, 215, 240))
            self.screen.blit(l_surf, (box_rect.x + 20, box_rect.y + 24 + idx * 28))

        # Tombol Mulai Berkedip
        if (ticks // 500) % 2 == 0:
            p_surf = prompt_font.render("[ TEKAN ENTER ATAU SPASI UNTUK MEMULAI ]", True, COLOR_PASTEL_MINT)
            self.screen.blit(p_surf, (SCREEN_WIDTH // 2 - p_surf.get_width() // 2, 520))

    def _render_intro_screen(self):
        """Layar pembuka narasi sebelum petualangan dimulai."""
        dim_rect = pygame.Rect(100, 140, SCREEN_WIDTH - 200, 320)
        UIHelper.draw_omori_box(self.screen, dim_rect, bg_color=(18, 14, 32, 250), border_color=COLOR_PASTEL_PURPLE)

        # Header
        h_font = UIHelper.get_font(18, bold=True)
        h_surf = h_font.render(f"PROLOGUE : Terdampar di Headspace ({self.intro_step + 1}/{len(self.intro_texts)})", True, COLOR_PASTEL_YELLOW)
        self.screen.blit(h_surf, (dim_rect.x + 30, dim_rect.y + 30))

        # Teks Narasi Berjalan
        n_font = UIHelper.get_font(15, bold=False)
        revealed_text = self.intro_texts[self.intro_step][:self.intro_char_count]
        
        # Word wrap sederhana
        words = revealed_text.split(" ")
        lines = []
        cur_line = ""
        for w in words:
            if n_font.size(cur_line + w)[0] < dim_rect.width - 60:
                cur_line += w + " "
            else:
                lines.append(cur_line)
                cur_line = w + " "
        lines.append(cur_line)

        for i, l in enumerate(lines):
            l_surf = n_font.render(l, True, COLOR_WHITE)
            self.screen.blit(l_surf, (dim_rect.x + 30, dim_rect.y + 90 + i * 28))

        # Prompt Lanjut
        p_font = UIHelper.get_font(13, bold=True)
        p_surf = p_font.render("[ Tekan SPASI / ENTER untuk Lanjut ]", True, COLOR_PASTEL_MINT)
        self.screen.blit(p_surf, (dim_rect.x + dim_rect.width - p_surf.get_width() - 30, dim_rect.y + dim_rect.height - 45))

    def _render_hud(self):
        """Render HUD atas (Progres Quest & Lokasi) dan HUD bawah (Panduan Tombol)."""
        hud_font = UIHelper.get_font(12, bold=True)
        
        # 1. Bar Atas Kiri: Info Quest & Progres
        q_cur = self.player.current_quest_index
        zone_info = QUEST_DATA[min(q_cur, 9)]
        hud_left_rect = pygame.Rect(16, 12, 360, 48)
        UIHelper.draw_omori_box(self.screen, hud_left_rect, bg_color=(18, 14, 30, 220), border_color=(100, 85, 140))
        
        z_title = f"Lokasi: {zone_info['location']} (Quest {min(q_cur + 1, 10)}/10)"
        zt_surf = hud_font.render(z_title, True, COLOR_PASTEL_MINT)
        self.screen.blit(zt_surf, (hud_left_rect.x + 12, hud_left_rect.y + 6))
        
        # Progress Bar Kotak
        bar_w = 336
        bar_h = 10
        bar_x = hud_left_rect.x + 12
        bar_y = hud_left_rect.y + 28
        pygame.draw.rect(self.screen, (30, 24, 46), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        filled_w = int((min(q_cur, 10) / 10.0) * bar_w)
        if filled_w > 0:
            pygame.draw.rect(self.screen, COLOR_PASTEL_PURPLE, (bar_x, bar_y, filled_w, bar_h), border_radius=3)
        pygame.draw.rect(self.screen, COLOR_WHITE, (bar_x, bar_y, bar_w, bar_h), 1, border_radius=3)

        # 2. Bar Atas Kanan: Tombol Inventaris / Catatan
        hud_right_rect = pygame.Rect(SCREEN_WIDTH - 220, 12, 204, 48)
        UIHelper.draw_omori_box(self.screen, hud_right_rect, bg_color=(18, 14, 30, 220), border_color=(100, 85, 140))
        inv_title = f"🎒 Tas: {len(self.player.inventory)}/10 Item [TAB]"
        it_surf = hud_font.render(inv_title, True, COLOR_PASTEL_YELLOW)
        self.screen.blit(it_surf, (hud_right_rect.x + 14, hud_right_rect.y + 14))

        # 3. Bar Bawah: Panduan Kontrol Cepat
        bottom_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 38, 500, 28)
        pygame.draw.rect(self.screen, (14, 10, 24, 200), bottom_rect, border_radius=6)
        pygame.draw.rect(self.screen, (60, 50, 80), bottom_rect, 1, border_radius=6)
        
        ctrl_text = "WASD/Panah: Gerak  |  [E/Spasi]: Bicara ke NPC  |  [TAB/I]: Buku Materi"
        c_surf = UIHelper.get_font(11, bold=False).render(ctrl_text, True, (210, 210, 230))
        self.screen.blit(c_surf, (bottom_rect.centerx - c_surf.get_width() // 2, bottom_rect.y + 6))

    def _render_inventory_modal(self):
        """Modal tas & ringkasan materi Python yang telah dipelajari."""
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((10, 8, 20, 180))
        self.screen.blit(dim_surf, (0, 0))

        inv_rect = pygame.Rect(80, 50, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 100)
        UIHelper.draw_omori_box(self.screen, inv_rect, bg_color=(20, 16, 36, 250), border_color=COLOR_PASTEL_PINK)

        # Title
        t_font = UIHelper.get_font(18, bold=True)
        ts = t_font.render("🎒 BUKU CATATAN MANTRA PYTHON & INVENTARIS", True, COLOR_WHITE)
        self.screen.blit(ts, (inv_rect.x + 30, inv_rect.y + 24))

        # Subtitle
        s_font = UIHelper.get_font(12, bold=False)
        ss = s_font.render("Daftar item quest yang didapat dan konsep Python yang telah kamu kuasai:", True, COLOR_PASTEL_MINT)
        self.screen.blit(ss, (inv_rect.x + 30, inv_rect.y + 52))

        # Grid 10 Quest Item
        item_font = UIHelper.get_font(12, bold=False)
        item_title_font = UIHelper.get_font(12, bold=True)
        
        for i in range(10):
            q_info = QUEST_DATA[i]
            col = i % 2
            row = i // 2
            
            ix = inv_rect.x + 30 + col * (inv_rect.width // 2 - 30)
            iy = inv_rect.y + 80 + row * 72
            
            is_unlocked = i < self.player.current_quest_index
            box_col = (35, 28, 55) if is_unlocked else (18, 14, 26)
            border_col = COLOR_PASTEL_PURPLE if is_unlocked else (45, 38, 60)
            
            card_rect = pygame.Rect(ix, iy, inv_rect.width // 2 - 45, 62)
            pygame.draw.rect(self.screen, box_col, card_rect, border_radius=6)
            pygame.draw.rect(self.screen, border_col, card_rect, 1, border_radius=6)
            
            # Ikon & Info
            status_symbol = "★" if is_unlocked else "🔒"
            status_col = COLOR_PASTEL_YELLOW if is_unlocked else (100, 90, 120)
            
            sym_surf = item_title_font.render(f"{status_symbol} Q{i+1}: {q_info['topic']}", True, status_col)
            self.screen.blit(sym_surf, (ix + 10, iy + 8))
            
            desc_text = f"Item: {q_info['reward_item']}" if is_unlocked else "(Selesaikan quest di " + q_info['location'] + ")"
            desc_col = COLOR_WHITE if is_unlocked else (120, 110, 130)
            d_surf = item_font.render(desc_text, True, desc_col)
            self.screen.blit(d_surf, (ix + 10, iy + 28))
            
            loc_surf = item_font.render(f"Lokasi: {q_info['location']}", True, (160, 150, 180))
            self.screen.blit(loc_surf, (ix + 10, iy + 44))

        # Close Hint
        c_surf = UIHelper.get_font(13, bold=True).render("[ Tekan TAB / ESC / SPASI untuk Kembali ]", True, COLOR_PASTEL_YELLOW)
        self.screen.blit(c_surf, (inv_rect.centerx - c_surf.get_width() // 2, inv_rect.y + inv_rect.height - 35))

    def _render_ending_screen(self):
        """Layar akhir epilogue: perahu berlayar di samudra sunset dengan perayaan penguasaan Python."""
        # Background Sunset Samudra Surealis
        # Langit Gradasi Ungu-Oranye
        for y in range(0, 360):
            r = int(70 + (y / 360) * 140)
            g = int(30 + (y / 360) * 80)
            b = int(90 + (y / 360) * 40)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Lautan Hitam-Ungu Reflektif
        pygame.draw.rect(self.screen, (20, 15, 35), (0, 360, SCREEN_WIDTH, SCREEN_HEIGHT - 360))
        for y in range(360, SCREEN_HEIGHT, 16):
            alpha_col = (180, 100, 140)
            wave_offset = int(math.sin(pygame.time.get_ticks() * 0.003 + y) * 20)
            pygame.draw.line(self.screen, alpha_col, (0, y), (SCREEN_WIDTH, y), 1)

        # Matahari Terbenam Pastel
        pygame.draw.circle(self.screen, (255, 210, 140), (SCREEN_WIDTH // 2, 340), 90)

        # Perahu Berlayar ke Kanan
        bx = int(100 + self.ending_boat_x) % (SCREEN_WIDTH + 200) - 100
        by = 380 + int(math.sin(pygame.time.get_ticks() * 0.005) * 6)
        
        # Lambung kapal
        pygame.draw.polygon(self.screen, (120, 75, 50), [(bx, by), (bx + 80, by), (bx + 65, by + 28), (bx + 15, by + 28)])
        # Tiang & Layar
        pygame.draw.line(self.screen, (60, 40, 30), (bx + 40, by), (bx + 40, by - 50), 3)
        pygame.draw.polygon(self.screen, COLOR_WHITE, [(bx + 42, by - 48), (bx + 75, by - 24), (bx + 42, by - 6)])
        # Pemain di perahu
        pygame.draw.circle(self.screen, (240, 240, 250), (bx + 25, by - 8), 6) # Kepala
        pygame.draw.rect(self.screen, (30, 25, 45), (bx + 20, by - 2, 10, 10)) # Badan

        # Partikel Sparkle Emas di Belakang Kapal
        if pygame.time.get_ticks() % 5 == 0:
            self.particles.burst(bx - 10, by + 15, count=2)
        self.particles.draw(self.screen)

        # Banner Kemenangan
        banner_rect = pygame.Rect(120, 50, SCREEN_WIDTH - 240, 240)
        UIHelper.draw_omori_box(self.screen, banner_rect, bg_color=(18, 14, 32, 240), border_color=COLOR_PASTEL_MINT)

        v_font = UIHelper.get_font(22, bold=True)
        v_surf = v_font.render("★ SELAMAT! PERAHU TELAH BERLAYAR! ★", True, COLOR_PASTEL_YELLOW)
        self.screen.blit(v_surf, (banner_rect.centerx - v_surf.get_width() // 2, banner_rect.y + 20))

        sub_v = UIHelper.get_font(13, bold=False)
        m_lines = [
            "Kamu telah menyelesaikan 10 Tantangan Quest Dasar Python:",
            "1. Output & Input (print/input)   2. Variabel & Tipe Data Dasar",
            "3. Operasi Aritmatika & Modulo    4. Kondisional Sederhana (if/else)",
            "5. Kondisional Lanjutan (elif)    6. List & Manipulasi Array",
            "7. Dictionary (Key-Value)         8. Perulangan (for & while loop)",
            "9. Pembuatan Fungsi (def/return)  10. Penanganan Error (try/except)"
        ]
        for idx, ml in enumerate(m_lines):
            col = COLOR_PASTEL_MINT if idx == 0 else (230, 225, 245)
            ml_surf = sub_v.render(ml, True, col)
            self.screen.blit(ml_surf, (banner_rect.x + 24, banner_rect.y + 60 + idx * 22))

        # Return Prompt
        p_font = UIHelper.get_font(13, bold=True)
        ps = p_font.render("[ Tekan ENTER untuk Kembali ke Menu Utama ]", True, COLOR_PASTEL_PINK)
        self.screen.blit(ps, (banner_rect.centerx - ps.get_width() // 2, banner_rect.y + banner_rect.height - 30))


if __name__ == "__main__":
    game = OmoriPythonGame()
    game.run()
