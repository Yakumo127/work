from module.base.button import ButtonGrid
from module.base.decorator import cached_property
from module.base.timer import Timer
from module.base.utils import *
from module.combat.assets import GET_ITEMS_1
from module.guild.assets import *
from module.guild.base import GuildBase
from module.handler.assets import POPUP_CONFIRM
from module.logger import logger
from module.ocr.ocr import Digit
from module.statistics.item import ItemGrid

RECORD_OPTION = ('RewardRecord', 'logistics_exchange')
RECORD_SINCE = (0,)

GUILD_EXCHANGE_LIMIT = Digit(OCR_GUILD_EXCHANGE_LIMIT, threshold=64)

EXCHANGE_GRIDS = ButtonGrid(
    origin=(470, 470), delta=(198.5, 0), button_shape=(83, 83), grid_shape=(3, 1), name='EXCHANGE_GRID')

DEFAULT_ITEM_PRIORITY = [
    't1',
    't2',
    't3',
    'oxycola',
    'coolant',
    'coins',
    'oil',
    'merit'
]

DEFAULT_PLATE_PRIORITY = [
    'torpedo',
    'antiair',
    'plane',
    'gun',
    'general'
]

GRADES = [s for s in DEFAULT_ITEM_PRIORITY if len(s) == 2]


class GuildLogistics(GuildBase):
    @cached_property
    def exchange_items(self):
        item_grid = ItemGrid(
            EXCHANGE_GRIDS, {}, template_area=(40, 21, 89, 70), amount_area=(60, 71, 91, 92))
        item_grid.load_template_folder('./assets/stats_basic')
        return item_grid

    def _guild_logistics_mission_available(self):
        """
        Color sample the GUILD_MISSION area to determine
        whether the button is enabled, mission already
        in progress, or no more missions can be accepted

        Used at least twice, 'Collect' and 'Accept'

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        r, g, b = get_color(self.device.image, GUILD_MISSION_ACCEPT_AXIS.area)
        if g > max(r, b) - 10:
            logger.info('All Done')
            return False
        else:
            # Unfinished mission accept/collect range from about 240 to 322
            if self.image_color_count(GUILD_MISSION_ACCEPT_AXIS, color=(255, 255, 255), threshold=180, count=400):
                logger.info('Mission/Collect Available')
                return True
            else:
                logger.info('Mission In Progress')
                return False

    def _guild_logistics_supply_available(self):
        """
        Color sample the GUILD_SUPPLY area to determine
        whether the button is enabled or disabled

        mode determines

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        color = get_color(self.device.image, GUILD_SUPPLY_REWARDS_AXIS.area)
        if np.max(color) > np.mean(color) + 25:
            logger.info('Supply Available')
            return True
        else:
            logger.info('Supply Unavailable')
            return False

    def _guild_logistics_collect(self, skip_first_screenshot=True):
        """
        Execute collect/accept screen transitions within
        logistics

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        # Quickly ascertain the affiliation for while loop terminator
        is_azur_affiliation = self._guild_logistics_azur_affiliation()
        if is_azur_affiliation is None:
            return
        btn_guild_logistics_check = GUILD_LOGISTICS_CHECK_AZUR if is_azur_affiliation else GUILD_LOGISTICS_CHECK_AXIS

        # Various timers for button and
        confirm_timer = Timer(3, count=6).start()
        mission_timer = Timer(1.5, count=3)
        supply_timer = Timer(1.5, count=3)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if (not mission_timer.started() or mission_timer.reached()) and self._guild_logistics_mission_available():
                self.device.click(GUILD_MISSION_ACCEPT_AXIS)
                mission_timer.reset()
                confirm_timer.reset()
                continue

            if (not supply_timer.started() or supply_timer.reached()) and self._guild_logistics_supply_available():
                self.device.click(GUILD_SUPPLY_REWARDS_AXIS)
                supply_timer.reset()
                confirm_timer.reset()
                continue

            if self.handle_popup_confirm('GUILD_MISSION_ACCEPT'):
                confirm_timer.reset()
                continue

            if self.appear_then_click(GET_ITEMS_1, interval=2):
                confirm_timer.reset()
                continue

            # End
            if self.appear(btn_guild_logistics_check):
                if not self.info_bar_count() and confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

    def _guild_exchange_priorities_helper(self, title, string_priority, default_priority):
        """
        Helper for _guild_exchange_priorities for repeated usage

        Use defaults if configurations are found
        invalid in any manner

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        # Parse the string to a list, perform any special processing when applicable
        priority_parsed = [s.strip().lower() for s in string_priority.split('>')]
        priority_parsed = list(filter(''.__ne__, priority_parsed))
        priority = priority_parsed.copy()
        [priority.remove(s) for s in priority_parsed if s not in default_priority]

        # If after all that processing, result is empty list, then use default
        if len(priority) == 0:
            priority = default_priority

        logger.info(f'{title:10}: {priority}')
        return priority

    def _guild_exchange_priorities(self):
        """
        Set up priorities lists and dictionaries
        based on configurations

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        # Items
        item_priority = self._guild_exchange_priorities_helper('Item', self.config.GUILD_LOGISTICS_ITEM_ORDER_STRING,
                                                               DEFAULT_ITEM_PRIORITY)

        # T1 Grade Plates
        t1_priority = self._guild_exchange_priorities_helper('T1 Plate',
                                                             self.config.GUILD_LOGISTICS_PLATE_T1_ORDER_STRING,
                                                             DEFAULT_PLATE_PRIORITY)

        # T2 Grade Plates
        t2_priority = self._guild_exchange_priorities_helper('T2 Plate',
                                                             self.config.GUILD_LOGISTICS_PLATE_T2_ORDER_STRING,
                                                             DEFAULT_PLATE_PRIORITY)

        # T3 Grade Plates
        t3_priority = self._guild_exchange_priorities_helper('T3 Plate',
                                                             self.config.GUILD_LOGISTICS_PLATE_T3_ORDER_STRING,
                                                             DEFAULT_PLATE_PRIORITY)

        # Build dictionary
        grade_to_plate_priorities = dict()
        grade_to_plate_priorities['t1'] = t1_priority
        grade_to_plate_priorities['t2'] = t2_priority
        grade_to_plate_priorities['t3'] = t3_priority

        return item_priority, grade_to_plate_priorities

    def _guild_exchange_scan(self):
        """
        Image scan of available options
        to be exchanged. Summarizes matching
        templates and whether red text present
        in a list of tuples

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """

        # Scan the available exchange items that are selectable
        self.exchange_items._load_image(self.device.image)
        name = [self.exchange_items.match_template(item.image) for item in self.exchange_items.items]
        name = [str(item).lower() for item in name]

        # Loop EXCHANGE_GRIDS to detect for red text in bottom right area
        # indicating player lacks inventory for that item
        in_red_list = []
        for button in EXCHANGE_GRIDS.buttons():
            area = area_offset((35, 64, 83, 83), button.area[0:2])
            if self.image_color_count(area, color=(255, 93, 90), threshold=221, count=20):
                in_red_list.append(True)
            else:
                in_red_list.append(False)

        # Zip contents of both lists into tuples
        return zip(name, in_red_list)

    def _guild_exchange_check(self, options, item_priority, grade_to_plate_priorities):
        """
        Sift through all exchangeable options
        Record details on each to determine
        selection order

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        # Contains the details of all options
        choices = dict()

        for i, (option, in_red) in enumerate(options):
            # Options already sorted sequentially
            # Button indexes are in sync
            btn_key = f'GUILD_EXCHANGE_{i + 1}'
            btn = globals()[btn_key]

            # Defaults set absurd values, which tells ALAS to skip option
            item_weight = len(DEFAULT_ITEM_PRIORITY)
            plate_weight = len(DEFAULT_PLATE_PRIORITY)
            can_exchange = False

            # Player lacks inventory of this item
            # so leave this choice under all defaults
            # to skip
            if not in_red:
                # Plate perhaps, extract last
                # 2 characters to ensure
                grade = option[-2:]
                if grade in GRADES:
                    item_weight = item_priority.index(grade)
                    can_exchange = True

                    plate_priority = grade_to_plate_priorities.get(grade)
                    plate_name = option[5:-2]
                    if plate_name in plate_priority:
                        plate_weight = plate_priority.index(plate_name)

                    # Did weight update?
                    # If not, then this choice given less priority
                    # also set to absurd cost to avoid using
                    if plate_weight == len(DEFAULT_PLATE_PRIORITY):
                        item_weight = len(DEFAULT_ITEM_PRIORITY)
                        can_exchange = False

                # Else normal item, check normally
                # Plates are skipped since only grade in priority
                if option in item_priority:
                    item_weight = item_priority.index(option)
                    can_exchange = True

            choices[f'{i + 1}'] = [item_weight, plate_weight, i + 1, can_exchange, btn]
            logger.info(f'Choice #{i + 1} - Name: {option:15}, Weight: {item_weight:3}, Exchangeable: {can_exchange}')

        return choices

    def _guild_exchange_item(self, target_button, skip_first_screenshot=True):
        """
        Execute exchange screen transitions

        Pages:
            in: ANY
            out: ANY
        """
        # Quickly ascertain the affiliation for ui_click and while loop terminator
        is_azur_affiliation = self._guild_logistics_azur_affiliation()
        if is_azur_affiliation is None:
            return False
        btn_guild_logistics_check = GUILD_LOGISTICS_CHECK_AZUR if is_azur_affiliation else GUILD_LOGISTICS_CHECK_AXIS

        # Start the exchange process, not inserted
        # into while to avoid potential multi-clicking
        self.ui_click(target_button, check_button=POPUP_CONFIRM,
                      appear_button=btn_guild_logistics_check, skip_first_screenshot=True)

        confirm_timer = Timer(1.5, count=3).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.handle_popup_confirm('GUILD_EXCHANGE'):
                confirm_timer.reset()
                continue

            if self.appear_then_click(GET_ITEMS_1, interval=2):
                confirm_timer.reset()
                continue

            # End
            if self.appear(btn_guild_logistics_check):
                if not self.info_bar_count() and confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

        return True

    def _guild_exchange_select(self, choices):
        """
        Execute exchange action on choices
        The order of selection based on item weight
        If none are applicable, return False

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        while len(choices):
            # Select minimum by order of details
            # First, item_weight then plate_weight then button_index
            key = min(choices, key=choices.get)
            details = choices.get(key)

            # Item is exchangeable and exchange was a success
            if details[3] and self._guild_exchange_item(details[4]):
                return True
            else:
                # Remove this choice since inapplicable, then choose again
                choices.pop(key)
        logger.warning('Failed to exchange with any of the 3 available options')
        return False

    def _guild_exchange(self, limit=0):
        """
        Performs sift check and executes the applicable
        exchanges, number performed based on limit
        If unable to exchange at all, loop terminates
        prematurely

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        item_priority, grade_to_plate_priorities = self._guild_exchange_priorities()
        for num in range(limit):
            options = self._guild_exchange_scan()
            choices = self._guild_exchange_check(options, item_priority, grade_to_plate_priorities)
            if not self._guild_exchange_select(choices):
                break

    def _guild_logistics_azur_affiliation(self):
        """
        Helper method to quickly ascertain
        affiliation iff in logistics

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """
        # Last screen capture expected to have
        # guild coins display in top-right
        # if not present, likely will return None
        color = get_color(self.device.image, GUILD_AFFILIATION_CHECK_LOGISTICS.area)
        if color_similar(color, (115, 146, 206)):
            return True
        elif color_similar(color, (206, 117, 115)):
            return False
        else:
            logger.warning(f'Unknown guild affiliation color: {color}')
            return

    def guild_logistics(self):
        """
        Execute all actions in logistics

        Pages:
            in: GUILD_LOGISTICS
            out: GUILD_LOGISTICS
        """

        # Transition to Logistics
        if not self.guild_sidebar_ensure(3):
            logger.info('Logistics sidebar not ensured, try again on next reward loop')
            return

        # Handle logistics actions collect/accept
        # Exchange will be executed separately
        self._guild_logistics_collect()

        # Limit check whether can exchange to once a day
        if not self.config.record_executed_since(option=RECORD_OPTION, since=RECORD_SINCE):
            # Quickly ascertain affiliation, if unable to do not record and try again next loop
            is_azur_affiliation = self._guild_logistics_azur_affiliation()
            if is_azur_affiliation is None:
                return

            # Handle action exchange, determine color of digit based on affiliation
            GUILD_EXCHANGE_LIMIT.letter = (173, 182, 206) if is_azur_affiliation else (214, 113, 115)
            limit = GUILD_EXCHANGE_LIMIT.ocr(self.device.image)
            if limit > 0:
                self._guild_exchange(limit)
            self.config.record_save(option=RECORD_OPTION)
