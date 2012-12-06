# vim: fileencoding=utf8 tw=120 expandtab ts=4 sw=4 :

# Ponytile
# Takes some picture files as input, generate a tile set of them and create a CSS stylesheet that enables you to use
# this in your webpage. Basically, it's creating a so-called CSS sprite.
#
# Copyright (c) 2012 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Under the terms of the WTFPL

import imp

def parse_config(filename):
    try:
        config = imp.load_source('ponytile-config', filename)
        ret = {}

        if not hasattr(config, "CSS_PREFIX"):
            return (None, "CSS_PREFIX is required in the configuration. It is a string that will be prepended to the"
                          + " file name to form the CSS selector.")

        if not hasattr(config, "FILES_LIST"):
            return (None, "FILES_LIST is required in the configuration. It should be a tuple of strings that describe"
                          + " the file names to be included, relatively to the configuration file. The glob syntax is"
                          + " allowed.")

        if not isinstance(config.CSS_PREFIX, basestring):
            return (None, "CSS_PREFIX should be a string.")

        if not isinstance(config.FILES_LIST, tuple):
            return (None, "FILES_LIST should be a tuple.")

        for x in config.FILES_LIST:
            if not isinstance(x, basestring):
                return (None, "FILES_LIST should be a tuple of file paths in the form of strings (the glob syntax is"
                              + " allowed).")

        ret["css_prefix"] = config.CSS_PREFIX
        ret["files_list"] = config.FILES_LIST

        return ret, None
    except:
        return None, "Wrong configuration syntax."

if __name__ == "__main__":
    cfg, err = parse_config("config.ptl")
    print err
    print cfg
