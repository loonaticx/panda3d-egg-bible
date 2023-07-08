.. _reference_objecttypes:

Object Type Reference
=====================

 <ObjectType> { type }

This is a short form to indicate one of several pre-canned sets of
attributes.  Type may be any word, and a Config definition will be
searched for by the name "egg-object-type-word", where "word" is
the type word.  This definition may contain any arbitrary egg
syntax to be parsed in at this group level.

A number of predefined ObjectType definitions are provided:

barrier

    This is equivalent to <Collide> { Polyset descend }.  The
    geometry defined at this root and below defines an invisible
    collision solid.

trigger

    This is equivalent to <Collide> { Polyset descend intangible }.
    The geometry defined at this root and below defines an invisible
    trigger surface.

sphere

    Equivalent to <Collide> { Sphere descend }.  The geometry is
    replaced with the smallest collision sphere that will enclose
    it.  Typically you model a sphere in polygons and put this flag
    on it to create a collision sphere of the same size.

tube

    Equivalent to <Collide> { Tube descend }.  As in sphere, above,
    but the geometry is replaced with a collision tube (a capsule).
    Typically you will model a capsule or a cylinder in polygons.

bubble

    Equivalent to <Collide> { Sphere keep descend }.  A collision
    bubble is placed around the geometry, which is otherwise
    unchanged.

ghost

    Equivalent to <Scalar> collide-mask { 0 }.  It means that the
    geometry beginning at this node and below should never be
    collided with--characters will pass through it.

backstage

    This has no equivalent; it is treated as a special case.  It
    means that the geometry at this node and below should not be
    translated.  This will normally be used on scale references and
    other modeling tools.
