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
                "SpawnRate": (3,6),
                "Round1" : {
                    "SpikeEnemy" : {
                        "EnemyLeft" : 1,
                        "MaxEnemy": 1,
                    },
                },
                "Round2" : {
                    "SpikeEnemy" : {
                        "EnemyLeft" : 1,
                        "MaxEnemy": 1
                    },
                },
                "Round3" : {
                    "SpikeEnemy" : {
                        "EnemyLeft" : 1,
                        "MaxEnemy": 1
                    },
                    "LaserEnemy" : {
                        "EnemyLeft" : 1,
                        "MaxEnemy": 1
                    },
                },
                "Round4" : {
                    "SpikeEnemy" : {
                        "EnemyLeft" : 15,
                        "MaxEnemy": 5
                    },
                    "LaserEnemy" : {
                        "EnemyLeft" : 15,
                        "MaxEnemy": 5
                    },
                },
                "Round19" : {
                    "SpikeEnemy" : {
                        "EnemyLeft" : 15,
                        "MaxEnemy": 5
                    },
                    "LaserEnemy" : {
                        "EnemyLeft" : 15,
                        "MaxEnemy": 5
                    },
                },
                "Round20" : {
                    "Monki" : {
                        "EnemyLeft" : 1,
                        "MaxEnemy": 1
                    },
                }
            }
        }