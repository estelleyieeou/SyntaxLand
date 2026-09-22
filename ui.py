"""
ui.py - Sistem Antarmuka Pengguna (GUI) Bergaya OMORI (Sketsa Double-Border, Typewriter Effect,
Editor Kode Interaktif dengan Syntax Highlighting, Modal Quest, HUD, dan Sistem Notifikasi Partikel).
"""

import math
import re
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK,
    COLOR_DARK_PURPLE, COLOR_DEEP_NAVY, COLOR_PASTEL_PURPLE,
    COLOR_PASTEL_PINK, COLOR_PASTEL_MINT, COLOR_PASTEL_YELLOW,
    COLOR_PASTEL_BLUE, SYNTAX_COLORS, COLOR_SUCCESS_GREEN,
    COLOR_ERROR_RED, COLOR_HINT_YELLOW
)
from sound_gen import audio_sys


class UIHelper:
    """Helper untuk merender frame sketsa khas OMORI dan teks multi-baris."""
    _font_cache = {}

    @classmethod
    def get_font(cls, size, bold=False):
        key = (size, bold)
        if key not in cls._font_cache:
            try:
                # Coba consolas atau courier untuk monospace rapi
                f = pygame.font.SysFont("consolas", size, bold=bold)
            except Exception:
                f = pygame.font.Font(None, size)
            cls._font_cache[key] = f
        return cls._font_cache[key]

    @staticmethod
    def draw_omori_box(surface, rect, bg_color=(18, 14, 30, 240), border_color=COLOR_WHITE):
        """Menggambar box dialog dengan border ganda sketsa khas OMORI."""
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        
        # Background transparan
        bg_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        bg_surf.fill(bg_color)
        surface.blit(bg_surf, (x, y))
        
        # Border Luar Tebal Putih/Pastel
        pygame.draw.rect(surface, border_color, (x, y, w, h), 3, border_radius=8)
        
        # Border Dalam Tipis
        pygame.draw.rect(surface, (border_color[0], border_color[1], border_color[2], 120),
                         (x + 4, y + 4, w - 8, h - 8), 1, border_radius=6)
        
        # Aksen Sudut Sketsa (Notches)
        corner_len = 8
        pygame.draw.line(surface, border_color, (x + 2, y + 2), (x + 2 + corner_len, y + 2), 2)
        pygame.draw.line(surface, border_color, (x + w - 2 - corner_len, y + 2), (x + w - 2, y + 2), 2)
        pygame.draw.line(surface, border_color, (x + 2, y + h - 2), (x + 2 + corner_len, y + h - 2), 2)
        pygame.draw.line(surface, border_color, (x + w - 2 - corner_len, y + h - 2), (x + w - 2, y + h - 2), 2)


class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.vx = (random_uniform(-1.0, 1.0)) * 180.0
        self.vy = (random_uniform(-1.5, 0.5)) * 220.0
        self.color = color
        self.radius = random_uniform(2.5, 5.5)
        self.life = 1.0  # 1.0 -> 0.0
        self.decay = random_uniform(0.7, 1.2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 300.0 * dt  # Gravitasi lembut
        self.life -= self.decay * dt
        return self.life > 0

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 255)
            surf = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            col = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(surf, col, (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(surf, (int(self.x - self.radius), int(self.y - self.radius)))


def random_uniform(a, b):
    import random
    return a + (b - a) * random.random()


class ParticleManager:
    """Manajer efek partikel confetti bintang."""
    def __init__(self):
        self.particles = []

    def burst(self, center_x, center_y, count=40):
        colors = [COLOR_PASTEL_PINK, COLOR_PASTEL_MINT, COLOR_PASTEL_YELLOW, COLOR_PASTEL_PURPLE, COLOR_WHITE]
        for _ in range(count):
            import random
            col = random.choice(colors)
            self.particles.append(Particle(center_x, center_y, col))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class CodeEditorBox:
    """Editor teks interaktif multiline dengan Syntax Highlighting dan kursor interaktif."""
    def __init__(self, rect):
        self.rect = rect
        self.lines = ["# Ketik kodemu di sini"]
        self.cursor_row = 0
        self.cursor_col = 0
        self.scroll_y = 0
        self.line_height = 20
        self.font = UIHelper.get_font(14, bold=False)
        self.font_num = UIHelper.get_font(12, bold=False)
        self.blink_timer = 0.0
        self.show_cursor = True

    def set_text(self, text):
        self.lines = text.split("\n")
        if not self.lines:
            self.lines = [""]
        self.cursor_row = min(self.cursor_row, len(self.lines) - 1)
        self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_row]))

    def get_text(self):
        return "\n".join(self.lines)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return False

        self.show_cursor = True
        self.blink_timer = 0.0
        current_line = self.lines[self.cursor_row]

        if event.key == pygame.K_BACKSPACE:
            if self.cursor_col > 0:
                self.lines[self.cursor_row] = current_line[:self.cursor_col - 1] + current_line[self.cursor_col:]
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                prev_line = self.lines[self.cursor_row - 1]
                self.cursor_col = len(prev_line)
                self.lines[self.cursor_row - 1] = prev_line + current_line
                self.lines.pop(self.cursor_row)
                self.cursor_row -= 1
            audio_sys.play_blip("low")
            return True

        elif event.key == pygame.K_DELETE:
            if self.cursor_col < len(current_line):
                self.lines[self.cursor_row] = current_line[:self.cursor_col] + current_line[self.cursor_col + 1:]
            elif self.cursor_row < len(self.lines) - 1:
                next_line = self.lines[self.cursor_row + 1]
                self.lines[self.cursor_row] = current_line + next_line
                self.lines.pop(self.cursor_row + 1)
            return True

        elif event.key == pygame.K_RETURN:
            # Enter: baris baru dengan auto-indentasi sederhana
            indent = len(current_line) - len(current_line.lstrip(" "))
            if current_line.strip().endswith(":"):
                indent += 4
            new_line = " " * indent + current_line[self.cursor_col:]
            self.lines[self.cursor_row] = current_line[:self.cursor_col]
            self.lines.insert(self.cursor_row + 1, new_line)
            self.cursor_row += 1
            self.cursor_col = indent
            audio_sys.play_blip("mid")
            return True

        elif event.key == pygame.K_TAB:
            # Tab -> 4 spaces
            self.lines[self.cursor_row] = current_line[:self.cursor_col] + "    " + current_line[self.cursor_col:]
            self.cursor_col += 4
            return True

        elif event.key == pygame.K_LEFT:
            if self.cursor_col > 0:
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                self.cursor_row -= 1
                self.cursor_col = len(self.lines[self.cursor_row])
            return True

        elif event.key == pygame.K_RIGHT:
            if self.cursor_col < len(current_line):
                self.cursor_col += 1
            elif self.cursor_row < len(self.lines) - 1:
                self.cursor_row += 1
                self.cursor_col = 0
            return True

        elif event.key == pygame.K_UP:
            if self.cursor_row > 0:
                self.cursor_row -= 1
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_row]))
            return True

        elif event.key == pygame.K_DOWN:
            if self.cursor_row < len(self.lines) - 1:
                self.cursor_row += 1
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_row]))
            return True

        elif event.key == pygame.K_HOME:
            self.cursor_col = 0
            return True

        elif event.key == pygame.K_END:
            self.cursor_col = len(current_line)
            return True

        elif event.unicode and event.unicode.isprintable():
            # Ketik karakter biasa
            self.lines[self.cursor_row] = current_line[:self.cursor_col] + event.unicode + current_line[self.cursor_col:]
            self.cursor_col += len(event.unicode)
            audio_sys.play_blip("high")
            return True

        return False

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= 0.45:
            self.blink_timer = 0.0
            self.show_cursor = not self.show_cursor

    def _tokenize_line(self, line):
        """Memecah baris menjadi token dan warna untuk syntax highlighting."""
        if not line:
            return [("", SYNTAX_COLORS["identifier"])]

        # Cek komentar
        if "#" in line:
            comment_idx = line.find("#")
            code_part = line[:comment_idx]
            comment_part = line[comment_idx:]
            tokens = self._tokenize_line(code_part)
            tokens.append((comment_part, SYNTAX_COLORS["comment"]))
            return tokens

        keywords = {"def", "return", "if", "elif", "else", "for", "while", "in", "try", "except", "and", "or", "not", "is"}
        builtins = {"print", "input", "range", "len", "str", "int", "float", "bool", "list", "dict", "True", "False", "None", "ZeroDivisionError", "Exception"}

        tokens = []
        # Regex token matcher: string literals, words, numbers, symbols, spaces
        pattern = r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\b\w+\b|\s+|[^\s\w]+)'
        matches = re.findall(pattern, line)

        for m in matches:
            if m.startswith('"') or m.startswith("'"):
                tokens.append((m, SYNTAX_COLORS["string"]))
            elif m in keywords:
                tokens.append((m, SYNTAX_COLORS["keyword"]))
            elif m in builtins:
                tokens.append((m, SYNTAX_COLORS["builtin"]))
            elif m.replace('.', '', 1).isdigit():
                tokens.append((m, SYNTAX_COLORS["number"]))
            elif re.match(r'^[+\-*/%=<>!&|^~:]+$', m):
                tokens.append((m, SYNTAX_COLORS["operator"]))
            else:
                tokens.append((m, SYNTAX_COLORS["identifier"]))

        return tokens

    def draw(self, surface):
        # 1. Background Frame Editor
        pygame.draw.rect(surface, (12, 10, 20), self.rect, border_radius=6)
        pygame.draw.rect(surface, (60, 50, 85), self.rect, 1, border_radius=6)
        
        # Kolom Nomor Baris (Gutter)
        gutter_w = 34
        pygame.draw.rect(surface, (20, 16, 32), (self.rect.x, self.rect.y, gutter_w, self.rect.height), border_top_left_radius=6, border_bottom_left_radius=6)
        pygame.draw.line(surface, (50, 42, 70), (self.rect.x + gutter_w, self.rect.y), (self.rect.x + gutter_w, self.rect.y + self.rect.height), 1)

        # 2. Render Baris & Token
        text_x_start = self.rect.x + gutter_w + 8
        max_visible_rows = (self.rect.height - 12) // self.line_height

        for i, line in enumerate(self.lines):
            row_y = self.rect.y + 6 + i * self.line_height
            if row_y + self.line_height > self.rect.y + self.rect.height:
                break  # Diluar area tampak

            # Nomor baris
            num_surf = self.font_num.render(str(i + 1), True, (120, 110, 140))
            surface.blit(num_surf, (self.rect.x + gutter_w - num_surf.get_width() - 6, row_y + 2))

            # Highlight baris aktif
            if i == self.cursor_row:
                active_rect = pygame.Rect(self.rect.x + gutter_w + 1, row_y - 1, self.rect.width - gutter_w - 2, self.line_height)
                pygame.draw.rect(surface, (28, 22, 48), active_rect)

            # Tokenize & render teks syntax
            tokens = self._tokenize_line(line)
            curr_x = text_x_start
            for text_chunk, color in tokens:
                chunk_surf = self.font.render(text_chunk, True, color)
                surface.blit(chunk_surf, (curr_x, row_y))
                curr_x += chunk_surf.get_width()

            # Kursor Berkedip
            if i == self.cursor_row and self.show_cursor:
                # Hitung offset x kursor berdasarkan substring sebelum cursor_col
                sub = line[:self.cursor_col]
                cx = text_x_start + self.font.size(sub)[0]
                pygame.draw.line(surface, COLOR_PASTEL_PINK, (cx, row_y + 1), (cx, row_y + self.line_height - 3), 2)


class Button:
    """Tombol interaktif dengan hover effect dan audio feedback."""
    def __init__(self, rect, text, bg_color=COLOR_PASTEL_PURPLE, text_color=COLOR_WHITE, icon=None):
        self.rect = rect
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = UIHelper.get_font(13, bold=True)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                audio_sys.play("click")
                return True
        return False

    def draw(self, surface):
        col = (min(255, self.bg_color[0] + 30), min(255, self.bg_color[1] + 30), min(255, self.bg_color[2] + 30)) if self.is_hovered else self.bg_color
        
        # Bayangan tombol
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (10, 8, 16), shadow_rect, border_radius=6)
        
        # Badan tombol
        pygame.draw.rect(surface, col, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_WHITE if self.is_hovered else (200, 200, 220), self.rect, 2, border_radius=6)
        
        # Teks
        txt_surf = self.font.render(self.text, True, self.text_color)
        tx = self.rect.centerx - txt_surf.get_width() // 2
        ty = self.rect.centery - txt_surf.get_height() // 2
        surface.blit(txt_surf, (tx, ty))


class ToastNotification:
    """Banner notifikasi mengambang saat mendapatkan item / progress quest."""
    def __init__(self):
        self.message = ""
        self.timer = 0.0
        self.duration = 4.0
        self.color = COLOR_SUCCESS_GREEN
        self.font = UIHelper.get_font(14, bold=True)

    def show(self, text, color=COLOR_SUCCESS_GREEN):
        self.message = text
        self.color = color
        self.timer = self.duration

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def draw(self, surface):
        if self.timer <= 0:
            return

        # Animasi slide down
        slide = min(1.0, (self.duration - self.timer) * 4.0)
        target_y = int(30 * slide)
        
        msg_surf = self.font.render(self.message, True, COLOR_WHITE)
        w = msg_surf.get_width() + 40
        h = 36
        x = SCREEN_WIDTH // 2 - w // 2
        
        toast_rect = pygame.Rect(x, target_y, w, h)
        UIHelper.draw_omori_box(surface, toast_rect, bg_color=(20, 16, 36, 240), border_color=self.color)
        
        # Ikon bintang kecil
        pygame.draw.circle(surface, self.color, (x + 18, target_y + h // 2), 5)
        surface.blit(msg_surf, (x + 30, target_y + 9))


class QuestModal:
    """Pop-up GUI dialog quest komprehensif bergaya OMORI."""
    def __init__(self):
        self.is_active = False
        self.quest_data = None
        self.player_ref = None
        self.on_quest_complete_cb = None
        
        # Window Rect
        self.rect = pygame.Rect(50, 40, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 80)
        
        # Tabs ("MATERI & CERITA", "KODING & TANTANGAN")
        self.current_tab = "code" # "lesson" atau "code"
        self.tab_lesson_rect = pygame.Rect(self.rect.x + 24, self.rect.y + 110, 180, 28)
        self.tab_code_rect = pygame.Rect(self.rect.x + 210, self.rect.y + 110, 180, 28)
        
        # Code Editor
        editor_w = self.rect.width - 48
        editor_h = 220
        self.editor = CodeEditorBox(pygame.Rect(self.rect.x + 24, self.rect.y + 145, editor_w, editor_h))
        
        # Buttons
        btn_y = self.rect.y + self.rect.height - 50
        self.btn_submit = Button(pygame.Rect(self.rect.x + self.rect.width - 190, btn_y, 166, 34), "▶ Kirim & Jalankan", bg_color=(45, 140, 95))
        self.btn_hint = Button(pygame.Rect(self.rect.x + self.rect.width - 340, btn_y, 136, 34), "💡 Petunjuk", bg_color=(160, 120, 45))
        self.btn_reset = Button(pygame.Rect(self.rect.x + 24, btn_y, 110, 34), "↺ Reset", bg_color=(120, 50, 70))
        self.btn_close = Button(pygame.Rect(self.rect.x + self.rect.width - 36, self.rect.y + 10, 26, 26), "X", bg_color=(180, 40, 60))
        
        # Feedback & Status Message
        self.feedback_msg = None
        self.feedback_is_success = False
        self.hint_index = 0
        
        # Typewriter Story Text
        self.story_chars_revealed = 0
        self.story_timer = 0.0

    def open(self, quest_dict, player, on_complete):
        self.is_active = True
        self.quest_data = quest_dict
        self.player_ref = player
        self.on_quest_complete_cb = on_complete
        
        self.current_tab = "code"
        self.editor.set_text(quest_dict["initial_code"])
        self.feedback_msg = None
        self.feedback_is_success = False
        self.hint_index = 0
        self.story_chars_revealed = 0
        self.story_timer = 0.0
        
        audio_sys.play("item")

    def close(self):
        self.is_active = False

    def handle_event(self, event, mouse_pos):
        if not self.is_active:
            return

        # Klik Tab
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.tab_lesson_rect.collidepoint(mouse_pos):
                self.current_tab = "lesson"
                audio_sys.play("click")
                return
            elif self.tab_code_rect.collidepoint(mouse_pos):
                self.current_tab = "code"
                audio_sys.play("click")
                return

        # Tombol Aksi
        if self.btn_close.is_clicked(event):
            self.close()
            return

        if self.btn_reset.is_clicked(event):
            self.editor.set_text(self.quest_data["initial_code"])
            self.feedback_msg = "Kode direset ke template awal."
            self.feedback_is_success = False
            return

        if self.btn_hint.is_clicked(event):
            hints = self.quest_data.get("hints", [])
            if hints:
                self.feedback_msg = f"💡 Petunjuk: {hints[self.hint_index % len(hints)]}"
                self.hint_index += 1
                self.feedback_is_success = False
                audio_sys.play_blip("high")
            return

        if self.btn_submit.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_F5):
            self._evaluate_submission()
            return

        # Handle Editor Keyboard Input
        if self.current_tab == "code":
            self.editor.handle_event(event)

    def _evaluate_submission(self):
        """Memverifikasi kode pemain menggunakan validator quest."""
        code_str = self.editor.get_text()
        validator_fn = self.quest_data["validator"]
        success, msg = validator_fn(code_str)
        
        self.feedback_msg = msg
        self.feedback_is_success = success
        
        if success:
            audio_sys.play("success")
            reward = self.quest_data["reward_item"]
            self.player_ref.add_reward_item(reward)
            if self.on_quest_complete_cb:
                self.on_quest_complete_cb(self.quest_data)
        else:
            audio_sys.play("error")

    def update(self, dt, mouse_pos):
        if not self.is_active:
            return

        self.editor.update(dt)
        self.btn_submit.update(mouse_pos)
        self.btn_hint.update(mouse_pos)
        self.btn_reset.update(mouse_pos)
        self.btn_close.update(mouse_pos)

        # Typewriter story progression
        if self.story_chars_revealed < len(self.quest_data["story"]):
            self.story_timer += dt
            if self.story_timer >= 0.02:
                self.story_timer = 0.0
                self.story_chars_revealed += 1
                audio_sys.play_blip(self.quest_data.get("npc_blip", "mid"))

    def draw(self, surface, npc_portrait=None):
        if not self.is_active:
            return

        # Dimmer background layar
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((10, 8, 20, 175))
        surface.blit(dim_surf, (0, 0))

        # Main Box OMORI Frame
        UIHelper.draw_omori_box(surface, self.rect, bg_color=(20, 16, 34, 245), border_color=COLOR_PASTEL_PURPLE)
        
        # 1. Header (Portrait NPC + Nama & Title + Lokasi Quest)
        header_y = self.rect.y + 16
        if npc_portrait:
            surface.blit(npc_portrait, (self.rect.x + 20, header_y))
        
        # Info NPC & Quest
        title_font = UIHelper.get_font(16, bold=True)
        sub_font = UIHelper.get_font(12, bold=False)
        
        # Quest Badge
        q_badge = f"[ QUEST {self.quest_data['id']}/10 : {self.quest_data['location'].upper()} ]"
        badge_surf = sub_font.render(q_badge, True, COLOR_PASTEL_MINT)
        surface.blit(badge_surf, (self.rect.x + 115, header_y + 2))
        
        # Nama NPC
        npc_name_surf = title_font.render(self.quest_data["npc_name"], True, COLOR_WHITE)
        surface.blit(npc_name_surf, (self.rect.x + 115, header_y + 22))
        
        # Topik Materi
        topic_surf = sub_font.render(f"Topik: {self.quest_data['topic']}", True, COLOR_PASTEL_YELLOW)
        surface.blit(topic_surf, (self.rect.x + 115, header_y + 45))

        # Narasi Cerita (Typewriter)
        story_font = UIHelper.get_font(12, bold=False)
        story_revealed = self.quest_data["story"][:self.story_chars_revealed]
        for idx, s_line in enumerate(story_revealed.split("\n")):
            st_surf = story_font.render(s_line, True, (210, 205, 230))
            surface.blit(st_surf, (self.rect.x + 115, header_y + 68 + idx * 16))

        # 2. Render Tabs
        # Tab Lesson
        col_l = COLOR_PASTEL_PURPLE if self.current_tab == "lesson" else (40, 32, 60)
        pygame.draw.rect(surface, col_l, self.tab_lesson_rect, border_top_left_radius=6, border_top_right_radius=6)
        pygame.draw.rect(surface, COLOR_WHITE, self.tab_lesson_rect, 2, border_top_left_radius=6, border_top_right_radius=6)
        t_l_surf = sub_font.render("📖 Materi & Konsep", True, COLOR_WHITE)
        surface.blit(t_l_surf, (self.tab_lesson_rect.x + 20, self.tab_lesson_rect.y + 6))

        # Tab Code
        col_c = COLOR_PASTEL_PURPLE if self.current_tab == "code" else (40, 32, 60)
        pygame.draw.rect(surface, col_c, self.tab_code_rect, border_top_left_radius=6, border_top_right_radius=6)
        pygame.draw.rect(surface, COLOR_WHITE, self.tab_code_rect, 2, border_top_left_radius=6, border_top_right_radius=6)
        t_c_surf = sub_font.render("⌨️ Editor Kode & Soal", True, COLOR_WHITE)
        surface.blit(t_c_surf, (self.tab_code_rect.x + 15, self.tab_code_rect.y + 6))

        # 3. Isi Tab
        if self.current_tab == "lesson":
            # Tampilkan Penjelasan Materi Edukatif
            lesson_rect = pygame.Rect(self.rect.x + 24, self.rect.y + 145, self.rect.width - 48, 260)
            UIHelper.draw_omori_box(surface, lesson_rect, bg_color=(14, 10, 24, 250), border_color=(80, 70, 110))
            
            l_font = UIHelper.get_font(13, bold=False)
            task_font = UIHelper.get_font(13, bold=True)
            
            lines = self.quest_data["lesson"].split("\n") + ["", "---"] + self.quest_data["task"].split("\n")
            for i, line in enumerate(lines):
                if i * 20 > lesson_rect.height - 25:
                    break
                is_task = "TUGAS:" in line or "1." in line or "2." in line or "3." in line
                f = task_font if is_task else l_font
                c = COLOR_PASTEL_YELLOW if is_task else (235, 230, 245)
                line_surf = f.render(line, True, c)
                surface.blit(line_surf, (lesson_rect.x + 16, lesson_rect.y + 14 + i * 20))
        else:
            # Tampilkan Editor Kode
            self.editor.draw(surface)

            # Task Prompt Ringkas di Atas/Bawah Editor
            task_short_rect = pygame.Rect(self.rect.x + 24, self.rect.y + 372, self.rect.width - 48, 48)
            pygame.draw.rect(surface, (16, 12, 28), task_short_rect, border_radius=4)
            pygame.draw.rect(surface, (60, 50, 80), task_short_rect, 1, border_radius=4)
            
            prompt_font = UIHelper.get_font(12, bold=False)
            task_first_line = self.quest_data["task"].split("\n")[1] if len(self.quest_data["task"].split("\n")) > 1 else self.quest_data["task"]
            p_surf = prompt_font.render(f"Instruksi: {task_first_line}", True, COLOR_PASTEL_MINT)
            surface.blit(p_surf, (task_short_rect.x + 10, task_short_rect.y + 8))
            
            # Sub-instruksi jika ada
            task_lines = self.quest_data["task"].split("\n")
            if len(task_lines) > 2:
                p2_surf = prompt_font.render(task_lines[2], True, (210, 210, 230))
                surface.blit(p2_surf, (task_short_rect.x + 10, task_short_rect.y + 26))

        # 4. Feedback Banner
        if self.feedback_msg:
            fb_y = self.rect.y + self.rect.height - 100
            fb_rect = pygame.Rect(self.rect.x + 24, fb_y, self.rect.width - 48, 40)
            fb_col = COLOR_SUCCESS_GREEN if self.feedback_is_success else COLOR_ERROR_RED
            
            pygame.draw.rect(surface, (20, 14, 30), fb_rect, border_radius=6)
            pygame.draw.rect(surface, fb_col, fb_rect, 2, border_radius=6)
            
            fb_font = UIHelper.get_font(13, bold=True)
            fb_surf = fb_font.render(self.feedback_msg, True, fb_col)
            surface.blit(fb_surf, (fb_rect.x + 14, fb_rect.y + 11))

        # 5. Render Buttons
        self.btn_submit.draw(surface)
        self.btn_hint.draw(surface)
        self.btn_reset.draw(surface)
        self.btn_close.draw(surface)
