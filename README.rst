========
Ponytile
========

A Python library/utility to create CSS sprites.

This library was made out of my frustration to be unable to find a library that
suited exactly what I had in mind. And also because I found the idea of writing
that quite fun :)

Now a first version is done, I don't know if I'm going to push the development
further. Don't use this in production, unless you are ready to dig into the
code and maintain the app yourself.

Usage
=====

PTL source file
---------------

Everything is generated from the PTL source file. It has a few options::

	[css]
	# The prefix that will be put in front of every generated CSS selector.
	# The selectors are generated from the file names. With the current
	# configuration, what you'd get for a toto.png file would be a
	# .icon-toto class.
	prefix = .icon-

	# This is a selector of the global class for all generated tiles (it
	# sets some styles attributes for everybody)
	general_selector = [class^="icon-"], [class*=" icon-"]

	[sprite]
	# A hint of the number of tiles that fits in the width of the sprite.
	width = 15

	# The relative path from the generated CSS file to the generated sprite
	# file. This sprite file will be generated at compilation time.
	filename = sprite.png

	# A valid PIL format name
	format = PNG

	[tile]
	# This is a hint about the tiles size. Put here your most common tile
	# size, or the LCM of your tiles sizes, or something in that mood.
	width = 16
	height = 16

	[files]
	# Here goes a plain glob list of files to be put in the sprite. The
	# path is relative to the .ptl file.
	sprite/*.png

CLI Tool
--------

Once you have the PTL source, compiling is quite simple::

	ponytile input.ptl output.css

It will generate the output.css file with the appropriate sprite file as
configured by the PTL file.

Using in your web page
----------------------

Just include the generated CSS somewhere, and then do::

	<i class="icon-toto"></i>

It should make the trick :)

Using the library
-----------------

Open `bin/ponytile` and look at how things are done. There is not much more to
say about the public API right now!

Copyright
=========

This whole thing is licenced under the WTFPL (see the attached LICENSE.txt
file).
