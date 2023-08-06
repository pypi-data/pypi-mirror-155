from html.parser import HTMLParser


class ParseError(Exception):
    pass


class HeadlineHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self._write_data = False
        self._key = None

    def handle_starttag(self, tag: str, attrs: tuple):
        # attrs example: (("class", "releasedDate"), ("data-version-created-date", "2021-10-03T11:08:19.096Z"))
        attrs_dict = dict(attrs)
        style_class = attrs_dict.get("class")
        if tag == "span" and style_class == "headline":
            self._write_data = True
            self._key = "headline"
        elif tag == "span" and style_class == "source":
            self.data["creator"] = attrs_dict.get("title")
        elif tag == "span" and style_class == "releasedDate":
            self.data["creation_date"] = attrs_dict.get("data-version-created-date")
        elif tag == "p":
            self._write_data = True
            self._key = "text"

    def handle_data(self, data: str):
        if self._write_data:
            if self._key == "text":
                if self.data.get("text") is None:
                    self.data["text"] = []
                self.data["text"].append(data)
            else:
                self.data[self._key] = data
            self._write_data = False

    def error(self, message):
        raise ParseError(message)
