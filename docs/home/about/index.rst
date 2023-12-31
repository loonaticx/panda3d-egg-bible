.. _about:


About
======

What Are Egg Files?
---------------------

*Egg* files are used by Panda3D to describe many properties of a scene: simple geometry, 
including special effects and collision surfaces, characters including skeletons, morphs, 
and multiple-joint assignments, and character animation tables.

Egg files are designed to be the lingua franca of model manipulation
for Panda tools.  A number of utilities are provided that read and
write egg files, for instance to convert to or from some other
modeling format, or to apply a transform or optimize vertices.  The
egg file philosophy is to describe objects in an abstract way that
facilitates easy manipulation; thus, the format doesn't (usually)
include information such as polygon connectivity or triangle meshes.
Egg files are furthermore designed to be human-readable to help a
developer diagnose (and sometimes repair) problems.  Also, the egg
syntax is always intended to be backward compatible with previous
versions, so that as the egg syntax is extended, old egg files will
continue to remain valid.

Bam Versus Egg
`````````````````

This is a different philosophy than Panda's bam file format, which is
a binary representation of a model and/or animation that is designed
to be loaded quickly and efficiently, and is strictly tied to a
particular version of Panda.  The data in a bam file closely mirrors
the actual Panda structures that are used for rendering.  Although an
effort is made to keep bam files backward compatible, occasionally
this is not possible and we must introduce a new bam file major
version.

Where egg files are used for model conversion and manipulation of
models, bam files are strictly used for loading models into Panda.
Although you can load an egg file directly, a bam file will be loaded
much more quickly.

Generating Egg Files
```````````````````````````

Egg files might be generated by outside sources, and thus it makes
sense to document its syntax here.  Bam files, on the other hand,
should only be generated by Panda3D, usually by the program ``egg2bam``.
The exact specification of the bam file format, if you should need it,
is documented within the Panda3D code itself.
