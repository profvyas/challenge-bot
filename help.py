
from constructs import Response

# ToDo: use better name than help
class Help():
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.loop = bot.loop

    def get_help(self, channel):
        return Response(content="help called in channel {0}".format(channel), delete_after=15)