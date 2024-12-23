.. _reference_collide:

Collide Reference
==================

Definition & Usage
--------------------

.. code-block:: ruby

  <Collide> name { type [flags] }

This entry indicates that geometry defined at this group level is
an invisible collision surface, and is not true geometry.
The geometry is used to define the extent of the collision
surface.  If there is no geometry defined at this level, then a
child is searched for with the same collision type specified, and
its geometry is used to define the extent of the collision
surface (unless the ``descend`` flag is given; see below).

.. note::

    It is now deprecated to use ``<Collide>`` without ``descend``; it will become the default soon. 
    You should always specify it for best compatibility.

.. note::
    It is not necessary, and in fact some cases it will actually cause
    problems if you set the transparency value for collision nodes to 0.0.
    These objects will automatically be invisible in the player if they do not have the ``keep`` keyword.

Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ruby

    <Collide> { polyset descend } // considered as a generic wall/mesh barrier
    <Collide> door_trigger { plane event intangible descend } // to implement a feature (like a door opening) if the player touches this plane

Collision Types
--------------------

``Plane``
^^^^^^^^^^^^

The geometry represents an infinite plane.  The first polygon
found in the group will define the plane.

``Polygon``
^^^^^^^^^^^^^^

The geometry represents a single polygon.  The first polygon is
used.

``Polyset``
^^^^^^^^^^^^^^

The geometry represents a complex shape made up of several
polygons. 

.. note:: 
    This collision type should not be overused, as it provides the least optimization benefit.

``Sphere``
^^^^^^^^^^^

The geometry represents a sphere.  The vertices in the group are
averaged together to determine the sphere's center and radius.

``Box``
^^^^^^^^^

The geometry represents a box.  The smallest axis-aligned box
that will fit around the vertices is used.

``InvSphere``
^^^^^^^^^^^^^^^

The geometry represents an inverse sphere.  This is the same as
Sphere, with the normal inverted, so that the solid part of an
inverse sphere is the entire world outside of it.  Note that an
inverse sphere is an infinitely large solid with a finite hole
cut into it.

``Tube``
^^^^^^^^^^^

The geometry represents a tube.  This is a cylinder-like shape
with hemispherical endcaps, sometimes called a capsule or
lozenge in other packages.  The smallest tube shape that will
fit around the vertices is used.

Collision Flags
-----------------

The flags may be any zero or more of:

``event``
^^^^^^^^^^^^^^

Throws the name of the ``<Collide>`` entry, or the name of the
surface if the ``<Collide>`` entry has no name, as an event whenever
an avatar strikes the solid.  This is the default if the
``<Collide>`` entry has a name.

``intangible``
^^^^^^^^^^^^^^^^

Rather than being a solid collision surface, the defined surface
represents a boundary.  The name of the surface will be thrown
as an event when an avatar crosses into the interior, and
name-out will be thrown when an avatar exits.

``descend``
^^^^^^^^^^^^^

Each group descended from this node that contains geometry will
define a new collision object of the given type.  The event
name, if any, will also be inherited from the top node and
shared among all the collision objects. 

.. note::
     This option will soon be the default; it is suggested that it is always specified for most compatibility.

``keep``
^^^^^^^^^^

Don't discard the visible geometry after using it to define a
collision surface; create both an invisible collision surface
and the visible geometry.

``level``
^^^^^^^^^^^^

Stores a special effective normal with the collision solid that
points up, regardless of the actual shape or orientation of the
solid.  This can be used to allow an avatar to stand on a
sloping surface without having a tendency to slide downward.
