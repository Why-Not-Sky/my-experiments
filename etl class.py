class data():
    def  __init__(self, dtype, url):
        self.type=dtype
        self.url=url

class etl():
    def __init__(self):
        self.source = data('url', 'http:')
        pass

    def _extract(self):
        pass

    def _transformation(self):
        pass

    def _load(self):
        pass

    def run(self):
        self._extract(self)
        self._transform(self)
        self._load(self)

class tse(etl):
    def __init__(self):
        pass