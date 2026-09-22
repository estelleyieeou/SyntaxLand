"""
sound_gen.py - Generator Efek Suara Prosedural Retro (Zero-Asset Sound Synthesizer).
Membuat efek suara secara dinamis menggunakan in-memory WAV PCM sehingga tidak membutuhkan file audio eksternal.
"""

import math
import struct
import io
import pygame

class SoundManager:
    """Mengelola dan memutar efek audio yang disintesis secara prosedural."""
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self.last_blip_time = 0
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._pregenerate_sounds()
        except Exception as e:
            print(f"[SoundManager] Warning: Audio mixer tidak dapat diinisialisasi ({e}). Melanjutkan tanpa audio.")
            self.enabled = False

    def _generate_wav(self, duration_sec, freq_fn, sample_rate=22050, volume=0.4):
        """Membuat buffer WAV 16-bit mono dari fungsi frekuensi/amplitudo dinamis."""
        num_samples = int(duration_sec * sample_rate)
        wav_buffer = io.BytesIO()
        
        # WAV Header & Data Construction
        with io.BytesIO() as bio:
            # Tulis dummy header (44 byte), data sample, lalu patch header
            raw_samples = bytearray()
            for i in range(num_samples):
                t = i / sample_rate
                # Dapatkan sample amplitude (-1.0 to 1.0)
                amp = freq_fn(t, duration_sec)
                # Clamp & scale to 16-bit signed integer
                sample_val = int(max(-1.0, min(1.0, amp * volume)) * 32767)
                raw_samples.extend(struct.pack('<h', sample_val))
            
            data_size = len(raw_samples)
            total_size = 36 + data_size
            
            # RIFF Header
            wav_buffer.write(b'RIFF')
            wav_buffer.write(struct.pack('<I', total_size))
            wav_buffer.write(b'WAVE')
            
            # fmt subchunk
            wav_buffer.write(b'fmt ')
            wav_buffer.write(struct.pack('<I', 16))          # Subchunk1Size
            wav_buffer.write(struct.pack('<H', 1))           # AudioFormat (PCM = 1)
            wav_buffer.write(struct.pack('<H', 1))           # NumChannels (Mono = 1)
            wav_buffer.write(struct.pack('<I', sample_rate)) # SampleRate
            wav_buffer.write(struct.pack('<I', sample_rate * 2)) # ByteRate
            wav_buffer.write(struct.pack('<H', 2))           # BlockAlign
            wav_buffer.write(struct.pack('<H', 16))          # BitsPerSample
            
            # data subchunk
            wav_buffer.write(b'data')
            wav_buffer.write(struct.pack('<I', data_size))
            wav_buffer.write(raw_samples)
            
        wav_buffer.seek(0)
        return wav_buffer

    def _pregenerate_sounds(self):
        """Membuat koleksi suara bawaan saat startup."""
        if not self.enabled:
            return

        # 1. Dialog Typewriter Blip (High & Low pitch)
        def blip_fn(freq):
            return lambda t, dur: (
                math.sin(2 * math.pi * freq * t) * (1.0 - t / dur)
                if (math.sin(2 * math.pi * freq * t) > 0) else -0.5 * (1.0 - t / dur)
            )

        self.sounds["blip_mid"] = self._create_sound(0.04, blip_fn(480), volume=0.25)
        self.sounds["blip_low"] = self._create_sound(0.04, blip_fn(240), volume=0.25)
        self.sounds["blip_high"] = self._create_sound(0.04, blip_fn(720), volume=0.25)

        # 2. Success Victory Fanfare (Arpeggio C5 -> E5 -> G5 -> C6)
        def success_fn(t, dur):
            notes = [523.25, 659.25, 783.99, 1046.50]
            idx = min(int(t / 0.1), 3)
            freq = notes[idx]
            local_t = t - (idx * 0.1)
            decay = max(0.0, 1.0 - (local_t / 0.25))
            return math.sin(2 * math.pi * freq * t) * decay * 0.8

        self.sounds["success"] = self._create_sound(0.45, success_fn, volume=0.45)

        # 3. Error Buzzer Sound
        def error_fn(t, dur):
            # Sawtooth-like low frequency buzz
            freq = 140.0
            phase = (t * freq) % 1.0
            val = (phase * 2.0 - 1.0) * (1.0 - t / dur)
            return val

        self.sounds["error"] = self._create_sound(0.25, error_fn, volume=0.4)

        # 4. Item / Quest Unlock Chime
        def item_fn(t, dur):
            freq = 880 + 440 * (t / dur)
            decay = math.exp(-6 * t)
            return (math.sin(2 * math.pi * freq * t) + 0.5 * math.sin(2 * math.pi * freq * 2 * t)) * decay

        self.sounds["item"] = self._create_sound(0.35, item_fn, volume=0.4)

        # 5. Magic Barrier Dissolve
        def barrier_fn(t, dur):
            base = math.sin(2 * math.pi * (300 + 200 * math.sin(20 * t)) * t)
            return base * (1.0 - t / dur)

        self.sounds["barrier"] = self._create_sound(0.5, barrier_fn, volume=0.35)

        # 6. Button Click
        def click_fn(t, dur):
            return math.sin(2 * math.pi * 800 * t) * (1.0 - t / dur)

        self.sounds["click"] = self._create_sound(0.03, click_fn, volume=0.3)

    def _create_sound(self, duration, freq_fn, volume=0.4):
        """Helper untuk mengonversi buffer wav ke pygame.mixer.Sound."""
        try:
            buf = self._generate_wav(duration, freq_fn, volume=volume)
            return pygame.mixer.Sound(buf)
        except Exception:
            return None

    def play(self, name):
        """Memutar suara dengan nama tertentu."""
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass

    def play_blip(self, pitch="mid"):
        """Memutar suara bleep dialog dengan batasan interval agar tidak bising."""
        now = pygame.time.get_ticks()
        if now - self.last_blip_time > 45:
            key = f"blip_{pitch}" if f"blip_{pitch}" in self.sounds else "blip_mid"
            self.play(key)
            self.last_blip_time = now


# Instance singleton global
audio_sys = SoundManager()
