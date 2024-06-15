from __future__ import annotations

import logging
import tkinter as tk
import tkinter.font as tkf
import tkinter.scrolledtext as st
import webbrowser as wb
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, Sequence

PARAGRAPH_BREAK: str = '\n\n'
LINE_BREAK: str = '\n'


@dataclass
class MdConfig:
    preformatted_font_family: str
    default_text_font_family: str
    font_size: int = 9
    headings_font_size: Sequence[tuple[str, int]] = (
        ('h1', 21),
        ('h2', 16),
        ('h3', 12),
        ('h4', 11),
        ('h5', 8),
        ('h6', 7),
    )

    @staticmethod
    def deafult_factory() -> MdConfig:
        _TKF_FONTS = tkf.families()

        for font in ('Courier', 'DejaVu Sans Mono', 'TkFixedFont'):
            if font in _TKF_FONTS:
                preformatted_font_family = font
                break
        else:
            preformatted_font_family = 'TkTextFont'

        for font in ('Segoe ui', 'Calibri', 'Helvetica', 'TkTextFont'):
            if font in _TKF_FONTS:
                default_text_font_family = font
                break
        else:
            default_text_font_family = 'TkTextFont'

        return MdConfig(preformatted_font_family, default_text_font_family)


class MdTag(StrEnum):
    Anchor = 'a'
    Bold = 'b'
    Italic = 'it'
    Code = 'code'
    Strike = 's'

    H1 = 'h1'
    H2 = 'h2'
    H3 = 'h3'
    H4 = 'h4'
    H5 = 'h5'
    H6 = 'h6'


class MdFrame(st.ScrolledText):
    def __init__(self, master: tk.Misc | None = None, **kwargs):
        kwargs.setdefault('wrap', tk.WORD)
        kwargs.setdefault('cursor', '')
        super().__init__(master, **kwargs)

        self.md_config: MdConfig = MdConfig.deafult_factory()

        self['font'] = tkf.Font(
            family=self.md_config.default_text_font_family, size=self.md_config.font_size
        )

        self._init_tags()

    @property
    def default_font(self) -> tkf.Font:
        """The default font used for paragraph text"""
        return self['font']

    def finalize(self) -> Self:
        self.config(state=tk.DISABLED)
        return self

    def _init_tags(self):
        default_size = self.md_config.font_size
        # Headings
        for tag, size in self.md_config.headings_font_size:
            self.tag_config(
                tag, font=tkf.Font(family=self.md_config.default_text_font_family, size=size)
            )

        # Anchors: blue text underlined
        self.tag_config(
            MdTag.Anchor,
            font=tkf.Font(family=self.md_config.default_text_font_family, size=default_size),
            underline=True,
            foreground='#0000EE',
            underlinefg='#0000EE',
        )

        # Bold
        self.tag_config(
            MdTag.Bold,
            font=tkf.Font(
                family=self.md_config.default_text_font_family, size=default_size, weight=tkf.BOLD
            ),
        )

        # Italic
        self.tag_config(
            MdTag.Italic,
            font=tkf.Font(
                family=self.md_config.default_text_font_family, size=default_size, slant=tkf.ITALIC
            ),
        )

        # Strike
        self.tag_config(
            MdTag.Strike,
            font=tkf.Font(
                family=self.md_config.default_text_font_family,
                size=default_size,
                overstrike=True,
            ),
        )

        # Code
        self.tag_config(
            MdTag.Code,
            font=tkf.Font(family=self.md_config.preformatted_font_family, size=default_size),
        )

    def heading(self, text: str, level: int = 1, end: str | None = LINE_BREAK) -> Self:
        if not (0 < level < 7):
            logging.error('Heading levels are between 1 and 6 inclusive')
            return self
        self.insert(tk.INSERT, text, 'h' + str(level))

        if end:
            self.insert(tk.INSERT, end)
        return self

    def paragraph(self, text: str, end: str | None = PARAGRAPH_BREAK) -> Self:
        self.insert(tk.INSERT, text)

        if end:
            self.insert(tk.INSERT, end)

        return self

    def link(self, link: str, text: str | None = None, end: str | None = None) -> Self:
        place_holder = text or link

        curr = self.index(tk.INSERT)
        row, col = curr.split('.')
        next_col = int(col) + len(place_holder)

        self.insert(curr, place_holder, MdTag.Anchor)
        self.tag_add(link, curr, f'{row}.{next_col}')

        self.tag_bind(link, '<Enter>', lambda _: self.config(cursor='hand2'))
        self.tag_bind(link, '<Leave>', lambda _: self.config(cursor=''))
        # TODO: arbitrary links
        self.tag_bind(link, '<ButtonPress>', lambda _: wb.open(link))

        if end:
            self.insert(tk.INSERT, end)
        return self

    def itemize(
        self,
        items: Sequence[str],
        bullet: str = '•',
        indent_by: str = '  ',
        level: int = 1,
        end: str | None = LINE_BREAK,
    ) -> Self:
        for item in items:
            self.insert(tk.INSERT, indent_by * level + bullet + ' ' + item + '\n')

        if end:
            self.insert(tk.INSERT, end)
        return self

    def enumerate(
        self,
        items: Sequence[str],
        start: int = 1,
        indent_by: str = '  ',
        level: int = 1,
        end: str | None = LINE_BREAK,
    ) -> Self:
        for idx, item in enumerate(items, start=start):
            self.insert(tk.INSERT, indent_by * level + str(idx) + '. ' + item + '\n')

        if end:
            self.insert(tk.INSERT, end)
        return self

    def strike(self, text: str, end: str | None = None) -> Self:
        self.insert(tk.INSERT, text, MdTag.Strike)
        if end:
            self.insert(tk.INSERT, end)
        return self

    def tag(self, text: str, tag: MdTag | None = None, end: str | None = None) -> Self:
        if tag:
            self.insert(tk.INSERT, text, tag)
        else:
            self.insert(tk.INSERT, text)

        if end:
            self.insert(tk.INSERT, end)

        return self
