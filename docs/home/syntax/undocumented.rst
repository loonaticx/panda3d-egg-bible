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

<Scalar> direct { 1 }
---------------------------------

<TexList> { 1 }
----------------------

<Scalar> no-fog { 1 }
------------------------------