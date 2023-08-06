import re
from urllib.parse import ParseResult, urlparse, ParseResultBytes

pattern_1 = re.compile("(.)([A-Z][a-z]+)")
pattern_2 = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(s):
    if not s:
        return s

    if "_" in s:
        words = [camel_to_snake(w) for w in s.split("_")]
        s = "_".join(words)

    else:
        s = pattern_1.sub(r"\1_\2", s)
        s = pattern_2.sub(r"\1_\2", s)

    return s.lower()


def parse_url(url: str) -> ParseResult:
    import sys

    py_ver = sys.version_info
    if py_ver.major == 3 and py_ver.minor < 9:

        result_urlparse = urlparse(url)

        if isinstance(result_urlparse, ParseResultBytes):
            return result_urlparse

        scheme = result_urlparse.scheme
        netloc = result_urlparse.netloc
        path = result_urlparse.path
        query = result_urlparse.query
        fragment = result_urlparse.fragment

        if not scheme and not netloc and path and ":" in path:
            splitted = path.split(":")
            if len(splitted) == 2:
                scheme, path = splitted

        result = ParseResult(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=result_urlparse.params,
            query=query,
            fragment=fragment,
        )
    else:

        result = urlparse(url)

    return result


def validate_endpoint_request_url_parameters(url, path_parameters):
    if url == "":
        raise ValueError("Requested URL is missing, please provide valid URL")

    if url.endswith("{universe}") and not path_parameters:
        raise ValueError(
            "Path parameter 'universe' is missing, please provide path parameter"
        )
