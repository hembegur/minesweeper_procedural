import pygame
import Global

class soundManager:
    def __init__(self):
        pygame.mixer.init()
        self._sounds  = {}   # cached Sound objects
        self._music   = None # current music path
        self.sfxVolume   = 1.0
        self.musicVolume = 1.0
        self.muted       = False

    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _load(self, path: str) -> pygame.mixer.Sound:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        return self._sounds[path]

    # ──────────────────────────────────────────
    # SFX
    # ──────────────────────────────────────────

    def playSFX(self, path: str, volume: float = 1.0, loops: int = 0):
        """Play a sound effect once."""
        if self.muted:
            return
        sound = self._load(path)
        sound.set_volume(self.sfxVolume * volume)
        sound.play(loops=loops)

    def stopSFX(self, path: str):
        if path in self._sounds:
            self._sounds[path].stop()

    def setSFXVolume(self, volume: float):
        self.sfxVolume = max(0.0, min(1.0, volume))

    # ──────────────────────────────────────────
    # Music
    # ──────────────────────────────────────────

    def playMusic(self, path: str, loops: int = -1, fadeIn: float = 0):
        """Play background music. loops=-1 = infinite."""
        if self._music == path and pygame.mixer.music.get_busy():
            return  # already playing
        self._music = path
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.musicVolume if not self.muted else 0)
        if fadeIn > 0:
            pygame.mixer.music.play(loops=loops, fade_ms=int(fadeIn * 1000))
        else:
            pygame.mixer.music.play(loops=loops)

    def stopMusic(self, fadeOut: float = 0):
        if fadeOut > 0:
            pygame.mixer.music.fadeout(int(fadeOut * 1000))
        else:
            pygame.mixer.music.stop()
        self._music = None

    def pauseMusic(self):
        pygame.mixer.music.pause()

    def resumeMusic(self):
        pygame.mixer.music.unpause()

    def setMusicVolume(self, volume: float):
        self.musicVolume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.musicVolume if not self.muted else 0)

    def isMusicPlaying(self) -> bool:
        return pygame.mixer.music.get_busy()

    # ──────────────────────────────────────────
    # Global mute
    # ──────────────────────────────────────────

    def setMute(self, muted: bool):
        self.muted = muted
        pygame.mixer.music.set_volume(0 if muted else self.musicVolume)

    def toggleMute(self):
        self.setMute(not self.muted)

    # ──────────────────────────────────────────
    # Preload
    # ──────────────────────────────────────────

    def preload(self, paths: list):
        """Load sounds ahead of time to avoid lag on first play."""
        for path in paths:
            self._load(path)