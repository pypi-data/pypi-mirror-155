import config as ext_config_mod

from typing import Union

from ._desktop_session import DesktopSession
from ._session_type import SessionType
from ._platform_session import PlatformSession
from ... import _configure as configure
from .grant_password import GrantPassword

CANNOT_FIND_APP_KEY = "Can't find 'app-key' in config object."

DEPLOYED_PLATFORM_URL_CONFIG_KEY = "realtime-distribution-system.url"
DEPLOYED_PLATFORM_USER_CONFIG_KEY = "realtime-distribution-system.dacs.username"
DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY = "realtime-distribution-system.dacs.position"
DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY = (
    "realtime-distribution-system.dacs.application-id"
)

PLATFORM_ARGUMENT_KEY_TO_CONFIG_KEY = {
    "app_key": "app-key",
    "signon_control": "signon_control",
    "deployed_platform_host": DEPLOYED_PLATFORM_URL_CONFIG_KEY,
    "deployed_platform_username": DEPLOYED_PLATFORM_USER_CONFIG_KEY,
    "dacs_position": DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY,
    "dacs_application_id": DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY,
    "realtime_distribution_system_url": DEPLOYED_PLATFORM_URL_CONFIG_KEY,
    "auto_reconnect": "auto-reconnect",
    "server_mode": "server-mode",
    "base_url": "base-url",
    "auth_url": "auth.url",
    "auth_authorize": "auth.authorize",
    "auth_token": "auth.token",
}

DESKTOP_ARGUMENT_KEY_TO_CONFIG_KEY = {
    "app_key": "app-key",
    "token": "token",
    "dacs_position": DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY,
    "dacs_application_id": DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY,
    "base_url": "base-url",
    "platform_path_rdp": "platform-paths.rdp",
    "platform_path_udf": "platform-paths.udf",
    "handshake_url": "handshake-url",
}

session_class_by_session_type = {
    SessionType.DESKTOP: DesktopSession,
    SessionType.PLATFORM: PlatformSession,
}

session_alias_by_session_type = {
    "platform": SessionType.PLATFORM,
    "desktop": SessionType.DESKTOP,
}


def get_session_type(value: Union[SessionType, str]):
    session_type = None

    if isinstance(value, SessionType):
        session_type = value

    elif isinstance(value, str):
        session_type = session_alias_by_session_type.get(value)

    if not session_type:
        raise ValueError(f"Cannot get session type by value:{value}")

    return session_type


def _retrieve_values_from_config(config, session_type, grant):
    arguments = {}
    if session_type == SessionType.PLATFORM:
        username = config.get("username")
        password = config.get("password")
        arguments["grant"] = grant or GrantPassword(username, password)

        for argument, value in PLATFORM_ARGUMENT_KEY_TO_CONFIG_KEY.items():
            arguments[argument] = config.get(value)
    else:

        for argument, value in DESKTOP_ARGUMENT_KEY_TO_CONFIG_KEY.items():
            arguments[argument] = config.get(value)

    return arguments


def _validate_platform_session_arguments(
    app_key=None,
    grant=None,
    deployed_platform_host=None,
    deployed_platform_username=None,
):
    if app_key == "":
        raise AttributeError(CANNOT_FIND_APP_KEY)

    if app_key is None:
        raise AttributeError(
            "Please, set app-key in [session.platform.default] section of "
            "the config file or provide 'app-key' attribute to the definition."
        )

    if not grant.is_valid() and (
        not deployed_platform_host or not deployed_platform_username
    ):
        raise AttributeError(
            "To create platform session, please provide 'grant' attribute to the "
            "definition or set 'username' and 'password' in the config file. "
            "To create deployed session, please provide 'deployed_platform_host' "
            "and 'deployed_platform_username' to the definition or the config file."
        )


def _make_platform_session_provider_by_arguments(
    session_name,
    app_key=None,
    signon_control=None,
    deployed_platform_host=None,
    deployed_platform_username=None,
    dacs_position=None,
    dacs_application_id=None,
    grant=None,
):
    session_config = configure.get(configure.keys.platform_session(session_name), {})
    default_session_config = configure.get(
        configure.keys.platform_session("default"), {}
    )

    if isinstance(session_config, dict) and len(session_config) == 0:
        raise ValueError(
            f"Session name: {session_name} is invalid or session_name object is empty"
        )

    arguments = {
        "app-key": app_key,
        "signon_control": signon_control,
        DEPLOYED_PLATFORM_URL_CONFIG_KEY: deployed_platform_host,
        DEPLOYED_PLATFORM_USER_CONFIG_KEY: deployed_platform_username,
        DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY: dacs_position,
        DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY: dacs_application_id,
    }
    filtered_arguments = {
        key: value for key, value in arguments.items() if value is not None
    }

    merged_config = ext_config_mod.ConfigurationSet(
        ext_config_mod.config_from_dict(filtered_arguments),
        session_config,
        default_session_config,
    )

    app_key = merged_config.get("app-key")
    username = merged_config.get("username")
    password = merged_config.get("password")
    deployed_platform_host = merged_config.get(DEPLOYED_PLATFORM_URL_CONFIG_KEY)
    deployed_platform_username = merged_config.get(DEPLOYED_PLATFORM_USER_CONFIG_KEY)
    grant = grant or GrantPassword(username, password)

    _validate_platform_session_arguments(
        app_key=app_key,
        grant=grant,
        deployed_platform_host=deployed_platform_host,
        deployed_platform_username=deployed_platform_username,
    )

    return make_session_provider(
        SessionType.PLATFORM, merged_config, grant, session_name
    )


def _validate_desktop_session_app_key(
    session_config=None, app_key=None, session_name=None
):
    if not app_key:
        raise AttributeError(CANNOT_FIND_APP_KEY)

    if not session_config and not app_key:
        raise ValueError(
            f"Can't get config by name: {session_name}. Please check config name or provide app_key"
        )


def _make_desktop_session_provider_by_arguments(session_name, app_key=None):
    session_config = configure.get(configure.keys.desktop_session(session_name), {})
    default_session_config = configure.get(
        configure.keys.desktop_session("workspace"), {}
    )

    if isinstance(session_config, dict) and len(session_config) == 0:
        raise ValueError(
            f"Session name: {session_name} is invalid or session_name object is empty"
        )

    arguments = {"app-key": app_key}
    filtered_arguments = {
        key: value for key, value in arguments.items() if value is not None
    }

    merged_config = ext_config_mod.ConfigurationSet(
        ext_config_mod.config_from_dict(filtered_arguments),
        session_config,
        default_session_config,
    )

    _validate_desktop_session_app_key(
        session_config=session_config,
        app_key=merged_config.get("app-key"),
        session_name=session_name,
    )

    return make_session_provider(
        SessionType.DESKTOP, merged_config, session_name=session_name
    )


def _validate_session_arguments(
    app_key, session_type, grant, deployed_platform_host, deployed_platform_username
):
    if app_key is None:
        raise AttributeError(CANNOT_FIND_APP_KEY)

    if (
        session_type == SessionType.PLATFORM
        and not grant.is_valid()
        and (not deployed_platform_host or not deployed_platform_username)
    ):
        raise AttributeError(
            "Please provide 'grant' attribute or set 'username' and 'password' in config. "
            "Or provide deployed parameters in config file to create deployed platform session"
        )


def _make_session_provider_by_arguments(session_name):
    from ._session_definition import (
        _get_session_type_and_name,
        _retrieve_config_and_set_type,
    )

    config_path = session_name  # can't rename argument, because public API, make it right at least in function body
    session_name, session_type = _get_session_type_and_name(config_path)
    session_config = _retrieve_config_and_set_type(session_name, session_type)

    if session_type == SessionType.DESKTOP:
        default_session_config = configure.get(
            configure.keys.desktop_session("workspace"), {}
        )
    else:
        default_session_config = configure.get(
            configure.keys.platform_session("default"), {}
        )

    merged_config = ext_config_mod.ConfigurationSet(
        session_config, default_session_config
    )
    app_key = merged_config.get("app-key")
    deployed_platform_host = merged_config.get(DEPLOYED_PLATFORM_URL_CONFIG_KEY)
    deployed_platform_username = merged_config.get(DEPLOYED_PLATFORM_USER_CONFIG_KEY)

    grant = None
    if session_type == SessionType.PLATFORM:
        grant = GrantPassword(
            merged_config.get("username"), merged_config.get("password")
        )

    _validate_session_arguments(
        app_key=app_key,
        session_type=session_type,
        grant=grant,
        deployed_platform_host=deployed_platform_host,
        deployed_platform_username=deployed_platform_username,
    )

    return make_session_provider(session_type, merged_config, grant, session_name)


def make_session_provider(
    session_type, config=None, grant=None, session_name="default"
):
    config = config or {}
    session_class = session_class_by_session_type.get(session_type)
    if not session_class:
        raise ValueError(f"Cannot find session class by session type {session_type}")
    session_class = get_session_class(session_type)

    def session_provider():
        params = _retrieve_values_from_config(config, session_type, grant)
        params["name"] = session_name
        sessions_inst = session_class(**params)
        sessions_inst.debug(f" + Session created {sessions_inst}")
        return sessions_inst

    return session_provider


def get_session_class(session_type):
    session_class = session_class_by_session_type.get(session_type, None)

    if session_class is None:
        raise ValueError(f"Cannot find session class by session type {session_type}")

    return session_class
