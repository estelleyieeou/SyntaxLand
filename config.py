"""
config.py - Konfigurasi Game, Palet Warna Surealis (OMORI Headspace), dan Konstanta Sistem.
"""

# Dimensi Layar dan Performa
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "OMORI: Pulau Sintaksis (Python Quest RPG)"

# Ukuran Tile Grid
TILE_SIZE = 48
MAP_COLS = 100  # Total lebar dunia terhubung
MAP_ROWS = 15   # Tinggi koridor dunia

# Palet Warna Surealis OMORI (Headspace & White Space)
COLOR_WHITE = (248, 248, 252)
COLOR_BLACK = (14, 12, 24)
COLOR_DARK_PURPLE = (26, 18, 48)
COLOR_DEEP_NAVY = (22, 26, 54)
COLOR_PANEL_BG = (18, 14, 32, 235)  # RGBA untuk modal transparan

# Warna Pastel Headspace
COLOR_PASTEL_PURPLE = (175, 145, 225)
COLOR_PASTEL_PINK = (255, 175, 210)
COLOR_PASTEL_MINT = (145, 240, 215)
COLOR_PASTEL_YELLOW = (255, 240, 180)
COLOR_PASTEL_BLUE = (150, 205, 255)
COLOR_PASTEL_ORANGE = (255, 195, 150)

# Warna Zona Wilayah (10 Area Tematik)
ZONE_COLORS = {
    0: {"name": "Pantai Hampa", "ground": (245, 228, 190), "accent": (145, 210, 245), "path": (225, 205, 160)},
    1: {"name": "Hutan Bisikan", "ground": (58, 85, 72), "accent": (145, 225, 185), "path": (48, 70, 60)},
    2: {"name": "Gua Gema", "ground": (45, 38, 62), "accent": (195, 145, 245), "path": (36, 30, 50)},
    3: {"name": "Rawa Keputusan", "ground": (52, 68, 55), "accent": (160, 210, 150), "path": (40, 52, 42)},
    4: {"name": "Taman Cabang", "ground": (190, 120, 160), "accent": (255, 190, 220), "path": (165, 100, 138)},
    5: {"name": "Lembah Berulang", "ground": (75, 62, 105), "accent": (210, 170, 255), "path": (60, 48, 88)},
    6: {"name": "Pasar Misteri", "ground": (140, 95, 65), "accent": (255, 215, 140), "path": (118, 78, 52)},
    7: {"name": "Menara Waktu", "ground": (85, 45, 70), "accent": (255, 145, 175), "path": (68, 35, 56)},
    8: {"name": "Kuil Mantra", "ground": (42, 68, 110), "accent": (140, 200, 255), "path": (32, 52, 88)},
    9: {"name": "Dermaga Tua", "ground": (110, 75, 95), "accent": (255, 180, 190), "path": (88, 58, 75)},
}

# Warna UI dan Syntax Highlighter
SYNTAX_COLORS = {
    "keyword": (255, 140, 190),      # def, return, if, elif, else, for, while, in, try, except
    "builtin": (140, 220, 255),      # print, input, range, len, str, int, float, bool, list, dict
    "string": (255, 220, 140),       # "text", 'text'
    "number": (160, 245, 180),       # 123, 45.6
    "comment": (140, 135, 165),      # # komentar
    "operator": (255, 170, 150),     # +, -, *, /, %, ==, !=, =, :, (, )
    "identifier": (245, 245, 250),   # variabel umum
}

# Warna Status Quest & Efek
COLOR_SUCCESS_GREEN = (100, 240, 160)
COLOR_ERROR_RED = (255, 110, 130)
COLOR_HINT_YELLOW = (255, 235, 130)
COLOR_BARRIER_GLOW = (220, 160, 255)

# Status Game (State Machine)
STATE_TITLE = "TITLE"
STATE_INTRO = "INTRO"
STATE_OVERWORLD = "OVERWORLD"
STATE_QUEST = "QUEST"
STATE_INVENTORY = "INVENTORY"
STATE_ENDING = "ENDING"
