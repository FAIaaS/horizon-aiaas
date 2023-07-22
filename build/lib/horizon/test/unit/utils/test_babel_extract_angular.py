# -*- encoding: utf-8 -*-
# Copyright 2015, Rackspace, US, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import io

from horizon.test import helpers as test
from horizon.utils.babel_extract_angular import extract_angular

default_keys = []


class ExtractAngularTestCase(test.TestCase):

    def test_extract_no_tags(self):
        buf = io.StringIO('<html></html>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([], messages)

    def test_simple_string(self):
        buf = io.StringIO(
            """<html><translate>hello world!</translate>'
            <div translate>hello world!</div></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', []),
                (2, 'gettext', 'hello world!', [])
            ],
            messages)

    def test_attr_value(self):
        """Should not translate tags with translate as the value of an attr."""
        buf = io.StringIO('<html><div id="translate">hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([], messages)

    def test_attr_value_plus_directive(self):
        """Unless they also have a translate directive."""
        buf = io.StringIO(
            '<html><div id="translate" translate>hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_translate_tag(self):
        buf = io.StringIO('<html><translate>hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_plural_form(self):
        buf = io.StringIO(
            (
                '<html><translate translate-plural="hello {$count$} worlds!">'
                'hello one world!</translate></html>'
            ))

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'ngettext',
                 ('hello one world!',
                  'hello {$count$} worlds!'
                  ),
                 [])
            ], messages)

    def test_translate_tag_comments(self):
        buf = io.StringIO(
            '<html><translate translate-comment='
            '"What a beautiful world">hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_comments(self):
        buf = io.StringIO(
            '<html><div translate translate-comment='
            '"What a beautiful world">hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_multiple_comments(self):
        buf = io.StringIO(
            '<html><translate '
            'translate-comment="What a beautiful world"'
            'translate-comment="Another comment"'
            '>hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!',
                 [
                     'What a beautiful world',
                     'Another comment'
                 ])
            ],
            messages)

    def test_filter(self):
        # test also for some forms that should not match
        buf = io.StringIO(
            """
            <img alt="{$ 'hello world1' | translate $}">
            <p>{$'hello world2'|translate$}</p>
            <img alt="something {$'hello world3'|translate$} something
            {$'hello world4'|translate$}">
            <img alt="{$expr()|translate$}">
            <img alt="{$'some other thing'$}">
            <p>{$'"it\\'s awesome"'|translate$}</p>
            <p>{$"oh \\"hello\\" there"|translate$}</p>
            <img alt="{$::'hello colon1' | translate $}">
            <p>{$ ::'hello colon2' |translate$}</p>
            <p>{$ :: 'hello colon3'| translate$}</p>
            <img alt="something {$::'hello colon4'|translate$} something
            {$ ::'hello colon5' | translate$}">
            <img alt="{::$expr()|translate$}">
            <img alt="{$::'some other thing'$}">
            <p>{$:: '"it\\'s awesome"'|translate$}</p>
            <p>{$ :: "oh \\"hello\\" there" | translate$}</p>
            """
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (2, 'gettext', 'hello world1', []),
                (3, 'gettext', 'hello world2', []),
                (4, 'gettext', 'hello world3', []),
                (4, 'gettext', 'hello world4', []),
                (8, 'gettext', '"it\\\'s awesome"', []),
                (9, 'gettext', 'oh \\"hello\\" there', []),
                (10, 'gettext', 'hello colon1', []),
                (11, 'gettext', 'hello colon2', []),
                (12, 'gettext', 'hello colon3', []),
                (13, 'gettext', 'hello colon4', []),
                (13, 'gettext', 'hello colon5', []),
                (17, 'gettext', '"it\\\'s awesome"', []),
                (18, 'gettext', 'oh \\"hello\\" there', []),
            ],
            messages)

    def test_trim_translate_tag(self):
        buf = io.StringIO(
            "<html><translate> \n hello\n world! \n "
            "</translate></html>")

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello\n world!', [])], messages)

    def test_nested_translate_tag(self):
        buf = io.StringIO(
            "<html><translate>hello <b>beautiful <i>world</i></b> !"
            "</translate></html>"
        )

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [(1, 'gettext', 'hello <b>beautiful <i>world</i></b> !', [])],
            messages)

    def test_nested_variations(self):
        buf = io.StringIO(
            '''
            <p translate>To <a href="link">link</a> here</p>
            <p translate>To <!-- a comment!! --> here</p>
            <p translate>To trademark&reg; &#62; &#x3E; here</p>
            '''
        )
        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (2, 'gettext', 'To <a href="link">link</a> here', []),
                (3, 'gettext', 'To <!-- a comment!! --> here', []),
                (4, 'gettext', 'To trademark® &#62; &#x3E; here', []),
            ],
            messages)
