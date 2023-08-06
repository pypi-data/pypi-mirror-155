# -*- coding: utf-8 -*-
# Copyright (c) 2010, Sebastian Wiesner <lunaryorn@googlemail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
    sphinxcontrib.ansi
    ==================

    This extension parses ANSI color codes in literal blocks.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import re
from os import path

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import flag
from sphinx.util.osutil import copyfile
from sphinx.util.console import bold


class ansi_literal_block(nodes.literal_block):
    """
    Represent a literal block, that contains ANSI color codes.
    """
    pass


#: the pattern to find ANSI color codes
COLOR_PATTERN = re.compile('\x1b\\[([^m]+)m')

#: map ANSI color codes to class names
CODE_CLASS_MAP = {
    1: 'bold',
    4: 'underscore',
    30: 'black',
    31: 'red',
    32: 'green',
    33: 'yellow',
    34: 'blue',
    35: 'magenta',
    36: 'cyan',
    37: 'white',
    40: 'bg_black',
    41: 'bg_red',
    42: 'bg_green',
    43: 'bg_yellow',
    44: 'bg_blue',
    45: 'bg_magenta',
    46: 'bg_cyan',
    47: 'bg_white',
}

# Tagscriptify stuff
operators_dict = {
    "==": "☺equal☺",
    "!=": "☺notequal☺",
    ">=": "☺greaterequal☺",
    "<=": "☺lesserequal☺",
    "|": "[1;35m|",
    "+": "[1;31m+",
    "/": "[1;31m/",
    "*": "[1;31m*",
    "~": "[1;33m~",
    ",": "[1;33m,",
    "__": "[1;31m__",
    "^": "[1;31m^",
    "-": "[1;31m-",
}

blocks_dict = {
    ">": "[1;35m>", # I know these 2 are operators, but so that everything get's parsed correctly they have to be here or another dict.
    "<": "[1;35m<",
    "{=": "{[1;32m=",
    "{var": "{[1;32mvar",
    "{let": "{[1;32mlet",
    "{assign": "{[1;32massign",
    "{user": "{[1;32muser",
    "{target": "{[1;32mtarget",
    "{server": "{[1;32mserver",
    "{channel": "{[1;32mchannel",
    "{if": "{[1;33mif",
    "{any": "{[1;33many",
    "{break": "{[1;33mbreak",
    "{all": "{[1;33mall",
    "{and": "{[1;33mand",
    "{or": "{[1;33mor",
    "{unix": "{[1;32munix",
    "{uses": "{[1;32muses",
    "{args": "{[1;32margs",
    "{message": "{[1;32mmessage",
    "{join": "{[1;32mjoin",
    "{mention": "{[1;32mmention",
    "{replace": "{[1;32mreplace",
    "{contains": "{[1;32mcontains",
    "{strf": "{[1;32mstrf",
    "{#": "{[1;32m#",
    "{random": "{[1;32mrandom",
    "{rand": "{[1;32mrand",
    "{urlencode": "{[1;32murlencode",
    "{td": "{[1;32mtd",
    "{index": "{[1;32mindex",
    "{list": "{[1;32mlist",
    "{cycle": "{[1;32mcycle",
    "{in": "{[1;32min",
    "{upper": "{[1;32mupper",
    "{lower": "{[1;32mlower",
    "{math": "{[1;32mmath", # regular math removed because it breaks a lot of things
    "{range": "{[1;32mrange",
    "{?": "{[1;32m?",
    "{rangef": "{[1;32mrangef",
    "{embed": "{[1;32membed",
    ":=": ":[1;32m=",
    ":var": ":[1;32mvar",
    ":let": ":[1;32mlet",
    ":assign": ":[1;32massign",
    ":user": ":[1;32muser",
    ":target": ":[1;32mtarget",
    ":server": ":[1;32mserver",
    ":channel": ":[1;32mchannel",
    ":if": ":[1;33mif",
    ":any": ":[1;33many",
    ":break": ":[1;33mbreak",
    ":all": ":[1;33mall",
    ":and": ":[1;33mand",
    ":or": ":[1;33mor",
    ":unix": ":[1;32munix",
    ":uses": ":[1;32muses",
    ":args": ":[1;32margs",
    ":message": ":[1;32mmessage",
    ":join": ":[1;32mjoin",
    ":mention": ":[1;32mmention",
    ":replace": ":[1;32mreplace",
    ":contains": ":[1;32mcontains",
    ":strf": ":[1;32mstrf",
    ":#": ":[1;32m#",
    ":random": ":[1;32mrandom",
    ":rand": ":[1;32mrand",
    ":urlencode": ":[1;32murlencode",
    ":td": ":[1;32mtd",
    ":index": ":[1;32mindex",
    ":list": ":[1;32mlist",
    ":cycle": ":[1;32mcycle",
    ":in": ":[1;32min",
    ":upper": ":[1;32mupper",
    ":lower": ":[1;32mlower",
    ":math": ":[1;32mmath",
    ":range": ":[1;32mrange",
    ":?": ":[1;32m?",
    ":rangef": ":[1;32mrangef",
    ":embed": ":[1;32membed",
    "|=": "|[1;32m=",
    "|var": "|[1;32mvar",
    "|let": "|[1;32mlet",
    "|assign": "|[1;32massign",
    "|user": "|[1;32muser",
    "|target": "|[1;32mtarget",
    "|server": "|[1;32mserver",
    "|channel": "|[1;32mchannel",
    "|if": "|[1;33mif",
    "|any": "|[1;33many",
    "|break": "|[1;33mbreak",
    "|all": "|[1;33mall",
    "|and": "|[1;33mand",
    "|or": "|[1;33mor",
    "|unix": "|[1;32munix",
    "|uses": "|[1;32muses",
    "|message": "|[1;32mmessage",
    "|join": "|[1;32mjoin",
    "|mention": "|[1;32mmention",
    "|replace": "|[1;32mreplace",
    "|contains": "|[1;32mcontains",
    "|strf": "|[1;32mstrf",
    "|#": "|[1;32m#",
    "|random": "|[1;32mrandom",
    "|rand": "|[1;32mrand",
    "|urlencode": "|[1;32murlencode",
    "|td": "|[1;32mtd",
    "||index": "|[1;32mindex",
    "|list": "|[1;32mlist",
    "|cycle": "|[1;32mcycle",
    "|in": "|[1;32min",
    "|upper": "|[1;32mupper",
    "|lower": "|[1;32mlower",
    "|math": "|[1;32mmath",
    "|range": "|[1;32mrange",
    "|?": "|[1;32m?",
    "|rangef": "|[1;32mrangef",
    "|embed": "|[1;32membed",
}

params_dict = {
    "(avatar": "([1;35mavatar",
    "(id": "([1;35mid",
    "(created_at": "([1;35mcreated_at",
    "(joined_at": "([1;35mjoined_at",
    "(roleids": "([1;35mroleids",
    "(color": "([1;35mcolor",
    "(name": "([1;35mname",
    "(proper": "([1;35mproper",
    "(position": "([1;35mposition",
    "(icon": "([1;35micon",
    "(owner": "([1;35mowner",
    "(randomonline": "([1;35mrandomonline",
    "(randomoffline": "([1;35mrandomoffline",
    "(members": "([1;35mmembers",
    "(bots": "([1;35mbots",
    "(humans": "([1;35mhumans",
    "(roles": "([1;35mroles",
    "(channels": "([1;35mchannels",
    "(topic": "([1;35mtopic",
    "(slowmode": "([1;35mslowmode",
    "(mention": "([1;35mmention",
    ":trunc": ":[1;35mtrunc",
    ":round": ":[1;35mround",
    ":abs": ":[1;35mabs",
    "(title": "([1;35mtitle",
    "(URL": "([1;35mURL",
    "(description": "([1;35mdescription",
    "(timestamp": "([1;35mtimestamp",
}

meta_dict = {
    "{delete": "{[1;33mdelete",
    "{del": "{[1;33mdel",
    "{silence": "{[1;33msilence",
    "{dm": "{[1;33mdm",
    "{override": "{[1;33moverride",
    "{blacklist": "{[1;33mblacklist",
    "{require": "{[1;33mrequire",
    "{redirect": "{[1;33mredirect",
    "{react": "{[1;33mreact",
    "{reactu": "{[1;33mreactu",
    ":delete": ":[1;33mdelete",
    ":del": ":[1;33mdel",
    ":silence": ":[1;33msilence",
    ":dm": ":[1;33mdm",
    ":override": ":[1;33moverride",
    ":blacklist": ":[1;33mblacklist",
    ":require": ":[1;33mrequire",
    ":redirect": ":[1;33mredirect",
    ":react": ":[1;33mreact",
    ":reactu": ":[1;33mreactu",
    "|delete": "|[1;33mdelete",
    "|del": "|[1;33mdel",
    "|silence": "|[1;33msilence",
    "|dm": "|[1;33mdm",
    "|override": "|[1;33moverride",
    "|blacklist": "|[1;33mblacklist",
    "|require": "|[1;33mrequire",
    "|redirect": "|[1;33mredirect",
    "|react": "|[1;33mreact",
    "|reactu": "|[1;33mreactu",
}

payload_dict = {
    "true": "[1;36mtrue",
    "false": "[1;36mfalse",
    "now": "[1;36mnow",
}

final_operators_dict = {
    "☺equal☺": "[1;35m==",
    "☺notequal☺": "[1;35m!=",
    "☺greaterequal☺": "[1;35m>=",
    "☺lesserequal☺": "[1;35m<=",
}

syntax_dict = {
    "{": "[1;31m{",
    "}": "[1;31m}",
    "(": "[1;34m(",
    ")": "[1;34m)",
    ":": "[1;34m:",
}


strf_flags = {
    # Might add later
    """%a %A %w %d %-d %b %B %m %-m %y %Y %H %-H %I %-I %p %M %-M %S %-S %f %z %Z %j %-j %U %W %c %x %X %u %n %i %s %m %-m %s %-s %z %w"""
}


class ANSIColorParser(object):
    """
    Traverse a document, look for ansi_literal_block nodes, parse these
    nodes, and replace them with literal blocks, containing proper child
    nodes for ANSI color sequences.
    """

    def _finalize_pending_nodes(self):
        """
        Finalize all pending nodes.

        Pending nodes will be append to the new nodes.
        """
        self.new_nodes.extend(self.pending_nodes)
        self.pending_nodes = []

    def _add_text(self, text):
        """
        If ``text`` is not empty, append a new Text node to the most recent
        pending node, if there is any, or to the new nodes, if there are no
        pending nodes.
        """
        if text:
            if self.pending_nodes:
                self.pending_nodes[-1].append(nodes.Text(text))
            else:
                self.new_nodes.append(nodes.Text(text))

    def _ansify_tagscript(self, text: str):
        """
        Ansify our tagscript before passing it to _colorize_block_contents
        """
        for key, value in operators_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        for key, value in blocks_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        for key, value in params_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        for key, value in meta_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        for key, value in payload_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        for key, value in final_operators_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")
        
        for key, value in syntax_dict.items():
            text = text.replace(key, f"{value}[1;37m")
        text = text.replace("[1;37m[", "[")

        return text

    def _colorize_block_contents(self, block):
        raw = block.rawsource
        raw = self._ansify_tagscript(raw)
        # create the "super" node, which contains to while block and all it
        # sub nodes, and replace the old block with it
        literal_node = nodes.literal_block()
        literal_node['classes'].append('tagscript')
        block.replace_self(literal_node)

        # this contains "pending" nodes.  A node representing an ANSI
        # color is "pending", if it has not yet seen a reset
        self.pending_nodes = []
        # these are the nodes, that will finally be added to the
        # literal_node
        self.new_nodes = []
        # this holds the end of the last regex match
        last_end = 0
        # iterate over all color codes
        for match in COLOR_PATTERN.finditer(raw):
            # add any text preceeding this match
            head = raw[last_end:match.start()]
            self._add_text(head)
            # update the match end
            last_end = match.end()
            # get the single format codes
            codes = [int(c) for c in match.group(1).split(';')]
            if codes[-1] == 0:
                # the last code is a reset, so finalize all pending
                # nodes.
                self._finalize_pending_nodes()
            else:
                # create a new color node
                code_node = nodes.inline()
                self.pending_nodes.append(code_node)
                # and set the classes for its colors
                for code in codes:
                    code_node['classes'].append(
                        'ansi-%s' % CODE_CLASS_MAP[code])
        # add any trailing text
        tail = raw[last_end:]
        self._add_text(tail)
        # move all pending nodes to new_nodes
        self._finalize_pending_nodes()
        # and add the new nodes to the block
        literal_node.extend(self.new_nodes)

    def _strip_color_from_block_content(self, block):
        content = COLOR_PATTERN.sub('', block.rawsource)
        literal_node = nodes.literal_block(content, content)
        block.replace_self(literal_node)

    def __call__(self, app, doctree, docname):
        """
        Extract and parse all ansi escapes in ansi_literal_block nodes.
        """
        handler = self._colorize_block_contents
        if app.builder.name != 'html':
            # strip all color codes in non-html output
            handler = self._strip_color_from_block_content
        for ansi_block in doctree.traverse(ansi_literal_block):
            handler(ansi_block)


def add_stylesheet(app):
    if app.config.html_ansi_stylesheet:
        try:
            app.add_stylesheet('ansi.css')
        except:
            pass

def copy_stylesheet(app, exception):
    if app.builder.name != 'html' or exception:
        return
    stylesheet = app.config.html_ansi_stylesheet
    if stylesheet:
        app.info(bold('Copying ansi stylesheet... '), nonl=True)
        dest = path.join(app.builder.outdir, '_static', 'ansi.css')
        source = path.abspath(path.dirname(__file__))
        copyfile(path.join(source, stylesheet), dest)
        app.info('done')


class TAGSCRIPTBlockDirective(rst.Directive):
    """
    This directive interprets its content as literal block with ANSI color
    codes.

    The content is decoded using ``string-escape`` to allow symbolic names
    as \x1b being used instead of the real escape character.
    """

    has_content = True

    option_spec = dict(string_escape=flag)

    def run(self):
        text = '\n'.join(self.content)
        if 'string_escape' in self.options:
            text = text.decode('string-escape')
        return [ansi_literal_block(text, text)]


def setup(app):
    app.require_sphinx('1.0')
    try:
        app.add_config_value('html_ansi_stylesheet', None, 'env')
    except:
        pass
    app.add_directive('tagscript', TAGSCRIPTBlockDirective)
    app.connect('builder-inited', add_stylesheet)
    app.connect('build-finished', copy_stylesheet)
    app.connect('doctree-resolved', ANSIColorParser())
