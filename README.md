# MdFrame

A simple minimalistic Tkinter widget for rendering Markdown documents. This module relies on [mistletoe]

[mistletoe]: <https://github.com/miyuchina/mistletoe>

## Use case 

For rendering the following:

```md
# An h1 header

Paragraphs are separated by a blank line.

2nd paragraph. _Italic_, **bold**, and `monospace`. Itemized lists look like:

- this one
- that one
- the other one

Note that --- not considering the asterisk --- the actual text content start at 4 columns in.

    Block quotes are written like so.

    They can span multiple paragraphs, if you like.

Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it's all in
chapters '12--14"). Three dots ... will be converted to an ellipsis. Unicode is
supported. 🙂

## An h2 header

Here's a numbered list:

1. first item
2. second item
3. third item

[Google Search Engine](https://www.google.com/)
```

Use the following:

```python
import tkinter as tk
from md_frame import MdFrame

root = tk.Tk()
root.title('Sample table')
root.geometry('800x600')

mdf = MdFrame(root) \
    .heading('An h1 header') \
    .paragraph('Paragraphs are separated by a blank line.') \
    .tag('2nd paragraph. ') \
    .tag('Italic', MdTag.Italic, ', ') \
    .tag('bold', MdTag.Bold, ', and ') \
    .tag('monospace', MdTag.Code, '. ') \
    .paragraph('Itemized lists look like:') \
    .itemize(('this one', 'that one', 'the other one')) \
    .paragraph('Note that ― not considering the asterisk ― the actual text content start at 4 columns in.') \
    .tag("""\
    Block quotes are written like so.

    They can span multiple paragraphs, if you like.""",
        MdTag.Code,
        PARAGRAPH_BREAK) \
    .paragraph(
        'Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it\'s all in chapters '
        '12−14"). Three dots … will be converted to an ellipsis. Unicode is supported. 🙂'
    ) \
    .heading('An h2 header', 2) \
    .paragraph("Here's a numbered list:") \
    .enumerate(('first item', 'second item', 'third item')) \
    .link('https://www.google.com/', 'Google Search Engine', ' ') \
    .finalize()

mdf.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)
root.mainloop()
```

## TODOs

- [X] Headings
- [X] Basic markup
    - [X] Bold
    - [X] Italic
    - [X] Bold-Italic
    - [X] Strike through
    - [X] Inline code
- [ ] Syntax highlighting (using Pygments)
- [ ] Hyperlinks
    - [X] Web
    - [ ] Local documents
    - [ ] Document headers
- [ ] Images
- [ ] Lists

- [ ] Tables
- [ ] LaTeX math formulas (maybe render to images using matplotlib)
