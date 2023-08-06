import datetime

import pandas as pd

from ._tools import _get_text_from_story, _get_headline_from_story
from ._udf_html_parser import HeadlineHTMLParser
from ._urgency import Urgency


class NewsData(object):
    def __init__(
        self,
        title,
        creator,
        source,
        language,
        item_codes,
        urgency,
        creation_date,
        update_date,
        raw,
        news_type,
    ):

        self.title = title
        self.creator = creator
        self.source = source
        self.language = language
        self.item_codes = item_codes
        self.urgency = Urgency(urgency)
        self.creation_date = pd.to_datetime(creation_date)
        self.update_date = pd.to_datetime(update_date)

        if news_type == "story":
            self.content = _get_text_from_story(raw)
            self.headline = _get_headline_from_story(raw)
        elif news_type == "headline":
            self.story_id = raw["storyId"]


class Headline(NewsData):
    @staticmethod
    def create(datum):
        news_item = datum.get("newsItem")
        content_meta = news_item.get("contentMeta")
        item_meta = news_item.get("itemMeta")
        subject = content_meta.get("subject")
        headline = Headline(
            title=item_meta.get("title")[0].get("$"),
            creator=content_meta.get("creator")[0].get("_qcode"),
            source=content_meta.get("infoSource"),
            language=content_meta.get("language"),
            item_codes=[item.get("_qcode") for item in subject],
            urgency=content_meta.get("urgency").get("$"),
            creation_date=item_meta.get("firstCreated").get("$"),
            update_date=item_meta.get("versionCreated").get("$"),
            raw=datum,
            news_type="headline",
        )
        return headline


class HeadlineUDF:
    def __init__(
        self,
        display_direction,
        document_type,
        first_created,
        is_alert,
        language,
        report_code,
        source_name,
        story_id,
        text,
        version_created,
    ):
        self.display_direction = display_direction
        self.document_type = document_type
        self.first_created = first_created
        self.is_alert = is_alert
        self.language = language
        self.report_code = report_code
        self.source_name = source_name
        self.story_id = story_id
        self.text = text
        self.version_created = version_created

    @staticmethod
    def create(datum):
        display_direction = datum.get("displayDirection")
        document_type = datum.get("documentType")
        first_created = datum.get("firstCreated")
        is_alert = datum.get("isAlert")
        language = datum.get("language")
        report_code = datum.get("reportCode")
        source_name = datum.get("sourceName")
        story_id = datum.get("storyId")
        text = datum.get("text")
        version_created = datum.get("versionCreated")
        headline = HeadlineUDF(
            display_direction=display_direction,
            document_type=document_type,
            first_created=first_created,
            is_alert=is_alert,
            language=language,
            report_code=report_code,
            source_name=source_name,
            story_id=story_id,
            text=text,
            version_created=version_created,
        )
        return headline


class Story(NewsData):
    @staticmethod
    def create(datum):
        news_item = datum.get("newsItem")
        content_meta = news_item.get("contentMeta")
        item_meta = news_item.get("itemMeta")
        subject = content_meta.get("subject")
        headline = Headline(
            title=item_meta.get("title")[0].get("$"),
            creator=content_meta.get("creator")[0].get("_qcode"),
            source=content_meta.get("infoSource"),
            language=content_meta.get("language"),
            item_codes=[item.get("_qcode") for item in subject],
            urgency=content_meta.get("urgency").get("$"),
            creation_date=item_meta.get("firstCreated").get("$"),
            update_date=item_meta.get("versionCreated").get("$"),
            raw=datum,
            news_type="story",
        )
        return headline


class StoryUDF:
    def __init__(
        self,
        title: str,
        content: str,
        creation_date: datetime.datetime,
        headline: str,
        creator=None,
    ) -> None:
        self.title = title
        self.content = content
        self.creator = creator
        self.creation_date = creation_date
        self.headline = headline

    @staticmethod
    def create(datum):
        parser = HeadlineHTMLParser()
        story = datum["story"]
        for i in story:
            parser.feed(story[i])
        text = parser.data.get("text") or []
        text = "\n".join(text)
        headline = StoryUDF(
            title=parser.data.get("headline"),
            content=text,
            creator=parser.data.get("creator"),
            creation_date=pd.to_datetime(parser.data.get("creation_date")),
            headline=parser.data.get("headline"),
        )
        return headline
