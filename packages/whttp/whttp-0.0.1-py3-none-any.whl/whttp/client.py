import pythoncom
from win32com.client import Dispatch

# CoInitialize in case of multi-threading
pythoncom.CoInitialize()


class HTTPResponse:
    def __init__(self, winhttp_obj):
        self.status = winhttp_obj.status
        self.text = winhttp_obj.ResponseText


class HTTPClient:
    def __init__(self):
        self._winhttp = Dispatch("winhttp.winhttprequest.5.1")

    def get(self, url: str) -> tuple([int, str]):
        winhttp = self._winhttp
        self._winhttp = Dispatch("winhttp.winhttprequest.5.1")
        winhttp.Open("GET", url, False)
        winhttp.Send()
        winhttp.WaitForResponse()
        return HTTPResponse(winhttp)
