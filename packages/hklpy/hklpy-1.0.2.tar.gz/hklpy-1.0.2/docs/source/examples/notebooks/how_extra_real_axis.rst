How to add extra motors to a diffractometer class
=================================================

Sometimes, it is desired to add additional motor(s) (or other
components) to a subclass of
`hkl.diffract.Diffractometer() <https://blueskyproject.io/hklpy/diffract.html#hkl.diffract.Diffractometer>`__.

**Objective**

Add one or more real positioners to the standard positioners of the
4-circle diffractometer (E4CV geometry). Use simulated motors for the
example (no EPICS required).

Imports
-------

Since the *hklpy* package is a thin interface to the *hkl* library
(compiled C++ code), we need to **first** load the
*gobject-introspection* package (``gi``, by name) and name our required
code and version.

This is needed *every* time before the *hkl* package is first imported.

.. code:: ipython3

    import gi
    gi.require_version('Hkl', '5.0')

Import the additional ophyd and hklpy needed for the example.

Standard 4-circle
-----------------

First, we start with the setup of a `4-circle
diffractometer <https://blueskyproject.io/hklpy/examples/notebooks/geo_e4cv.html#define-this-diffractometer>`__
(E4CV is the name of the geometry). The `E4CV
geometry <https://blueskyproject.io/hklpy/geometry_tables.html#geometries-indexed-by-number-of-circles>`__
requires these real positioners for the diffractometer circles:
``omega``, ``chi``, ``phi``, and ``tth``. For simulated axes without
using EPICS, we use the
`ophyd.SoftPositioner <https://blueskyproject.io/ophyd/positioners.html#softpositioner>`__.
We’ll use the (default) `hkl calculation
engine <https://blueskyproject.io/hklpy/geometry_tables.html#e4cv-table>`__
which requires pseudo-positioners ``h``, ``k``, and ``l``. These
pseudo-positioners are provided by the ``hkl.geometries.SimMixin``
class.

.. code:: ipython3

    from hkl import E4CV, SimMixin
    from ophyd import SoftPositioner
    from ophyd import Component
    
    class FourCircle(SimMixin, E4CV):
        """
        Our 4-circle.  Eulerian, vertical scattering orientation.
        """
        # the reciprocal axes are defined by SimMixin
    
        omega = Component(SoftPositioner, kind="hinted", limits=(-180, 180), init_pos=0)
        chi = Component(SoftPositioner, kind="hinted", limits=(-180, 180), init_pos=0)
        phi = Component(SoftPositioner, kind="hinted", limits=(-180, 180), init_pos=0)
        tth = Component(SoftPositioner, kind="hinted", limits=(-180, 180), init_pos=0)

Then, create the diffractometer object.

.. code:: ipython3

    fourc = FourCircle("", name="fourc")
    print(f"{fourc = }")


.. parsed-literal::

    fourc = FourCircle(prefix='', name='fourc', settle_time=0.0, timeout=None, egu='', limits=(0, 0), source='computed', read_attrs=['h', 'h.readback', 'h.setpoint', 'k', 'k.readback', 'k.setpoint', 'l', 'l.readback', 'l.setpoint', 'omega', 'chi', 'phi', 'tth'], configuration_attrs=['energy', 'energy_units', 'energy_offset', 'geometry_name', 'class_name', 'sample_name', 'lattice', 'lattice_reciprocal', 'U', 'UB', 'reflections_details', 'ux', 'uy', 'uz', 'diffractometer_name', '_hklpy_version', '_pseudos', '_reals', '_constraints', '_mode', 'orientation_attrs', 'h', 'k', 'l'], concurrent=True)


Show the configuration of this diffractometer.

.. code:: ipython3

    fourc.wh()


.. parsed-literal::

    ===================== ========= =========
    term                  value     axis_type
    ===================== ========= =========
    diffractometer        fourc              
    sample name           main               
    energy (keV)          8.05092            
    wavelength (angstrom) 1.54000            
    calc engine           hkl                
    mode                  bissector          
    h                     0.0       pseudo   
    k                     0.0       pseudo   
    l                     0.0       pseudo   
    omega                 0         real     
    chi                   0         real     
    phi                   0         real     
    tth                   0         real     
    ===================== ========= =========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f2c26669910>



Add additional positioner
-------------------------

We can use the ``FourCircle()`` class, defined above, as the base class
when we add a positioner.

First, subclass ``FourCircle``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let’s start by first creating and testing the subclass without an extra
positioner.

.. code:: ipython3

    class EnhancedFourCircle(FourCircle):
        pass
    
    e4c = EnhancedFourCircle("", name="e4c")
    e4c.wh()


.. parsed-literal::

    ===================== ========= =========
    term                  value     axis_type
    ===================== ========= =========
    diffractometer        e4c                
    sample name           main               
    energy (keV)          8.05092            
    wavelength (angstrom) 1.54000            
    calc engine           hkl                
    mode                  bissector          
    h                     0.0       pseudo   
    k                     0.0       pseudo   
    l                     0.0       pseudo   
    omega                 0         real     
    chi                   0         real     
    phi                   0         real     
    tth                   0         real     
    ===================== ========= =========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f2c6bd27190>



Compare these tables for the ``fourc`` and ``e4c``, they are identical
except for the name difference.

Customize the subclass
~~~~~~~~~~~~~~~~~~~~~~

Following a pattern, we simply add a *spinner* motor to the class and
create a new diffractometer object. Our simulated *spinner* will use
``rotations`` as units and we’ll set it up to allow +/- 10,000
rotations. We’ll show you the first attempt (but **do NOT execute this
code** for reasons explained below):

.. code:: python

   class EnhancedFourCircle(FourCircle):
       spinner = Component(SoftPositioner, kind="hinted", limits=(-10000, 10000), egu="rotations", init_pos=0)

   e4c = EnhancedFourCircle("", name="e4c")
   e4c.wh()

But, if you actually execute this code, you crash the Python kernel
directly with no ability to interrupt that failure. (So we only *show*
you this code and do not provide it in an executable notebook cell.)

**Q**: What goes wrong? **A**: The ``Diffractometer`` class is a
subclass of the
`ophyd.PseudoPositioner <https://blueskyproject.io/ophyd/positioners.html?highlight=pseudopositioner#pseudopositioner>`__.
The PseudoPositioner maintains the transforms between the *real* axes
and the *pseudo* axes through ``.forward()`` and ``.inverse()``
transformation methods. These two methods expect a fixed set of axis
names, yet the new ``spinner`` Component has been added to the list of
real axes. This extra real axis cause the failure observed. That error
*would* get caught by Python under other circumstances. Since
``Diffractometer.forward()`` and ``Diffractometer.inverse()`` call the
underlying *libhkl* code with the full list of real positioners, and
that code does not handle this error gracefully, so the entire Python
process crashes out, without further diagnostic.

**Q**: How *should* it be done so Python does not crash? **A**: The
``PseudoPositioner`` has a feature for exactly this case: ``._real`` is
a list of the names of the Components that are needed specifically by
``.forward()`` and ``.inverse()``. (In our 4-circle example, this would
be ``_real = ["omega", "chi", "phi", "tth"]``) If we define this list in
our subclass, *then* we can add as many *real* components as we wish.

.. code:: ipython3

    class EnhancedFourCircle(FourCircle):
        _real = ["omega", "chi", "phi", "tth"]
        spinner = Component(SoftPositioner, kind="hinted", limits=(-10000, 10000), egu="rotations", init_pos=0)
    
    e4c = EnhancedFourCircle("", name="e4c")
    e4c.wh()


.. parsed-literal::

    ===================== ========= ==========
    term                  value     axis_type 
    ===================== ========= ==========
    diffractometer        e4c                 
    sample name           main                
    energy (keV)          8.05092             
    wavelength (angstrom) 1.54000             
    calc engine           hkl                 
    mode                  bissector           
    h                     0.0       pseudo    
    k                     0.0       pseudo    
    l                     0.0       pseudo    
    omega                 0         real      
    chi                   0         real      
    phi                   0         real      
    tth                   0         real      
    spinner               0         additional
    ===================== ========= ==========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f2c2562c5b0>



Show that we can still use both ``.forward()`` and ``.inverse()``
methods.

.. code:: ipython3

    print(f"{fourc.forward(1, 1, 0) = }")
    print(f"{fourc.inverse((30, 0, 0, 60)) = }")


.. parsed-literal::

    fourc.forward(1, 1, 0) = PosCalcE4CV(omega=44.99999999999999, chi=45.00000000000001, phi=89.99999999999999, tth=89.99999999999999)
    fourc.inverse((30, 0, 0, 60)) = FourCirclePseudoPos(h=-1.0461952917773851e-16, k=6.123233995736767e-17, l=1.0)


Can we add other pseudo axes?
-----------------------------

**Q**: With this capability to add additional Components as real
positioners, can we add axes to the pseudo positioners?

**A**: Unfortunately,
`no <https://github.com/bluesky/ophyd/issues/924#issuecomment-718177332>`__.
That capability is not built into the ophyd PseudoPositioner at this
time.

Add additional Signals and Devices
----------------------------------

Finally, we add additional Signals and Devices as Components as a
demonstration.

.. code:: ipython3

    from ophyd import Signal, Device
    from ophyd.signal import SignalRO
    
    class XYStage(Device):
        x = Component(SoftPositioner, kind="hinted", limits=(-20, 105), init_pos=0)
        y = Component(SoftPositioner, kind="hinted", limits=(-20, 105), init_pos=0)
        solenoid_lock = Component(Signal, value=True)
    
    class EnhancedFourCircle(FourCircle):
        _real = ["omega", "chi", "phi", "tth"]
        spinner = Component(SoftPositioner, kind="hinted", limits=(-10000, 10000), egu="rotations", init_pos=0)
        some_signal = Component(Signal, value=0)
        other_signal = Component(SignalRO, value=0)
        xy = Component(XYStage)
    
    e4c = EnhancedFourCircle("", name="e4c")
    e4c.wh()


.. parsed-literal::

    ===================== ========= ==========
    term                  value     axis_type 
    ===================== ========= ==========
    diffractometer        e4c                 
    sample name           main                
    energy (keV)          8.05092             
    wavelength (angstrom) 1.54000             
    calc engine           hkl                 
    mode                  bissector           
    h                     0.0       pseudo    
    k                     0.0       pseudo    
    l                     0.0       pseudo    
    omega                 0         real      
    chi                   0         real      
    phi                   0         real      
    tth                   0         real      
    spinner               0         additional
    ===================== ========= ==========
    




.. parsed-literal::

    <pyRestTable.rest_table.Table at 0x7f2c255e21f0>



Challenges
----------

1. Use ``EpicsMotor`` instead of ``SoftPositioner`` (and connect with
   PVs of your EPICS system.)
2. Use ``EpicsSignal`` instead of ``Signal``
3. Use ``EpicsSignalRO`` instead of ``SignalRO``
