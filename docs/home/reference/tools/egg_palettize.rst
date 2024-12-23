.. _reference_tool_pal_usage:

Using egg-palettize
=====================

**egg-palettize** is used when building models to optimize texture usage on all models before loading them into the show. 
It is capable of collecting together several different small texture images
from different models and assembling them together onto the same image
file, potentially reducing the total number of different texture
images that must be loaded and displayed at runtime from several
thousand to several hundred or fewer.

It also can be used to group together related textures that will be
rendered at the same time (for instance, textures related to one
area), and if nothing else, it can resize textures at build
time so that they may be painted at any arbitrary resolution according
to the artist's convenience, and then reduced to a suitable size for
texture memory management (and to meet hardware requirements of having
dimensions that are always a power of two).

It is suggested that textures always be painted at high resolution and
reduced using egg-palettize, since this allows the show designer the
greatest flexibility; if a decision is later made to increase the
resolution of a texture, this may be done by changing an option with
egg-palettize, and does not require the intervention of the artist.


The behavior of egg-palettize is largely controlled through a source
file called ``textures.txa``, which is usually found in the ``src/maps``
directory within the model tree.  For a complete description of the
syntax of the ``textures.txa`` file, invoke the command ``egg-palettize -H``.


Grouping Egg Files
---------------------

Much of the contents of ``textures.txa`` involves assigning egg files to
various groups; assigning two egg files to the same group indicates
that they are associated in some way, and their texture images may be
copied together into the same palettes.

The groups are arbitrary and should be defined at the beginning of the
egg file with the syntax:

.. code-block:: console

  :group groupname

Where ``groupname`` is the name of the group.  It is also possible to
assign a directory name to a group.  This is optional, but if done, it
indicates that all of the textures for this group should be installed
within the named subdirectory.  The syntax is:

.. code-block:: console

  :group groupname dir dirname

Where ``dirname`` is the name of the subdirectory.  If you are
generating a phased download, the dirname should be one of phase_1,
phase_2, etc., corresponding to the ``PHASE`` variable in the ``install_egg``
rule (see `ppremake documentation <https://github.com/toontownretro/ppremake/wiki/Documentation>`_ for more information).


Finally, it is possible to relate the different groups to each other
hierarchically.  Doing this allows egg-palettize to assign textures to
the minimal common subset between egg files that share the textures.
For instance, if group beta and group gamma both depend on group
alpha, a texture that is assigned to both groups beta and gamma can
actually be placed on group alpha, to maximize sharing and minimize
duplication of palette space.

You relate two groups with the syntax:

.. code-block:: console

  :group groupname with basegroupname


Once all the groups are defined, you can assign egg files to the
various groups with a syntax like this:

.. code-block:: console

  model.egg : groupname

where ``model.egg`` is the name of some egg model file built within the
tree.  You can explicitly group each egg file in this way, or you can
use wildcards to group several at once, e.g.:

.. code-block:: console
    
  dog*.egg : dogs

Assigning an egg file to a group assigns all of the textures used by
that egg file to that same group.  If no other egg files reference the
same textures, those textures will be placed in one or more palette
images named after the group.  If another egg file within a different
group also references the textures, they will be assigned to the
lowest group that both groups have in common (see relating the groups
hierarchically, above), or copied into both palette images if the two
groups having nothing in common.


Controlling Texture Parameters
------------------------------------

Most of the contents of the ``textures.txa`` is usually devoted to scaling
the texture images appropriately.  This is usually done with a line
something like this:

.. code-block:: console

  texture.rgb : 64 64

where ``texture.rgb`` is the name of some texture image, and 64 64 is the
size in pixels it should be scaled to.  It is also possible to specify
the target size as a factor of the source size, e.g.:

.. code-block:: console

  bigtexture.rgb : 50%

specifies that the indicated texture should be scaled to 50% in each
dimension (for a total reduction to 0.5 * 0.5 = 25% of the original
area).

As above, you may group multiple textures on the same line
using wildcards, e.g.:

.. code-block:: console

  wall*.rgb : 25%

Finally, you may include one or more optional keywords on the end of
the texture scaling line that indicate additional properties to apply
to the named textures.  See ``egg-palettize -H`` for a complete list.
Some of the more common keywords are:

  mipmap - Enables mipmaps for the texture.

  linear - Disables mipmaps for the texture.

  omit - Omits the texture from any palettes.
    The texture will still be scaled and installed, but it will not be combined with other
    textures.  Normally you need to do this only when the texture will
    be applied to some geometry at runtime.  (Since palettizing a
    texture requires adjusting the UV's of all the geometry that
    references it, a texture that is applied to geometry at runtime
    cannot be palettized.)
    

Running egg-palettize
------------------------

Using Makefiles
^^^^^^^^^^^^^^^^^^^

Normally, egg-palettize is run automatically just by typing:

.. code-block:: console

  make install

in the model tree.  It automatically reads the textures.txa file and
generates and installs the appropriate palette image files, as part of
the whole build process, and requires no further intervention from the
user.  See the `ppremake documentation <https://github.com/toontownretro/ppremake/wiki/Documentation>`_ for more information on setting up the
model tree.

When egg-palettize runs in the normal mode, it generates suboptimal
palettes.  Sometimes, for instance, a palette image is created with
only one small texture in the corner, and the rest of it unused.  This
happens because egg-palettize is reserving space for future textures,
and is ideal for development; but it is not suitable for shipping a
finished product.  When you are ready to repack all of the palettes as
optimally as possible, run the command:

.. code-block:: console

  make opt-pal

This causes egg-palettize to reorganize all of the palette images to
make the best usage of texture memory.  It will force a regeneration
of most of the egg files in the model tree, so it can be a fairly
involved operation.

It is sometimes useful to analyze the results of egg-palettize.  You
can type:

.. code-block:: console

  make pi >pi.txt

to write a detailed report of every egg file, texture image, and
generated palette image to the file pi.txt.

Finally, the command:

.. code-block:: console

  make pal-stats >stats.txt

will write a report to stats.txt of the estimated texture memory usage
for all textures, broken down by group.


When Things Go Wrong
-------------------------

The whole palettizing process is fairly complex; it's necessary for
egg-palettize to keep a record of the complete state of all egg files
and all textures ever built in a particular model tree.  It generally
does a good job of figuring out when things change and correctly
regenerating the necessary egg files and textures when needed, but
sometimes it gets confused.

This is particularly likely to happen when you have reassigned some
egg files from one group to another, or redefined the relationship
between different groups.  Sometimes egg-palettize appears to run
correctly, but does not generate correct palettes. 


Assertion Errors and Segfaults
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While rare, is possible for the tool with an assertion failure, or even a segment
fault (general protection fault) when running egg-palettize, due to
this kind of confusion.  This behavior should not happen, but it does
happen every once and a while.


Makefile-based Solution
``````````````````````````

When this sort of thing happens, often the best thing to do is to
invoke the command:

.. code-block:: console

  make undo-pal

followed by:

.. code-block:: console

  make install

This removes all of the old palettization information, including the
state information cached from previous runs, and rebuilds a new set of
palettes from scratch.  It is a fairly heavy hammer, and may take some
time to complete, depending on the size of your model tree, but it
almost always clears up any problems related to egg-palettize.
