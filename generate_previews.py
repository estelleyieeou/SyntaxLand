"""
generate_previews.py - Menangkap tangkapan layar (screenshot) representatif dari setiap layar game:
1. Layar Judul (Title Screen)
2. Layar Dunia Eksplorasi (Overworld)
3. Modal Dialog Quest OMORI (Quest Screen)
4. Layar Epilogue / Ending
"""

import os
import pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import config
from main import OmoriPythonGame
from quests import QUEST_DATA

def capture_all():
    artifact_dir = r"C:\Users\ASUS\.gemini\antigravity-ide\brain\60317c38-2e81-419f-b80c-107e7cedf30d"
    os.makedirs(artifact_dir, exist_ok=True)
    
    game = OmoriPythonGame()
    
    # 1. Capture Title Screen
    game.state = config.STATE_TITLE
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_title.png"))
    print("Saved preview_title.png")

    # 2. Capture Intro Screen
    game.state = config.STATE_INTRO
    game.intro_char_count = len(game.intro_texts[0])
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_intro.png"))
    print("Saved preview_intro.png")

    # 3. Capture Overworld Screen
    game.state = config.STATE_OVERWORLD
    game.player.x = 220
    game.player.y = 290
    game.camera.update(game.player.get_hitbox())
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_overworld.png"))
    print("Saved preview_overworld.png")

    # 4. Capture Quest Dialog Modal
    game.state = config.STATE_QUEST
    npc1 = game.world_map.npcs[0]
    game.player.interact_target = npc1
    game.quest_modal.open(QUEST_DATA[0], game.player, game._on_quest_solved)
    game.quest_modal.story_chars_revealed = len(QUEST_DATA[0]["story"])
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_quest.png"))
    print("Saved preview_quest.png")

    # 5. Capture Inventory Modal
    game.state = config.STATE_INVENTORY
    game.player.add_reward_item("Kerang Gema Suara")
    game.player.add_reward_item("Lensa Data Murni")
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_inventory.png"))
    print("Saved preview_inventory.png")

    # 6. Capture Ending Screen
    game.state = config.STATE_ENDING
    game.ending_boat_x = 280
    game._render()
    pygame.image.save(game.screen, os.path.join(artifact_dir, "preview_ending.png"))
    print("Saved preview_ending.png")

if __name__ == "__main__":
    capture_all()
