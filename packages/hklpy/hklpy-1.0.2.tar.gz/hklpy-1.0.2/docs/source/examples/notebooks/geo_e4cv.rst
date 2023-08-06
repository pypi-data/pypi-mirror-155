E4CV : 4-circle diffractometer example
======================================

The `IUCr provides a schematic of the 4-circle
diffractometer <http://ww1.iucr.org/iucr-top/comm/cteach/pamphlets/2/node14.html>`__
(in horizontal geometry typical of a laboratory instrument).

.. raw:: html

   <!-- image source:
     http://ww1.iucr.org/iucr-top/comm/cteach/pamphlets/2/
     -->

.. figure:: resources/img69.gif
   :alt: E4CH geometry

   E4CH geometry

At X-ray synchrotrons, the vertical geometry is more common due to the
polarization of the X-rays.

--------------

Note: This example is available as a `Jupyter
notebook <https://jupyter.org/>`__ from the *hklpy* source code website:
https://github.com/bluesky/hklpy/tree/main/examples

Load the *hklpy* package (named *hkl*)
--------------------------------------

Since the *hklpy* package is a thin interface to the *hkl* library
(compiled C++ code), we need to **first** load the
*gobject-introspection* package (named *``gi``*) and name our required
code and version.

This is needed *every* time before the *hkl* package is first imported.

.. code:: ipython3

    import gi
    gi.require_version('Hkl', '5.0')

Setup the *E4CV* diffractometer in *hklpy*
------------------------------------------

In *hkl* *E4CV* geometry
(https://people.debian.org/~picca/hkl/hkl.html#org7ef08ba):

.. figure:: resources/3S+1D.png
   :alt: E4CV geometry

   E4CV geometry

-  xrays incident on the :math:`\vec{x}` direction (1, 0, 0)

===== ======== ================ ============
axis  moves    rotation axis    vector
===== ======== ================ ============
omega sample   :math:`-\vec{y}` ``[0 -1 0]``
chi   sample   :math:`\vec{x}`  ``[1 0 0]``
phi   sample   :math:`-\vec{y}` ``[0 -1 0]``
tth   detector :math:`-\vec{y}` ``[0 -1 0]``
===== ======== ================ ============

Define *this* diffractometer
----------------------------

Create a Python class that specifies the names of the real-space
positioners. We call it ``FourCircle`` here but that choice is
arbitrary. Pick any valid Python name not already in use. The convention
is to start Python class names with a capital letter and use CamelCase
to mark word starts.

The argument to the ``FourCircle()`` class tells which *hklpy* base
class will be used. This sets the geometry. (The class we show here
could be replaced entirely with ``hkl.geometries.SimulatedE4CV`` but we
choose to show here the complete steps to produce that class.) The
`hklpy
documentation <https://blueskyproject.io/hklpy/master/geometries.html>`__
provides a complete list of diffractometer geometries.

In *hklpy*, the reciprocal-space axes are known as ``pseudo``
positioners while the real-space axes are known as ``real`` positioners.
For the real positioners, it is possible to use different names than the
canonical names used internally by the *hkl* library. That is not
covered here.

Note: The keyword argument ``kind="hinted"`` is an indication that this
signal may be plotted.

This ``FourCircle()`` class example uses simulated motors. See the
drop-down for an example how to use EPICS motors.

.. raw:: html

   <details>

.. raw:: html

   <summary>

FourCircle() class using EPICS motors

.. raw:: html

   </summary>

.. code:: python


   from hkl import E4CV
   from ophyd import EpicsMotor, PseudoSingle
   from ophyd import Component as Cpt

   class FourCircle(E6C):
       """
       Our 4-circle.  Eulerian.  Vertical scattering orientation.
       """
       # the reciprocal axes are called "pseudo" in hklpy
       h = Cpt(PseudoSingle, '', kind="hinted")
       k = Cpt(PseudoSingle, '', kind="hinted")
       l = Cpt(PseudoSingle, '', kind="hinted")

       # the motor axes are called "real" in hklpy
       omega = Cpt(EpicsMotor, "pv_prefix:m41", kind="hinted")
       chi = Cpt(EpicsMotor, "pv_prefix:m22", kind="hinted")
       phi = Cpt(EpicsMotor, "pv_prefix:m35", kind="hinted")
       tth = Cpt(EpicsMotor, "pv_prefix:m7", kind="hinted")

.. raw:: html

   </details>

.. code:: ipython3

    from hkl import E4CV, SimMixin
    from ophyd import SoftPositioner
    from ophyd import Component as Cpt
    
    class FourCircle(SimMixin, E4CV):
        """
        Our 4-circle.  Eulerian, vertical scattering orientation.
        """
        # the reciprocal axes are defined by SimMixin
    
        omega = Cpt(SoftPositioner, kind="hinted", init_pos=0)
        chi = Cpt(SoftPositioner, kind="hinted", init_pos=0)
        phi = Cpt(SoftPositioner, kind="hinted", init_pos=0)
        tth = Cpt(SoftPositioner, kind="hinted", init_pos=0)

Create the Python diffractometer object (``fourc``) using the
``FourCircle()`` class. By convention, the ``name`` keyword is the same
as the object name.

.. code:: ipython3

    fourc = FourCircle("", name="fourc")

Add a sample with a crystal structure
-------------------------------------

.. code:: ipython3

    from hkl import Lattice
    from hkl import SI_LATTICE_PARAMETER
    
    # add the sample to the calculation engine
    a0 = SI_LATTICE_PARAMETER
    fourc.calc.new_sample(
        "silicon",
        lattice=Lattice(a=a0, b=a0, c=a0, alpha=90, beta=90, gamma=90)
        )




.. parsed-literal::

    HklSample(name='silicon', lattice=LatticeTuple(a=5.431020511, b=5.431020511, c=5.431020511, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]]), UB=array([[ 1.15690694e+00, -7.08401189e-17, -7.08401189e-17],
           [ 0.00000000e+00,  1.15690694e+00, -7.08401189e-17],
           [ 0.00000000e+00,  0.00000000e+00,  1.15690694e+00]]), reflections=[])



Setup the UB orientation matrix using *hklpy*
---------------------------------------------

Define the crystal’s orientation on the diffractometer using the
2-reflection method described by `Busing & Levy, Acta Cryst 22 (1967)
457 <https://www.psi.ch/sites/default/files/import/sinq/zebra/PracticalsEN/1967-Busing-Levy-3-4-circle-Acta22.pdf>`__.

Set the same X-ray wavelength for both reflections, by setting the diffractometer energy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    from hkl import A_KEV
    fourc.energy.put(A_KEV / 1.54)  # (8.0509 keV)

Specify the first reflection and identify its Miller indices: (*hkl*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    r1 = fourc.calc.sample.add_reflection(
        4, 0, 0,
        position=fourc.calc.Position(
            tth=69.0966,
            omega=-145.451,
            chi=0,
            phi=0,
        )
    )

Specify the second reflection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    r2 = fourc.calc.sample.add_reflection(
        0, 4, 0,
        position=fourc.calc.Position(
            tth=69.0966,
            omega=-145.451,
            chi=90,
            phi=0,
        )
    )

Compute the *UB* orientation matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``add_reflection()`` method uses the current wavelength at the time
it is called. (To add reflections at different wavelengths, change the
wavelength *before* calling ``add_reflection()`` each time.) The
``compute_UB()`` method returns the computed **UB** matrix. Ignore it
here.

.. code:: ipython3

    fourc.calc.sample.compute_UB(r1, r2)




.. parsed-literal::

    array([[-1.41342846e-05, -1.41342846e-05, -1.15690694e+00],
           [ 0.00000000e+00, -1.15690694e+00,  1.41342846e-05],
           [-1.15690694e+00,  1.72682934e-10,  1.41342846e-05]])



Report what we have setup
-------------------------

.. code:: ipython3

    fourc.pa()


.. parsed-literal::

    ===================== ===========================================================================
    term                  value                                                                      
    ===================== ===========================================================================
    diffractometer        fourc                                                                      
    geometry              E4CV                                                                       
    class                 FourCircle                                                                 
    energy (keV)          8.05092                                                                    
    wavelength (angstrom) 1.54000                                                                    
    calc engine           hkl                                                                        
    mode                  bissector                                                                  
    positions             ===== =======                                                              
                          name  value                                                                
                          ===== =======                                                              
                          omega 0.00000                                                              
                          chi   0.00000                                                              
                          phi   0.00000                                                              
                          tth   0.00000                                                              
                          ===== =======                                                              
    constraints           ===== ========= ========== ===== ====                                      
                          axis  low_limit high_limit value fit                                       
                          ===== ========= ========== ===== ====                                      
                          omega -180.0    180.0      0.0   True                                      
                          chi   -180.0    180.0      0.0   True                                      
                          phi   -180.0    180.0      0.0   True                                      
                          tth   -180.0    180.0      0.0   True                                      
                          ===== ========= ========== ===== ====                                      
    sample: silicon       ================= =========================================================
                          term              value                                                    
                          ================= =========================================================
                          unit cell edges   a=5.431020511, b=5.431020511, c=5.431020511              
                          unit cell angles  alpha=90.0, beta=90.0, gamma=90.0                        
                          ref 1 (hkl)       h=4.0, k=0.0, l=0.0                                      
                          ref 1 positioners omega=-145.45100, chi=0.00000, phi=0.00000, tth=69.09660 
                          ref 2 (hkl)       h=0.0, k=4.0, l=0.0                                      
                          ref 2 positioners omega=-145.45100, chi=90.00000, phi=0.00000, tth=69.09660
                          [U]               [[-1.22173048e-05 -1.22173048e-05 -1.00000000e+00]       
                                             [ 0.00000000e+00 -1.00000000e+00  1.22173048e-05]       
                                             [-1.00000000e+00  1.49262536e-10  1.22173048e-05]]      
                          [UB]              [[-1.41342846e-05 -1.41342846e-05 -1.15690694e+00]       
                                             [ 0.00000000e+00 -1.15690694e+00  1.41342846e-05]       
                                             [-1.15690694e+00  1.72682934e-10  1.41342846e-05]]      
                          ================= =========================================================
    ===================== ===========================================================================
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f52eadf1820>



Check the orientation matrix
----------------------------

Perform checks with *forward* (hkl to angle) and *inverse* (angle to
hkl) computations to verify the diffractometer will move to the same
positions where the reflections were identified.

Constrain the motors to limited ranges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  allow for slight roundoff errors
-  keep ``tth`` in the positive range
-  keep ``omega`` in the negative range
-  keep ``phi`` fixed at zero

First, we apply constraints directly to the ``calc``-level support.

.. code:: ipython3

    fourc.calc["tth"].limits = (-0.001, 180)
    fourc.calc["omega"].limits = (-180, 0.001)
    fourc.show_constraints()
    
    fourc.phi.move(0)
    fourc.engine.mode = "constant_phi"


.. parsed-literal::

    ===== ========= ========== ===== ====
    axis  low_limit high_limit value fit 
    ===== ========= ========== ===== ====
    omega -180.0    0.001      0.0   True
    chi   -180.0    180.0      0.0   True
    phi   -180.0    180.0      0.0   True
    tth   -0.001    180.0      0.0   True
    ===== ========= ========== ===== ====
    


Next, we show how to use additional methods of ``Diffractometer()`` that
support *undo* and *reset* features for applied constraints. The support
is based on a *stack* (a Python list). A set of constraints is added
(``apply_constraints()``) or removed (``undo_last_constraints()``) from
the stack. Or, the stack can be cleared (``reset_constraints()``).

+-----------------------------------+-----------------------------------+
| method                            | what happens                      |
+===================================+===================================+
| ``apply_constraints()``           | Add a set of constraints and use  |
|                                   | them                              |
+-----------------------------------+-----------------------------------+
| ``undo_last_constraints()``       | Remove the most-recent set of     |
|                                   | constraints and restore the       |
|                                   | previous one from the stack.      |
+-----------------------------------+-----------------------------------+
| ``reset_constraints()``           | Set constraints back to initial   |
|                                   | settings.                         |
+-----------------------------------+-----------------------------------+
| ``show_constraints()``            | Print the current constraints in  |
|                                   | a table.                          |
+-----------------------------------+-----------------------------------+

A set of constraints is a Python dictionary that uses the real
positioner names (the motors) as the keys. Only those constraints with
changes need be added to the dictionary but it is permissable to
describe all the real positioners. Each value in the dictionary is a
```hkl.diffract.Constraint`` <https://blueskyproject.io/hklpy/diffract.html#hkl.diffract.Constraint>`__,
where the values are specified in this order:
``low_limit, high_limit, value, fit``.

+-----------------------------------+-----------------------------------+
| ``fit``                           | constraint                        |
+===================================+===================================+
| ``True``                          | Only accept solutions with        |
|                                   | positions between ``low_limit``   |
|                                   | and ``high_limit``.               |
+-----------------------------------+-----------------------------------+
| ``False``                         | Do not allow this positioner to   |
|                                   | be adjusted and fix its position  |
|                                   | to ``value``.                     |
+-----------------------------------+-----------------------------------+

Apply new constraints using the
```applyConstraints()`` <https://blueskyproject.io/hklpy/diffract.html#hkl.diffract.Diffractometer.apply_constraints>`__
method. These *add* to the existing constraints, as shown in the table.

.. code:: ipython3

    from hkl import Constraint
    fourc.apply_constraints(
        {
            "tth": Constraint(-0.001, 90, 0, True),
            "chi": Constraint(-90, 90, 0, True),
        }
    )
    fourc.show_constraints()


.. parsed-literal::

    ===== ========= ========== ===== ====
    axis  low_limit high_limit value fit 
    ===== ========= ========== ===== ====
    omega -180.0    0.001      0.0   True
    chi   -90.0     90.0       0.0   True
    phi   -180.0    180.0      0.0   True
    tth   -0.001    90.0       0.0   True
    ===== ========= ========== ===== ====
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f52ebe68f40>



Then remove (undo) those new additions.

.. code:: ipython3

    fourc.undo_last_constraints()
    fourc.show_constraints()


.. parsed-literal::

    ===== ========= ========== ===== ====
    axis  low_limit high_limit value fit 
    ===== ========= ========== ===== ====
    omega -180.0    0.001      0.0   True
    chi   -180.0    180.0      0.0   True
    phi   -180.0    180.0      0.0   True
    tth   -0.001    180.0      0.0   True
    ===== ========= ========== ===== ====
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f52ebe60d30>



(400) reflection test
~~~~~~~~~~~~~~~~~~~~~

1. Check the ``inverse`` (angles -> (*hkl*)) computation.
2. Check the ``forward`` ((*hkl*) -> angles) computation.

Check the inverse calculation: (400)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To calculate the (*hkl*) corresponding to a given set of motor angles,
call ``fourc.inverse((h, k, l))``. Note the second set of parentheses
needed by this function.

The values are specified, without names, in the order specified by
``fourc.calc.physical_axis_names``.

.. code:: ipython3

    print("axis names:", fourc.calc.physical_axis_names)


.. parsed-literal::

    axis names: ['omega', 'chi', 'phi', 'tth']


Now, proceed with the inverse calculation.

.. code:: ipython3

    sol = fourc.inverse((-145.451, 0, 0, 69.0966))
    print(f"(4 0 0) ? {sol.h:.2f} {sol.k:.2f} {sol.l:.2f}")


.. parsed-literal::

    (4 0 0) ? 4.00 0.00 0.00


Check the forward calculation: (400)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Compute the angles necessary to position the diffractometer for the
given reflection.

Note that for the forward computation, more than one set of angles may
be used to reach the same crystal reflection. This test will report the
*default* selection. The *default* selection (which may be changed
through methods described in the ``hkl.calc`` module) is the first
solution.

======================== ==============================
function                 returns
======================== ==============================
``fourc.forward()``      The *default* solution
``fourc.calc.forward()`` List of all allowed solutions.
======================== ==============================

.. code:: ipython3

    sol = fourc.forward((4, 0, 0))
    print(
        "(400) :", 
        f"tth={sol.tth:.4f}", 
        f"omega={sol.omega:.4f}", 
        f"chi={sol.chi:.4f}", 
        f"phi={sol.phi:.4f}"
        )


.. parsed-literal::

    (400) : tth=69.0982 omega=-145.4502 chi=0.0000 phi=0.0000


(040) reflection test
~~~~~~~~~~~~~~~~~~~~~

Repeat the ``inverse`` and ``forward`` calculations for the second
orientation reflection.

Check the inverse calculation: (040)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    sol = fourc.inverse((-145.451, 90, 0, 69.0966))
    print(f"(0 4 0) ? {sol.h:.2f} {sol.k:.2f} {sol.l:.2f}")


.. parsed-literal::

    (0 4 0) ? 0.00 4.00 0.00


Check the forward calculation: (040)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    sol = fourc.forward((0, 4, 0))
    print(
        "(040) :", 
        f"tth={sol.tth:.4f}", 
        f"omega={sol.omega:.4f}", 
        f"chi={sol.chi:.4f}", 
        f"phi={sol.phi:.4f}"
        )


.. parsed-literal::

    (040) : tth=69.0982 omega=-145.4502 chi=90.0000 phi=0.0000


Scan in reciprocal space using Bluesky
--------------------------------------

To scan with Bluesky, we need more setup.

.. code:: ipython3

    %matplotlib inline
    
    from bluesky import RunEngine
    from bluesky import SupplementalData
    from bluesky.callbacks.best_effort import BestEffortCallback
    from bluesky.magics import BlueskyMagics
    import bluesky.plans as bp
    import bluesky.plan_stubs as bps
    import databroker
    from IPython import get_ipython
    import matplotlib.pyplot as plt
    
    plt.ion()
    
    bec = BestEffortCallback()
    db = databroker.temp().v1
    sd = SupplementalData()
    
    get_ipython().register_magics(BlueskyMagics)
    
    RE = RunEngine({})
    RE.md = {}
    RE.preprocessors.append(sd)
    RE.subscribe(db.insert)
    RE.subscribe(bec)




.. parsed-literal::

    1



(*h00*) scan near (400)
~~~~~~~~~~~~~~~~~~~~~~~

In this example, we have no detector. Still, we add the diffractometer
object in the detector list so that the *hkl* and motor positions will
appear as columns in the table.

.. code:: ipython3

    RE(bp.scan([fourc], fourc.h, 3.9, 4.1, 5))


.. parsed-literal::

    
    
    Transient Scan ID: 1     Time: 2021-07-19 16:02:09
    Persistent Unique Scan ID: '60d5f02f-8ba8-4035-9d74-c37151428675'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |   seq_num |       time |    fourc_h |    fourc_k |    fourc_l | fourc_omega |  fourc_chi |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |         1 | 16:02:09.5 |      3.900 |     -0.000 |     -0.000 |    -146.431 |     -0.000 |      0.000 |     67.137 |
    |         2 | 16:02:10.0 |      3.950 |     -0.000 |     -0.000 |    -145.942 |      0.000 |      0.000 |     68.115 |
    |         3 | 16:02:10.6 |      4.000 |      0.000 |      0.000 |    -145.450 |      0.000 |      0.000 |     69.098 |
    |         4 | 16:02:11.1 |      4.050 |      0.000 |      0.000 |    -144.956 |      0.000 |      0.000 |     70.087 |
    |         5 | 16:02:11.7 |      4.100 |     -0.000 |     -0.000 |    -144.458 |      0.000 |      0.000 |     71.083 |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    generator scan ['60d5f02f'] (scan num: 1)


.. parsed-literal::

    /home/prjemian/.local/lib/python3.8/site-packages/bluesky/callbacks/fitting.py:165: RuntimeWarning: invalid value encountered in double_scalars
      np.sum(input * grids[dir].astype(float), labels, index) / normalizer


.. parsed-literal::

    
    
    




.. parsed-literal::

    ('60d5f02f-8ba8-4035-9d74-c37151428675',)




.. image:: geo_e4cv_files/geo_e4cv_42_4.png


chi scan from (400) to (040)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we do this with :math:`\omega=-145.4500` and :math:`2\theta=69.0985`,
this will be a scan between the two orientation reflections.

Use ``%mov`` (IPython *magic* command) to move both motors at the same
time.

.. code:: ipython3

    print("possible modes:", fourc.calc.engine.modes)
    print("chosen mode:", fourc.calc.engine.mode)
    
    # same as orientation reflections
    %mov fourc.omega -145.4500 fourc.tth 69.0985
    
    RE(bp.scan([fourc], fourc.chi, 0, 90, 10))


.. parsed-literal::

    possible modes: ['bissector', 'constant_omega', 'constant_chi', 'constant_phi', 'double_diffraction', 'psi_constant']
    chosen mode: constant_phi
    
    
    Transient Scan ID: 2     Time: 2021-07-19 16:02:13
    Persistent Unique Scan ID: 'db8f0264-bb9d-49eb-9aae-0e90a5e42001'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+------------+-------------+------------+------------+
    |   seq_num |       time |  fourc_chi |    fourc_h |    fourc_k |    fourc_l | fourc_omega |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+------------+-------------+------------+------------+
    |         1 | 16:02:13.4 |      0.000 |      4.000 |      0.000 |      0.000 |    -145.450 |      0.000 |     69.099 |
    |         2 | 16:02:13.9 |     10.000 |      3.939 |      0.695 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         3 | 16:02:14.6 |     20.000 |      3.759 |      1.368 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         4 | 16:02:15.3 |     30.000 |      3.464 |      2.000 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         5 | 16:02:15.9 |     40.000 |      3.064 |      2.571 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         6 | 16:02:16.4 |     50.000 |      2.571 |      3.064 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         7 | 16:02:17.0 |     60.000 |      2.000 |      3.464 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         8 | 16:02:17.5 |     70.000 |      1.368 |      3.759 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |         9 | 16:02:18.0 |     80.000 |      0.695 |      3.939 |     -0.000 |    -145.450 |      0.000 |     69.099 |
    |        10 | 16:02:18.5 |     90.000 |      0.000 |      4.000 |      0.000 |    -145.450 |      0.000 |     69.099 |
    +-----------+------------+------------+------------+------------+------------+-------------+------------+------------+
    generator scan ['db8f0264'] (scan num: 2)
    
    
    




.. parsed-literal::

    ('db8f0264-bb9d-49eb-9aae-0e90a5e42001',)




.. image:: geo_e4cv_files/geo_e4cv_44_2.png


(*0k0*) scan near (040)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    RE(bp.scan([fourc], fourc.k, 3.9, 4.1, 5))


.. parsed-literal::

    
    
    Transient Scan ID: 3     Time: 2021-07-19 16:02:20
    Persistent Unique Scan ID: '90e9bb44-1528-4554-8aab-af4e3e47e678'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |   seq_num |       time |    fourc_k |    fourc_h |    fourc_l | fourc_omega |  fourc_chi |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |         1 | 16:02:20.3 |      3.900 |      4.100 |     -0.000 |    -126.652 |     43.568 |      0.000 |    106.695 |
    |         2 | 16:02:20.8 |      3.950 |      4.100 |     -0.000 |    -126.179 |     43.933 |      0.000 |    107.641 |
    |         3 | 16:02:21.4 |      4.000 |      4.100 |     -0.000 |    -125.697 |     44.293 |      0.000 |    108.604 |
    |         4 | 16:02:21.9 |      4.050 |      4.100 |     -0.000 |    -125.206 |     44.648 |      0.000 |    109.585 |
    |         5 | 16:02:22.5 |      4.100 |      4.100 |     -0.000 |    -124.707 |     45.000 |      0.000 |    110.585 |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    generator scan ['90e9bb44'] (scan num: 3)
    
    
    




.. parsed-literal::

    ('90e9bb44-1528-4554-8aab-af4e3e47e678',)




.. image:: geo_e4cv_files/geo_e4cv_46_2.png


(*hk0*) scan near (440)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    RE(bp.scan([fourc], fourc.h, 3.9, 4.1, fourc.k, 3.9, 4.1, 5))


.. parsed-literal::

    
    
    Transient Scan ID: 4     Time: 2021-07-19 16:02:24
    Persistent Unique Scan ID: '289b70e8-2da2-47dc-a795-99237a567fcf'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |   seq_num |       time |    fourc_h |    fourc_k |    fourc_l | fourc_omega |  fourc_chi |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |         1 | 16:02:24.2 |      3.900 |      3.900 |      0.000 |    -128.558 |     45.000 |      0.000 |    102.882 |
    |         2 | 16:02:24.6 |      3.950 |      3.950 |      0.000 |    -127.627 |     45.000 |      0.000 |    104.744 |
    |         3 | 16:02:25.0 |      4.000 |      4.000 |     -0.000 |    -126.676 |     45.000 |      0.000 |    106.647 |
    |         4 | 16:02:25.4 |      4.050 |      4.050 |     -0.000 |    -125.703 |     45.000 |      0.000 |    108.592 |
    |         5 | 16:02:25.8 |      4.100 |      4.100 |      0.000 |    -124.707 |     45.000 |      0.000 |    110.585 |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    generator scan ['289b70e8'] (scan num: 4)
    
    
    




.. parsed-literal::

    ('289b70e8-2da2-47dc-a795-99237a567fcf',)




.. image:: geo_e4cv_files/geo_e4cv_48_2.png


Move to the (*440*) reflection.

.. code:: ipython3

    fourc.move((4,4,0))
    print(f"{fourc.position = }")


.. parsed-literal::

    fourc.position = FourCirclePseudoPos(h=4.0, k=4.000000000000001, l=-1.1471889002931275e-15)


Repeat the same scan about the (*440*) but use *relative* positions.

.. code:: ipython3

    RE(bp.rel_scan([fourc], fourc.h, -0.1, 0.1, fourc.k, -0.1, 0.1, 5))


.. parsed-literal::

    
    
    Transient Scan ID: 5     Time: 2021-07-19 16:02:27
    Persistent Unique Scan ID: '197bb65c-e257-4aa3-a002-358fa4089834'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |   seq_num |       time |    fourc_h |    fourc_k |    fourc_l | fourc_omega |  fourc_chi |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |         1 | 16:02:27.1 |      3.900 |      3.900 |      0.000 |    -128.558 |     45.000 |      0.000 |    102.882 |
    |         2 | 16:02:27.5 |      3.950 |      3.950 |      0.000 |    -127.627 |     45.000 |      0.000 |    104.744 |
    |         3 | 16:02:27.9 |      4.000 |      4.000 |     -0.000 |    -126.676 |     45.000 |      0.000 |    106.647 |
    |         4 | 16:02:28.3 |      4.050 |      4.050 |     -0.000 |    -125.703 |     45.000 |      0.000 |    108.592 |
    |         5 | 16:02:28.7 |      4.100 |      4.100 |     -0.000 |    -124.707 |     45.000 |      0.000 |    110.585 |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    generator rel_scan ['197bb65c'] (scan num: 5)
    
    
    




.. parsed-literal::

    ('197bb65c-e257-4aa3-a002-358fa4089834',)




.. image:: geo_e4cv_files/geo_e4cv_52_2.png

