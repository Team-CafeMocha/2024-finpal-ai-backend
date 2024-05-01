class ChatResponse:
    requestContent = None
    responseContent = None

    def __init__(self, requestContent: str, responseContent: str):
        self.requestContent = requestContent
        self.responseContent = responseContent

    def toResponse(self) -> dict:
        return {"request": self.requestContent, "response": self.responseContent}


class EmbedResponse:
    fileName = None
    response = None

    def __init__(self, fileName: str, response: str):
        self.fileName = fileName
        self.response = response

    def toResponse(self) -> dict:
        return {"fileName": self.fileName, "response": self.response}
