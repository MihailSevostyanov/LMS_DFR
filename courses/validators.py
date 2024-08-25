import re

from rest_framework.exceptions import ValidationError


class VideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile("\Byoutube.com\B")

        tmp_val = dict(value).get(self.field)
        if tmp_val is None:
            return

        first_match = re.search("youtube.com", tmp_val)

        if not bool(first_match):
            raise ValidationError("Video_url must be only link to 'youtube'")
