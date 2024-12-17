.. _reference_objecttypes:

Object Type Reference
=====================

Syntax Notation
----------------

.. code-block:: ruby
    
 <ObjectType> { type }

This is a short form to indicate one of several pre-canned sets of
attributes.  Type may be any word, and a Config definition will be
searched for by the name ``egg-object-type-word``, where ``word`` is
the type word.  This definition may contain any arbitrary egg
syntax to be parsed in at this group level.

Example Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^

In a config file, such as ``Config.prc``, you would include this entry:

.. code-block:: ruby

    egg-object-type-surface-snow <Tag> surface { snow }

In an egg file, it can be appended to the appropriate part using this:

.. code-block:: ruby

    <ObjectType> { surface-snow }

Which would be equivalent to:

.. code-block:: ruby

    <Tag> surface { snow }

if the object type is defined in ``Config.prc``.

Predefined Object Types
-------------------------

A number of predefined ObjectType definitions are provided:

Barrier
^^^^^^^^^^^^^

.. code-block:: ruby

  <ObjectType> { barrier }

This is equivalent to ``<Collide> { Polyset descend }``.  The
geometry defined at this root and below defines an invisible
collision solid, meant to block avatars from crossing them.

Use these to funnel avatars through doorways, keep them from falling off bridges, and so on.

Trigger
^^^^^^^^^^^^^

.. code-block:: ruby

  <ObjectType> { trigger }

This is equivalent to ``<Collide> { Polyset descend intangible }``.
The geometry defined at this root and below defines an invisible
trigger surface.

Triggers can be used to signal when avatars have entered a certain area of the model.
One could place a trigger polygon in front of a door, for example, so the player can tell when the avatar has moved through the door.

Sphere
^^^^^^^^

.. code-block:: ruby

  <ObjectType> { sphere }

Equivalent to ``<Collide> { Sphere descend }``.  The geometry is
replaced with the smallest collision sphere that will enclose
it.  Typically you model a sphere in polygons and put this flag
on it to create a collision sphere of the same size.

Tube
^^^^^^

.. code-block:: ruby

  <ObjectType> { tube }

Equivalent to ``<Collide> { Tube descend }``.  As in sphere, above,
but the geometry is replaced with a collision tube (a capsule).
Typically you will model a capsule or a cylinder in polygons.

Bubble
^^^^^^^

.. code-block:: ruby

  <ObjectType> { bubble }

Equivalent to ``<Collide> { Sphere keep descend }``.  A collision
bubble is placed around the geometry, which is otherwise
unchanged.

Ghost
^^^^^

.. code-block:: ruby

  <ObjectType> { ghost }

Equivalent to ``<Scalar> collide-mask { 0 }``.  It means that the
geometry beginning at this node and below should never be
collided with--characters will pass through it.

Backstage
^^^^^^^^^^^^

.. code-block:: ruby

  <ObjectType> { backstage }


.. note::
    This has no equivalent reference; it is treated as a special case.

It means that the geometry at this node and below should not be
translated.  This will normally be used on scale references and
other modeling tools.

Modelers should use this flag on reference objects that they include to help in the modeling task (such as scale references)
