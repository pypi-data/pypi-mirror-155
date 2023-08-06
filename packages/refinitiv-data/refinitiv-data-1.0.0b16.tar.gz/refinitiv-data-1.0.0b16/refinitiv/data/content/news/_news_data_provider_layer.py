from .._content_type import ContentType
from ..._core.session import SessionType, get_valid_session
from ...delivery._data._data_provider import DataProviderLayer

NEWS_UNDERLYING_PLATFORM_KEY = "apis.data.news.underlying-platform"

udf_news_content_type_by_rdp = {
    ContentType.NEWS_STORY_RDP: ContentType.NEWS_STORY_UDF,
    ContentType.NEWS_HEADLINES_RDP: ContentType.NEWS_HEADLINES_UDF,
}


class NewsDataProviderLayer(DataProviderLayer):
    def _check_underlying_platform(self, session):
        underlying_platform = session.config.get(NEWS_UNDERLYING_PLATFORM_KEY) or "rdp"

        if underlying_platform not in {"rdp", "udf"}:
            message = (
                f"Not correct value for '{NEWS_UNDERLYING_PLATFORM_KEY}'. "
                "Possible values: 'udf', 'rdp'"
            )
            session.error(message)
            raise ValueError(message)

        if underlying_platform == "udf":
            if session.type == SessionType.PLATFORM:
                session.debug(
                    "UDF News service cannot be used with platform sessions, RDP News will be used instead. "
                    f"The '{NEWS_UNDERLYING_PLATFORM_KEY}' = 'udf' parameter "
                    "will be discarded, meaning that the regular RDP News service "
                    "will be used for News Story and News Headlines data requests."
                )

            else:
                content_type = udf_news_content_type_by_rdp.get(self._data_type)
                self._initialize(content_type, **self._kwargs)

    def get_data(self, session=None, on_response=None, *args, **kwargs):
        session = get_valid_session(session)
        self._check_underlying_platform(session)
        response = super().get_data(session, on_response, **kwargs)
        return response

    async def get_data_async(self, session=None, on_response=None, *args, **kwargs):
        session = get_valid_session(session)
        self._check_underlying_platform(session)
        response = await super().get_data_async(session, on_response, **kwargs)
        return response
