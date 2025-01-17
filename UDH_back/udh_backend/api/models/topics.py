import typing

from django.db import models

from api.status import StatusEnumerator


class Topics(models.Model):
    # TODO: remove topic if no articles
    MAXIMUM_TITLE_LENGTH = 100

    title = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=0)

    @classmethod
    def get_topic(cls, _topic: str):
        topic: cls = cls.objects.filter(title=_topic).first()
        if topic:
            return topic

        if len(_topic) > cls.MAXIMUM_TITLE_LENGTH:
            return StatusEnumerator.DataTooLong

        topic = cls()
        topic.title = _topic
        topic.save()
        return topic

    @classmethod
    def parse_topics(cls, raw_topics: typing.List | typing.Tuple):
        topics = list()

        for raw_topic in raw_topics:
            topic = cls.get_topic(raw_topic)
            if isinstance(topic, StatusEnumerator):
                return topic
            topics.append(topic)

        for topic in topics:
            topic.increment_view()
            topic.save()
        return topics

    def increment_view(self):
        self.rating += 1
