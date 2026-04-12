import json
import os

SAVE_FILE = "Data/save_data.json"

class SaveManager:
    def __init__(self):
        self.saveFile = SAVE_FILE

    # Internal
    def _collectData(self) -> dict:
        import Global
        return {
            "currentRound":          Global.currentRound,
            "currentDifficulty":     Global.currentDifficulty,
            "playerStats":           Global.playerStats.copy(),
            "playerStatsMultiplier": Global.playerStatsMultiplier.copy(),
            "playerStatsGain":       Global.playerStatsGain.copy(),
            "playerStatsLose":       Global.playerStatsLose.copy(),
            "currentRarity":         Global.currentRarity.copy(),
            "money":                 Global.money,
            "gameProgress":          Global.gameProgress,
        }

    def _applyData(self, data: dict):
        import Global
        Global.currentRound          = data.get("currentRound",          1)
        Global.currentDifficulty     = data.get("currentDifficulty",     "Normal")
        Global.playerStats           = data.get("playerStats",           Global.defaultData.playerStats.copy())
        Global.playerStatsMultiplier = data.get("playerStatsMultiplier", Global.defaultData.playerStatsMultiplier.copy())
        Global.playerStatsGain       = data.get("playerStatsGain",       Global.defaultData.playerStatsGain.copy())
        Global.playerStatsLose       = data.get("playerStatsLose",       Global.defaultData.playerStatsLose.copy())
        Global.currentRarity         = data.get("currentRarity",         Global.defaultData.startRarity.copy())
        Global.money                 = data.get("money",                 0)
        Global.gameProgress          = data.get("gameProgress",          Global.defaultData.gameProgress.copy())

    # Save / Load
    def save(self):
        """Save current game state to file."""
        data = self._collectData()
        with open(self.saveFile, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[SaveManager] Saved to {self.saveFile}")

    def load(self) -> bool:
        """Load game state from file. Returns True if successful."""
        if not os.path.exists(self.saveFile):
            print("[SaveManager] No save file found.")
            return False
        try:
            with open(self.saveFile, "r") as f:
                data = json.load(f)
            self._applyData(data)
            print(f"[SaveManager] Loaded from {self.saveFile}")
            return True
        except Exception as e:
            print(f"[SaveManager] Failed to load: {e}")
            return False

    def deleteSave(self):
        """Delete the save file."""
        if os.path.exists(self.saveFile):
            os.remove(self.saveFile)
            print("[SaveManager] Save deleted.")

    def hasSave(self) -> bool:
        return os.path.exists(self.saveFile)

    # Revert
    def saveCheckpoint(self):
        """Save a checkpoint at the start of each round to revert to on death."""
        data = self._collectData()
        checkpoint_file = self.saveFile.replace(".json", "_checkpoint.json")
        with open(checkpoint_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[SaveManager] Checkpoint saved at round {data['currentRound']}")

    def revertToCheckpoint(self):
        """Revert to last checkpoint (e.g. on player death)."""
        checkpoint_file = self.saveFile.replace(".json", "_checkpoint.json")
        if not os.path.exists(checkpoint_file):
            print("[SaveManager] No checkpoint found, reverting to defaults.")
            self.resetToDefault()
            return False
        try:
            with open(checkpoint_file, "r") as f:
                data = json.load(f)
            self._applyData(data)
            print(f"[SaveManager] Reverted to checkpoint at round {data['currentRound']}")
            return True
        except Exception as e:
            print(f"[SaveManager] Failed to revert: {e}")
            return False

    # Reset
    def resetToDefault(self):
        """Wipe everything and restore default data."""
        import Global, copy
        Global.currentRound          = 1
        Global.currentDifficulty     = "Normal"
        Global.playerStats           = Global.defaultData.playerStats.copy()
        Global.playerStatsMultiplier = Global.defaultData.playerStatsMultiplier.copy()
        Global.playerStatsGain       = Global.defaultData.playerStatsGain.copy()
        Global.playerStatsLose       = Global.defaultData.playerStatsLose.copy()
        Global.currentRarity         = Global.defaultData.startRarity.copy()
        Global.money                 = 0
        Global.gameProgress          = copy.deepcopy(Global.defaultData.gameProgress)
        print(Global.defaultData.gameProgress["Normal"]["Round20"])
        print("[SaveManager] Reset to defaults.")