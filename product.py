from hoshino.aiorequests import get

class product:
    def __init__(self, name):
        self.name = name
    @property
    async def price(self) -> float:
        raise NotImplementedError

class sina_product(product):
    def __init__(self, id, name):
        self.id = id
        super().__init__(name)
    
    @property
    async def price(self) -> float:
        return float((await (await get("http://hq.sinajs.cn/list=" + self.id)).content).decode('gbk').split(',')[3])