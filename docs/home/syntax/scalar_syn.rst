.. _syntax_scalar_entry:

Scalar Definitions
====================

Scalars can appear in various contexts. They are always optional, and specify some attribute value relevant to the current context.

The scalar name is the name of the attribute; different attribute names are meaningful in different contexts.

The value is either a numeric or a (quoted or unquoted) string value; the interpretation as a number or as a string depends on the nature of the named attribute.


Alpha Scalars
---------------

Image Alpha File
^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> alpha-file { alpha-filename }

If this scalar is present, the texture file's alpha channel is
read in from the named image file (which should contain a
grayscale image), and the two images are combined into a single
two- or four-channel image internally.  This is useful for loading
alpha channels along with image file formats like JPEG that don't


Image Alpha File Channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> alpha-file-channel { channel }

This defines the channel that should be extracted from the file
named by alpha-file to determine the alpha channel for the
resulting channel.  

The default is ``0``, which means the grayscale combination of r, g, b.  
Otherwise, this should be the 1-based channel number, for instance ``1``, ``2``, or ``3`` for r, g, or b, respectively, or ``4`` for the alpha channel of a four-component image.

Alpha Blending
^^^^^^^^^^^^^^^^^^

.. code-block:: ruby
  
  <Scalar> alpha { alpha-type }

This specifies whether and what type of transparency will be
performed.  Alpha-type may be one of:

.. code-block:: console

    OFF
    ON
    BLEND
    BLEND_NO_OCCLUDE
    MS
    MS_MASK
    BINARY
    DUAL

If alpha-type is ``OFF``, it means not to enable transparency, even if
the image contains an alpha channel or the format is ``RGBA``.  If
alpha-type is ``ON``, it means to enable the default transparency,
even if the image filename does not contain an alpha channel.  If
alpha-type is any of the other options, it specifies the type of
transparency to be enabled.

Blend Mode (Group)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> blend { mode }

Specifies that a special blend mode should be applied geometry at
this level and below.  The available options are ``none``, ``add``,
``subtract``, ``inv-subtract``, ``min``, and ``max``.  See ColorBlendAttrib.

.. code-block:: ruby

  <Scalar> blendop-a { mode }
  <Scalar> blendop-b { mode }

If blend mode, above, is not none, this specifies the A and B
operands to the blend equation.  Common options are ``zero``, ``one``,
``incoming-color``, ``one-minus-incoming-color``.  See ColorBlendAttrib
for the complete list of available options.  The default is "one".

.. code-block:: ruby

  <Scalar> blendr { red-value }
  <Scalar> blendg { green-value }
  <Scalar> blendb { blue-value }
  <Scalar> blenda { alpha-value }

If blend mode, above, is not none, and one of the blend operands
is ``constant-color`` or a related option, this defines the constant
color that will be used.


Image Scalars
-----------------

Image Compression
^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> compression { compression-mode }

Defines an explicit control over the real-time compression mode
applied to the texture.  The various options are:

.. code-block:: console

  DEFAULT
  OFF
  ON
  FXT1
  DXT1
  DXT2
  DXT3
  DXT4
  DXT5

This controls the compression of the texture when it is loaded
into graphics memory, and has nothing to do with on-disk
compression such as JPEG. 

If this option is omitted or ``DEFAULT``, then the texture compression is controlled by the compressed-textures config variable. 

If it is ``OFF``, texture compression is explicitly off for this texture regardless of the setting of the config variable; if it is "``ON``", texture compression is explicitly on, and a default compression algorithm supported by the driver is selected. 

If any of the other options, it names the specific compression algorithm to be used.

Image Format
^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> format { format-definition }

This defines the load format of the image file. 

The format-definition is one of:

.. code-block:: console

  RGBA
  RGBM
  RGBA12
  RGBA8
  RGBA4
  RGB
  RGB12
  RGB8
  RGB5
  RGB332
  LUMINANCE_ALPHA
  RED
  GREEN
  BLUE
  ALPHA
  LUMINANCE

The formats whose names end in digits specifically request a
particular texel width.  ``RGB12`` and ``RGBA12`` specify 48-bit texels
with or without alpha; ``RGB8`` and ``RGBA8`` specify 32-bit texels, and
``RGB5`` and ``RGBA4`` specify 16-bit texels.  ``RGB332`` specifies 8-bit
texels.

The remaining formats are generic and specify only the semantic
meaning of the channels.  The size of the texels is determined by
the width of the components in the image file.  ``RGBA`` is the most
general; ``RGB`` is the same, but without any alpha channel.

``RGBM`` is like ``RGBA``, except that it requests only one bit of alpha, if the
graphics card can provide that, to leave more room for the RGB
components, which is especially important for older 16-bit
graphics cards (the "``M``" stands for "mask", as in a cutout).

The number of components of the image file should match the format
specified; if it does not, the egg loader will attempt to provide
the closest match that does.


Environment Type
^^^^^^^^^^^^^^^^^^
.. code-block:: ruby

  <Scalar> envtype { environment-type }

This specifies the type of texture environment to create; i.e. it
controls the way in which textures apply to models.
Environment-type may be one of:

.. code-block:: console
    
    MODULATE
    DECAL
    BLEND
    REPLACE
    ADD
    BLEND_COLOR_SCALE
    MODULATE_GLOW
    MODULATE_GLOSS
    *NORMAL
    *NORMAL_HEIGHT
    *GLOW
    *GLOSS
    *HEIGHT
    *SELECTOR

The default environment type is ``MODULATE``, which means the texture
color is multiplied with the base polygon (or vertex) color.  This
is the most common texture environment by far.  Other environment
types are more esoteric and are especially useful in the presence
of multitexture.  In particular, the types prefixed by an asterisk
(``*``) require enabling Panda's automatic ShaderGenerator.


Image Combine Modes
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby
    
  <Scalar> combine-rgb { combine-mode }
  <Scalar> combine-alpha { combine-mode }
  <Scalar> combine-rgb-source0 { combine-source }
  <Scalar> combine-rgb-operand0 { combine-operand }
  <Scalar> combine-rgb-source1 { combine-source }
  <Scalar> combine-rgb-operand1 { combine-operand }
  <Scalar> combine-rgb-source2 { combine-source }
  <Scalar> combine-rgb-operand2 { combine-operand }
  <Scalar> combine-alpha-source0 { combine-source }
  <Scalar> combine-alpha-operand0 { combine-operand }
  <Scalar> combine-alpha-source1 { combine-source }
  <Scalar> combine-alpha-operand1 { combine-operand }
  <Scalar> combine-alpha-source2 { combine-source }
  <Scalar> combine-alpha-operand2 { combine-operand }

These options replace the envtype and specify the texture combiner
mode, which is usually used for multitexturing.  This specifies
how the texture combines with the base color and/or the other
textures applied previously.  You must specify both an rgb and an
alpha combine mode.  Some combine-modes use one source/operand
pair, and some use all three; most use just two.

``combine-mode`` may be one of:

.. code-block:: console

      REPLACE
      MODULATE
      ADD
      ADD-SIGNED
      INTERPOLATE
      SUBTRACT
      DOT3-RGB
      DOT3-RGBA

``combine-source`` may be one of:

.. code-block:: console

      TEXTURE
      CONSTANT
      PRIMARY-COLOR
      PREVIOUS
      CONSTANT_COLOR_SCALE
      LAST_SAVED_RESULT

``combine-operand`` may be one of:

.. code-block:: console
    
      SRC-COLOR
      ONE-MINUS-SRC-COLOR
      SRC-ALPHA
      ONE-MINUS-SRC-ALPHA

The default values if any of these are omitted are:

.. code-block:: ruby
    
  <Scalar> combine-rgb { modulate }
  <Scalar> combine-alpha { modulate }
  <Scalar> combine-rgb-source0 { previous }
  <Scalar> combine-rgb-operand0 { src-color }
  <Scalar> combine-rgb-source1 { texture }
  <Scalar> combine-rgb-operand1 { src-color }
  <Scalar> combine-rgb-source2 { constant }
  <Scalar> combine-rgb-operand2 { src-alpha }
  <Scalar> combine-alpha-source0 { previous }
  <Scalar> combine-alpha-operand0 { src-alpha }
  <Scalar> combine-alpha-source1 { texture }
  <Scalar> combine-alpha-operand1 { src-alpha }
  <Scalar> combine-alpha-source2 { constant }
  <Scalar> combine-alpha-operand2 { src-alpha }


Image Min/Mag Filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> minfilter { filter-type }
  <Scalar> magfilter { filter-type }
  <Scalar> magfilteralpha { filter-type }
  <Scalar> magfiltercolor { filter-type }

This specifies the type of filter applied when minimizing or
maximizing. 

Filter-type may be one of:

.. code-block:: console

  NEAREST
  LINEAR
  NEAREST_MIPMAP_NEAREST
  LINEAR_MIPMAP_NEAREST
  NEAREST_MIPMAP_LINEAR
  LINEAR_MIPMAP_LINEAR

There are also some additional filter types that are supported for
historical reasons, but each of those additional types maps to one
of the above.  New egg files should use only the above filter
types.

Image Mipmaps
^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> read-mipmaps { flag }

If this flag is nonzero, then pre-generated mipmap levels will be
loaded along with the texture.  In this case, the filename should
contain a sequence of one or more hash mark (``#``) characters,
which will be filled in with the mipmap level number; the texture
filename thus determines a series of images, one for each mipmap
level.  The base texture image is mipmap level 0.

If this flag is specified in conjunction with a 3D or cube map
texture (as specified above), then the filename should contain two
hash mark sequences, separated by a character such as an
underscore, hyphen, or dot.  The first sequence will be filled in
with the mipmap level index, and the second sequence will be
filled in with the 3D sequence or cube map face.

Image Anisotropic Degree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> anisotropic-degree { degree }

Enables anisotropic filtering for the texture, and specifies the
degree of filtering.  If the degree is ``0`` or ``1``, anisotropic
filtering is disabled.  The default is disabled.

Image Border Color
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Scalar> borderr { red-value }
    <Scalar> borderg { green-value }
    <Scalar> borderb { blue-value }
    <Scalar> bordera { alpha-value }

These define the "border color" of the texture, which is
particularly important when one of the UV wrap modes is
``BORDER_COLOR``.


Image Type
^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> type { texture-type }

This may be one of the following attributes:

.. code-block:: console

  1D
  2D
  3D
  CUBE_MAP

The default is ``2D``, which specifies a normal, 2-d texture.  If
any of the other types is specified instead, a texture image of
the corresponding type is loaded.

If ``3D`` or ``CUBE_MAP`` is specified, then a series of texture images
must be loaded to make up the complete texture; in this case, the
texture filename is expected to include a sequence of one or more
hash mark (``#``) characters, which will be filled in with the
sequence number.  The first image in the sequence must be numbered
0, and there must be no gaps in the sequence.  In this case, a
separate alpha-file designation is ignored; the alpha channel, if
present, must be included in the same image with the color
channel(s).

Multiview Textures
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> multiview { flag }

If this flag is nonzero, the texture is loaded as a multiview
texture.  In this case, the filename must contain a hash mark
(``#``) as in the ``3D`` or ``CUBE_MAP`` case, above, and the different
images are loaded into the different views of the multiview
textures.  If the texture is already a cube map texture, the
same hash sequence is used for both purposes: the first six images
define the first view, the next six images define the second view,
and so on.  If the texture is a 3-D texture, you must also specify
``num-views``, below, to tell the loader how many images are loaded
for views, and how many are loaded for levels.

A multiview texture is most often used to load stereo textures,
where a different image is presented to each eye viewing the
texture, but other uses are possible, such as for texture
animation.

.. code-block:: ruby

  <Scalar> num-views { count }

This is used only when loading a 3-D multiview texture.  It
specifies how many different views the texture holds; the z height
of the texture is then implicitly determined as (number of images)
/ (number of views).

Texture Generation Mode
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> tex-gen { mode }

This specifies that texture coordinates for the primitives that
reference this texture should be dynamically computed at runtime,
for instance to apply a reflection map or some other effect.  The
valid values for mode are:

.. code-block:: console

  EYE_SPHERE_MAP (or SPHERE_MAP)
  WORLD_CUBE_MAP
  EYE_CUBE_MAP (or CUBE_MAP)
  WORLD_NORMAL
  EYE_NORMAL
  WORLD_POSITION
  EYE_POSITION
  POINT_SPRITE

Texture Priority
^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> priority { priority-value }

Specifies an integer sort value to rank this texture in priority
among other textures that are applied to the same geometry.  This
is only used to eliminate low-priority textures in case more
textures are requested for a particular piece of geometry than the
graphics hardware can render.


Texture Quality level
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> quality-level { quality }

Sets a hint to the renderer about the desired performance /
quality tradeoff for this particular texture.  This is most useful
for the tinydisplay software renderer; for normal,
hardware-accelerated renderers, this may have little or no effect.

This may be one of:

.. code-block:: console

  DEFAULT
  FASTEST
  NORMAL
  BEST

"Default" means to use whatever quality level is specified by the
global texture-quality-level config variable.


Texture Stage Scalars
------------------------

Stage Name
^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> stage-name { name }

Specifies the name of the ``TextureStage`` object that is created to
render this texture.  If this is omitted, a custom ``TextureStage`` is
created for this texture if it is required (e.g. because some
other multitexturing parameter has been specified), or the system
default ``TextureStage`` is used if multitexturing is not required.


Saved Result
^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> saved-result { flag }

If flag is nonzero, then it indicates that this particular texture
stage will be supplied as the "*last_saved_result*" source for any
future texture stages.


Material Scalars
--------------------

Material Components
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> diffr { number }
  <Scalar> diffg { number }
  <Scalar> diffb { number }
  <Scalar> diffa { number }

  <Scalar> ambr { number }
  <Scalar> ambg { number }
  <Scalar> ambb { number }
  <Scalar> amba { number }

  <Scalar> emitr { number }
  <Scalar> emitg { number }
  <Scalar> emitb { number }
  <Scalar> emita { number }

  <Scalar> specr { number }
  <Scalar> specg { number }
  <Scalar> specb { number }
  <Scalar> speca { number }


The four color groups, ``diff*``, ``amb*``, ``emit*``, and ``spec*`` specify the
diffuse, ambient, emission, and specular components of the lighting
equation, respectively.  Any of them may be omitted; the omitted
component(s) take their color from the native color of the
primitive, otherwise the primitive color is replaced with the
material color.

These properties collectively define a "material" that controls the
lighting effects that are applied to a surface; a material is only
in effect in the presence of lighting.


Material Shininess
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> shininess { number }
  <Scalar> local { flag }

The ``shininess`` property controls the size of the specular highlight, and the value ranges from 0 to 128. 

A larger value creates a smaller highlight (creating the appearance of a shinier surface).


Render Order Scalars
----------------------

Bin Order
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> bin { bin-name }


For *textures*, this specifies the bin name order of all polygons with this
texture applied, in the absence of a bin name specified on the polygon itself.

For *polygons*, this specifies the bin name for all polygons at or below this node that do not explicitly set their own bin. 

Draw Order
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> draw-order { number }

This specifies the fixed drawing order of all polygons with this
texture applied, in the absence of a drawing order specified on
the polygon itself. 

For Groups: This specifies the drawing order for all polygons at or below this node that do not explicitly set their own drawing order.  See the description of draw-order for geometry attributes, above.


Visibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> visibility { hidden | normal }

If the visibility of a group is set to ``hidden``, the primitives
nested within that group are not generated as a normally visible
primitive. 

If the Config.prc variable ``egg-suppress-hidden`` is set to true, the primitives are not converted at all; otherwise, they are converted as a "stashed" node.

Render Node Types
^^^^^^^^^^^^^^^^^^^^^^

Portal
`````````````````````

.. code-block:: ruby

  <Scalar> portal { boolean-value }

Used on a rectangular polygon to set it as a `PortalNode <https://docs.panda3d.org/1.11/python/reference/panda3d.core.PortalNode>`_.
This portal is used by the camera to "see through" to the other cells.
Meaning, when the camera is looking through the portal, the cell on the other side of the portal window is made visible.

Note: Nodes tagged a ``PortalNode`` will not be inherently visible in the scene graph, but will still report a bounding volume.


Polylight
`````````````````````

.. code-block:: ruby

  <Scalar> polylight { boolean-value }

Create a polylight instead of a regular polyset.

Note: Nodes tagged with ``polylight`` will be flagged as a ``PolylightNode`` in the scene graph with a ``Radius`` attribute. These nodes are not inherently visible in the scene graph and will not report a bounding volume.

Occluder
`````````````````````

.. code-block:: ruby

  <Scalar> occluder { boolean-value }

This makes the first (or only) polygon within this group node into
an occluder.  The polygon must have exactly four vertices.  An
occluder polygon is invisible.  When the occluder is activated
with ``model.set_occluder(occluder)``, objects that are behind the
occluder will not be drawn.  This can be a useful rendering
optimization for complex scenes, but should not be overused or
performance can suffer.


Depth Buffer Scalars
------------------------

For textures: Specifies special depth buffer properties of all polygons with this
texture applied. 

Depth Offset
^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> depth-offset { number }


Depth Write
^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> depth-write { mode }


Depth Test
^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> depth-test { mode }

For Groups: Specifies special depth buffer properties of all polygons at or below this node that do not override this. 


Decal Properties
-----------------

.. code-block:: ruby

  <Scalar> decal { boolean-value }

If this is present and boolean-value is non-zero, it indicates
that the geometry *below* this level is coplanar with the geometry
*at* this level, and the geometry below is to be drawn as a decal
onto the geometry at this level.  This means the geometry below
this level will be rendered "on top of" this geometry, but without
the Z-fighting artifacts one might expect without the use of the
decal flag.

.. code-block:: ruby

  <Scalar> decalbase { boolean-value }

This can optionally be used with the ``decal`` scalar, above. 
If present, it should be applied to a sibling of one or more nodes
with the ``decal`` scalar on.  It indicates which of the sibling
nodes should be treated as the base of the decal.  In the absence
of this scalar, the parent of all decal nodes is used as the decal
base.  This scalar is useful when the modeling package is unable
to parent geometry nodes to other geometry nodes.

UV Scalars 
-----------

UV Name
^^^^^^^^^

.. code-block:: ruby

  <Scalar> uv-name { name }

Specifies the name of the texture coordinates that are to be associated with this texture. 

If this is omitted, the default texture coordinates are used.


UV Scroll Mode
^^^^^^^^^^^^^^^^
.. code-block:: ruby

  <Scalar> scroll_u { speed }
  <Scalar> scroll_v { speed }
  <Scalar> scroll_w { speed }
  <Scalar> scroll_r { speed }


This declares a scroll speed on the texture image.

``speed`` can be a floating point value.


UV Wrap Mode
^^^^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> wrap { repeat-definition }
  <Scalar> wrapu { repeat-definition }
  <Scalar> wrapv { repeat-definition }
  <Scalar> wrapw { repeat-definition }

This defines the behavior of the texture image outside of the
normal (u,v) range 0.0 - 1.0.  

It is ``REPEAT`` to repeat the texture to infinity, ``CLAMP`` not to.  

The wrapping behavior may be specified independently for each axis via ``wrapu`` and ``wrapv``, or it may be specified for both simultaneously via "wrap".

Although less often used, for 3-d textures wrapw may also be specified, and it behaves similarly to ``wrapu`` and ``wrapv``.

There are other legal values in additional to ``REPEAT`` and ``CLAMP``.
The full list is:

.. code-block:: console

  CLAMP
  REPEAT
  MIRROR
  MIRROR_ONCE
  BORDER_COLOR


Animation Scalars
-------------------

FPS  
^^^^^^^^

.. code-block:: ruby

  <Scalar> fps { frame-rate }

This specifies the rate of animation for a ``SequenceNode`` (created
when the ``Switch`` flag is specified).  A value of zero
indicates a ``SwitchNode`` should be created instead.


NURBS Scalars
---------------

NURBS Type
^^^^^^^^^^^^

.. code-block:: ruby

  <Scalar> type { curve-type }

This defines the semantic meaning of this curve, either ``XYZ``, ``HPR``,
or ``T``.  If the type is ``XYZ``, the curve will automatically be
transformed between Y-up and Z-up if necessary; otherwise, it will
be left alone.

NURBS Subdivision
^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby
  
  <Scalar> subdiv { num-segments }

If this scalar is given and nonzero, Panda will create a visible
representation of the curve when the scene is loaded.  The number
represents the number of line segments to draw to approximate the
curve.

.. code-block:: ruby

  <Scalar> U-subdiv { u-num-segments }
  <Scalar> V-subdiv { v-num-segments }

These define the number of subdivisions to make in the U and V
directions to represent the surface.  A uniform subdivision is
always made, and trim curves are not respected (though they will
be drawn in if the trim curves themselves also have a subdiv
parameter).  This is only intended as a cheesy visualization.


PointLight Scalars 
-------------------

Thickness
^^^^^^^^^^

.. code-block:: ruby

  <Scalar> thick { number }

This specifies the size of the ``PointLight`` (or the width of a
line), in pixels, when it is rendered.  This may be a
floating-point number, but the fractional part is meaningful only
when antialiasing is in effect.  The default is ``1.0``.


Perspective
^^^^^^^^^^^^^^^

.. code-block:: ruby
  
  <Scalar> perspective { boolean-value }

If this is specified, then the thickness, above, is to interpreted
as a size in 3-d spatial units, rather than a size in pixels, and
the point should be scaled according to its distance from the
viewer normally.



Collide Scalars
---------------------

.. code-block:: ruby

  <Scalar> collide-mask { value }
  <Scalar> from-collide-mask { value }
  <Scalar> into-collide-mask { value }

Sets the ``CollideMasks`` on the collision nodes and geometry nodes
created at or below this group to the indicated values.  These
are bits that indicate which objects can collide with which
other objects.  Setting ``collide-mask`` is equivalent to setting
both ``from-collide-mask`` and ``into-collide-mask`` to the same
value.

The value may be an ordinary decimal integer, or a hex number in
the form 0x000, or a binary number in the form 0b000.