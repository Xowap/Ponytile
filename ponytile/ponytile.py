# vim: fileencoding=utf8 tw=120 expandtab ts=4 sw=4 :

# Ponytile
# Takes some picture files as input, generate a tile set of them and create a CSS stylesheet that enables you to use
# this in your webpage. Basically, it's creating a so-called CSS sprite.
#
# Copyright (c) 2012 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Under the terms of the WTFPL

from __future__ import division

import ConfigParser
import Image
import floory
from os.path import dirname, abspath, normpath, relpath, join, exists, basename, splitext
from glob import glob
from math import ceil

# TODO modified file date
# TODO Python 3.x compat -> what about PIL ?

class Ponyitem(floory.Item):
    def __init__(self, filename, block_w, block_h):
        self.filename = filename
        self.pil = Image.open(filename)

        self.block_w, self.block_h = block_w, block_h
        self.img_w, self.img_h = self.pil.size

        w = ceil(self.img_w / self.block_w)
        h = ceil(self.img_h / self.block_h)

        super(Ponyitem, self).__init__(self.filename, w, h)

    def left(self):
        return int(self.x * self.block_w)

    def upper(self):
        return int(self.y * self.block_h)

    def right(self):
        return int(self.x * self.block_w + self.img_w)

    def lower(self):
        return int(self.y * self.block_h + self.img_h)

    def width(self):
        return self.img_w

    def height(self):
        return self.img_h


class Ponytile(object):
    _default_conf = join(dirname(__file__), "default_config.ptl")

    def __init__(self, filename):
        self.cfg = None
        self.filename = filename
        self.cwd = abspath(dirname(self.filename))

    def load_cfg(self):
        self.cfg, error = self._parse_config(self.filename)

        return error

    def compile(self, destfile):
        """
        Will compile the source file into the specified destfile, and will also generate the according sprite file as
        specified in the source file.
        """

        self.target_cwd = dirname(abspath(destfile))
        self.spritefile = normpath(join(self.target_cwd, self.cfg.get('sprite', 'filename')))

        try:
            # TODO overwrite warning
            outfh = open(destfile, "w")
        except IOError:
            return "Unable to open the destination file"

        input_img = self._expand_file_list([k for k, v in self.cfg.items('files')])
        block_w = self.cfg.getint('tile', 'width')
        block_h = self.cfg.getint('tile', 'height')

        items = [Ponyitem(x, block_w, block_h) for x in input_img]
        grid = floory.plan(items, self.cfg.getint('sprite', 'width'))

        self._make_image(items, grid)
        out = self._make_css(items)

        outfh.write(out)
        outfh.close()

        return None

    def _make_image(self, items, grid):
        img_w = grid.w * self.cfg.getint('tile', 'width')
        img_h = grid.h * self.cfg.getint('tile', 'height')

        img = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))

        for item in items:
            box = (
                item.left(),
                item.upper(),
                item.right(),
                item.lower(),
            )

            img.paste(item.pil, box)

        img.save(self.spritefile, self.cfg.get('sprite', 'format'))

    def _make_css(self, items):
        tpl_string = """%s%s {
    background: url(%s) -%dpx -%dpx;
    width: %dpx;
    height: %dpx;
}
"""
        ret = "%s {\n    display: inline-block;\n}\n" % self.cfg.get('css', 'general_selector')

        for item in items:
            ret += tpl_string % (
                self.cfg.get('css', 'prefix'),
                splitext(basename(item.name))[0],
                relpath(self.spritefile, self.target_cwd),
                item.left(),
                item.upper(),
                item.width(),
                item.height(),
            )

        return ret

    def _expand_file_list(self, file_list):
        ret = []

        for exp in file_list:
            ret += glob(join(self.cwd, exp))

        return ret

    def _parse_config(self, filename):
        # TODO better config checking
        if not exists(filename):
            return None, "Missing file: %s" % filename

        cfg = ConfigParser.ConfigParser(allow_no_value=True)
        cfg.read([self._default_conf, filename])

        return cfg, None

if __name__ == "__main__":
    ptl = Ponytile("config.ptl")
    cfg, err = ptl.load_cfg()
    ptl.compile()
