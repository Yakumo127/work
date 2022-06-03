from module.campaign.campaign_base import CampaignBase
from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import RoadGrids, SelectedGrids

MAP = CampaignMap("C1")
MAP.shape = "I5"
MAP.camera_data = ["D2", "D3", "F2", "F3"]
MAP.camera_data_spawn_point = ["D3", "D2"]
MAP.map_data = """
    SP -- ++ ME -- ME ++ -- --
    -- ME -- -- ME -- Me ++ Me
    -- -- MS -- -- MS __ -- --
    -- ME -- -- ++ Me -- Me --
    SP -- -- Me ++ -- Me -- MB
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {"battle": 0, "enemy": 2, "siren": 2},
    {"battle": 1, "enemy": 1},
    {"battle": 2, "enemy": 2},
    {"battle": 3, "enemy": 1},
    {"battle": 4, "enemy": 1, "boss": 1},
]
MAP.spawn_data_loop = [
    {"battle": 0, "enemy": 2, "siren": 2},
    {"battle": 1, "enemy": 1},
    {"battle": 2, "enemy": 2},
    {"battle": 3, "enemy": 1},
    {"battle": 4, "enemy": 2, "boss": 1},
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
    A2,
    B2,
    C2,
    D2,
    E2,
    F2,
    G2,
    H2,
    I2,
    A3,
    B3,
    C3,
    D3,
    E3,
    F3,
    G3,
    H3,
    I3,
    A4,
    B4,
    C4,
    D4,
    E4,
    F4,
    G4,
    H4,
    I4,
    A5,
    B5,
    C5,
    D5,
    E5,
    F5,
    G5,
    H5,
    I5,
) = MAP.flatten()


class Config:
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ["DD"]
    MOVABLE_ENEMY_TURN = (3,)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    # ===== End of generated config =====

    TRUST_EDGE_LINES = True

    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        "height": (80, 255 - 40),
        "width": (0.9, 10),
        "prominence": 10,
        "distance": 35,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        "height": (255 - 40, 255),
        "prominence": 10,
        "distance": 50,
        "wlen": 1000,
    }


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_siren():
            return True

        return self.battle_default()

    def battle_4(self):
        return self.clear_boss()
