# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import enum

from dataproperty import Align

from .._function import normalize_enum
from ._font import FontSize, FontWeight


@enum.unique
class ThousandSeparator(enum.Enum):
    NONE = 0
    COMMA = 1
    SPACE = 2


_s_to_ts = {"": ThousandSeparator.NONE, ",": ThousandSeparator.COMMA, " ": ThousandSeparator.SPACE}


class Style(object):
    """Style specifier class for table elements.

    Args:
        align (str / pytablewriter.Align):
            Text alignment specification for cells in a column.
            This can be applied only for text format writer classes.
            Possible values are:

            - ``"auto"``/``pytablewriter.Align.AUTO``
                - Detect data type for each column and set alignment that appropriate
                  for the type automatically
            - ``"left"``/``pytablewriter.Align.LEFT``
            - ``"right"``/``pytablewriter.Align.RIGHT``
            - ``"center"``/``pytablewriter.Align.CENTER``

        font_size (str / pytablewriter.style.FontSize):
            Font size specification for cells in a column.
            This can be applied only for HTML/Latex writer classes.
            Possible values are:

            - ``"tiny"``/``pytablewriter.style.FontSize.TINY``
            - ``"small"``/``pytablewriter.style.FontSize.SMALL``
            - ``"medium"``/``pytablewriter.style.FontSize.MEDIUM``
            - ``"large"``/``pytablewriter.style.FontSize.LARGE``
            - ``pytablewriter.style.FontSize.NONE`` (no font size specification)

        font_weight (str / pytablewriter.style.FontWeight):
            Font weight specification for cells in a column.
            This can be applied only for HTML/Latex/Markdown writer classes.
            Possible values are:

            - ``"normal"``/``pytablewriter.style.FontWeight.NORMAL``
            - ``"bold"``/``pytablewriter.style.FontWeight.BOLD``

        thousand_separator (str / pytablewriter.style.ThousandSeparator):
            Thousand separator specification for numbers in a column.
            This can be applied only for text format writer classes.
            Possible values are:

            - ``","``/``"comma"``/``pytablewriter.style.ThousandSeparator.COMMA``
            - ``" "``/``"space"``/``pytablewriter.style.ThousandSeparator.SPACE``
            - ``""``/``"none"``/``pytablewriter.style.ThousandSeparator.NONE``

    Example:
        :ref:`example-style`
    """

    @property
    def align(self):
        return self.__align

    @property
    def font_size(self):
        return self.__font_size

    @property
    def font_weight(self):
        return self.__font_weight

    @property
    def thousand_separator(self):
        return self.__thousand_separator

    def __init__(self, **kwargs):
        self.__align = normalize_enum(kwargs.pop("align", Align.AUTO), Align)
        self.__validate_attr("align", Align)

        self.__font_size = normalize_enum(kwargs.pop("font_size", FontSize.NONE), FontSize)
        self.__validate_attr("font_size", FontSize)

        self.__font_weight = normalize_enum(
            kwargs.pop("font_weight", FontWeight.NORMAL), FontWeight
        )

        self.__thousand_separator = self.__normalie_thousand_separator(
            normalize_enum(
                kwargs.pop("thousand_separator", ThousandSeparator.NONE), ThousandSeparator
            )
        )

        self.__validate_attr("thousand_separator", ThousandSeparator)

    def __repr__(self):
        items = []

        if self.align:
            items.append("align={}".format(self.align))
        if self.font_size:
            items.append("font_size={}".format(self.font_size))
        if self.__font_weight:
            items.append("__font_weight={}".format(self.__font_weight))
        if self.thousand_separator:
            items.append("thousand_separator={}".format(self.thousand_separator))

        return ", ".join(items)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        return all(
            [
                self.align is other.align,
                self.font_size is other.font_size,
                self.font_weight is other.font_weight,
                self.thousand_separator is other.thousand_separator,
            ]
        )

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __validate_attr(self, attr_name, expected_type):
        value = getattr(self, attr_name)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError("align must be a {} instancce".format(expected_type.__name__))

    @staticmethod
    def __normalie_thousand_separator(value):
        if isinstance(value, ThousandSeparator):
            return value

        norm_value = _s_to_ts.get(value)
        if norm_value is None:
            return value

        return norm_value
