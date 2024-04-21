class Chore:
    def __init__(self, json):
        self.name = json.get("name", default="Chore", type=str)
        self.description = json.get("description", default="", type=str)
        self.poster = json.get("poster", default="Anonymous", type=str)
        self.fulfiller = json.get("fulfiller", default="All", type=str)

