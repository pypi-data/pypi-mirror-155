Use ``E4CV``\ ’s :math:`Q` calculation engine
=============================================

Many of the diffractometer geometries support different calculation
*engines*. By default, *hklpy* provides ``h``, ``k``, & ``l`` pseudo
positioners (the *hkl* engine) since this is the most common case. For
example, the
`E4CV <https://people.debian.org/~picca/hkl/hkl.html#org7ef08ba>`__
geometry supports several calculation engines:

+---------------+-------------------------+-------------------------+
| engine        | pseudo(s)               | real(s)                 |
+===============+=========================+=========================+
| ``hkl``       | ``h``, ``k``, ``l``     | ``omega``, ``chi``,     |
|               |                         | ``phi``, ``tth``        |
+---------------+-------------------------+-------------------------+
| ``psi``       | ``psi``                 | ``omega``, ``chi``,     |
|               |                         | ``phi``, ``tth``        |
+---------------+-------------------------+-------------------------+
| ``q``         | ``q``                   | ``tth``                 |
+---------------+-------------------------+-------------------------+
| ``incidence`` | ``incidence``,          | ``omega``, ``chi``,     |
|               | ``azimuth``             | ``phi``                 |
+---------------+-------------------------+-------------------------+
| ``emergence`` | ``emergence``,          | ``omega``, ``chi``,     |
|               | ``azimuth``             | ``phi``, ``tth``        |
+---------------+-------------------------+-------------------------+

NOTE: The choice of calculation engine is locked in the
``hkl.diffract.Diffractometer()`` class. Once the diffractometer object
is created, the calculation engine cannot be changed.

**Objective**

Many of the examples in the *hklpy* repository use the *hkl* engine, it
is the most common use case. Below, we’ll demonstrate the ``q``
calculation engine of the ``E4CV`` (4-circle Eulerian in vertical
scattering) geometry.

Standard Imports
----------------

First, we start by importing the ``gi``
(`gobject-introspection <https://pygobject.readthedocs.io/en/latest/index.html>`__)
package which is required to link the *libhkl* library (``'Hkl', 5.0``)
into Python. Then import the constant, ``A_KEV`` (product of Planck’s
constant and speed of light in a vacuum). The value of this constant is
obtained from the `2019 NIST publication of 2018 CODATA Fundamental
Physical
Constants <https://www.nist.gov/programs-projects/codata-values-fundamental-physical-constants>`__.
(Keep in mind that ``gi`` is not the ``Gtk`` library, just the tools
that enable other languages such as Python to use the libraries compiled
with `Gnome’s Glib Object:
GObject <https://developer.gnome.org/gobject/stable/>`__ framework.)

.. code:: ipython3

    import gi
    gi.require_version('Hkl', '5.0')
    from hkl import A_KEV

``q`` engine
------------

The ```q``
engine <https://people.debian.org/~picca/hkl/hkl.html#org7ef08ba>`__ is
easy to demonstrate since it only involves the actions of the ``tth``
circle (:math:`q=4\pi\sin(\theta)/\lambda` where :math:`\theta` is half
of ``tth``) **and** no crystal orientation reflections are necessary.

**Still**, it is necessary to define *all* required real positioners of
the geometry. The required positioners are listed as *Axes* directly
under the section title in the *libhkl* documentation for each geometry.
Also, specify them *in the order they appear in the documentation*. The
*real* positioners stay the same for all engines of a diffractometer
geometry. The *pseudo* positioners are defined by the calculation engine
and may be different for each engine.

TIP: If you do not define all the required *Axes* of the geometry,
Python will likely terminate (and with no useful message, at that) when
you first try to create the diffractometer object.

======== =========
term     value
======== =========
geometry ``E4CV``
engine   ``q``
mode     *default*
======== =========

Create a custom class for the ``E4CV`` geometry with the ``q``
calculation engine. There is only one pseudo positioner, ``q``, for the
calculation engine and the four real positioners for the geometry. Since
this demonstration uses ``SoftPositioners``, we must provide an
``init_pos`` kwarg with the initial position for each real axis. There
is no particular significance to the initial positions used in this
example.

.. code:: ipython3

    from hkl import E4CV
    from ophyd import Component
    from ophyd import PseudoSingle
    from ophyd import SoftPositioner
    
    class FourcQ(E4CV):
        # one pseudo axis for the q calculation engine
        q = Component(PseudoSingle)
        
        # four real axes (MUST specify in canonical order)
        omega = Component(SoftPositioner, init_pos=20)
        chi = Component(SoftPositioner, init_pos=90)
        phi = Component(SoftPositioner, init_pos=0)
        tth = Component(SoftPositioner, init_pos=40)  # "q" engine calls this "tth"

Create the diffractometer object.
---------------------------------

You specify the ``q`` calculation engine will be used when you create
the diffractometer object. (A request has been made to *hklpy* so this
can be defined in the class, including a default to ``hkl``.) Otherwise,
the support will default to the ``hkl`` engine and you cannot change it
later in the object. Once the object is created, the calculation engine
cannot be changed.

.. code:: ipython3

    fourcq = FourcQ("", name="fourcq", calc_kw=dict(engine="q"))

Test the ``q`` engine by calculating the angles associated with
:math:`Q=1.00` 1/angstrom. There is only one pseudo positioner so only
one value is provided to the ``forward()`` calculation. Notice that only
the ``tth`` position is computed.

.. code:: ipython3

    print(f"q to angle: {fourcq.forward(1) = }")


.. parsed-literal::

    q to angle: fourcq.forward(1) = PosCalcE4CV(omega=20.0, chi=90.0, phi=0.0, tth=14.0785064531777)


Calculate the :math:`q` associated with ``tth=1.0`` degrees. While four
real motors are defined, only ``tth`` is used for the calculation so
only one value is provided to the ``inverse()`` calculation.

.. code:: ipython3

    print(f"angle to q: {fourcq.inverse(1) = }")


.. parsed-literal::

    angle to q: fourcq.inverse(1) = FourcQPseudoPos(q=2.790877843251037)


Show the basic settings of the ``fourcq`` diffractometer.

.. code:: ipython3

    fourcq.wh()


.. parsed-literal::

    ===================== ================= =========
    term                  value             axis_type
    ===================== ================= =========
    diffractometer        fourcq                     
    sample name           main                       
    energy (keV)          8.05092                    
    wavelength (angstrom) 1.54000                    
    calc engine           q                          
    mode                  q                          
    q                     2.790877843251037 pseudo   
    omega                 20                real     
    chi                   90                real     
    phi                   0                 real     
    tth                   40                real     
    ===================== ================= =========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7fcf71412880>



Move ``fourcq`` to :math:`Q=1.0` 1/Angstrom and show the settings again.

.. code:: ipython3

    fourcq.move(1)
    fourcq.wh()


.. parsed-literal::

    ===================== ================= =========
    term                  value             axis_type
    ===================== ================= =========
    diffractometer        fourcq                     
    sample name           main                       
    energy (keV)          8.05092                    
    wavelength (angstrom) 1.54000                    
    calc engine           q                          
    mode                  q                          
    q                     1.000000000000004 pseudo   
    omega                 20.0              real     
    chi                   90.0              real     
    phi                   0.0               real     
    tth                   14.0785064531777  real     
    ===================== ================= =========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7fcfbffee760>



Show all the ``fourcq`` diffractometer settings.

.. code:: ipython3

    fourcq.pa()


.. parsed-literal::

    ===================== ====================================================================
    term                  value                                                               
    ===================== ====================================================================
    diffractometer        fourcq                                                              
    geometry              E4CV                                                                
    class                 FourcQ                                                              
    energy (keV)          8.05092                                                             
    wavelength (angstrom) 1.54000                                                             
    calc engine           q                                                                   
    mode                  q                                                                   
    positions             ===== ========                                                      
                          name  value                                                         
                          ===== ========                                                      
                          omega 20.00000                                                      
                          chi   90.00000                                                      
                          phi   0.00000                                                       
                          tth   14.07851                                                      
                          ===== ========                                                      
    constraints           ===== ========= ========== ================ ====                    
                          axis  low_limit high_limit value            fit                     
                          ===== ========= ========== ================ ====                    
                          omega -180.0    180.0      20.0             True                    
                          chi   -180.0    180.0      90.0             True                    
                          phi   -180.0    180.0      0.0              True                    
                          tth   -180.0    180.0      14.0785064531777 True                    
                          ===== ========= ========== ================ ====                    
    sample: main          ================ ===================================================
                          term             value                                              
                          ================ ===================================================
                          unit cell edges  a=1.54, b=1.54, c=1.54                             
                          unit cell angles alpha=90.0, beta=90.0, gamma=90.0                  
                          [U]              [[1. 0. 0.]                                        
                                            [0. 1. 0.]                                        
                                            [0. 0. 1.]]                                       
                          [UB]             [[ 4.07999046e+00 -2.49827363e-16 -2.49827363e-16] 
                                            [ 0.00000000e+00  4.07999046e+00 -2.49827363e-16] 
                                            [ 0.00000000e+00  0.00000000e+00  4.07999046e+00]]
                          ================ ===================================================
    ===================== ====================================================================
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7fcf71412790>



Move to a different wavelength (1.00 Angstrom) and move back to the same
:math:`Q` of 1.000 1/Angstrom.

.. code:: ipython3

    fourcq.energy.set(A_KEV / 1.0)
    fourcq.move(1)
    fourcq.wh()


.. parsed-literal::

    ===================== ================== =========
    term                  value              axis_type
    ===================== ================== =========
    diffractometer        fourcq                      
    sample name           main                        
    energy (keV)          12.39842                    
    wavelength (angstrom) 1.00000                     
    calc engine           q                           
    mode                  q                           
    q                     1.0000000000000022 pseudo   
    omega                 20.0               real     
    chi                   90.0               real     
    phi                   0.0                real     
    tth                   9.128558416134153  real     
    ===================== ================== =========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7fcf714122b0>


