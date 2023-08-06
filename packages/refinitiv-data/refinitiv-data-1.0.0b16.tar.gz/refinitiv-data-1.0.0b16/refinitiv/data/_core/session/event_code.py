from enum import unique, Enum


@unique
class EventCode(Enum):
    """
    Each session can report different status events during it's lifecycle.
        StreamConnecting : Denotes the connection to the stream service within the
        session is pending.
        StreamConnected : Denotes the connection to the stream service has been
        successfully established.
        StreamDisconnected : Denotes the connection to the stream service is not
        established.
        SessionAuthenticationSuccess : Denotes the session has successfully
        authenticated this client.
        SessionAuthenticationFailed : Denotes the session has failed to authenticate
        this client.
        StreamAuthenticationSuccess: Denotes the stream has successfully
        authenticated this client.
        StreamAuthenticationFailed: Denotes the stream has failed to authenticate
        this client.
        DataRequestOk : The request for content from the session data services has
        completed successfully.
        DataRequestFailed : The request for content from the session data services
        has failed.
    """

    StreamConnecting = 1
    StreamConnected = 2
    StreamDisconnected = 3
    StreamAuthenticationSuccess = 4
    StreamAuthenticationFailed = 5
    StreamReconnecting = 6

    SessionConnecting = 21
    SessionConnected = 22
    SessionDisconnected = 23
    SessionAuthenticationSuccess = 24
    SessionAuthenticationFailed = 25
    SessionReconnecting = 26

    DataRequestOk = 61
    DataRequestFailed = 62
