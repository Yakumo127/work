import datetime

# This file was automatically generated by module/config/config_updater.py.
# Don't modify it manually.


class GeneratedConfig:
    """
    Auto generated configuration
    """

    # Group `Scheduler`
    Scheduler_Enable = False
    Scheduler_NextRun = datetime.datetime(2020, 1, 1, 0, 0)
    Scheduler_Command = 'Alas'
    Scheduler_ServerUpdate = '04:00'

    # Group `Emulator`
    Emulator_Serial = 'auto'
    Emulator_PackageName = 'auto'  # auto, com.miHoYo.hkrpg, com.HoYoverse.hkrpgoversea, com.miHoYo.hkrpg.bilibili
    Emulator_ScreenshotMethod = 'auto'  # auto, ADB, ADB_nc, uiautomator2, aScreenCap, aScreenCap_nc, DroidCast, DroidCast_raw, scrcpy
    Emulator_ControlMethod = 'MaaTouch'  # minitouch, MaaTouch
    Emulator_AdbRestart = False

    # Group `EmulatorInfo`
    EmulatorInfo_Emulator = 'auto'  # auto, NoxPlayer, NoxPlayer64, BlueStacks4, BlueStacks5, BlueStacks4HyperV, BlueStacks5HyperV, LDPlayer3, LDPlayer4, LDPlayer9, MuMuPlayer, MuMuPlayerX, MuMuPlayer12, MEmuPlayer
    EmulatorInfo_name = None
    EmulatorInfo_path = None

    # Group `Error`
    Error_Restart = 'game'  # game, game_emulator
    Error_SaveError = True
    Error_ScreenshotLength = 1
    Error_OnePushConfig = 'provider: null'

    # Group `Optimization`
    Optimization_ScreenshotInterval = 0.3
    Optimization_CombatScreenshotInterval = 1.0
    Optimization_WhenTaskQueueEmpty = 'goto_main'  # stay_there, goto_main, close_game

    # Group `Dungeon`
    Dungeon_Name = 'Calyx_Golden_Treasures'  # Calyx_Golden_Memories, Calyx_Golden_Aether, Calyx_Golden_Treasures, Calyx_Crimson_Destruction, Calyx_Crimson_Preservation, Calyx_Crimson_Hunt, Calyx_Crimson_Abundance, Calyx_Crimson_Erudition, Calyx_Crimson_Harmony, Calyx_Crimson_Nihility, Stagnant_Shadow_Quanta, Stagnant_Shadow_Gust, Stagnant_Shadow_Fulmination, Stagnant_Shadow_Blaze, Stagnant_Shadow_Spike, Stagnant_Shadow_Rime, Stagnant_Shadow_Mirage, Stagnant_Shadow_Icicle, Stagnant_Shadow_Doom, Stagnant_Shadow_Celestial, Cavern_of_Corrosion_Path_of_Gelid_Wind, Cavern_of_Corrosion_Path_of_Jabbing_Punch, Cavern_of_Corrosion_Path_of_Drifting, Cavern_of_Corrosion_Path_of_Providence, Cavern_of_Corrosion_Path_of_Holy_Hymn, Cavern_of_Corrosion_Path_of_Conflagration, Cavern_of_Corrosion_Path_of_Elixir_Seekers
    Dungeon_NameAtDoubleCalyx = 'Calyx_Golden_Treasures'  # do_not_participate, Calyx_Golden_Memories, Calyx_Golden_Aether, Calyx_Golden_Treasures, Calyx_Crimson_Destruction, Calyx_Crimson_Preservation, Calyx_Crimson_Hunt, Calyx_Crimson_Abundance, Calyx_Crimson_Erudition, Calyx_Crimson_Harmony, Calyx_Crimson_Nihility
    Dungeon_Team = 1  # 1, 2, 3, 4, 5, 6
    Dungeon_Support = 'when_daily'  # do_not_use, always_use, when_daily
    Dungeon_SupportCharacter = 'FirstCharacter'  # FirstCharacter, Arlan, Asta, Bailu, Blade, Bronya, Clara, DanHeng, Gepard, Herta, Himeko, Hook, JingYuan, Luocha, March7th, Natasha, Pela, Qingque, Sampo, Seele, Serval, SilverWolf, Sushang, Tingyun, TrailblazerDestruction, TrailblazerPreservation, Welt, Yanqing, Yukong

    # Group `Assignment`
    Assignment_Duration = 20  # 4, 8, 12, 20
    Assignment_Name_1 = 'Nameless_Land_Nameless_People'  # Nine_Billion_Names, Destruction_of_the_Destroyer, Winter_Soldiers, Born_to_Obey, Root_Out_the_Turpitude, Fire_Lord_Inflames_Blades_of_War, Nameless_Land_Nameless_People, Akashic_Records, The_Invisible_Hand, Abandoned_and_Insulted, Spring_of_Life, The_Land_of_Gold, The_Blossom_in_the_Storm
    Assignment_Name_2 = 'Akashic_Records'  # Nine_Billion_Names, Destruction_of_the_Destroyer, Winter_Soldiers, Born_to_Obey, Root_Out_the_Turpitude, Fire_Lord_Inflames_Blades_of_War, Nameless_Land_Nameless_People, Akashic_Records, The_Invisible_Hand, Abandoned_and_Insulted, Spring_of_Life, The_Land_of_Gold, The_Blossom_in_the_Storm
    Assignment_Name_3 = 'The_Invisible_Hand'  # Nine_Billion_Names, Destruction_of_the_Destroyer, Winter_Soldiers, Born_to_Obey, Root_Out_the_Turpitude, Fire_Lord_Inflames_Blades_of_War, Nameless_Land_Nameless_People, Akashic_Records, The_Invisible_Hand, Abandoned_and_Insulted, Spring_of_Life, The_Land_of_Gold, The_Blossom_in_the_Storm
    Assignment_Name_4 = 'Nine_Billion_Names'  # Nine_Billion_Names, Destruction_of_the_Destroyer, Winter_Soldiers, Born_to_Obey, Root_Out_the_Turpitude, Fire_Lord_Inflames_Blades_of_War, Nameless_Land_Nameless_People, Akashic_Records, The_Invisible_Hand, Abandoned_and_Insulted, Spring_of_Life, The_Land_of_Gold, The_Blossom_in_the_Storm

    # Group `Rogue`
    Rogue_Path = 'The Hunt'  # Preservation, Remembrance, Nihility, Abundance, The Hunt, Destruction, Elation
    Rogue_PresetResonanceFilter = 'preset-1'  # preset-1, custom
    Rogue_CustomResonanceFilter = '回响构音：均晶转变 > 回响构音：零维强化\n> 回响构音：第二次初恋 > 回响构音：体验的富翁\n> 回响构音：局外人 > 回响构音：怀疑的四重根\n> 回响构音：诸法无我 > 回响构音：诸行无常\n> 回响构音：射不主皮 > 回响构音：柘弓危矢\n> 回响构音：激变变星 > 回响构音：极端氦闪\n> 回响构音：末日狂欢 > 回响构音：树苗长高舞'
    Rogue_PresetBlessingFilter = 'preset-1'  # preset-1, custom
    Rogue_CustomBlessingFilter = '巡猎-3 > 《冠军晚餐·猫的摇篮》 > 丰饶众生，一法界心 > 毁灭-3 \n> 火堆外的夜 > 巡猎-2 > 毁灭-2 > 巡猎 > reset > random'
    Rogue_PresetCurioFilter = 'preset-1'  # preset-1, custom
    Rogue_CustomCurioFilter = '博士之袍 > 福灵胶 > 巡猎火漆 > 分裂金币 > 信仰债券 > random'
