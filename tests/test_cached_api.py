# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

import os
import sys
import unittest
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_api_proxy.cached_api import CachedAPI


class TestCachedAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = CachedAPI("test")

    def test_cached_request(self):
        url = "https://neon.ai"
        res = self.api.session.get(url, timeout=10)
        cached = self.api.session.get(url, timeout=10)
        self.assertTrue(cached.from_cache)
        self.assertEqual(res.content, cached.content)

    def test_request_no_cache(self):
        url = "https://neon.ai"
        res = self.api.session.get(url, timeout=10)
        with self.api.session.cache_disabled():
            cached = self.api.session.get(url, timeout=10)
            self.assertFalse(cached.from_cache)
        self.assertEqual(res.content, cached.content)

    def test_get_with_cache_timeout(self):
        url = "https://chatbotsforum.org"
        res = self.api.get_with_cache_timeout(url, 5)
        self.assertFalse(res.from_cache)
        cached = self.api.get_with_cache_timeout(url, 15)
        self.assertTrue(cached.from_cache)
        self.assertEqual(res.content, cached.content)
        sleep(5)
        expired = self.api.get_with_cache_timeout(url)
        self.assertFalse(expired.from_cache)

    def test_get_bypass_cache(self):
        url = "https://klat.com"
        res = self.api.get_with_cache_timeout(url)
        self.assertFalse(res.from_cache)
        cached = self.api.get_with_cache_timeout(url)
        self.assertTrue(cached.from_cache)
        no_cache = self.api.get_bypass_cache(url)
        self.assertFalse(no_cache.from_cache)


if __name__ == '__main__':
    unittest.main()
