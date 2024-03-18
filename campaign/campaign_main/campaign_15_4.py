from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids

from .campaign_15_base import CampaignBase
from .campaign_15_base import Config as ConfigBase

MAP = CampaignMap('15-4')
MAP.shape = 'K9'
MAP.camera_data = ['D2', 'D5', 'D7', 'H2', 'H5', 'H7']
MAP.camera_data_spawn_point = ['H2']
MAP.map_data = """
    -- -- ME ME Me -- ME ++ ++ ME ME
    ME -- -- -- -- ME -- ++ ++ -- ME
    ++ -- -- -- -- -- ME SP SP ME Me
    ++ ME -- ++ ++ -- -- -- -- ME --
    -- Me ME MA ++ ME -- -- -- -- ME
    ME ME ME -- -- -- -- ++ ME -- Me
    ME -- __ -- ME ME -- ME ME -- ++
    -- -- ++ -- Me -- ME ME ME -- ME
    -- Me -- ME ME Me ++ ++ ++ -- --
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 8},
    {'battle': 1, 'enemy': 1},
    {'battle': 2, 'enemy': 1},
    {'battle': 3, 'enemy': 1, 'boss': 1},
    {'battle': 4, 'enemy': 2},
    {'battle': 5},
    {'battle': 6, 'boss': 1},
    {'battle': 7, 'enemy': 1},
    {'battle': 8, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1, \
A2, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, \
A3, B3, C3, D3, E3, F3, G3, H3, I3, J3, K3, \
A4, B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, \
A5, B5, C5, D5, E5, F5, G5, H5, I5, J5, K5, \
A6, B6, C6, D6, E6, F6, G6, H6, I6, J6, K6, \
A7, B7, C7, D7, E7, F7, G7, H7, I7, J7, K7, \
A8, B8, C8, D8, E8, F8, G8, H8, I8, J8, K8, \
A9, B9, C9, D9, E9, F9, G9, H9, I9, J9, K9, \
    = MAP.flatten()


# W15 has special enemy spawn mechanism
# After entering map, additional enemies spawn on these nodes:
# ['J8'] must spawns an enemy.
# Additionally, 'A1' and 'K9' spawn a special carrier 
# which allow mob air reinforcement. 
# 15-4 has special boss spawn mechanism
# The boss first spawns at H5, then spawns at D3, finally spawns at A9.

OVERRIDE = CampaignMap('15-4')
OVERRIDE.map_data = """
    ME -- ME ME ME -- ME -- -- ME ME
    ME -- -- -- -- ME -- -- -- -- ME
    -- -- -- MB -- -- ME -- -- ME ME
    -- ME -- -- -- -- -- -- -- ME --
    -- ME ME -- -- ME -- MB -- -- ME
    ME ME ME -- -- -- -- -- ME -- ME
    ME -- -- -- ME ME -- ME ME -- --
    -- -- -- -- ME -- ME ME ME ME ME
    MB ME -- ME ME ME -- -- -- -- ME
"""


class Config(ConfigBase):
    # ===== Start of generated config =====
    # MAP_SIREN_TEMPLATE = ['0']
    # MOVABLE_ENEMY_TURN = (2,)
    # MAP_HAS_SIREN = True
    # MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = False
    MAP_HAS_AMBUSH = True
    # MAP_HAS_MYSTERY = True
    # ===== End of generated config =====


class Campaign(CampaignBase):
    MAP = MAP
    
    def map_data_init(self, map_):
        super().map_data_init(map_)
        for override_grid in OVERRIDE:
            # Set may_enemy, but keep may_ambush
            self.map[override_grid.location].may_enemy = override_grid.may_enemy
            self.map[override_grid.location].may_boss = override_grid.may_boss

    @Config.when(Campaign_UseClearMode=False)
    def battle_0(self):
        self.goto(A1)
        return True
    
    @Config.when(Campaign_UseClearMode=False)
    def battle_1(self):
        self.mob_move(J8, J7)
        self.full_scan_movable()
        self.goto(K9)
        return True

    @Config.when(Campaign_UseClearMode=True)
    def battle_0(self):
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()

    def battle_2(self):
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()
    
    @Config.when(Campaign_UseClearMode=False)
    def battle_3(self):
        self.fleet_boss.goto(H5)
        self.fleet_1.switch_to()
        return True

    @Config.when(Campaign_UseClearMode=True)
    def battle_3(self):
        self.goto(H5)
        return True

    def battle_4(self):
        self.pick_up_ammo()

        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()

    def battle_6(self):
        self.goto(D3)
        return True

    def battle_7(self):
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()

    def battle_8(self):
        return self.fleet_boss.clear_boss()
