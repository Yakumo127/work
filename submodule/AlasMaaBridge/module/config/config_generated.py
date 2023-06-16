import datetime

# This file was automatically generated by module/config/config_updater.py.
# Don't modify it manually.


class GeneratedConfig:
    """
    Auto generated configuration
    """

    # Group `Scheduler`
    Scheduler_Enable = False
    Scheduler_NextRun = datetime.datetime(2020, 1, 1, 4, 0)
    Scheduler_Command = 'Maa'
    Scheduler_SuccessInterval = 60
    Scheduler_FailureInterval = 120
    Scheduler_ServerUpdate = '04:00'

    # Group `Emulator`
    Emulator_ServerName = 'disabled'

    # Group `Error`
    Error_SaveError = False
    Error_OnePushConfig = 'provider: null'

    # Group `Optimization`
    Optimization_WhenTaskQueueEmpty = 'stay_there'

    # Group `MaaEmulator`
    MaaEmulator_Serial = '127.0.0.1:5555'
    MaaEmulator_PackageName = 'Official'  # Official, Bilibili, YoStarEN, YoStarJP, YoStarKR, txwy
    MaaEmulator_MaaPath = 'D:/Program Files/MAA'
    MaaEmulator_TouchMethod = 'minitouch'  # minitouch, maatouch, adb
    MaaEmulator_DeploymentWithPause = False

    # Group `MaaRecord`
    MaaRecord_ReportToPenguin = False
    MaaRecord_PenguinID = None

    # Group `MaaRestart`
    MaaRestart_TimeInterval = 0

    # Group `MaaFight`
    MaaFight_Stage = 'last'  # last, 1-7, LS-6, CA-5, SK-5, AP-5, CE-6, PR-A-1, PR-A-2, PR-B-1, PR-B-2, PR-C-1, PR-C-2, PR-D-1, PR-D-2, custom
    MaaFight_CustomStage = None
    MaaFight_MedicineTactics = 'no_use'  # no_use, expiring, run_out
    MaaFight_Medicine = None
    MaaFight_Stone = None
    MaaFight_Times = None
    MaaFight_Drops = None
    MaaFight_DrGrandet = False

    # Group `MaaFightWeekly`
    MaaFightWeekly_Enable = True
    MaaFightWeekly_Monday = 'default'  # default, LS-6, SK-5, AP-5, PR-A-1, PR-A-2, PR-B-1, PR-B-2
    MaaFightWeekly_Tuesday = 'default'  # default, LS-6, CA-5, CE-6, PR-B-1, PR-B-2, PR-D-1, PR-D-2
    MaaFightWeekly_Wednesday = 'default'  # default, LS-6, CA-5, SK-5, PR-C-1, PR-C-2, PR-D-1, PR-D-2
    MaaFightWeekly_Thursday = 'default'  # default, LS-6, AP-5, CE-6, PR-A-1, PR-A-2, PR-C-1, PR-C-2
    MaaFightWeekly_Friday = 'default'  # default, LS-6, CA-5, SK-5, PR-A-1, PR-A-2, PR-B-1, PR-B-2
    MaaFightWeekly_Saturday = 'default'  # default, LS-6, SK-5, AP-5, CE-6, PR-B-1, PR-B-2, PR-C-1, PR-C-2, PR-D-1, PR-D-2
    MaaFightWeekly_Sunday = 'default'  # default, LS-6, CA-5, AP-5, CE-6, PR-A-1, PR-A-2, PR-C-1, PR-C-2, PR-D-1, PR-D-2

    # Group `MaaRecruit`
    MaaRecruit_Refresh = True
    MaaRecruit_SkipRobot = True
    MaaRecruit_Select3 = True
    MaaRecruit_Select4 = True
    MaaRecruit_Select5 = True
    MaaRecruit_Level3ShortTime = True
    MaaRecruit_Times = 4
    MaaRecruit_Expedite = False

    # Group `MaaInfrast`
    MaaInfrast_Facility = 'Mfg > Trade > Power > Control > Reception > Office > Dorm'
    MaaInfrast_Drones = 'Money'  # _NotUse, Money, SyntheticJade, CombatRecord, PureGold, OriginStone, Chip
    MaaInfrast_WorkThreshold = 12
    MaaInfrast_ShiftThreshold = 4
    MaaInfrast_Notstationed = True
    MaaInfrast_Trust = True
    MaaInfrast_Replenish = False

    # Group `MaaCustomInfrast`
    MaaCustomInfrast_Enable = False
    MaaCustomInfrast_BuiltinConfig = 'custom'  # custom, 153-3, 243-3, 243-4, 252-3, 333-3
    MaaCustomInfrast_Filename = None
    MaaCustomInfrast_CustomPeriod = '16, 4, 4'
    MaaCustomInfrast_PlanIndex = 0

    # Group `MaaMall`
    MaaMall_CreditFight = False
    MaaMall_Shopping = True
    MaaMall_ForceShoppingIfCreditFull = False
    MaaMall_BuyFirst = '招聘许可'
    MaaMall_BlackList = '碳 > 家具 > 加急许可'

    # Group `MaaRoguelike`
    MaaRoguelike_Theme = 'Phantom'  # Phantom, Mizuki
    MaaRoguelike_Mode = 0  # 0, 1
    MaaRoguelike_StartsCount = 9999999
    MaaRoguelike_InvestmentsCount = 9999999
    MaaRoguelike_StopWhenInvestmentFull = False
    MaaRoguelike_Squad = '指挥分队'  # 心胜于物分队, 物尽其用分队, 以人为本分队, 指挥分队, 集群分队, 后勤分队, 矛头分队, 突击战术分队, 堡垒战术分队, 远程战术分队, 破坏战术分队, 研究分队, 高规格分队
    MaaRoguelike_Roles = '取长补短'  # 先手必胜, 稳扎稳打, 取长补短, 随心所欲
    MaaRoguelike_CoreChar = None
    MaaRoguelike_Support = 'no_use'  # no_use, friend_support, nonfriend_support
    MaaRoguelike_RestartGameWhenSwitchNeeded = False

    # Group `MaaCopilot`
    MaaCopilot_FileName = None
    MaaCopilot_Identify = False
    MaaCopilot_Formation = False
    MaaCopilot_Cycle = 1

    # Group `Storage`
    Storage_Storage = {}
