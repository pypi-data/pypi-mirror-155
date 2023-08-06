import socket


class DacsParams(object):
    """DacsParams object."""

    def __init__(self, *args, **kwargs):
        self.deployed_platform_username = kwargs.get(
            "deployed_platform_username", "user"
        )
        self.dacs_application_id = kwargs.get("dacs_application_id", "256")
        self.dacs_position = kwargs.get("dacs_position")
        if self.dacs_position in [None, ""]:
            try:
                position_host = socket.gethostname()
                self.dacs_position = "{}/{}".format(
                    socket.gethostbyname(position_host), position_host
                )
            except socket.gaierror:
                self.dacs_position = "127.0.0.1/net"
        self.authentication_token = kwargs.get("authentication_token")
