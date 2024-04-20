import datetime


class Chore:
    def __init__(self, args):
        self.name = args.get("name", default="Chore", type=str)
        self.description = args.get("description", default="", type=str)
        self.poster = args.get("poster", default="Anonymous", type=str)
        self.fulfiller = args.get("fulfiller", default="All", type=str)

        datetime = args.get("datetime", default="", type=str)
        if datetime != "":
            self.datetime = datetime.strptime(datetime, "%Y-%m-%d %H:%M")
        else:
            self.datetime = datetime.datetime.now()

