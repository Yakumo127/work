from module.base.decorator import cached_property
from module.logger import logger
from module.ocr.ocr import Digit
from module.shop.assets import *
from module.shop.base import ShopBase, ShopItemGrid

OCR_SHOP_GOLD_COINS = Digit(SHOP_GOLD_COINS, letter=(239, 239, 239), name='OCR_SHOP_GOLD_COINS')
OCR_SHOP_GEMS = Digit(SHOP_GEMS, letter=(255, 243, 82), name='OCR_SHOP_GEMS')


class GeneralShop(ShopBase):
    _shop_gold_coins = 0
    _shop_gems = 0

    def shop_get_general_currency(self):
        self._shop_gold_coins = OCR_SHOP_GOLD_COINS.ocr(self.device.image)
        self._shop_gems = OCR_SHOP_GEMS.ocr(self.device.image)
        logger.info(f'Gold coins: {self._shop_gold_coins}, Gems: {self._shop_gems}')

    @cached_property
    def shop_general_items(self):
        """
        Returns:
            ShopItemGrid:
        """
        shop_grid = self.shop_grid
        shop_general_items = ShopItemGrid(shop_grid, templates={}, amount_area=(60, 74, 96, 95))
        shop_general_items.load_template_folder('./assets/general_shop')
        shop_general_items.load_cost_template_folder('./assets/shop_cost')
        return shop_general_items

    def shop_check_item_general(self, item):
        """
        Args:
            item: Item to check

        Returns:
            bool:
        """
        if item.cost == 'Coins':
            if item.price > self._shop_gold_coins:
                return False
            return True

        if self.config.SHOP_GENERAL_GEMS_ENABLED:
            if item.cost == 'Gems':
                if item.price > self._shop_gems:
                    return False
                return True
        return False
