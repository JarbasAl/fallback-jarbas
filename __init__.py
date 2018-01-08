# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import dirname
from mycroft.skills.core import FallbackSkill
import sys

# add skill folder to import path
sys.path.append(dirname(__file__))

# import server api
from api import JarbasAPI

__author__ = "jarbas"


class JarbasServerSkill(FallbackSkill):
    def __init__(self):
        super(JarbasServerSkill, self).__init__()
        self.api = self.settings.get("api_key")

    def initialize(self):
        self.https_api = JarbasAPI(self.api, self.lang, self.settings["url"])
        self.register_fallback(self.handle_fallback, 97)

    def handle_fallback(self, message):
        utterance = message.data['utterance']
        # ask the https endpoint
        res = self.https_api.ask_mycroft(utterance)
        ans = res.get("data", {}).get("utterance", "")
        if ans in ["server timed out", "", "i have no idea how to answer that", "something went wrong, ask me later"]:
            return False
        self.speak(ans)
        return True


def create_skill():
    return JarbasServerSkill()
