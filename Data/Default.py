class DefaultData:
    def __init__(self):
        self.startRarity = {
            "Common" : 70,
            "Rare" : 25,
            "Epic" : 5,
        }
        self.targetRarity = {
            "Common": 30,
            "Rare": 35,
            "Epic": 35,
        }

        self.playerStats = {
            "HP" :  100,
            "MP" :  0,
            "Ult" : 0,
            "MaxHP" : 100,
            "MaxMP" : 10,
            "MaxUlt" : 1,
            "NormalDamage" : 10,
            "BaseAttackSpeed" : 250,
            "AttackSpeed": 100,
            "Burst" : 1,
            "BurstAttackSpeed": 800,
            "HPRegen" : 0,
            "Defense" : 0,
            "LifeSteal" : 0,
            "Aoe" : 0,
        }
        self.playerStatsMultiplier = {
            "NormalDamage" : 0,
            "UltDamage" : 0,
        }
        self.playerStatsGain = {
            "HP" :  1,
            "MP" :  1,
            "Ult" : 1,
        }
        self.playerStatsLose = {
            "HP" :  1,
            "MP" :  1,
            "Ult" : 1,
        }

        self.enemyStats = {
            "SpikeEnemy" : {
                "HP" : 30,
                "Damage" : 25,
                "CD": 4,
                "Money": 60,
            },
            "LaserEnemy" : {
                "HP" : 25,
                "Damage" : 25,
                "CD": 4,
                "Money": 70,
            },
            "ClownEnemy" : {
                "HP" : 40,
                "PunchDamage" : 30,
                "SpikeDamage" : 10,
                "CD": 4,
                "Money": 80,
            },
            "MinigunEnemy" : {
                "HP" : 40,
                "Damage" : 10,
                "CD": 6,
                "BulletCount": 30,
                "Money": 100,
            },
            "Monki" : { #BOSS
                "HP" : 1800,
                "CD": 5,
                "Money": 10000,
                "PunchDamage" : 80,
                "PunchCount" : 12,
                "BananaDamage" : 60,
                "LaserDamage" : 80,
            }
        }
        self.difficultyScale = {
            "Normal": {
                "HPScale":     0.2,
                "DamageScale": 0.2,
                "MoneyScale": 0.05,
                "PriceScale": 0.08,
            }
        }

        self.rarityColor = {
            "Common" : { 
                "color" : (250, 250, 250, 255), 
                "borderColor" : (50, 50, 50, 255) 
            },
            "Rare": {
                "color": (180, 210, 255, 255),
                "borderColor": (0, 100, 255, 255)
            },
            "Epic": {
                "color": (220, 180, 255, 255),
                "borderColor": (180, 0, 255, 255)
            }
        }
        self.gameProgress = {
            "Normal": {
                # ===== EARLY GAME (SPIKE ONLY) =====
                "Round1": {
                    "SpawnRate": (9,10), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 5, "MaxEnemy": 3},
                    #"SpikeEnemy": {"EnemyLeft": 2, "MaxEnemy": 1},
                },

                "Round2": {
                    "SpawnRate": (9,10), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                },

                "Round3": {
                    "SpawnRate": (8,10), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 12, "MaxEnemy": 5},
                },

                # ===== INTRO LASER =====
                "Round4": {
                    "SpawnRate": (8,10), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 10, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 4, "MaxEnemy": 3},
                },

                "Round5": {
                    "SpawnRate": (8,9), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                },

                "Round6": {
                    "SpawnRate": (8,9), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 6},
                    "LaserEnemy": {"EnemyLeft": 10, "MaxEnemy": 5},
                },

                # ===== INTRO CLOWN =====
                "Round7": {
                    "SpawnRate": (7,9), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 10, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 2, "MaxEnemy": 1},
                },

                "Round8": {
                    "SpawnRate": (7,9), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 12, "MaxEnemy": 5},
                    "ClownEnemy": {"EnemyLeft": 3, "MaxEnemy": 1},
                },

                "Round9": {
                    "SpawnRate": (7,9), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 18, "MaxEnemy": 6},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                },

                # ===== INTRO MINIGUN =====
                "Round10": {
                    "SpawnRate": (7,8), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 12, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 3, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round11": {
                    "SpawnRate": (7,8), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 18, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round12": {
                    "SpawnRate": (7,8), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 20, "MaxEnemy": 6},
                    "LaserEnemy": {"EnemyLeft": 16, "MaxEnemy": 5},
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                # ===== SPECIAL ROUND =====
                "Round13": {
                    "SpawnRate": (6,8), "SpawnBurst": (8,12),
                    "SpikeEnemy": {"EnemyLeft": 40, "MaxEnemy": 15},
                },
                # ===== MID GAME (ALL ENEMIES) =====
                "Round14": {
                    "SpawnRate": (6,8), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 22, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 20, "MaxEnemy": 5},
                    "ClownEnemy": {"EnemyLeft": 5, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round15": {
                    "SpawnRate": (6,8), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 24, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 22, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 6, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                # ===== LATE GAME (HIGH PRESSURE) =====
                "Round16": {
                    "SpawnRate": (6,7), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 26, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 24, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 6, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                "Round17": {
                    "SpawnRate": (6,7), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 28, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 26, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 7, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                "Round18": {
                    "SpawnRate": (6,7), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 30, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 28, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 7, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                "Round19": {
                    "SpawnRate": (6,7), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 32, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 30, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 8, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                # ===== BOSS =====
                "Round20": {
                    "SpawnRate": (1,1), "SpawnBurst": (1,1),
                    "Monki": {"EnemyLeft": 1, "MaxEnemy": 1},
                }
            }
        }