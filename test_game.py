"""
test_game.py - Skrip Pengujian Otomatis untuk Validator 10 Quest, Sintaksis, dan Alur Permainan.
"""

import sys
import os
import io

# Pastikan UTF-8 encoding jika didukung
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import pygame
import config
from quests import QUEST_DATA, QuestValidator

def test_all_quests():
    print("==================================================")
    print("MULAI PENGUJIAN 10 VALIDATOR QUEST PYTHON")
    print("==================================================")
    
    passed_count = 0
    
    for q in QUEST_DATA:
        qid = q["id"]
        title = q["topic"]
        print(f"\n[Menguji Quest {qid}]: {title} ({q['location']})")
        
        # 1. Uji dengan initial_code (solusi template yang benar)
        init_code = q["initial_code"]
        success, msg = q["validator"](init_code)
        
        if success:
            print(f"  [OK] Solusi Benar Berhasil Diverifikasi: {msg}")
            passed_count += 1
        else:
            print(f"  [FAIL] GAGAL pada Solusi Template: {msg}")
            return False

        # 2. Uji dengan kode salah / sengaja salah untuk memastikan hint muncul
        wrong_code = "variabel_salah = 999999\n"
        w_success, w_msg = q["validator"](wrong_code)
        if not w_success:
            print(f"  [OK] Validasi Kesalahan Berfungsi (Pesan: {w_msg})")
        else:
            print(f"  [FAIL] GAGAL: Validator menerima kode salah tanpa error.")
            return False

    print("\n==================================================")
    print(f"HASIL: {passed_count}/{len(QUEST_DATA)} QUEST BERHASIL 100%!")
    print("==================================================")
    return True


def test_game_headless_simulation():
    print("\n==================================================")
    print("PENGUJIAN SIMULASI LOOP GAME HEADLESS (Pygame Dummy)")
    print("==================================================")
    
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    
    from main import OmoriPythonGame
    game = OmoriPythonGame()
    
    # 1. State Title -> Intro
    print("1. Menguji State TITLE...")
    assert game.state == config.STATE_TITLE, "State awal harus TITLE"
    
    # Simulasikan Enter
    dummy_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(dummy_event)
    game._handle_events((0, 0))
    assert game.state == config.STATE_INTRO, "State harus bertransisi ke INTRO"
    print("  [OK] Transisi TITLE -> INTRO Berhasil.")
    
    # 2. State Intro -> Overworld
    print("2. Menguji State INTRO...")
    game.intro_step = len(game.intro_texts) - 1
    game.intro_char_count = len(game.intro_texts[-1])
    dummy_event2 = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    pygame.event.post(dummy_event2)
    game._handle_events((0, 0))
    assert game.state == config.STATE_OVERWORLD, "State harus bertransisi ke OVERWORLD"
    print("  [OK] Transisi INTRO -> OVERWORLD Berhasil.")

    # 3. Uji pergerakan pemain di Overworld
    print("3. Menguji Pergerakan Pemain...")
    initial_x = game.player.x
    dummy_keys = {pygame.K_d: True}
    pygame.key.get_pressed = lambda: dummy_keys
    game._update(0.1, (0, 0))
    assert game.player.x > initial_x, "Pemain harus bergerak ke kanan saat tombol D ditekan"
    print("  [OK] Pergerakan dan update pemain Berhasil.")

    # 4. Uji interaksi quest NPC 1
    print("4. Menguji Interaksi NPC & Modal Quest...")
    npc1 = game.world_map.npcs[0]
    game.player.x = npc1.x
    game.player.y = npc1.y
    game.player.check_npc_interaction(game.world_map.npcs)
    
    dummy_event_e = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    pygame.event.post(dummy_event_e)
    game._handle_events((0, 0))
    assert game.state == config.STATE_QUEST, "State harus bertransisi ke QUEST saat tekan E"
    assert game.quest_modal.is_active is True, "Quest modal harus aktif"
    print("  [OK] Pembukaan Quest Modal Berhasil.")

    # 5. Uji penyelesaian Quest 1
    print("5. Menguji Submit Jawaban Quest...")
    game.quest_modal._evaluate_submission()
    assert len(game.player.inventory) == 1, "Inventaris harus bertambah 1 item setelah submit benar"
    assert game.player.current_quest_index == 1, "Indeks quest pemain harus bertambah ke 1"
    print(f"  [OK] Item didapat: {game.player.inventory[0]}")

    # 6. Uji Rendering Frame tanpa crash
    print("6. Menguji Rendering Layar...")
    game._render()
    print("  [OK] Seluruh frame GUI, Tilemap, NPC, dan UI ter-render tanpa exception.")

    print("\n==================================================")
    print("SEMUA PENGUJIAN OTOMATIS SUKSES 100%!")
    print("==================================================")
    return True


if __name__ == "__main__":
    if test_all_quests() and test_game_headless_simulation():
        print("\nSELURUH VALIDASI BERHASIL!")
        sys.exit(0)
    else:
        print("\nADA KEGAGALAN DALAM PENGUJIAN.")
        sys.exit(1)
