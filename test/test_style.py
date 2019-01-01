# encoding: utf-8

from __future__ import print_function, unicode_literals

import sys

import pytest
from pytablewriter.style import Align, FontSize, Style, ThousandSeparator


class Test_Style_constructor(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                {
                    "align": Align.RIGHT,
                    "font_size": FontSize.TINY,
                    "thousand_separator": ThousandSeparator.SPACE,
                },
                {
                    "align": Align.RIGHT,
                    "font_size": FontSize.TINY,
                    "thousand_separator": ThousandSeparator.SPACE,
                },
            ],
            [
                {"align": "left", "font_size": "small", "thousand_separator": ","},
                {
                    "align": Align.LEFT,
                    "font_size": FontSize.SMALL,
                    "thousand_separator": ThousandSeparator.COMMA,
                },
            ],
            [
                {"font_size": "TINY"},
                {"font_size": FontSize.TINY, "thousand_separator": ThousandSeparator.NONE},
            ],
        ],
    )
    def test_normal(self, value, expected):
        style = Style(**value)

        print("expected: {}\nactual: {}".format(expected, style), file=sys.stderr)

        assert style.align is expected.get("align")
        assert style.font_size is expected.get("font_size")
        assert style.thousand_separator is expected.get("thousand_separator")


class Test_Style_eq(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [Style(), Style(), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT), True],
            [Style(align=Align.RIGHT), Style(align=Align.LEFT), False],
            [Style(align=Align.RIGHT), Style(align="right"), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT, font_size=FontSize.TINY), False],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.TINY), True],
            [Style(font_size=FontSize.TINY), Style(font_size="tiny"), True],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.LARGE), False],
            [Style(thousand_separator=","), Style(thousand_separator=","), True],
            [Style(thousand_separator=","), Style(thousand_separator="comma"), True],
            [Style(thousand_separator=""), Style(thousand_separator=","), False],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA),
                True,
            ],
            [
                Style(thousand_separator="space"),
                Style(thousand_separator=ThousandSeparator.SPACE),
                True,
            ],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA, font_size=FontSize.TINY),
                False,
            ],
            [
                Style(
                    align=Align.LEFT,
                    font_size=FontSize.TINY,
                    thousand_separator=ThousandSeparator.COMMA,
                ),
                Style(align="left", font_size="tiny", thousand_separator=","),
                True,
            ],
            [Style(), None, False],
        ],
    )
    def test_normal(self, lhs, rhs, expected):
        assert (lhs == rhs) == expected
        assert (lhs != rhs) != expected

    @pytest.mark.parametrize(
        ["align", "font_size", "thousand_separator", "expected"],
        [
            ["invali", None, None, TypeError],
            [FontSize.TINY, None, None, TypeError],
            [None, "invali", None, TypeError],
            [None, Align.LEFT, None, TypeError],
            [None, None, "invalid", TypeError],
        ],
    )
    def test_exception(self, align, font_size, thousand_separator, expected):
        with pytest.raises(expected):
            Style(align=align, font_size=font_size, thousand_separator=thousand_separator)
