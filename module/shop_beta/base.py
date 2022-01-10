from module.base.button import ButtonGrid
from module.base.decorator import cached_property
from module.base.timer import Timer
from module.combat.assets import GET_ITEMS_1, GET_SHIP
from module.logger import logger
from module.shop.assets import *
from module.shop.base_globals import *
from module.statistics.item import ItemGrid
from module.tactical.tactical_class import Book
from module.ui.assets import BACK_ARROW
from module.ui.ui import UI


class ShopItemGrid(ItemGrid):
    def predict(self, image, name=True, amount=True, cost=False, price=False, tag=False):
        """
        Overridden to iterate, corrects 'Book' type items and add additional
        attributes used to generalize identification
        """
        super().predict(image, name, amount, cost, price, tag)

        for item in self.items:
            # Give all items a set of attributes
            # for the Filter class
            item.group = None
            item.sub_genre = None
            item.tier = None

            if item.name in ITEM_NO_TIERS:
                item.group = item.name[:-2]
                continue

            if 'Book' in item.name:
                # Although attribute marked as protected
                # access for Book identification
                book = Book(image, item._button)

                item.name = f'{item.name[:-2]}{book.tier_str}'
                item.group, item.sub_genre, item.tier = \
                ['Book', book.genre_str, book.tier_str]
                continue

            if 'Plate' in item.name:
                item.group, item.sub_genre, item.tier = \
                ['Plate', item.name[5:-2], item.name[-2:]]
                continue

            if 'Retrofit' in item.name:
                item.group, item.sub_genre, item.tier = \
                ['Retrofit', item.name[8:-2], item.name[-2:]]
                continue

            if 'PR' in item.name or 'DR' in item.name:
                item.group = item.name[:2]
                item.sub_genre = item.name[2:-2]
                item.tier = f'S{BP_SERIES[item.name[2:-2].lower()]}'
                continue

        return self.items


class ShopBase(UI):
    @cached_property
    def shop_filter(self):
        """
        Returns:
            str:
        """
        return ''

    @cached_property
    def shop_grid(self):
        """
        Returns:
            ButtonGrid:
        """
        shop_grid = ButtonGrid(
            origin=(477, 152), delta=(156, 214), button_shape=(96, 97), grid_shape=(5, 2), name='SHOP_GRID')
        return shop_grid

    @cached_property
    def shop_items(self):
        """
        Returns:
            None, base default value
            ShopItemGrid, variant value
        """
        return None

    def shop_currency(self):
        """
        Returns:
            int:
        """
        return 0

    def shop_has_loaded(self, items):
        """
        Custom steps for variant shop
        if needed to ensure shop has
        loaded completely
        ShopMedal for example will initally
        display default items at default prices

        Args:
            items: list[Item]

        Returns:
            bool:
        """
        return True

    def shop_get_items(self, skip_first_screenshot=True):
        """
        Args:
            skip_first_screenshot (bool):

        Returns:
            list[Item]:
        """
        # Retrieve ShopItemGrid
        shop_items = self.shop_items
        if shop_items is None:
            logger.warning('Expected type \'ShopItemGrid\' but was None')
            return []

        # Loop on predict to ensure items
        # have loaded and can accurately
        # be read
        record = 0
        timeout = Timer(3, count=9).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            shop_items.predict(
                self.device.image,
                name=True,
                amount=False,
                cost=True,
                price=True,
                tag=False
            )

            if timeout.reached():
                logger.warning('Items loading timeout; continue and assumed has loaded')
                break

            # Check unloaded items, because AL loads items too slow.
            items = shop_items.items
            known = len([item for item in items if item.is_known_item])
            logger.attr('Item detected', known)
            if known == 0 or known != record:
                record = known
                continue
            else:
                record = known

            # End
            if self.shop_has_loaded(items):
                break

        # Log final result on predicted items
        items = shop_items.items
        grids = shop_items.grids
        if len(items):
            min_row = grids[0, 0].area[1]
            row = [str(item) for item in items if item.button[1] == min_row]
            logger.info(f'Shop row 1: {row}')
            row = [str(item) for item in items if item.button[1] != min_row]
            logger.info(f'Shop row 2: {row}')
            return items
        else:
            logger.info('No shop items found')
            return []

    def shop_check_item(self, item):
        """
        Override in variant class
        for specific check item
        actions

        Args:
            item: Item to check

        Returns:
            bool:
        """
        return False

    def shop_check_custom_item(self, item):
        """
        Override in variant class
        for specific check custom item
        actions; no restriction to filter string

        Args:
            item (Item):

        Returns:
            bool:
        """
        return False

    def shop_interval_clear(self):
        """
        Override in variant class
        if need to clear particular
        asset intervals
        """
        pass

    def shop_buy_handle(self, item):
        """
        Override in variant class
        for specific buy handle
        actions

        Args:
            item (Item):

        Returns:
            bool:
        """
        return False

    def shop_get_item_to_buy(self, items):
        """
        Args:
            items list(Item): acquired from shop_get_items

        Returns:
            Item: Item to buy, or None.
        """
        # Convert selection to list{str], remove any empty/whitespace entries
        selection = self.shop_filter.replace(' ', '').replace('\n', '').split('>')
        selection = list(filter(''.__ne__, selection))

        # First, must scan for custom items
        # as has no template or filter support
        for item in items:
            if self.shop_check_custom_item(item):
                return item

        # Second, load selection, apply filter,
        # and return 1st item in result if any
        def _filter_check(item):
            if self.shop_check_item(item):
                return True
            return False

        FILTER.load(selection)
        filtered = FILTER.apply(items, _filter_check)

        if not filtered:
            return None
        logger.attr('Item_sort', ' > '.join([str(item) for item in filtered]))

        return filtered[0]

    def shop_buy_execute(self, item, skip_first_screenshot=True):
        """
        Args:
            item: Item to check
            skip_first_screenshot: bool

        Returns:
            None: exits appropriately therefore successful
        """
        success = False
        self.interval_clear(BACK_ARROW)
        self.interval_clear(SHOP_BUY_CONFIRM)
        self.shop_interval_clear()

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
            if self.shop_buy_handle(item):
                self.interval_reset(BACK_ARROW)
                continue
            if self.appear(GET_SHIP, interval=1):
                self.device.click(SHOP_CLICK_SAFE_AREA)
                self.interval_reset(BACK_ARROW)
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

    def shop_buy(self):
        """
        Returns:
            bool: If success, and able to continue.
        """
        for _ in range(12):
            # Get first for innate delay to ocr
            # shop currency for accurate parse
            items = self.shop_get_items()
            currency = self.shop_currency()
            if currency <= 0:
                logger.warning(f'Current funds: {currency}, stopped')
                return False

            item = self.shop_get_item_to_buy(items)
            if item is None:
                logger.info('Shop buy finished')
                return True
            else:
                self.shop_buy_execute(item)
                continue

        logger.warning('Too many items to buy, stopped')
        return True
