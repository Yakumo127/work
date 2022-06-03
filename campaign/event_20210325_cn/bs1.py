from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import RoadGrids, SelectedGrids

from .campaign_base import CampaignBase

MAP = CampaignMap("BS1")
MAP.shape = "H7"
MAP.camera_data = ["D2", "D5", "E2", "E5"]
MAP.camera_data_spawn_point = ["E5", "D5"]
MAP.map_data = """
    -- -- -- MS -- -- -- ++
    -- ME -- ++ ++ ME -- ++
    -- -- MB ++ ++ -- -- ++
    MS ME -- -- -- ME -- Me
    -- -- -- __ ME Me -- --
    -- MS ++ -- -- ME ME --
    -- -- ++ SP SP -- -- --
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {"battle": 0, "enemy": 2, "siren": 1},
    {"battle": 1, "enemy": 1},
    {"battle": 2, "enemy": 2},
    {"battle": 3, "enemy": 1},
    {"battle": 4, "enemy": 2, "boss": 1},
    {"battle": 5, "enemy": 1},
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
    A2,
    B2,
    C2,
    D2,
    E2,
    F2,
    G2,
    H2,
    A3,
    B3,
    C3,
    D3,
    E3,
    F3,
    G3,
    H3,
    A4,
    B4,
    C4,
    D4,
    E4,
    F4,
    G4,
    H4,
    A5,
    B5,
    C5,
    D5,
    E5,
    F5,
    G5,
    H5,
    A6,
    B6,
    C6,
    D6,
    E6,
    F6,
    G6,
    H6,
    A7,
    B7,
    C7,
    D7,
    E7,
    F7,
    G7,
    H7,
) = MAP.flatten()


class Config:
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ["SanDiego", "Dace"]
    MOVABLE_ENEMY_TURN = (1, 2)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    STAR_REQUIRE_1 = 0
    STAR_REQUIRE_2 = 0
    STAR_REQUIRE_3 = 0
    # ===== End of generated config =====

    MAP_IS_ONE_TIME_STAGE = True
    MOVABLE_ENEMY_TURN = (2,)
    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        "height": (150, 255 - 24),
        "width": (1.5, 10),
        "prominence": 10,
        "distance": 35,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        "height": (255 - 24, 255),
        "prominence": 10,
        "distance": 50,
        "wlen": 1000,
    }
    HOMO_EDGE_HOUGHLINES_THRESHOLD = 120
    HOMO_EDGE_COLOR_RANGE = (0, 12)


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_siren():
            return True

        return self.battle_default()

    def battle_4(self):
        return self.clear_boss()
