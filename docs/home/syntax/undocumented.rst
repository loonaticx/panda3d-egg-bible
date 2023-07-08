.. _syntax_undocumented:

Undocumented Entries
========================

<BillboardCenter> 
---------------------

.. code-block:: console

  if (has_billboard_center()) {
    indent(out, indent_level)
      << "<BillboardCenter> { " << get_billboard_center() << " }\n";
  }



<Scalar> indexed
--------------------

.. code-block:: console

  if (has_indexed_flag()) {
    indent(out, indent_level + 2)
      << "<Scalar> indexed { " << get_indexed_flag() << " }\n";
  }


<Scalar> portal { 1 }
-------------------------
Create a portal instead of a regular polyset.

<Scalar> occluder { 1 }
---------------------------
Create an occluder instead of a regular polyset

<Scalar> polylight { 1 }
----------------------------
    // Create a polylight instead of a regular polyset.  use make_sphere to
    // get the center, radius and color egg2pg_cat.debug() << "polylight
    // node\n"

<Scalar> scroll_u { ... }
------------------------------

<Scalar> scroll_v { ... }
------------------------------

<Scalar> scroll_w { ... }
------------------------------

<Scalar> scroll_r { ... }
------------------------------

<Scalar> direct { 1 }
---------------------------------

<TexList> { 1 }
----------------------

<Scalar> no-fog { 1 }
------------------------------