.. _syntax_general:

General Egg Syntax
====================

Egg files consist of a series of sequential and hierarchically-nested entries. 

In general, the syntax of each entry is:

.. code-block:: console
    
    <Entry-type> name { contents }

Where the name is optional (and in many cases, ignored anyway) and the syntax of the contents is determined by the entry-type.

The name (and strings in general) may be either quoted with double quotes or unquoted.

Newlines are treated like any other whitespace, and case is not significant. 

The angle brackets are literally a part of the entry keyword. 
(Square brackets and ellipses in this document are used to indicate optional pieces, and are not literally part of the syntax.)

The name field is always syntactically allowed between an entry keyword and its opening brace, even if it will be ignored. 


Comments
--------

Comments may be delimited using either the C++-style ``// ...`` or the C-style ``/* ... */``.  C comments do not nest. 

There is also a ``<Comment>`` entry type, of the form:

.. code-block:: console

    <Comment> { text }

``<Comment>`` entries are slightly different, in that tools which read and write egg files will preserve the text within ``<Comment>`` entries, but they may not preserve comments delimited by ``//`` or ``/* */``. 

Special characters and keywords within a ``<Comment>`` entry should be quoted; it's safest to quote the entire comment.


Local Information Entries
-------------------------------

These nodes contain information relevant to the current level of nesting only.

.. code-block:: console

    <Scalar> name { value }
    <Char*> name { value }

Because of a syntactic accident with the way the egg
syntax evolved, ``<Scalar>`` and ``<Char*>`` are lexically the same and both
can represent either a string or a number.  ``<Char*>`` is being phased
out; it is suggested that new egg files use only ``<Scalar>``.

Global Information Entries
-------------------------------

These nodes contain information relevant to the file as a whole.  They
can be nested along with geometry nodes, but this nesting is
irrelevant and the only significant placement rule is that they should
appear before they are referenced.

Textures
-----------

.. code-block:: console
    
    <Texture> name { filename [scalars] }

This describes a texture file that can be referenced later with ``<TRef> { name }``.

It is not necessary to make a ``<Texture>`` entry for each texture to be used; a texture may also be referenced directly
by the geometry via an abbreviated inline ``<Texture>`` entry, but a separate ``<Texture>`` entry is the only way 
to specify anything other than the default texture attributes.

If the filename is a relative path, the current egg file's directory is searched first, and then the texture-path and model-path are searched.

The following attributes are presently implemented for textures:
    `<Scalar> alpha-file { alpha-filename }`_
    
    `<Scalar> alpha-file-channel { channel }`_
    
    `<Scalar> format { format-definition }`_
    
    `<Scalar> compression { compression-mode }`_
    
    `<Scalar> wrap { repeat-definition }`_

    `<Scalar> wrapu { repeat-definition }`_

    `<Scalar> wrapv { repeat-definition }`_

    `<Scalar> wrapw { repeat-definition }`_

    <Scalar> borderr { red-value }

    <Scalar> borderg { green-value }

    <Scalar> borderb { blue-value }

    <Scalar> bordera { alpha-value }

    <Scalar> type { texture-type }

    <Scalar> multiview { flag }

    <Scalar> num-views { count }

    <Scalar> read-mipmaps { flag }

    `<Scalar> minfilter { filter-type }`_

    `<Scalar> magfilter { filter-type }`_

    `<Scalar> magfilteralpha { filter-type }`_

    `<Scalar> magfiltercolor { filter-type }`_

    `<Scalar> anisotropic-degree { degree }`_

    `<Scalar> envtype { environment-type }`_


.. _<Scalar> alpha-file { alpha-filename }: scalar_syn.html#image-alpha-file
.. _<Scalar> alpha-file-channel { channel }: scalar_syn.html#image-alpha-file-channel
.. _<Scalar> format { format-definition }: scalar_syn.html#image-format
.. _<Scalar> compression { compression-mode }: scalar_syn.html#image-compression
.. _<Scalar> wrap { repeat-definition }: scalar_syn.html#uv-wrap-mode
.. _<Scalar> wrapu { repeat-definition }: scalar_syn.html#uv-wrap-mode
.. _<Scalar> wrapv { repeat-definition }: scalar_syn.html#uv-wrap-mode
.. _<Scalar> wrapw { repeat-definition }: scalar_syn.html#uv-wrap-mode
.. _<Scalar> minfilter { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfilter { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfilteralpha { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfiltercolor { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> anisotropic-degree { degree }: scalar_syn.html#image-anisotropic-degree
.. _<Scalar> envtype { environment-type }: scalar_syn.html#environment-type


Geometry 
---------

Polygons
^^^^^^^^^

.. code-block:: console

    <Polygon> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
    }

A polygon consists of a sequence of vertices from a single vertex
pool.  Vertices are identified by pool-name and index number within
the pool; indices is a list of vertex numbers within the given
vertex pool.  Vertices are listed in counterclockwise order.
Although the vertices must all come from the same vertex pool, they
may have been assigned to arbitrarily many different joints
regardless of joint connectivity (there is no "straddle-polygon"
limitation).  See Joints, below.

The polygon syntax is quite verbose, and there isn't any way to
specify a set of attributes that applies to a group of polygons--the
attributes list must be repeated for each polygon.  This is why egg
files tend to be very large.


Patches
^^^^^^^^^

.. code-block:: console

    <Patch> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
    }

A patch is similar to a polygon, but it is a special primitive that
can only be rendered with the use of a tessellation shader.  Each
patch consists of an arbitrary number of vertices; all patches with
the same number of vertices are collected together into the same
``GeomPatches`` object to be delivered to the shader in a single batch.
It is then up to the shader to create the correct set of triangles
from the patch data.

All of the attributes that are valid for Polygon, above, may also be
specified for Patch.


PointLight
^^^^^^^^^^^^

.. code-block:: console

    <PointLight> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
    }

A ``PointLight`` is a set of single points.  One point is drawn for each
vertex listed in the ``<VertexRef>``.  Normals, textures, and colors may
be specified for ``PointLights``, as well as draw-order, plus one
additional attribute valid only for ``PointLights`` and ``Lines``:

<Scalar> thick { number }
<Scalar> perspective { boolean-value }



Lines
^^^^^^^^^

.. code-block:: console

    <Line> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
        [component attributes]
    }

A Line is a connected set of line segments.  The listed N vertices
define a series of N-1 line segments, drawn between vertex 0 and
vertex 1, vertex 1 and vertex 2, etc.  The line is not implicitly
closed; if you wish to represent a loop, you must repeat vertex 0 at
the end.  As with a PointLight, normals, textures, colors,
draw-order, and the "thick" attribute are all valid (but not
"perspective").  Also, since a Line (with more than two vertices) is
made up of multiple line segments, it may contain a number of
``<Component>`` entries, to set a different color and/or normal for each
line segment, as in TriangleStrip, below.



Triangle Strips
^^^^^^^^^^^^^^^^^^

.. code-block:: console

    <TriangleStrip> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
        [component attributes]
    }

A triangle strip is only rarely encountered in an egg file; it is
normally generated automatically only during load time, when
connected triangles are automatically meshed for loading, and even
then it exists only momentarily.  Since a triangle strip is a
rendering optimization only and adds no useful scene information
over a loose collection of triangles, its usage is contrary to the
general egg philosophy of representing a scene in the abstract.
Nevertheless, the syntax exists, primarily to allow inspection of
the meshing results when needed.  You can also add custom
TriangleStrip entries to force a particular mesh arrangement.

A triangle strip is defined as a series of connected triangles.
After the first three vertices, which define the first triangle,
each new vertex defines one additional triangle, by alternating up
and down.

It is possible for the individual triangles of a triangle strip to
have a separate normal and/or color.  If so, a ``<Component>`` entry
should be given for each so-modified triangle:

.. code-block:: console

  <Component> index {
    <RGBA> { r g b a [morph-list] }
    <Normal> { x y z [morph-list] }
  }

Where index ranges from 0 to the number of components defined by the
triangle strip (less 1).  Note that the component attribute list
must always follow the vertex list.
  
Parametric Curves & Surfaces
-------------------------------

The following entries define parametric curves and surfaces.
Generally, Panda supports these only in the abstract; they're not
geometry in the true sense but do exist in the scene graph and may
have specific meaning to the application.  However, Panda can create
visible representations of these parametrics to aid visualization.

These entries might also have meaning to external tools outside of an
interactive Panda session, such as ``egg-qtess``, which can be used to
convert NURBS surfaces to polygons at different levels of resolution.

In general, dynamic attributes such as morphs and joint assignment are
legal for the control vertices of the following parametrics, but Panda
itself doesn't support them and will always create static curves and
surfaces.  External tools like ``egg-qtess``, however, may respect them.

NURBS Curve
^^^^^^^^^^^^^^

.. code-block:: console
    
    <NURBSCurve> {
        [attributes]

        <Order> { order }
        <Knots> { knot-list }
        <VertexRef> { indices <Ref> { pool-name } }
    }

A NURBS curve is a general parametric curve.  It is often used to
represent a motion path, e.g. for a camera or an object.

The order is equal to the degree of the polynomial basis plus 1.  It
must be an integer in the range ``[1,4]``.

The number of vertices must be equal to the number of knots minus the
order.

Each control vertex of a NURBS is defined in homogeneous space with
four coordinates ``x y z w`` (to convert to 3-space, divide x, y, and z
by w).  The last coordinate is always the homogeneous coordinate; if
only three coordinates are given, it specifies a curve in two
dimensions plus a homogeneous coordinate (x y w).

The following attributes may be defined:

<Scalar> type { curve-type }

<Scalar> subdiv { num-segments }

<RGBA> { r g b a [morph-list] }

This specifies the color of the overall curve.


NURBS control vertices may also be given color and/or morph
attributes, but ``<Normal>`` and ``<UV>`` entries do not apply to NURBS
vertices.

NURBS Surface
^^^^^^^^^^^^^^^^^^

.. code-block:: console
    
<NURBSSurface> name {
    [attributes]

    <Order> { u-order v-order }
    <U-knots> { u-knot-list }
    <V-knots> { v-knot-list }

    <VertexRef> {
        indices
        <Ref> { pool-name }
    }
}

A NURBS surface is an extension of a NURBS curve into two parametric
dimensions, u and v.  NURBS surfaces may be given the same set of
attributes assigned to polygons, except for normals: ``<TRef>``,
``<Texture>``, ``<MRef>``, ``<RGBA>``, and ``draw-order`` are all valid attributes
for NURBS.  NURBS vertices, similarly, may be colored or morphed,
but ``<Normal>`` and ``<UV>`` entries do not apply to NURBS vertices.  The
attributes may also include ``<NURBSCurve>`` and ``<Trim>`` entries; see
below.

To have Panda create a visualization of a NURBS surface, the
following two attributes should be defined as well:

<Scalar> U-subdiv { u-num-segments }

<Scalar> V-subdiv { v-num-segments }


The same sort of restrictions on order and knots applies to NURBS
surfaces as do to NURBS curves.  The order and knot description may
be different in each dimension.

The surface must have u-num * v-num vertices, where u-num is the
number of u-knots minus the u-order, and v-num is the number of
v-knots minus the v-order.  All vertices must come from the same
vertex pool.  The nth (zero-based) index number defines control
vertex (u, v) of the surface, where n = (v * u-num) + u.  Thus, it
is the u coordinate which changes faster.

As with the NURBS curve, each control vertex is defined in
homogeneous space with four coordinates ``x y z w``.


A NURBS may also contain curves on its surface.  These are one or
more nested ``<NURBSCurve>`` entries included with the attributes; these
curves are defined in the two-dimensional parametric space of the
surface.  Thus, these curve vertices should have only two dimensions
plus the homogeneous coordinate: u v w.  A curve-on-surface has no
intrinsic meaning to the surface, unless it is defined within a
``<Trim>`` entry, below.

Finally, a NURBS may be trimmed by one or more trim curves.  These
are special curves on the surface which exclude certain areas from
the NURBS surface definition.  The inside is specified using two
rules: an odd winding rule that states that the inside consists of
all regions for which an infinite ray from any point in the region
will intersect the trim curve an odd number of times, and a curve
orientation rule that states that the inside consists of the regions
to the left as the curve is traced.

Each trim curve contains one or more loops, and each loop contains
one or more NURBS curves.  The curves of a loop connect in a
head-to-tail fashion and must be explicitly closed.

The trim curve syntax is as follows:

.. code-block:: console
    
  <Trim> {
    <Loop> {
      <NURBSCurve> {
        <Order> { order }
	<Knots> { knot-list }

	<VertexRef> { indices <Ref> { pool-name } }
      }
      [ <NURBSCurve> { ... } ... ]
    }
    [ <Loop> { ... } ... ]
  }

Although the egg syntax supports trim curves, there are at present
no egg processing tools that respect them.  For instance, ``egg-qtess``
ignores trim curves and always tessellates the entire NURBS surface.


Morphs
---------

Morphs are linear interpolations of attribute values at run time,
according to values read from an animation table.  In general, vertex
positions, surface normals, texture coordinates, and colors may be
morphed.

A morph target is defined by giving a net morph offset for a series of
vertex or polygon attributes; this offset is the value that will be
added to the attribute when the morph target has the value 1.0.  At
run time, the morph target's value may be animated to any scalar value
(but generally between 0.0 and 1.0); the corresponding fraction of the
offset is added to the attribute each frame.

There is no explicit morph target definition; a morph target exists
solely as the set of all offsets that share the same target name.  The
target name may be any arbitrary string; like any name in an egg file,
it should be quoted if it contains special characters.

The following types of morph offsets may be defined, within their
corresponding attribute entries:

.. code-block:: console
    
    <Dxyz> target { x y z }

A position delta, valid within a ``<Vertex>`` entry or a ``<CV>`` entry.
The given offset vector, scaled by the morph target's value, is
added to the vertex or CV position each frame.

.. code-block:: console
    
    <DNormal> target { x y z }

A normal delta, similar to the position delta, valid within a
``<Normal>`` entry (for vertex or polygon normals).  The given offset
vector, scaled by the morph target's value, is added to the normal
vector each frame.  The resulting vector may not be automatically
normalized to unit length.

.. code-block:: console
    
    <DUV> target { u v [w] }

A texture-coordinate delta, valid within a ``<UV>`` entry (within a
``<Vertex>`` entry).  The offset vector should be 2-valued if the
enclosing UV is 2-valued, or 3-valued if the enclosing UV is
3-valued.  The given offset vector, scaled by the morph target's
value, is added to the vertex's texture coordinates each frame.


.. code-block:: console
    
    <DRGBA> target { r g b a }

A color delta, valid within an ``<RGBA>`` entry (for vertex or polygon
colors).  The given 4-valued offset vector, scaled by the morph
target's value, is added to the color value each frame.


Groups
---------

.. code-block:: console

    <Group> name { group-body }

A ``<Group>`` node is the primary means of providing structure to the
egg file.  Groups can contain vertex pools and polygons, as well as
other groups.  The egg loader translates ``<Group>`` nodes directly into
PandaNodes in the scene graph (although the egg loader reserves the
right to arbitrarily remove nodes that it deems unimportant--see the
<Model> flag, below to avoid this).  In addition, the following
entries can be given specifically within a ``<Group>`` node to specify
attributes of the group:

Group Binary Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

These attributes may be either on or off; they are off by default.
They are turned on by specifying a non-zero "boolean-value".

<DCS> { boolean-value }

DCS stands for Dynamic Coordinate System.  This indicates that
show code will expect to be able to read the transform set on this
node at run time, and may need to modify the transform further.
This is a special case of <Model>, below.

<DCS> { dcs-type }

This is another syntax for the ``<DCS>`` flag.  The dcs-type string
should be one of either ``local`` or ``net``, which specifies the kind
of preserve_transform flag that will be set on the corresponding
ModelNode.  If the string is ``local``, it indicates that the local
transform on this node (as well as the net transform) will not be
affected by any flattening operation and will be preserved through
the entire model loading process.  If the string is ``net``, then
only the net transform will be preserved; the local transform may
be adjusted in the event of a flatten operation.

<Model> { boolean-value }

This indicates that the show code might need a pointer to this
particular group.  This creates a ModelNode at the corresponding
level, which is guaranteed not to be removed by any flatten
operation.  However, its transform might still be changed, but see
also the ``<DCS>`` flag, above.


<Dart> { boolean-value }

This indicates that this group begins an animated character.  A
Character node, which is the fundamental animatable object of
Panda's high-level Actor class, will be created for this group.

This flag should always be present within the ``<Group>`` entry at the
top of any hierarchy of ``<Joint>``'s and/or geometry with morphed
vertices; joints and morphs appearing outside of a hierarchy
identified with a ``<Dart>`` flag are undefined.

<Dart> { structured }

This is an optional alternative for the ``<Dart>`` flag.
By default, Panda will collapse all of the geometry in a group (with the ``<Dart> { 1 }`` flag)
a single node. While this is optimal for conditions such as characters moving around
a scene, it may be suboptimal for larger or more complex characters.
This entry is typically generated by the ``egg-optchar`` program with the ``-dart structured`` flag.
``<Dart> { structured }`` implies ``<Dart> { 1 }``.

<Switch> { boolean-value }

This attribute indicates that the child nodes of this group
represent a series of animation frames that should be
consecutively displayed.  In the absence of an "``fps``" scalar for
the group (see below), the egg loader creates a ``SwitchNode``, and it
the responsibility of the show code to perform the switching.  If
an fps scalar is defined and is nonzero, the egg loader creates a
SequenceNode instead, which automatically cycles through its
children.


Group Scalars
^^^^^^^^^^^^^^^

  `<Scalar> fps { frame-rate }`_

  `<Scalar> bin { bin-name }`_

  `<Scalar> draw-order { number }`_

  `<Scalar> depth-offset { number }`_

  `<Scalar> depth-write { mode }`_

  `<Scalar> depth-test { mode }`_

  `<Scalar> visibility { hidden | normal }`_

  `<Scalar> decal { boolean-value }`_

  `<Scalar> decalbase { boolean-value }`_

  `<Scalar> collide-mask { value }`_

  `<Scalar> from-collide-mask { value }`_

  `<Scalar> into-collide-mask { value }`_

  `<Scalar> blend { mode }`_

  `<Scalar> blendop-a { mode }`_

  `<Scalar> blendop-b { mode }`_

  `<Scalar> blendr { red-value }`_

  `<Scalar> blendg { green-value }`_

  `<Scalar> blendb { blue-value }`_
  
  `<Scalar> blenda { alpha-value }`_

  `<Scalar> occluder { boolean-value }`_

.. _<Scalar> fps { frame-rate }: scalar_syn.html#fps
.. _<Scalar> bin { bin-name }: scalar_syn.html#bin-order
.. _<Scalar> draw-order { number }: scalar_syn.html#draw-order
.. _<Scalar> depth-offset { number }: scalar_syn.html#depth-offset
.. _<Scalar> depth-write { mode }: scalar_syn.html#depth-write
.. _<Scalar> depth-test { mode }: scalar_syn.html#depth-test


Other Group Attributes
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console
    
    <Billboard> { type }

This entry indicates that all geometry defined at or below this
group level is part of a billboard that will rotate to face the
camera.  Type is either "``axis``" or "``point``", describing the type of
rotation.

Billboards rotate about their local axis.  In the case of a Y-up
file, the billboards rotate about the Y axis; in a Z-up file, they
rotate about the Z axis.  Point-rotation billboards rotate about
the origin.

There is an implicit <Instance> around billboard geometry.  This
means that the geometry within a billboard is not specified in
world coordinates, but in the local billboard space.  Thus, a
vertex drawn at point 0,0,0 will appear to be at the pivot point
of the billboard, not at the origin of the scene.

.. code-block:: console
    
  <SwitchCondition> {
     <Distance> {
        in out [fade] <Vertex> { x y z }
     }
  }

The subtree beginning at this node and below represents a single
level of detail for a particular model.  Sibling nodes represent
the additional levels of detail.  The geometry at this node will
be visible when the point (x, y, z) is closer than "in" units, but
further than "out" units, from the camera.  "fade" is presently
ignored.

.. code-block:: console

    <Tag> key { value }

This attribute defines the indicated tag (as a key/value pair),
retrievable via ``NodePath::get_tag()`` and related interfaces, on
this node.

Instances
------------