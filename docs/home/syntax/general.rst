.. _syntax_general:

General Egg Syntax
====================

Egg files consist of a series of sequential and hierarchically-nested entries. 

In general, the syntax of each entry is:

.. code-block:: ruby
    
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

.. code-block:: ruby

    <Comment> { text }

``<Comment>`` entries are slightly different, in that tools which read and write egg files will preserve the text within ``<Comment>`` entries, but they may not preserve comments delimited by ``//`` or ``/* */``. 

Special characters and keywords within a ``<Comment>`` entry should be quoted; it's safest to quote the entire comment.


Local Information Entries
-------------------------------

These nodes contain information relevant to the current level of nesting only.

.. code-block:: ruby

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

.. code-block:: ruby
    
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

    `<Scalar> uv-name { name }`_

    `<Scalar> borderr { red-value }`_

    `<Scalar> borderg { green-value }`_

    `<Scalar> borderb { blue-value }`_

    `<Scalar> bordera { alpha-value }`_

    `<Scalar> type { texture-type }`_

    `<Scalar> multiview { flag }`_

    `<Scalar> num-views { count }`_

    `<Scalar> read-mipmaps { flag }`_

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
.. _<Scalar> uv-name { name }: scalar_syn.html#uv-name
.. _<Scalar> borderr { red-value }: scalar_syn.html#image-border-color
.. _<Scalar> borderg { green-value }: scalar_syn.html#image-border-color
.. _<Scalar> borderb { blue-value }: scalar_syn.html#image-border-color
.. _<Scalar> bordera { alpha-value }: scalar_syn.html#image-border-color
.. _<Scalar> type { texture-type }: scalar_syn.html#image-type
.. _<Scalar> multiview { flag }: scalar_syn.html#multiview-textures
.. _<Scalar> num-views { count }: scalar_syn.html#multiview-textures
.. _<Scalar> read-mipmaps { flag }: scalar_syn.html#image-mipmaps
.. _<Scalar> minfilter { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfilter { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfilteralpha { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> magfiltercolor { filter-type }: scalar_syn.html#image-min-mag-filtering
.. _<Scalar> anisotropic-degree { degree }: scalar_syn.html#image-anisotropic-degree
.. _<Scalar> envtype { environment-type }: scalar_syn.html#environment-type




Geometry 
---------

Vertices
`````````````

.. code-block:: ruby

  <Vertex> number { x [y [z [w]]] [attributes] }

A ``<Vertex>`` entry is only valid within a vertex pool definition.
The number is the index by which this vertex will be referenced.
It is optional; if it is omitted, the vertices are implicitly
numbered consecutively beginning at one.  If the number is
supplied, the vertices need not be consecutive.

Normally, vertices are three-dimensional (with coordinates x, y,
and z); however, in certain cases vertices may have fewer or more
dimensions, up to four.  This is particularly true of vertices
used as control vertices of NURBS curves and surfaces.  If more
coordinates are supplied than needed, the extra coordinates are
ignored; if fewer are supplied than needed, the missing
coordinates are assumed to be 0.

The vertex's coordinates are always given in world space,
regardless of any transforms before the vertex pool or before the
referencing geometry.  If the vertex is referenced by geometry
under a transform, the egg loader will do an inverse transform to
move the vertex into the proper coordinate space without changing
its position in world space.  One exception is geometry under an
``<Instance>`` node; in this case the vertex coordinates are given in
the space of the ``<Instance>`` node.  (Another exception is a
``<DynamicVertexPool>``; see below.)

While each vertex must at least have a position, it may also have
a color, normal, pair of UV coordinates, and/or a set of morph
offsets.  Furthermore, the color, normal, and UV coordinates may
themselves have morph offsets.  Thus, the [attributes] in the
syntax line above may be replaced with zero or more of the
following entries:

.. code-block:: ruby

    <Dxyz> target { x y z }

This specifies the offset of this vertex for the named morph
target.  See the "MORPH DESCRIPTION ENTRIES" header, below.

.. code-block:: ruby

    <Normal> { x y z [morph-list] }

This specifies the surface normal of the vertex.  If omitted, the
vertex will have no normal.  Normals may also be morphed;
``morph-list`` here is thus an optional list of ``<DNormal>`` entries,
similar to the above.

.. code-block:: ruby

    <RGBA> { r g b a [morph-list] }

This specifies the four-valued color of the vertex.  Each
component is in the range 0.0 to 1.0.  A vertex color, if
specified for all vertices of the polygon, overrides the polygon's
color.  If neither color is given, the default is white
(1 1 1 1).  The ``morph-list`` is an optional list of ``<DRGBA>`` entries.


Vertex Pools
^^^^^^^^^^^^^^^

.. code-block:: ruby
    
    <VertexPool> name { vertices }

A *vertex pool* is a set of vertices.  All geometry is created by
referring to vertices by number in a particular vertex pool.  There
may be one or several vertex pools in an egg file, but all vertices
that make up a single polygon must come from the same vertex pool.
The body of a ``<VertexPool>`` entry is simply a list of one or more 
``<Vertex>`` entries.

In neither case does it make a difference whether the vertex pool
is itself declared under a transform or an ``<Instance>`` node.  The
only deciding factor is whether the geometry that *uses* the
vertex pool appears under an ``<Instance>`` node.  It is possible for
a single vertex to be interpreted in different coordinate spaces
by different polygons.


.. code-block:: ruby

    <DynamicVertexPool> name { vertices }

A dynamic vertex pool is similar to a vertex pool in most respects,
except that each vertex might be animated by substituting in values
from a ``<VertexAnim>`` table.  Also, the vertices defined within a
dynamic vertex pool are always given in local coordinates, instead
of world coordinates.

The presence of a dynamic vertex pool makes sense only within a
character model, and a single dynamic vertex pool may not span
multiple characters.  Each dynamic vertex pool creates a DynVerts
object within the character by the same name; this name is used
later when matching up the corresponding ``<VertexAnim>``.

.. note::

    At the present time, the DynamicVertexPool is not implemented in Panda3D.


UVs (Vertexes)
^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <UV> [name] { u v [w] [tangent] [binormal] [morph-list] }

This gives the texture coordinates of a vertex.  This must be
specified if a texture is to be mapped onto this geometry.

The texture coordinates are usually two-dimensional, with two
component values (u v), but they may also be three-dimensional,
with three component values (u v w).  (Arguably, it should be
called ``<UVW>`` instead of ``<UV>`` in the three-dimensional case, but
it's not.)

As before, morph-list is an optional list of ``<DUV>`` entries.

Unlike the other kinds of attributes, there may be multiple sets
of UV's on each vertex, each with a unique name; this provides
support for multitexturing.  The name may be omitted to specify
the default UV's.

The UV's also support an optional tangent and binormal.  These
values are based on the vertex normal and the UV coordinates of
connected vertices, and are used to render normal maps and similar
lighting effects.  They are defined within the ``<UV>`` entry because
there may be a different set of tangents and binormals for each
different UV coordinate set.  If present, they have the expected
syntax:

.. code-block:: ruby

    <UV> [name] { u v [w] <Tangent> { x y z } <Binormal> { x y z } }


    <AUX> name { x y z w }

This specifies some named per-vertex auxiliary data which is
imported from the egg file without further interpretation by
Panda.  The auxiliary data is copied to the vertex data under a
column with the specified name.  Presumably the data will have
meaning to custom code or a custom shader.  Like named UV's, there
may be multiple Aux entries for a given vertex, each with a
different name.

Polygons
`````````````

.. code-block:: ruby

    <Polygon> name {
        [attributes]
        <VertexRef> {
            indices
            <Ref> { pool-name }
        }
    }

A *polygon* consists of a sequence of vertices from a single vertex
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

The following attributes may be specified for polygons:

.. code-block:: ruby

  <TRef> { texture-name }

This refers to a named ``<Texture>`` entry given earlier.  It applies
the given texture to the polygon.  This requires that all the
polygon's vertices have been assigned texture coordinates.

This attribute may be repeated multiple times to specify
multitexture.  In this case, each named texture is applied to the
polygon, in the order specified.


.. code-block:: ruby

  <Texture> { filename }

This is another way to apply a texture to a polygon.  The
``<Texture>`` entry is defined "inline" to the polygon, instead of
referring to a ``<Texture>`` entry given earlier.  There is no way to
specify texture attributes given this form.

There's no advantage to this syntax for texture mapping.  It's
supported only because it's required by some older egg files.


.. code-block:: ruby


  <MRef> { material-name }

This applies the material properties defined in the earlier
<Material> entry to the polygon.


.. code-block:: ruby

  <Normal> { x y z [morph-list] }

This defines a polygon surface normal.  The polygon normal will be
used unless all vertices also have a normal.  If no normal is
defined, none will be supplied.  The polygon normal, like the
vertex normal, may be morphed by specifying a series of ``<DNormal>``
entries.

The polygon normal is used only for lighting and environment
mapping calculations, and is not related to the implicit normal
calculated for ``CollisionPolygons``.


.. code-block:: ruby


  <RGBA> { r g b a [morph-list] }

This defines the polygon's color, which will be used unless all
vertices also have a color.  If no color is defined, the default
is white (1 1 1 1).  The color may be morphed with a series of
<DRGBA> entries.


.. code-block:: ruby


  <BFace> { boolean-value }

This defines whether the polygon will be rendered double-sided
(i.e. its back face will be visible).  By default, this option is
disabled, and polygons are one-sided; specifying a nonzero value
disables backface culling for this particular polygon and allows
it to be viewed from either side.


.. code-block:: ruby

    <Scalar> bin { bin-name }
    
    <Scalar> draw-order { number }
    
    <Scalar> depth-offset { number }
    
    <Scalar> depth-write { mode }
    
    <Scalar> depth-test { mode }
    
    <Scalar> visibility { hidden | normal }


Patches
`````````````

.. code-block:: ruby

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
`````````````

.. code-block:: ruby

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

.. code-block:: ruby

    <Scalar> thick { number }

    <Scalar> perspective { boolean-value }



Lines
`````````````

.. code-block:: ruby

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
```````````````````

.. code-block:: ruby

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

.. code-block:: ruby

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

.. code-block:: ruby
    
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

.. code-block:: ruby

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

.. code-block:: ruby
    
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

Transformations
------------------

.. code-block:: ruby

  <Transform> { transform-definition }

This specifies a matrix transform at this group level.  This
defines a local coordinate space for this group and its
descendents.  Vertices are still specified in world coordinates
(in a vertex pool), but any geometry assigned to this group will
be inverse transformed to move its vertices to the local space.

The transform definition may be any sequence of zero or more of
the following.  Transformations are post multiplied in the order
they are encountered to produce a net transformation matrix.
Rotations are defined as a counterclockwise angle in degrees about
a particular axis, either implicit (about the x, y, or z axis), or
arbitrary.  Matrices, when specified explicitly, are row-major.

.. code-block:: ruby

      <Translate> { x y z }
      <RotX> { degrees }
      <RotY> { degrees }
      <RotZ> { degrees }
      <Rotate> { degrees x y z }
      <Scale> { x y z }
      <Scale> { s }

      <Matrix4> {
        00 01 02 03
        10 11 12 13
        20 21 22 23
        30 31 32 33
      }

Note that the ``<Transform>`` block should always define a 3-d
transform when it appears within the body of a ``<Group>``, while it
may define either a 2-d or a 3-d transform when it appears within
the body of a ``<Texture>``.  See <Texture>, above.


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

.. code-block:: ruby
    
    <Dxyz> target { x y z }

A position delta, valid within a ``<Vertex>`` entry or a ``<CV>`` entry.
The given offset vector, scaled by the morph target's value, is
added to the vertex or CV position each frame.

.. code-block:: ruby
    
    <DNormal> target { x y z }

A normal delta, similar to the position delta, valid within a
``<Normal>`` entry (for vertex or polygon normals).  The given offset
vector, scaled by the morph target's value, is added to the normal
vector each frame.  The resulting vector may not be automatically
normalized to unit length.

.. code-block:: ruby
    
    <DUV> target { u v [w] }

A texture-coordinate delta, valid within a ``<UV>`` entry (within a
``<Vertex>`` entry).  The offset vector should be 2-valued if the
enclosing UV is 2-valued, or 3-valued if the enclosing UV is
3-valued.  The given offset vector, scaled by the morph target's
value, is added to the vertex's texture coordinates each frame.


.. code-block:: ruby
    
    <DRGBA> target { r g b a }

A color delta, valid within an ``<RGBA>`` entry (for vertex or polygon
colors).  The given 4-valued offset vector, scaled by the morph
target's value, is added to the color value each frame.


Groups
---------

.. code-block:: ruby

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
````````````````````````````````````

These attributes may be either on or off; they are off by default.
They are turned on by specifying a non-zero "boolean-value".

DCS Attributes
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <DCS> { boolean-value }

DCS stands for Dynamic Coordinate System.  This indicates that
show code will expect to be able to read the transform set on this
node at run time, and may need to modify the transform further.
This is a special case of <Model>, below.

.. code-block:: ruby

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

Model Attribute
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Model> { boolean-value }

This indicates that the show code might need a pointer to this
particular group.  This creates a ModelNode at the corresponding
level, which is guaranteed not to be removed by any flatten
operation.  However, its transform might still be changed, but see
also the ``<DCS>`` flag, above.

Dart Attributes
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Dart> { boolean-value }

This indicates that this group begins an animated character.  A
Character node, which is the fundamental animatable object of
Panda's high-level Actor class, will be created for this group.

This flag should always be present within the ``<Group>`` entry at the
top of any hierarchy of ``<Joint>``'s and/or geometry with morphed
vertices; joints and morphs appearing outside of a hierarchy
identified with a ``<Dart>`` flag are undefined.

.. code-block:: ruby

    <Dart> { structured }

This is an optional alternative for the ``<Dart>`` flag.

By default, Panda will collapse all of the geometry in a group (with the ``<Dart> { 1 }`` flag)
a single node. While this is optimal for conditions such as characters moving around
a scene, it may be suboptimal for larger or more complex characters.

This entry is typically generated by the ``egg-optchar`` program with the ``-dart structured`` flag.
``<Dart> { structured }`` implies ``<Dart> { 1 }``.

Switch Attribute
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Switch> { boolean-value }

This attribute indicates that the child nodes of this group
represent a series of animation frames that should be
consecutively displayed. 

In the absence of an "``fps``" scalar for the group (see below), the egg loader creates a ``SwitchNode``, and it
the responsibility of the show code to perform the switching.  If
an fps scalar is defined and is nonzero, the egg loader creates a
SequenceNode instead, which automatically cycles through its
children.


Group Scalars
````````````````````````

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
.. _<Scalar> visibility { hidden | normal }: scalar_syn.html#visibility
.. _<Scalar> decal { boolean-value }: scalar_syn.html#decal-properties
.. _<Scalar> decalbase { boolean-value }: scalar_syn.html#decal-properties
.. _<Scalar> collide-mask { value }: scalar_syn.html#collide-scalars
.. _<Scalar> from-collide-mask { value }: scalar_syn.html#collide-scalars
.. _<Scalar> into-collide-mask { value }: scalar_syn.html#collide-scalars
.. _<Scalar> blend { mode }: scalar_syn.html#blend-mode-group
.. _<Scalar> blendop-a { mode }: scalar_syn.html#blend-mode-group
.. _<Scalar> blendop-b { mode }: scalar_syn.html#blend-mode-group
.. _<Scalar> blendr { red-value }: scalar_syn.html#blend-mode-group
.. _<Scalar> blendg { green-value }: scalar_syn.html#blend-mode-group
.. _<Scalar> blendb { blue-value }: scalar_syn.html#blend-mode-group
.. _<Scalar> blenda { alpha-value }: scalar_syn.html#blend-mode-group
.. _<Scalar> occluder { boolean-value }: scalar_syn.html#occluder


Other Group Attributes
``````````````````````````

Billboards
^^^^^^^^^^^

.. code-block:: ruby
    
    <Billboard> { type }

This entry indicates that all geometry defined at or below this
group level is part of a billboard that will rotate to face the
camera.  Type is either ``axis`` or ``point``, describing the type of
rotation.

Billboards rotate about their local axis.  In the case of a Y-up
file, the billboards rotate about the Y axis; in a Z-up file, they
rotate about the Z axis.  Point-rotation billboards rotate about
the origin.

There is an implicit ``<Instance>`` around billboard geometry.  This
means that the geometry within a billboard is not specified in
world coordinates, but in the local billboard space.  Thus, a
vertex drawn at point 0,0,0 will appear to be at the pivot point
of the billboard, not at the origin of the scene.

Level of Detail (LOD)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby
    
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

Vertex References
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <VertexRef> { indices <Ref> { pool-name } }

This moves geometry created from the named vertices into the
current group, regardless of the group in which the geometry is
actually defined. 

Instances
------------

.. code-block:: ruby

    <Instance> name { group-body }

An ``<Instance>`` node is exactly like a ``<Group>`` node, except that
vertices referenced by geometry created under the ``<Instance>`` node
are not assumed to be given in world coordinates, but are instead
given in the local space of the ``<Instance>`` node itself (including
any transforms given to the node).

In other words, geometry under an ``<Instance>`` node is defined in
local coordinates.  In principle, similar geometry can be created
under several different ``<Instance>`` nodes, and thus can be positioned
in a different place in the scene each instance.  This doesn't
necessarily imply the use of shared geometry in the Panda3D scene
graph, but see the ``<Ref>`` syntax, below.

This is particularly useful in conjunction with a ``<File>`` entry, to
load external file references at places other than the origin.


A special syntax of ``<Instance>`` entries does actually create shared
geometry in the scene graph.  The syntax is:

.. code-block:: ruby

    <Instance> name {
        <Ref> { group-name }
        [ <Ref> { group-name } ... ]
    }

In this case, the referenced group name will appear as a *duplicate*
instance in this part of the tree.  Local transforms can be applied
and are relative to the referencing group's transform.  The
referenced group must appear preceding this point in the egg file,
and it will also be a part of the scene in the point at which it
first appears.  The referenced group may be either a ``<Group>`` or an
``<Instance>`` of its own; usually, it is a ``<Group>`` nested within an
earlier ``<Instance>`` entry.

Joints
---------

.. code-block:: ruby

    <Joint> name { [transform] [ref-list] [joint-list] }

A joint is a highly specialized kind of grouping node.  A tree of
joints is used to specify the skeletal structure of an animated
character.

A joint may only contain one of three things.  It may contain a
``<Transform>`` entry, as above, which defines the joint's unanimated
(rest) position; it may contain lists of assigned vertices or CV's;
and it may contain other joints.

A tree of ``<Joint>`` nodes only makes sense within a character
definition, which is created by applying the ``<Dart>`` flag to a group.
See ``<Dart>``, above.

The vertex assignment is crucial.  This is how the geometry of a
character is made to move with the joints.  The character's geometry
is actually defined outside the joint tree, and each vertex must be
assigned to one or more joints within the tree.

This is done with zero or more ``<VertexRef>`` entries per joint, as the
following:

.. code-block:: ruby

  <VertexRef> { indices [<Scalar> membership { m }] <Ref> { pool-name } }

This is syntactically similar to the way vertices are assigned to
polygons.  Each ``<VertexRef>`` entry can assign vertices from only one
vertex pool (but there may be many ``<VertexRef>`` entries per joint).
Indices is a list of vertex numbers from the specied vertex pool, in
an arbitrary order.

The ``membership`` scalar is optional.  If specified, it is a value
between 0.0 and 1.0 that indicates the fraction of dominance this
joint has over the vertices.  This is used to implement
soft-skinning, so that each vertex may have partial ownership in
several joints.

The ``<VertexRef>`` entry may also be given to ordinary ``<Group>`` nodes.
In this case, it treats the geometry as if it was parented under the
group in the first place.  Non-total membership assignments are
meaningless.

Tables and Bundles
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Bundle> name { table-list }
    <Table> name { table-body }

A table is a set of animated values for joints.  A tree of tables
with the same structure as the corresponding tree of joints must be
defined for each character to be animated.  Such a tree is placed
under a ``<Bundle>`` node, which provides a handle within Panda to the
tree as a whole.

Bundles may only contain tables; tables may contain more tables,
bundles, or any one of the following (``<Scalar>`` entries are optional,
and default as shown):

.. code-block:: ruby

    <S$Anim> name {
        <Scalar> fps { 24 }
        <V> { values }
    }

This is a table of scalar values, one per frame.  This may be
applied to a morph slider, for instance.

.. code-block:: ruby

    <Xfm$Anim> name {
        <Scalar> fps { 24 }
        <Scalar> order { srpht }
        <Scalar> contents { ijkabcrphxyz }
        <V> { values }
    }

This is a table of matrix transforms, one per frame, such as may
be applied to a joint.  The "contents" string consists of a subset
of the letters "``ijkabcrphxyz``", where each letter corresponds to a
column of the table; ``<V>`` is a list of numbers of length(contents)
* num_frames.  Each letter of the contents string corresponds to a
type of transformation:

.. code-block:: javascript

      i, j, k - scale in x, y, z directions, respectively
      a, b, c - shear in xy, xz, and yz planes, respectively
      r, p, h - rotate by roll, pitch, heading
      x, y, z - translate in x, y, z directions

The net transformation matrix specified by each row of the table
is defined as the net effect of each of the individual columns'
transform, according to the corresponding letter in the contents
string.  The order the transforms are applied is defined by the
order string:

.. code-block:: javascript

      s       - all scale and shear transforms
      r, p, h - individual rotate transforms
      t       - all translation transforms


.. code-block:: ruby

    <Xfm$Anim_S$> name {
        <Scalar> fps { 24 }
        <Scalar> order { srpht }
        <S$Anim> i { ... }
        <S$Anim> j { ... }
        ...
    }

This is a variant on the ``<Xfm$Anim>`` entry, where each column of
the table is entered as a separate ``<S$Anim>`` table.  This syntax
reflects an attempt to simplify the description by not requiring
repetition of values for columns that did not change value during
an animation sequence.

.. code-block:: ruby

  <VertexAnim> name {
      <Scalar> width { table-width }
      <Scalar> fps { 24 }
      <V> { values }
  }

This is a table of vertex positions, normals, texture coordinates,
or colors.  These values will be subsituted at runtime for the
corresponding values in a ``<DynamicVertexPool>``.  The name of the
table should be "``coords``", "``norms``", "``texCoords``", or "``colors``",
according to the type of values defined.  The number table-width
is the number of floats in each row of the table.  In the case of
a coords or norms table, this must be 3 times the number of
vertices in the corresponding dynamic vertex pool.  (For texCoords
and colors, this number must be 2 times and 4 times, respectively.)


Animation Structure
-----------------------

Unanimated models may be defined in egg files without much regard to
any particular structure, so long as named entries like VertexPools
and Textures appear before they are referenced.

However, a certain rigid structural convention must be followed in
order to properly define an animated skeleton-morph model and its
associated animation data.

The structure for an animated model should resemble the following:

.. code-block:: ruby
    
    <Group> CHARACTER_NAME {
    <Dart> { 1 }
    <Joint> JOINT_A {
        <Transform> { ... }
        <VertexRef> { ... }
        <Group> { <Polygon> ... }
        <Joint> JOINT_B {
        <Transform> { ... }
        <VertexRef> { ... }
        <Group> { <Polygon> ... }
        }
        <Joint> JOINT_C {
        <Transform> { ... }
        <VertexRef> { ... }
        <Group> { <Polygon> ... }
        }
        ...
    }
    }

The ``<Dart>`` flag is necessary to indicate that this group begins an
animated model description.

Without the ``<Dart>`` flag, joints will be treated as ordinary groups, and morphs will be ignored.

It is important to note that utilizing ``<Dart> { 1 }`` will collapse all of the
model's geometry into a single node. To omit this, use ``<Dart> { structured }`` instead.
(See ``<Dart``> above.)

In the above, UPPERCASE NAMES represent an arbitrary name that you
may choose.  The name of the enclosing group, CHARACTER_NAME, is
taken as the name of the animated model.  It should generally match
the bundle name in the associated animation tables.

Within the ``<Dart>`` group, you may define an arbitrary hierarchy of
``<Joint>`` entries.  There may be as many ``<Joint>`` entries as you like,
and they may have any nesting complexity you like.  There may be
either one root ``<Joint>``, or multiple roots.  However, you must
always include at least one ``<Joint>``, even if your animation consists
entirely of morphs.

Polygons may be directly attached to joints by enclosing them within
the ``<Joint>`` group, perhaps with additional nesting ``<Group>`` entries,
as illustrated above.  This will result in the polygon's vertices
being hard-assigned to the joint it appears within.  Alternatively,
you declare the polygons elsewhere in the egg file, and use
``<VertexRef>`` entries within the ``<Joint>`` group to associate the
vertices with the joints.  This is the more common approach, since
it allows for soft-assignment of vertices to multiple joints.

It is not necessary for every joint to have vertices at all.  Every
joint should include a transform entry, however, which defines the
initial, resting transform of the joint (but see also ``<DefaultPose>``,
above).  If a transform is omitted, the identity transform is
assumed.

Some of the vertex definitions may include morph entries, as
described in MORPH DESCRIPTION ENTRIES, above.  These are meaningful
only for vertices that are assigned, either implicitly or
explicitly, to at least one joint.

You may have multiple versions of a particular animated model--for
instance, multiple different LOD's, or multiple different clothing
options.  Normally each different version is stored in a different
egg file, but it is also possible to include multiple versions
within the same egg file.  If the different versions are intended to
play the same animations, they should all have the same
CHARACTER_NAME, and their joint hierarchies should exactly match in
structure and names.

The structure for an animation table should resemble the following:

.. code-block:: ruby

    <Table> {
    <Bundle> CHARACTER_NAME {
        <Table> "<skeleton>" {
        <Table> JOINT_A {
            <Xfm$Anim_S$> xform {
            <Char*> order { sphrt }
            <Scalar> fps { 24 }
            <S$Anim> x { 0 0 10 10 20 ... }
            <S$Anim> y { 0 0 0 0 0 ... }
            <S$Anim> z { 20 20 20 20 20 ... }
            }
            <Table> JOINT_B {
            <Xfm$Anim_S$> xform {
                <Char*> order { sphrt }
                <Scalar> fps { 24 }
                <S$Anim> x { ... }
                <S$Anim> y { ... }
                <S$Anim> z { ... }
            }
            }
            <Table> JOINT_C {
            <Xfm$Anim_S$> xform {
                <Char*> order { sphrt }
                <Scalar> fps { 24 }
                <S$Anim> x { ... }
                <S$Anim> y { ... }
                <S$Anim> z { ... }
            }
            }
        }
        }
        <Table> morph {
        <S$Anim> MORPH_A {
            <Scalar> fps { 24 }
            <V> { 0 0 0 0.1 0.2 0.3 1 ... }
        }
        <S$Anim> MORPH_B {
            <Scalar> fps { 24 }
            <V> { ... }
        }
        <S$Anim> MORPH_C {
            <Scalar> fps { 24 }
            <V> { ... }
        }
        }
    }
    }

The ``<Bundle>`` entry begins an animation table description.  This
entry must have at least one child: a ``<Table>`` named ``<skeleton>``
(this name is a literal keyword and must be present).  The children
of this ``<Table>`` entry should be a hierarchy of additional ``<Table>``
entries, one for each joint in the model.  The joint structure and
names defined by the ``<Table>`` hierarchy should exactly match the
joint structure and names defined by the ``<Joint>`` hierarchy in the
corresponding model.

Each ``<Table>`` that corresponds to a joint should have one child, an
``<Xfm$Anim_S$>`` entry named ``xform`` (this name is a literal keyword
and must be present).  Within this entry, there is a series of up to
twelve ``<S$Anim>`` entries, each with a one-letter name like "x", "y",
or "z", which define the per-frame x, y, z position of the
corresponding joint.  There is one numeric entry for each frame, and
all frames represent the same length of time.  You can also define
rotation, scale, and shear.  See the full description of
``<Xfm$Anim_S$>``, above.

Within a particular animation bundle, all of the various components
throughout the various ``<Tables>`` should define the same number of
frames, with the exception that if any of them define exactly one
frame value, that value is understood to be replicated the
appropriate number of times to match the number of frames defined by
other components.

(Note that you may alternatively define an animation table with an
``<Xfm$Anim>`` entry, which defines all of the individual components in
one big matrix instead of individually.  See the full description
above.)

Each joint defines its frame rate independently, with an "fps"
scalar.  This determines the number of frames per second for the
frame data within this table.  Typically, all joints have the same
frame rate, but it is possible for different joints to animate at
different speeds.

Each joint also defines the order in which its components should be
composed to determine the complete transform matrix, with an "order"
scalar.  This is described in more detail above.


If any of the vertices in the model have morphs, the top-level
``<Table>`` should also include a ``<Table>`` named ``morph`` (this name is
also a literal keyword).  This table in turn contains a list of
``<S$Anim>`` entries, one for each named morph description.  Each table
contains a list of numeric values, one per frame; as with the joint
data, there should be the same number of numeric values in all
tables, with the exception that just one value is understood to mean
hold that value through the entire animation.

The "morph" table may be omitted if there are no morphs defined in
the model.

There should be a separate ``<Bundle>`` definition for each different
animation.  The ``<Bundle>`` name should match the CHARACTER_NAME used
for the model, above.  Typically each bundle is stored in a separate
egg file, but it is also possible to store multiple different
animation bundles within the same egg file.  If you do this, you may
violate the CHARACTER_NAME rule, and give each bundle a different
name; this will become the name of the animation in the Actor
interface.

Although animations and models are typically stored in separate egg
files, it is possible to store them together in one large egg file.
The Actor interface will then make available all of the animations
it finds within the egg file, by bundle name.


Default Pose
^^^^^^^^^^^^^

.. code-block:: ruby

  <DefaultPose> { transform-definition }

This defines an optional default pose transform, which might be a
different transform from that defined by the ``<Transform>`` entry,
above.  This makes sense only for a ``<Joint>``.  See the ``<Joint>``
description, below.

The default pose transform defines the transform the joint will
maintain in the absence of any animation being applied.  This is
different from the ``<Transform>`` entry, which defines the coordinate
space the joint must have in order to keep its vertices in their
(global space) position as given in the egg file.  If this is
different from the ``<Transform>`` entry, the joint's vertices will
*not* be in their egg file position at initial load.  If there is
no ``<DefaultPose>`` entry for a particular joint, the implicit
default-pose transform is the same as the ``<Transform>`` entry.

Normally, the ``<DefaultPose>`` entry, if any, is created by the
``egg-optchar -defpose`` option.  Most other software has little
reason to specify an explicit ``<DefaultPose>``.

AnimPreload
^^^^^^^^^^^^^

.. code-block:: ruby

  <AnimPreload> {
    <Scalar> fps { float-value }
    <Scalar> num-frames { integer-value }
  }

One or more AnimPreload entries may appear within the ``<Group>`` that
contains a ``<Dart>`` entry, indicating an animated character (see
above).  These AnimPreload entries record the minimal preloaded
animation data required in order to support asynchronous animation
binding.  These entries are typically generated by the egg-optchar
program with the ``-preload`` option, and are used by the Actor code
when allow-async-bind is True (the default).


Miscellaneous
---------------

File
^^^^^^^^^^^

.. code-block:: ruby

    <File> { filename }

This includes a copy of the referenced egg file at the current
point.  This is usually placed under an ``<Instance>`` node, so that the
current transform will apply to the geometry in the external file.
The extension ``.egg`` is implied if it is omitted.

As with texture filenames, the filename may be a relative path, in
which case the current egg file's directory is searched first, and
then the model-path is searched.

Node Tags
^^^^^^^^^^^

.. code-block:: ruby

    <Tag> key { value }

This attribute defines the indicated tag (as a key/value pair),
retrievable via ``NodePath::get_tag()`` and related interfaces, on
this node.