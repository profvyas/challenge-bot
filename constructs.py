class Response:

    def __init__(self, content, reply=False, delete_after=0):
        self._content = content
        self.reply = reply
        self.delete_after = delete_after
    
    @property
    def content(self):
        return self._content

# Example response type
class GraphResponse(Response):

    def __init__(self, content, delete_after=0):
        super().__init__(content, delete_after=delete_after)