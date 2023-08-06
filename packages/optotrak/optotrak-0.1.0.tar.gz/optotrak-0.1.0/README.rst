optotrak
++++++++

Read data exported from NDI First Principles. Only tested for use with Optotrak
sensors.


Installation
============

Pip:

.. code::

   pip install optotrak

Conda:

.. code::

   conda install -c otaithleigh optotrak


Usage
=====

Read the example file into a pandas DataFrame:

>>> from optotrak import load_optotrak
>>> load_optotrak('test_optotrak.tsv')
                      x           y            z
Frame Name
1     Beam1  486.618958 -560.735657 -2618.344971
      Beam2  349.383820 -561.470093 -2552.003174
2     Beam1  486.617706 -560.736206 -2618.349365
      Beam2  349.381195 -561.467651 -2551.989258
3     Beam1  486.620819 -560.732178 -2618.347412
      Beam2  349.382477 -561.469910 -2551.998535
4     Beam1  486.624023 -560.735962 -2618.353760
      Beam2  349.385376 -561.468994 -2551.997070
5     Beam1  486.622925 -560.734924 -2618.353760
      Beam2  349.384094 -561.467957 -2551.995605
6     Beam1  486.618439 -560.733887 -2618.344971
      Beam2  349.382568 -561.467041 -2551.992432
7     Beam1  486.617798 -560.736206 -2618.344238
      Beam2  349.382965 -561.469482 -2551.994141
8     Beam1  486.620270 -560.736145 -2618.348877
      Beam2  349.382446 -561.466797 -2551.987305
9     Beam1  486.622437 -560.734375 -2618.348389
      Beam2  349.384796 -561.470032 -2551.996826
10    Beam1  486.623932 -560.736755 -2618.351318
      Beam2  349.382874 -561.468628 -2551.993896
