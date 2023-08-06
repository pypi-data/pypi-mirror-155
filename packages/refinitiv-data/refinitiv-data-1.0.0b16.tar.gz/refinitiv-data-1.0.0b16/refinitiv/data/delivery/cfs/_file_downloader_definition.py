from typing import Union

from ._file_downloader_facade import FileDownloader
from ._iter_object import CFSFile
from ._stream import CFSStream


class Definition:
    """
    Parameters
    __________
        file: dict, CFSFile
            dictionary with the keys 'id' and 'filename' or CFSFile object
            if 'filename' contains any of the characters ':/|\\?*<>"' these characters will be removed

    Methods
    _______
        retrieve(session)
            Returns FileDownloader object
    """

    def __init__(self, file: Union[dict, CFSFile]):
        self._file_id = file["id"]
        self._filename_ext = file["filename"]

    def retrieve(self, session=None) -> FileDownloader:
        stream = CFSStream(id=self._file_id).get_data(session=session)
        raw = stream.data.raw

        if raw.get("error", None):
            raise ValueError(raw["error"]["message"])

        url = raw.get("url", None)

        if not url:
            raise FileNotFoundError("file not found")

        return FileDownloader(url, self._filename_ext)
