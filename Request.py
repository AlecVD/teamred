class Request(object):
    def __init__(self, *args, **kwargs):
        self.raw = kwargs.pop("raw", None)
        self.parse(**kwargs)
        
    def parse(self, **kwargs):
        if self.raw is None:
            raise ValueError("No request body")
        tag = kwargs.get("tag", "")
        lines = self.raw.split("\r\n")
        methLine = lines[0].split(" ")
        self.method = methLine[0]
        self.path = methLine[1]
        self.httpver = methLine[2]
        self.requestDict = {}
        for line in lines[1:]:
            sides = line.split(": ")
            if len(sides) != 2:
                continue
            if sides[0].startswith(tag):
                sides[0] = sides[0][len(tag):]
            else:
                continue
            self.requestDict[sides[0]] = sides[1]