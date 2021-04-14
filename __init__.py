from .manager import manager
from .backend import json_backend, balance, duel_backend
from .product import sina_product
from hoshino.service import Service

mgr = manager(
    # json_backend代表独立的json存储
    # duel_backend代表与pcrduel金币联动的存储
    duel_backend(),
    balance(),
    [
        sina_product("sh601005", "大头菜"),
        sina_product("sh600276", "霓裳花"),
        sina_product("sh601166", "电气水晶"),
        sina_product("sh601166", "琉璃百合"),
        sina_product("sh601012", "琉璃袋"),
        sina_product("sh600519", "椰奶"),
    ]
)


sv = Service('market', enable_on_default=True, help_='''购买大头菜
[买入/卖出 商品名*n] 买卖n个某种商品
[市场列表] 看看市场价格
[仓库列表] 看看仓库还剩啥''')


@sv.on_rex(r'^(买入|卖出)(.*?)\*(\d*.?\d*)$')
async def buy_or_sell(bot, ev):
    await bot.finish(ev, await (mgr.sell_products if ev['match'].group(1) == '卖出' else mgr.buy_products)(str(ev['group_id']), str(ev['user_id']), ev['match'].group(2).strip(), float(ev['match'].group(3))), at_sender=True)

@sv.on_rex(r'^市场列表$')
async def buy_or_sell(bot, ev):
    await bot.finish(ev, await mgr.list_products(), at_sender=True)

@sv.on_rex(r'^仓库列表$')
async def buy_or_sell(bot, ev):
    await bot.finish(ev, mgr.list_balances(str(ev['group_id']), str(ev['user_id'])), at_sender=True)