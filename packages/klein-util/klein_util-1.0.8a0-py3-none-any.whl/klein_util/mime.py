# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
import re


class Detect:

    mimetype = ""
    html = re.compile("(text/(html))|(application/x(html).*)")
    rtf = re.compile("(text/(rtf))")
    calendar = re.compile("(text/(calendar))")
    text = re.compile("(text/.*)")
    image = re.compile("(image/(.*))")
    audio = re.compile("(audio/(.*))")
    video = re.compile("(video/(.*))")
    archive = re.compile("application/(gzip|vnd.ms-cab-compressed|x-(7z-compressed|ace-compressed|alz-compressed|apple-diskimage|arj|astrotite-afa|b1|bzip2|cfs-compressed|compress|cpio|dar|dgc-compressed|gca-compressed|gtar|lzh|lzip|lzma|lzop|lzx|par2|rar-compressed|sbx|shar|snappy-framed|stuffit|stuffitx|tar|xz|zoo)|zip)")
    tabular = [
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "application/vnd.ms-excel.sheet.macroenabled.12"
    ]
        

    def __init__(self, mimetype):
        self.mimetype = mimetype

    def is_html(self):
        return self.html.match(self.mimetype)

    def is_rtf(self):
        return self.rtf.match(self.mimetype)

    def is_calendar(self):
        return self.calendar.match(self.mimetype)

    def is_text(self):
        return self.text.match(self.mimetype)

    def is_archive(self):
        return self.archive.match(self.mimetype)

    def is_tabular(self):
        return (self.mimetype in self.tabular)

    def is_image(self):
        return self.image.match(self.mimetype)

    def is_audio(self):
        return self.audio.match(self.mimetype)

    def is_video(self):
        return self.video.match(self.mimetype)

    def is_ner_friendly(self):
        return (not self.is_image() and not self.is_archive() and not self.is_audio() and not self.is_video())
