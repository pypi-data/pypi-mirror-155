WIP: save reflection information in stream
==========================================

See: https://github.com/bluesky/hklpy/issues/158

.. code:: ipython3

    import gi
    gi.require_version('Hkl', '5.0')
    
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    import bluesky.plans as bp
    import bluesky.plan_stubs as bps
    import bluesky.preprocessors as bpp
    import databroker
    import hkl
    from hkl import *  # TODO: wildcard import, yikes!
    import numpy as np
    import pyRestTable
    from ophyd import Component, Device, EpicsSignal, Signal
    from ophyd.signal import AttributeSignal, ArrayAttributeSignal
    from ophyd.sim import *
    import pandas as pd
    
    bec = BestEffortCallback()
    bec.disable_plots()
    cat = databroker.temp().v2
    
    RE = RunEngine({})
    RE.subscribe(bec)
    RE.subscribe(cat.v1.insert)
    RE.md["notebook"] = "tst_UB_in_stream"
    RE.md["objective"] = "Demonstrate UB matrix save & restore in stream of bluesky run"

.. code:: ipython3

    from collections import namedtuple
    
    Lattice = namedtuple("LatticeTuple", "a b c alpha beta gamma")
    Position = namedtuple("PositionTuple", "omega chi phi tth")
    Reflection = namedtuple("ReflectionTuple", "h k l position")
    
    class Holder:
        samples = {}
    
    class Reflections:
        reflections = []
    
    class MyDevice(Device):
        uptime = Component(EpicsSignal, "gp:UPTIME", kind="normal")
        apple = Component(Signal, value="Fuji", kind="omitted")
        orange = Component(Signal, value="Valencia", kind="omitted")
        octopus = Component(Signal, value="spotted", kind="omitted")
    
        stream_name = Component(AttributeSignal, attr="_stream_name", doc="stream name", kind="omitted")
        stream_attrs = Component(AttributeSignal, attr="_stream_attrs", doc="attributes in stream", kind="omitted")
    
        _samples = {}
        _stream_name = "bozo"
        # _stream_attrs = "orange octopus samples stream_name stream_attrs".split()
        _stream_attrs = "orange octopus stream_name stream_attrs".split()
    
        # cannot make AttributeSignal from these that can be written by bluesky
        paddle = Holder()
        spots = Reflections()
    
        def other_streams(self, label=None):
            label = label or self._stream_name
            yield from bps.create(name=label)
            for attr in self._stream_attrs:
                yield from bps.read(getattr(self, attr))
            yield from bps.save()
    
            yield from bps.create("fruit")
            yield from bps.read(self.apple)
            yield from bps.read(self.orange)
            yield from bps.save()
    
            yield from bps.create("animal")
            yield from bps.read(self.octopus)
            yield from bps.save()
    
    
    nitwit = MyDevice("", name="nitwit")
    nitwit.paddle.samples["main"] = Lattice(1,1,1,30,60,90)
    nitwit.paddle.samples["second"] = Lattice(2,2,2, 2,2,2)
    
    def try_it():
        yield from bps.open_run()
    
        yield from bps.create()
        yield from bps.read(nitwit)
        yield from bps.save()
    
        yield from nitwit.other_streams()
    
        yield from bps.close_run()

.. code:: ipython3

    nitwit.wait_for_connection()
    nitwit.read()




.. parsed-literal::

    OrderedDict([('nitwit_uptime',
                  {'value': '11 days, 23:18:03', 'timestamp': 1624045412.918992})])



.. code:: ipython3

    # RE(bp.count([nitwit]))
    RE(try_it())


.. parsed-literal::

    
    
    Transient Scan ID: 1     Time: 2021-06-18 14:43:33
    Persistent Unique Scan ID: '21cbae5c-f852-4e22-87d8-d415062ffbcf'
    New stream: 'primary'
    +-----------+------------+
    |   seq_num |       time |
    +-----------+------------+
    |         1 | 14:43:33.8 |
    New stream: 'bozo'
    New stream: 'fruit'
    New stream: 'animal'
    +-----------+------------+
    generator try_it ['21cbae5c'] (scan num: 1)
    
    
    




.. parsed-literal::

    ('21cbae5c-f852-4e22-87d8-d415062ffbcf',)



.. code:: ipython3

    cat[-1]




.. parsed-literal::

    BlueskyRun
      uid='21cbae5c-f852-4e22-87d8-d415062ffbcf'
      exit_status='success'
      2021-06-18 14:43:33.835 -- 2021-06-18 14:43:33.880
      Streams:
        * bozo
        * animal
        * fruit
        * primary




.. code:: ipython3

    run = cat[-1]
    for stream in list(run):
        print(f"{stream = }")
        print(getattr(run, stream).read())


.. parsed-literal::

    stream = 'bozo'
    <xarray.Dataset>
    Dimensions:              (dim_0: 4, time: 1)
    Coordinates:
      * time                 (time) float64 1.624e+09
    Dimensions without coordinates: dim_0
    Data variables:
        nitwit_stream_attrs  (time, dim_0) <U12 'orange' ... 'stream_attrs'
        nitwit_orange        (time) <U8 'Valencia'
        nitwit_octopus       (time) <U7 'spotted'
        nitwit_stream_name   (time) <U4 'bozo'
    stream = 'animal'
    <xarray.Dataset>
    Dimensions:         (time: 1)
    Coordinates:
      * time            (time) float64 1.624e+09
    Data variables:
        nitwit_octopus  (time) <U7 'spotted'
    stream = 'fruit'
    <xarray.Dataset>
    Dimensions:        (time: 1)
    Coordinates:
      * time           (time) float64 1.624e+09
    Data variables:
        nitwit_orange  (time) <U8 'Valencia'
        nitwit_apple   (time) <U4 'Fuji'
    stream = 'primary'
    <xarray.Dataset>
    Dimensions:        (time: 1)
    Coordinates:
      * time           (time) float64 1.624e+09
    Data variables:
        nitwit_uptime  (time) <U17 '11 days, 23:18:03'


.. code:: ipython3

    nitwit.paddle.samples["main"][:]




.. parsed-literal::

    (1, 1, 1, 30, 60, 90)



.. code:: ipython3

    nitwit.octopus.read()




.. parsed-literal::

    {'nitwit_octopus': {'value': 'spotted', 'timestamp': 1624045413.7587433}}



.. code:: ipython3

    for k, v in nitwit.paddle.samples.items():
        print(f"{k = }")
        print(f"{v[:] = }")


.. parsed-literal::

    k = 'main'
    v[:] = (1, 1, 1, 30, 60, 90)
    k = 'second'
    v[:] = (2, 2, 2, 2, 2, 2)


.. code:: ipython3

    sig = Signal(name="sig", value=dict(main=nitwit.paddle.samples["main"]._asdict()))
    print(f"{sig.read() = }")
    print(f"{nitwit.paddle.samples['main'] = }")


.. parsed-literal::

    sig.read() = {'sig': {'value': {'main': {'a': 1, 'b': 1, 'c': 1, 'alpha': 30, 'beta': 60, 'gamma': 90}}, 'timestamp': 1624045414.1055214}}
    nitwit.paddle.samples['main'] = LatticeTuple(a=1, b=1, c=1, alpha=30, beta=60, gamma=90)


.. code:: ipython3

    r = Reflection(4.0, 0., 0., Position(omega=-145.451, chi=0.0, phi=0.0, tth=69.0966))
    r[-1][:]




.. parsed-literal::

    (-145.451, 0.0, 0.0, 69.0966)



.. code:: ipython3

    def read_soft_signal(key, value):
        yield from bps.read(Signal(name=key, value=value))
    
    def stream_dict(dictionary, label):
        yield from bps.create(label)
        for k, v in dictionary.items():
            yield from read_soft_signal(k, v)
        yield from bps.save()
    
    
    def stream_samples(samples, label="samples"):
        if len(samples):
            yield from bps.create(label)
            for sname, lattice in samples.items():
                yield from read_soft_signal(sname, lattice[:])
            yield from read_soft_signal("_keys", list(lattice._fields))
            yield from bps.save()
        else:
            # because you have to yield _something_
            yield from bps.null()
    
    
    def stream_test(reflections, label="reflections"):
        if len(reflections):
            yield from bps.create(label)
            keys = []
            for i, refl in enumerate(reflections):
                key = f"r{i+1}"
                keys.append(key)
                yield from read_soft_signal(key, (*refl[:3], refl[3][:]))
                yield from read_soft_signal(key+"_hkl", refl[:3])
                yield from read_soft_signal(key+"_axis_values", refl[3])
                yield from read_soft_signal(key+"_wavelength", 2.101)
            yield from read_soft_signal("_keys", keys)
            yield from bps.save()
        else:
            # because you have to yield _something_
            yield from bps.null()
    
    
    def stream_reflections(self, label="reflections"):
        reflections = self.calc.sample._sample.reflections_get()
        if len(reflections):
            yield from bps.create(label)
            orient_refls = self.calc.sample._orientation_reflections
            keys = []
            for i, refl in enumerate(reflections):
                key = f"r{i+1}"
                keys.append(key)
                hkl_tuple = refl.hkl_get()
                geom = refl.geometry_get()
                yield from read_soft_signal(key, (*hkl_tuple[:], geom.axis_values_get(1)))
                yield from read_soft_signal(key+"_hkl", hkl_tuple[:])
                yield from read_soft_signal(key+"_axis_names", geom.axis_names_get(1))
                yield from read_soft_signal(key+"_axis_values", geom.axis_values_get(1))
                yield from read_soft_signal(key+"_wavelength", geom.wavelength_get(1))
                yield from read_soft_signal(key+"_for_calcUB", refl in orient_refls)
                # ignore `flag`, no documentation for it, always 1 (?used by libhkl's GUI?)
            yield from read_soft_signal("_keys", keys)
            yield from bps.save()
        else:
            # because you have to yield _something_
            yield from bps.null()
    
    
    def stream_multi(label="multi"):
        for i in range(3):
            yield from bps.create(label)
            yield from read_soft_signal("a", 1.2345 + i)
            yield from read_soft_signal("b", f"4.{i}56")
            yield from read_soft_signal("arr", [-1, i , 1.1])
            yield from bps.save()
        else:
            # because you have to yield _something_
            yield from bps.null()
    
    
    def streams():
        yield from bps.open_run()
    
        yield from stream_samples(nitwit.paddle.samples)
        # yield from stream_reflections(
        yield from stream_test(
            [
                Reflection(4.0, 0., 0., Position(omega=-145.451, chi=0.0, phi=0.0, tth=69.0966)),
                Reflection(0., 4.0, 0., Position(omega=-145.451, chi=0.0, phi=90.0, tth=69.0966))
            ]
        )
        # yield from stream_multi()
    
        yield from bps.close_run()
    
    
    RE(streams())
    for nm, stream in cat[-1].items():
        print(f"{nm = }")
        print(stream.read())
        print("-"*30)


.. parsed-literal::

    
    
    Transient Scan ID: 2     Time: 2021-06-18 14:43:34
    Persistent Unique Scan ID: 'd6e5b82d-a035-4f47-873b-9ce215e74272'
    New stream: 'samples'
    New stream: 'reflections'
    
    
    
    nm = 'reflections'


.. parsed-literal::

    /home/prjemian/.local/lib/python3.8/site-packages/numpy/core/_asarray.py:102: VisibleDeprecationWarning: Creating an ndarray from ragged nested sequences (which is a list-or-tuple of lists-or-tuples-or ndarrays with different lengths or shapes) is deprecated. If you meant to do this, you must specify 'dtype=object' when creating the ndarray.
      return array(a, dtype, copy=False, order=order)


.. parsed-literal::

    <xarray.Dataset>
    Dimensions:         (dim_0: 3, dim_1: 4, dim_2: 3, dim_3: 2, dim_4: 4, dim_5: 4, dim_6: 4, time: 1)
    Coordinates:
      * time            (time) float64 1.624e+09
    Dimensions without coordinates: dim_0, dim_1, dim_2, dim_3, dim_4, dim_5, dim_6
    Data variables:
        r1_hkl          (time, dim_0) float64 4.0 0.0 0.0
        r1              (time, dim_1) object 4.0 ... [-145.451, 0.0, 0.0, 69.0966]
        r1_wavelength   (time) float64 2.101
        r2_hkl          (time, dim_2) float64 0.0 4.0 0.0
        _keys           (time, dim_3) <U2 'r1' 'r2'
        r1_axis_values  (time, dim_4) float64 -145.5 0.0 0.0 69.1
        r2_axis_values  (time, dim_5) float64 -145.5 0.0 90.0 69.1
        r2_wavelength   (time) float64 2.101
        r2              (time, dim_6) object 0.0 ... [-145.451, 0.0, 90.0, 69.0966]
    ------------------------------
    nm = 'samples'
    <xarray.Dataset>
    Dimensions:  (dim_0: 6, dim_1: 6, dim_2: 6, time: 1)
    Coordinates:
      * time     (time) float64 1.624e+09
    Dimensions without coordinates: dim_0, dim_1, dim_2
    Data variables:
        main     (time, dim_0) int64 1 1 1 30 60 90
        second   (time, dim_1) int64 2 2 2 2 2 2
        _keys    (time, dim_2) <U5 'a' 'b' 'c' 'alpha' 'beta' 'gamma'
    ------------------------------


.. code:: ipython3

    k = "r1"
    r = cat[-1].reflections.read()[k+"_hkl"][0]
    a = cat[-1].reflections.read()[k+"_axis_values"][0]
    (*r.data, a.data)




.. parsed-literal::

    (4.0, 0.0, 0.0, array([-145.451 ,    0.    ,    0.    ,   69.0966]))


