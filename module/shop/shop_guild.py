from module.base.decorator import cached_property
from module.base.timer import Timer
from module.base.utils import area_offset, get_color
from module.combat.assets import GET_ITEMS_1, GET_SHIP
from module.logger import logger
from module.ocr.ocr import Digit
from module.shop.assets import *
from module.shop.base import ShopBase, ShopItemGrid
from module.shop.shop_guild_globals import *
from module.ui.assets import BACK_ARROW

SHOP_SELECT_PRS = [SHOP_SELECT_PR1, SHOP_SELECT_PR2, SHOP_SELECT_PR3]

OCR_SHOP_GUILD_COINS = Digit(SHOP_GUILD_COINS, letter=(255, 255, 255), name='OCR_SHOP_GUILD_COINS')
OCR_SHOP_SELECT_TOTAL_PRICE = Digit(SHOP_SELECT_TOTAL_PRICE, letter=(255, 255, 255), name='OCR_SHOP_SELECT_TOTAL_PRICE')


class GuildItemGrid(ShopItemGrid):
    def predict(self, image, name=True, amount=True, cost=False, price=False):
        super().predict(image, name, amount, cost, price)

        # Loop again for Guild Shop items
        # Add attr 'secondary_grid' used to flag and id
        # Add attr 'additional' to id specific config
        # if applicable
        for item in self.items:
            # Defaults
            item.secondary_grid = None
            item.additional = None

            name = item.name[:-2].lower()
            if name in SELECT_ITEMS:
                item.secondary_grid = name
                if name != 'pr' and name != 'dr':
                    item.additional = item.name[-2:]

        return self.items


class GuildShop(ShopBase):
    _shop_guild_coins = 0

    def shop_guild_get_currency(self):
        self._shop_guild_coins = OCR_SHOP_GUILD_COINS.ocr(self.device.image)
        logger.info(f'Guild coins: {self._shop_guild_coins}')

    @cached_property
    def shop_guild_items(self):
        """
        Returns:
            GuildItemGrid:
        """
        shop_grid = self.shop_grid
        shop_guild_items = GuildItemGrid(shop_grid, templates={}, amount_area=(60, 74, 96, 95))
        shop_guild_items.load_template_folder('./assets/guild_shop')
        shop_guild_items.load_cost_template_folder('./assets/shop_cost')
        return shop_guild_items

    def shop_guild_check_item(self, item):
        """
        Args:
            item: Item to check

        Returns:
            bool:
        """
        if item.cost == 'GuildCoins':
            if item.price > self._shop_guild_coins:
                return False
            return True
        return False

    def shop_get_select(self, category, choice):
        """
        Args:
            category: String identifies SELECT combination
            choice (string, list): String identifies index within SELECT combination
                                   List types exclusively for PR series selection

        Returns:
            Button:
        """
        # Ensure there is valid SELECT combination according to category
        try:
            choices = globals()[f'SELECT_{category.upper()}']
        except KeyError:
            logger.warning(f'shop_get_select --> Missing SELECT_{category.upper()}')
            return None

        # Retrieve the correct SELECT_GRID based on category
        shop_select_grid = None
        if category == 'book':
            shop_select_grid = SELECT_GRID_3X1
        elif category == 'box' or category == 'retrofit':
            shop_select_grid = SELECT_GRID_4X1
        elif category == 'pr' and isinstance(choice, list):
            # Determine series of PR is displayed
            # Position of successful appearance
            # determines correct shop_select_grid
            results = [self.appear(button, offset=(20, 20)) for button in SHOP_SELECT_PRS]
            for idx, result in enumerate(results):
                if result:
                    choice = choice[idx]
                    if idx == 0:
                        shop_select_grid = SELECT_GRID_6X1
                    else:
                        shop_select_grid = SELECT_GRID_4X1
                    break
        elif category == 'plate':
            shop_select_grid = SELECT_GRID_5X1

        if shop_select_grid is None:
            logger.warning(f'shop_get_select --> No grid applicable to category \'{category}\'')
            return None

        # Utilize known fixed location for correct item
        if choice in choices:
            return shop_select_grid.buttons()[choices.get(choice)]

        logger.warning(f'shop_get_select --> Missing \'{choice}\' in SELECT_{category.upper()}')
        return None

    def shop_buy_select_execute(self, item):
        """
        Args:
            item: Item to check

        Returns:
            None: implicating failed to execute
        """
        # Base Case - Must have 'secondary_grid' attr and must not be None
        if not hasattr(item, 'secondary_grid') or item.secondary_grid is None:
            logger.warning('shop_buy_select_execute --> Detected secondary '
                        'prompt but item not classified of having this option')
            self.device.click(SHOP_CLICK_SAFE_AREA)  # Close secondary prompt
            return False

        # Proceed and verify required components can be acquired
        category = item.secondary_grid
        additional = '' if item.additional is None else item.additional
        try:
            limit = globals()[f'SELECT_{category.upper()}_LIMIT']
            choice = getattr(self.config, f'SHOP_GUILD_{category.upper()}{additional.upper()}')
        except KeyError:
            logger.warning(f'shop_buy_select_execute --> Missing SELECT_{category.upper()}_LIMIT')
            self.device.click(SHOP_CLICK_SAFE_AREA)  # Close secondary prompt
            return False
        except AttributeError:
            logger.warning(f'shop_buy_select_execute --> Missing Config SHOP_GUILD_{category.upper()}')
            self.device.click(SHOP_CLICK_SAFE_AREA)  # Close secondary prompt
            return False

        # Find and click appropriate button within secondary grid
        # This results in plus/minus appearing, click until those appear
        select = self.shop_get_select(category, choice)
        click_timer = Timer(3, count=6)
        while 1:
            if select is not None:
                if click_timer.reached():
                    self.device.click(select)
                    click_timer.reset()
            else:
                self.device.click(SHOP_CLICK_SAFE_AREA)  # Close secondary prompt
                return False

            # Scan for plus/minus locations varies based on grid and item selected
            self.device.screenshot()
            sim0, point0 = TEMPLATE_PLUS.match_result(self.device.image)
            sim1, point1 = TEMPLATE_MINUS.match_result(self.device.image)
            if sim0 < 0.85 or sim1 < 0.85:
                continue

            for index, name in enumerate(['PLUS', 'MINUS']):
                button = area_offset(area=(-12, -12, 44, 32), offset=locals()[f'point{index}'])
                color = get_color(self.device.image, button)
                locals()[name] = Button(area=button, color=color, button=button, name=f'{name}')

            break

        # Total number to purchase altogether
        while 1:
            if (limit * item.price) <= self._shop_guild_coins:
                break
            else:
                limit -= 1

        # For ui_ensure_index to calculate amount/count
        # representation of total_price
        def total_price_to_count(image):
            total_price = OCR_SHOP_SELECT_TOTAL_PRICE.ocr(image)
            return int(total_price / item.price)

        self.ui_ensure_index(limit, letter=total_price_to_count, prev_button=locals()['MINUS'],
                             next_button=locals()['PLUS'], skip_first_screenshot=True)
        self.device.click(SHOP_BUY_CONFIRM_SELECT)
        return True

    def shop_buy_execute(self, item, skip_first_screenshot=True):
        """
        Extended from 'ShopBase' to include handling of
        purchases in items that have a secondary_grid

        Args:
            item: Item to click and buy
            skip_first_screenshot: bool

        Returns:
            None: exits appropriately therefore successful
        """
        success = False
        self.interval_clear(BACK_ARROW)
        self.interval_clear(SHOP_BUY_CONFIRM)
        self.interval_clear(SHOP_SELECT_CHECK)

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear(BACK_ARROW, offset=(20, 20), interval=3):
                self.device.click(item)
                continue
            if self.appear_then_click(SHOP_BUY_CONFIRM, offset=(20, 20), interval=3):
                self.interval_reset(BACK_ARROW)
                continue
            if self.appear(GET_SHIP, interval=1):
                self.device.click(SHOP_CLICK_SAFE_AREA)
                self.interval_reset(BACK_ARROW)
                continue
            if self.appear(SHOP_SELECT_CHECK, interval=3):
                if not self.shop_buy_select_execute(item):
                    logger.warning('Failed to purchase secondary grid item, may need re-configure settings')
                    exit(1)
                self.interval_reset(BACK_ARROW)
                self.interval_reset(SHOP_SELECT_CHECK)
                continue
            if self.appear(GET_ITEMS_1, interval=1):
                self.device.click(SHOP_CLICK_SAFE_AREA)
                self.interval_reset(BACK_ARROW)
                success = True
                continue
            if self.handle_info_bar():
                self.interval_reset(BACK_ARROW)
                success = True
                continue

            # End
            if success and self.appear(BACK_ARROW, offset=(20, 20)):
                break
