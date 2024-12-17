.. _reference_tool_optchar_usage:

Using egg-optchar
====================

**egg-optchar** performs basic optimizations of a character model and its
associated animations, primarily by analyzing the animation tables and
removing unneeded joints and/or morphs.  It can also perform basic
restructuring operations on the character hierarchy.


Program Arguments
---------------------

.. code-block:: console

  -noabs

Don't allow any of the named egg files to have absolute
pathnames.  If any do, abort with an error.  This option
is designed to help detect errors when populating or
building a standalone model tree, which should be
self-contained and include only relative pathnames.

.. code-block:: console

  -ls          
  
List the joint hierarchy instead of performing any operations.

.. code-block:: console

  -lsv         

List the joint hierarchy along with an indication of the properties each joint.

.. code-block:: console

  -lsp

List the existing joint hierarchy as a series of ``-p``
joint,parent commands, suitable for pasting into an
egg-optchar command line.

.. code-block:: console

  -keep joint[,joint...]

Keep the named joints (or sliders) in the character, even
if they do not appear to be needed by the animation.

.. code-block:: console

  -drop joint[,joint...]

Removes the named joints or sliders, even if they appear to be needed.

.. code-block:: console
  
  -expose joint[,joint...]

Expose the named joints by flagging them with a DCS
attribute, so each one can be found in the scene graph
when the character is loaded, and objects can be parented
to it.  This implies ``-keep``.

.. code-block:: console

  -suppress joint[,joint...]

The opposite of suppress, this prevents the named joints
from being created with an implicit DCS attribute, even
if they contain rigid geometry.  The default is to create
an implicit node for any joint that contains rigid
geometry, to take advantage of display list and/or vertex
buffer caching.  This does *not* imply ``-keep``.

.. code-block:: console

  -flag node[,node...][=name]

Assign the indicated name to the geometry within the
given nodes.  This will make the geometry visible as a
node in the resulting character model when it is loaded
in the scene graph (normally, the node hierarchy is
suppressed when loading characters).  This is different
from -expose in that it reveals geometry rather than
joints; the revealed node can be hidden or its attributes
changed at runtime, but it will be animated by its
vertices, not the node, so objects parented to this node
will not inherit its animation.

.. code-block:: console

  -defpose anim.egg,frame

Specify the model's default pose.  The pose is taken from
the indicated frame of the named animation file (which
must also be named separately on the command line).  The
pose will be held by the model in the absence of any
animation, and need not be the same pose in which the
model was originally skinned.

.. code-block:: console

  -preload     

Add an `<AnimPreload> <../../syntax/general.html#AnimPreload>`_ entry for each animation to the
model file(s).  This can be used at runtime to support
asynchronous loading and binding of animation channels.



.. code-block:: console

  -zero joint[,hprxyzijkabc]

Zeroes out the animation channels for the named joint.
If a subset of the component letters ``hprxyzijkabc`` is
included, the operation is restricted to just those
components; otherwise the entire transform is cleared.

.. code-block:: console
  
  -keepall     

Keep all joints and sliders in the character, except
those named explicitly by ``-drop``.

.. code-block:: console

  -p joint,parent

Moves the named joint under the named parent joint.  Use
``-p joint,`` to reparent a joint to the root.  The joint
transform is recomputed appropriately under its new
parent so that the animation is not affected (the effect
is similar to ``NodePath::wrt_reparent_to``).

.. code-block:: console

  -new joint,source

Creates a new joint under the named parent joint.  The
new joint will inherit the same net transform as its
parent.

.. code-block:: console

  -rename joint,newjoint

Renames the indicated joint, if present, to the given
name.

.. code-block:: console

  -q quantum   

Quantize joint membership values to the given unit.  This
is the smallest significant change in joint membership.
There can be a significant performance (and memory
utilization) runtime benefit for eliminating small
differences in joint memberships between neighboring
vertices.  The default is 0.01; specifying 0 means to
preserve the original values.

.. code-block:: console

  -qa quantum[,hprxyzijkabc]

Quantizes animation channels to the given unit.  This
rounds each of the named components of all joints to the
nearest multiple of unit.  There is no performance
benefit, and little compression benefit, for doing this;
and this may introduce visible artifacts to the
animation.  However, sometimes it is a useful tool for
animation analysis and comparison.  This option may be
repeated several times to quantize different channels by
a different amount.

.. code-block:: console

  -dart [default, sync, nosync, or structured]

change the dart value in the given eggs

.. code-block:: console

  -fixrest     
  
Specify this to force all the initial rest frames of the
various model files to the same value as the first model
specified.  This is a fairly drastic way to repair models
whose initial rest frame values are completely bogus, but
should not be performed when the input models are
correct.

.. code-block:: console

  -pr path_replace

Sometimes references to other files (textures, external
references) are stored with a full path that is
appropriate for some other system, but does not exist
here.  This option may be used to specify how those
invalid paths map to correct paths.  Generally, this is
of the form ``'orig_prefix=replacement_prefix'``, which
indicates a particular initial sequence of characters
that should be replaced with a new sequence; e.g.
``'/c/home/models=/beta/fish'``.  If the replacement prefix
does not begin with a slash, the file will then be
searched for along the search path specified by ``-pp``.  You
may use standard filename matching characters (``'*'``, ``'?'``,
etc.) in the original prefix, and ``'**'`` as a component by
itself stands for any number of components.

This option may be repeated as necessary; each file will
be tried against each specified method, in the order in
which they appear in the command line, until the file is
found.  If the file is not found, the last matching
prefix is used anyway.

.. code-block:: console

  -pp dirname  

Adds the indicated directory name to the list of
directories to search for filenames referenced by the
source file.  This is used only for relative paths, or
for paths that are made relative by a ``-pr`` replacement
string that doesn't begin with a leading slash.  The
model-path is always implicitly searched anyway.

.. code-block:: console

  -ps path_store

Specifies the way an externally referenced file is to be
represented in the resulting output file.  This assumes
the named filename actually exists; see ``-pr`` to indicate
how to deal with external references that have bad
pathnames.  This option will not help you to find a
missing file, but simply controls how filenames are
represented in the output.

The option may be one of: ``rel``, ``abs``, ``rel_abs``, ``strip``, or
``keep``.  If either ``rel`` or ``rel_abs`` is specified, the files
are made relative to the directory specified by ``-pd``.  The
default is ``rel``.

.. code-block:: console

  -pd path_directory

Specifies the name of a directory to make paths relative
to, if ``-ps rel`` or ``-ps rel_abs`` is specified.  If this
is omitted, the directory name is taken from the name of
the output file.

.. code-block:: console

  -pc target_directory

Copies textures and other dependent files into the
indicated directory.  If a relative pathname is
specified, it is relative to the directory specified with
``-pd``, above.

.. code-block:: console

  -no

Strip all normals.

.. code-block:: console

  -np          

Strip existing normals and redefine polygon normals.

.. code-block:: console

  -nv threshold

Strip existing normals and redefine vertex normals.
Consider an edge between adjacent polygons to be smooth
if the angle between them is less than threshold degrees.

.. code-block:: console

  -nn
          
Preserve normals exactly as they are.  This is the
default.

.. code-block:: console

  -tbn name    

Compute tangent and binormal for the named texture
coordinate set(s).  The name may include wildcard
characters such as ``*`` and ``?``.  The normal must already
exist or have been computed via one of the above options.
The tangent and binormal are used to implement bump
mapping and related texture-based lighting effects.  This
option may be repeated as necessary to name multiple
texture coordinate sets.

.. code-block:: console

  -tbnall      

Compute tangent and binormal for all texture coordinate
sets.  This is equivalent to ``-tbn "*"``.

.. code-block:: console

  -tbnauto

Compute tangent and binormal for all normal maps.

.. code-block:: console

  -TS sx[,sy,sz]

Scale the model uniformly by the given factor (if only
one number is given) or in each axis by ``sx``, ``sy``, ``sz`` (if
three numbers are given).

.. code-block:: console

  -TR x,y,z

Rotate the model ``x`` degrees about the x axis, then ``y``
degrees about the y axis, and then z degrees about the ``z``
axis.

.. code-block:: console

  -TA angle,x,y,z

Rotate the model angle degrees counterclockwise about the
given axis.

.. code-block:: console

  -TT x,y,z

Translate the model by the indicated amount.

All transformation options (``-TS``, ``-TR``, ``-TA``, ``-TT``) are
cumulative and are applied in the order they are
encountered on the command line.

.. code-block:: console

  -o filename 

Specify the filename to which the resulting egg file will
be written.  This is only valid when there is only one
input egg file on the command line.  If you want to
process multiple files simultaneously, you must use
either ``-d`` or ``-inplace``.

.. code-block:: console
  
  -d dirname  

Specify the name of the directory in which to write the
resulting egg files.  If you are processing only one egg
file, this may be omitted in lieu of the ``-o`` option.  If
you are processing multiple egg files, this may be
omitted only if you specify ``-inplace`` instead.

.. code-block:: console

  -inplace    

If this option is given, the input egg files will be
rewritten in place with the results.  This obviates the
need to specify ``-d`` for an output directory; however, it's
risky because the original input egg files are lost.

.. code-block:: console

  -cs coordinate-system

Specify the coordinate system to operate in.  This may be
one of ``y-up``, ``z-up``, ``y-up-left``, or ``z-up-left``.

.. code-block:: console

  -f          

Force complete loading: load up the egg file along with
all of its external references.

.. code-block:: console

  -inf filename

Reads input args from a text file instead of the command
line.  Useful for really, really large lists of args that
break the OS-imposed limits on the length of command
lines.