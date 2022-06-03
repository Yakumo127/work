from module.campaign.campaign_base import CampaignBase
from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import RoadGrids, SelectedGrids

from .a1 import Config as ConfigBase

MAP = CampaignMap("A2")
MAP.shape = "J6"
MAP.camera_data = ["D2", "D4", "G2", "G4"]
MAP.camera_data_spawn_point = ["D2"]
MAP.map_data = """
    ++ SP -- SP -- -- ++ -- ++ ++
    ++ -- -- -- -- -- -- ME -- ++
    ME -- MS ++ -- MS -- -- ME --
    ME -- -- -- -- ++ ME __ -- MB
    -- Me ++ ++ Me ++ -- -- ME --
    -- -- ++ ++ -- -- -- ME -- ++
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50
    50 10 10 10 10 50 50 50 50 50
    50 10 90 90 10 50 50 50 50 50
    50 10 90 90 10 50 50 50 50 50
"""
MAP.spawn_data = [
    {"battle": 0, "enemy": 3, "siren": 1},
    {"battle": 1, "enemy": 1},
    {"battle": 2, "enemy": 1},
    {"battle": 3, "enemy": 1},
    {"battle": 4, "boss": 1},
]
MAP.spawn_data_loop = [
    {"battle": 0, "enemy": 2, "siren": 1},
    {"battle": 1, "enemy": 1},
    {"battle": 2, "enemy": 1},
    {"battle": 3, "enemy": 1},
    {"battle": 4, "enemy": 1, "boss": 1},
]
(
    A1,
    B1,
    C1,
    D1,
    E1,
    F1,
    G1,
    H1,
    I1,
    J1,
    A2,
    B2,
    C2,
    D2,
    E2,
    F2,
    G2,
    H2,
    I2,
    J2,
    A3,
    B3,
    C3,
    D3,
    E3,
    F3,
    G3,
    H3,
    I3,
    J3,
    A4,
    B4,
    C4,
    D4,
    E4,
    F4,
    G4,
    H4,
    I4,
    J4,
    A5,
    B5,
    C5,
    D5,
    E5,
    F5,
    G5,
    H5,
    I5,
    J5,
    A6,
    B6,
    C6,
    D6,
    E6,
    F6,
    G6,
    H6,
    I6,
    J6,
) = MAP.flatten()


class Config(ConfigBase):
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ["Dorsetshire", "Rodney", "ArkRoyal"]
    MOVABLE_ENEMY_TURN = (2,)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = True
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    # ===== End of generated config =====


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_siren():
            return True

        return self.battle_default()

    def battle_4(self):
        return self.clear_boss()
