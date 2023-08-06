import pandas as pd

from ..._tools._dataframe import (
    convert_column_df_to_datetime,
    convert_items_df_to_datetime,
)
from ...eikon._tools import tz_replacer


def news_build_df_udf(raw, **kwargs):
    df = convert_content_data_to_df_udf(raw)
    return df


def news_build_df_rdp(raw, **kwargs):
    columns = ["versionCreated", "text", "storyId", "sourceCode"]

    if isinstance(raw, list):
        data = []

        for i in raw:
            data.extend(i["data"])

    else:
        data = raw["data"]

    first_created = [
        tz_replacer(headline["newsItem"]["itemMeta"]["firstCreated"]["$"])
        for headline in data
    ]
    index = convert_items_df_to_datetime(first_created)
    headlines = []

    for headline_data in data:
        news_item = headline_data.get("newsItem", dict())
        item_meta = news_item.get("itemMeta", {})
        info_sources = news_item["contentMeta"]["infoSource"]
        info_source = next(
            (
                item["_qcode"]
                for item in info_sources
                if item["_role"] == "sRole:source"
            ),
            None,
        )
        version_created = pd.to_datetime(item_meta["versionCreated"]["$"])
        headlines.append(
            [
                version_created,
                item_meta["title"][0]["$"],
                headline_data["storyId"],
                info_source,
            ]
        )
    if headlines:
        dataframe = pd.DataFrame(
            data=headlines,
            index=index,
            columns=columns,
        )

        if not dataframe.empty:
            dataframe = dataframe.convert_dtypes()
        dataframe["versionCreated"] = dataframe["versionCreated"].dt.tz_localize(None)

    else:
        dataframe = pd.DataFrame([], columns=columns)
    return dataframe


def convert_content_data_to_df_udf(content_data: dict) -> pd.DataFrame:
    selected_fields = ["versionCreated", "text", "storyId", "sourceCode"]

    raw_headlines = content_data.get("headlines", [])
    first_created = [
        tz_replacer(headline["firstCreated"]) for headline in raw_headlines
    ]
    index = convert_items_df_to_datetime(first_created)

    headlines = [
        [headline[field] for field in selected_fields] for headline in raw_headlines
    ]
    if len(headlines):
        df = pd.DataFrame(
            headlines,
            index=index,
            columns=selected_fields,
        )

        if not df.empty:
            df = df.convert_dtypes()

    else:
        df = pd.DataFrame([], index, selected_fields)

    convert_column_df_to_datetime(df, "versionCreated")
    df.fillna(pd.NA, inplace=True)

    return df


def _get_text_from_story(story):
    news_item = story.get("newsItem", dict())
    content_set = news_item.get("contentSet", dict())
    inline_data = content_set.get("inlineData", [dict()])
    return inline_data[0].get("$")


def _get_headline_from_story(story):
    news_item = story.get("newsItem", dict())
    content_meta = news_item.get("contentMeta", dict())
    headline = content_meta.get("headline", [dict()])
    return headline[0].get("$")


def get_headlines_rdp(raw, create_headline_func, limit):
    headlines = []

    if isinstance(raw, list):

        data = []
        for i in raw:
            data.extend(i.get("data", i.get("headlines", [])))

    else:
        data = raw.get("data", raw.get("headlines", []))

    for datum in data:
        headline = create_headline_func(datum)
        headlines.append(headline)

    headlines = headlines[:limit]
    return headlines
