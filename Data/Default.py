class DefaultData:
    def __init__(self):
        self.currentRarity = {
            "Common" : 30,
            "Rare" : 30,
            "Epic" : 30,
        }

        self.playerStats = {
            "HP" :  1,
            "MP" :  0,
            "Ult" : 0,
            "MaxHP" : 1,
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
            "NormalDamage" : 100,
            "UltDamage" : 100,
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
                "Damage" : 10,
                "CD": 4
            },
            "LaserEnemy" : {
                "HP" : 25,
                "Damage" : 10,
                "CD": 4
            },
            "ClownEnemy" : {
                "HP" : 40,
                "PunchDamage" : 10,
                "SpikeDamage" : 5,
                "CD": 4,
            },
            "MinigunEnemy" : {
                "HP" : 25,
                "Damage" : 8,
                "CD": 6,
                "BulletCount": 30,
            },
            "Monki" : { #BOSS
                "HP" : 1000,
                "CD": 6,
            }
        }
        self.difficultyScale = {
            "Normal": {
                "SpawnRate": (3, 6),
                "HPScale":     0.08,
                "DamageScale": 0.08,
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
                "Round1": {
                    "SpawnRate": (11,12), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 3, "MaxEnemy": 2},
                },

                "Round2": {
                    "SpawnRate": (11,12), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 6, "MaxEnemy": 3},
                },

                "Round3": {
                    "SpawnRate": (10,12), "SpawnBurst": (1,2),
                    "SpikeEnemy": {"EnemyLeft": 5, "MaxEnemy": 3},
                    "LaserEnemy": {"EnemyLeft": 3, "MaxEnemy": 2},
                },

                "Round4": {
                    "SpawnRate": (10,11), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 5, "MaxEnemy": 3},
                },

                "Round5": {
                    "SpawnRate": (10,11), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 10, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                },

                "Round6": {
                    "SpawnRate": (10,11), "SpawnBurst": (2,3),
                    "ClownEnemy": {"EnemyLeft": 2, "MaxEnemy": 1},
                    "SpikeEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                },

                "Round7": {
                    "SpawnRate": (9,11), "SpawnBurst": (2,3),
                    "SpikeEnemy": {"EnemyLeft": 10, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 8, "MaxEnemy": 4},
                },

                "Round8": {
                    "SpawnRate": (9,11), "SpawnBurst": (2,4),
                    "ClownEnemy": {"EnemyLeft": 3, "MaxEnemy": 1},
                    "LaserEnemy": {"EnemyLeft": 10, "MaxEnemy": 4},
                },

                "Round9": {
                    "SpawnRate": (9,11), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 12, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 10, "MaxEnemy": 5},
                },

                "Round10": {
                    "SpawnRate": (9,10), "SpawnBurst": (2,4),
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                    "SpikeEnemy": {"EnemyLeft": 10, "MaxEnemy": 5},
                },

                "Round11": {
                    "SpawnRate": (9,10), "SpawnBurst": (2,4),
                    "SpikeEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 12, "MaxEnemy": 5},
                },

                "Round12": {
                    "SpawnRate": (9,10), "SpawnBurst": (2,4),
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                    "LaserEnemy": {"EnemyLeft": 12, "MaxEnemy": 5},
                },

                "Round13": {
                    "SpawnRate": (8,10), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 5},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                },

                "Round14": {
                    "SpawnRate": (8,10), "SpawnBurst": (3,4),
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 1},
                    "SpikeEnemy": {"EnemyLeft": 14, "MaxEnemy": 5},
                },

                "Round15": {
                    "SpawnRate": (8,10), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 14, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 12, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round16": {
                    "SpawnRate": (8,9), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 4, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round17": {
                    "SpawnRate": (8,9), "SpawnBurst": (3,4),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 5, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 1, "MaxEnemy": 1},
                },

                "Round18": {
                    "SpawnRate": (8,9), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 18, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 16, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 5, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                "Round19": {
                    "SpawnRate": (8,9), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 18, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 16, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 6, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                },

                "Round20": {
                    "SpawnRate": (8,9), "SpawnBurst": (3,5),
                    "SpikeEnemy": {"EnemyLeft": 16, "MaxEnemy": 4},
                    "LaserEnemy": {"EnemyLeft": 14, "MaxEnemy": 4},
                    "ClownEnemy": {"EnemyLeft": 6, "MaxEnemy": 2},
                    "MinigunEnemy": {"EnemyLeft": 2, "MaxEnemy": 2},
                }
            }
        }
