# pyacptrak

## What is it?

**pyacptrak** helps you to create ACOPOStrak resources for projects, training, meetings, mappView widgets, etc... It is a powerful tool when used together with Jupyter-Lab (Or Jupyter Notes) but could be used as stand alone module.

[![PyPI Latest Release](https://img.shields.io/pypi/v/pyacptrak)](https://pypi.org/project/pyacptrak/)
[![PyPI License](https://img.shields.io/pypi/l/pyacptrak)](https://github.com/HeytalePazguato/pyacptrak/blob/master/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/pyacptrak)](https://www.python.org/downloads/)
[![Twitter](https://img.shields.io/twitter/follow/HeytalePazguato?style=social)](https://twitter.com/intent/follow?original_referer=https%3A%2F%2Fpublish.twitter.com%2F&ref_src=twsrc%5Etfw%7Ctwcamp%5Ebuttonembed%7Ctwterm%5Efollow%7Ctwgr%5EHeytalePazguato&region=follow_link&screen_name=HeytalePazguato)

## Install

To install pyacptrak, run the following command:

```
pip install pyacptrak
```

## Install with development dependencies

To install pyacptrak, along with the tools you need to develop and run tests, run the following command:

```
pip install pyacptrak[dev]
```

## Main Features

### Work with segments (Segment class)

The library support the 4 type of segments ('AA', 'AB', 'BA' and 'BB').

Obtain segment information:

```
import pyacptrak as at

print(at.Segment('aa').info())
```

Output:
```
{'length': 660,
 'type': '8F1I01.AA66.xxxx-1',
 'description': 'ACOPOStrak straight segment'}
```
Plot segment:
```
import pyacptrak as at

at.Segment('aa').plot()
```
![image](https://user-images.githubusercontent.com/101816677/158948767-9d10a414-21d3-42b3-ab1c-e54eace0c39f.png)

The plot function supports rotation in degrees:
```
import pyacptrak as at

at.Segment('ab').plot(-45)
```
![image](https://user-images.githubusercontent.com/101816677/158949082-e38760c1-25fe-425e-b56e-ef96c223fbc2.png)

### Work with tracks (Track class)

The library has 5 types of pre-built tracks (TRACK0, TRACK45, TRACK90, TRACK135 and TRACK180).

```
import pyacptrak as at

at.TRACK135.plot()
```
![image](https://user-images.githubusercontent.com/101816677/158949482-f06e91bc-f8b9-4e11-b0fc-a7fe1149a15e.png)

But you could also build your own tracks using individual segments.

```
import pyacptrak as at
track1 = (at.Segment('aa') * 2) + at.Segment('ab') + (at.Segment('bb') * 2) + at.Segment('ba')
track1.plot()
```
![image](https://user-images.githubusercontent.com/101816677/158949973-eea998ae-32fc-491f-955c-c5fbef496978.png)

Or using the pre-configured tracks (This makes it easier).

```
import pyacptrak as at
track1 = (at.TRACK0 * 2) + at.TRACK135
track1.plot()
```
![image](https://user-images.githubusercontent.com/101816677/158949973-eea998ae-32fc-491f-955c-c5fbef496978.png)

The plot function supports rotation for tracks:

```
import pyacptrak as at
track1 = (at.TRACK0 * 2) + at.TRACK135
track1.plot(15)
```
![image](https://user-images.githubusercontent.com/101816677/158950300-9ffa4009-c5fe-4402-8284-003a8c8d5a1f.png)

The arguments `seg_prefix` (Default value "gSeg_") and `seg_offset` (default value "1") are available from v0.0.5 to configure the segment variable names

### Work with loops (Loop class)

The library supports working with loops, the arguments for the loop are width and height, the unit is considering the 660mm grid so a `loop(2,1)` would draw the smallest possible loop (If no arguments are passed it will consider w=2, h=1).

```
import pyacptrak as at
at.Loop(2,1).plot()
```
![image](https://user-images.githubusercontent.com/101816677/158950730-1c74eb26-49b6-483a-b807-2f9887d9b7d8.png)

For loops wider than 1 it uses 90° tracks instead of 180°

```
import pyacptrak as at
at.Loop(3,2).plot()
```
![image](https://user-images.githubusercontent.com/101816677/158950937-3a69abb0-5b25-4b3a-9b56-447b6b741304.png)

The plot function also support rotation for loops

```
import pyacptrak as at
at.Loop(3,2).plot(190)
```
![image](https://user-images.githubusercontent.com/101816677/158951085-4ce1008d-aa84-4158-98d0-e83406bb5326.png)

### Save the SVG files

It is possible to save the SVG file of any of the classes by chaining the method `save()`.

The `save()` accepts one argument to define the name of the output file, if no name is passed, the default filename will be the class name.

```
import pyacptrak as at
at.Loop(3,2).plot(190).save()
```

Output: Saves a "Loop.svg" file

### Configure shuttle type and controller settings

It is possible to configure the shuttle type by using the size (50mm , 100mm, 244mm), selecting if it is one or two sided magnet (For diverter) and the magnet type (Straight, skewed) by using the `PARAM` class

```
at.PARAM.shuttle.size = 100                 # 50, 100, 244
at.PARAM.shuttle.magnet_plate = 1           # 1 = Non diverter, 2 = Diverter
at.PARAM.shuttle.magnet_type = 'Straight'   # Straight, Skewed
```

It is possible to configure the default control parameters, the PID values will be calculated automatically depending the configured shuttle and the controller type (Soft, medium, hard).

```
at.PARAM.segment.controller = 'Hard'        # soft, medium, hard
```

When any of these parameters changes, the user will be notified if the control parameters and/or the shuttle type have been updated

```
The control parameters have been updated
The shuttle model and dimensions have been updated: 8F1SA.203.xxxxxx-x
```

The complete `PARAM` class is shown below:

```
<class 'pyacptrak.pyacptrak._param'>
    segment = <class 'pyacptrak.pyacptrak._segment'>
        control_par = <class 'pyacptrak.pyacptrak._control_par'>
            ff_force_neg = 2.0
            ff_force_pos = 2.0
            ff_speed_force_factor = 2.0
            ff_total_mass = 0.8
            pos_proportional_gain = 300
            speed_proportional_gain = 180
        elongation = Inactive
        simulation = Off
        speed_filter = Not Used
        stop_reaction = Induction Halt
    shuttle = <class 'pyacptrak.pyacptrak._shuttle'>
        auto_dimensions = True
        collision_distance = 0.002
        collision_strategy = Constant
        convoy = Inactive
        count = 10
        error_stop = 0.006
        extent_back = 0.05
        extent_front = 0.05
        model = 8F1SA.203.xxxxxx-x
        stereotype = ShuttleStereotype_1
        stereotype_par = <class 'pyacptrak.pyacptrak._sh_stereotype_par'>
            acceleration = 50.0
            deceleration = 50.0
            jerk = 0.02
            recontrol = Active
            user_data = 0
            velocity = 4.0
        width = 0.03
    visu = <class 'pyacptrak.pyacptrak._visu'>
        task = 4
```

### Work with assemblies (Assembly class)

The library supports working with assemblies, the arguments for the assembly are a list of Track elements and a name (By default "gAssembly_1") which will be used for the exported files

```
import pyacptrak as at
asm1 = at.Assembly([at.Loop(3,1), at.Loop()])
```

It is possible to plot each track of the assembly by accessing the track index:

```
asm1.track[0].plot()
```

![image](https://user-images.githubusercontent.com/101816677/173235687-9875f2f7-02fc-4baf-88d3-8c51a142a0c0.png)

```
asm1.track[1].plot()
```

![image](https://user-images.githubusercontent.com/101816677/173235711-c0866d72-0b7e-4fcf-baa9-c8011e4269fa.png)

It is also possible to access all track methods from each Track element within the assembly class.

The arguments `seg_prefix` (Default value "gSeg_") and `seg_offset` (default value "1") are available from v0.0.5 to configure the segment variable names. When each track has different `seg_prefix` name the offset will reset by default (This behavior could be overriden by passing a value in the `seg_offset` argument):

```
import pyacptrak as at
l1 = at.Loop(3,1, seg_prefix='gLoop1_')
l2 = at.Loop(seg_prefix='gLoop2_')
asm = at.Assembly([l1,l2])
print(asm.track[0].info())
```

This will print all the information of the track:

```
{'seg_prefix': 'gLoop1_',
 'seg_offset': 1,
 'length': 4560,
 'segment': [{'name': 'gLoop1_001',
   'length': 450,
   'type': '8F1I01.AB2B.xxxx-1',
   'description': 'ACOPOStrak curve segment A'},
  {'name': 'gLoop1_002',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_003',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_004',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_005',
   'length': 450,
   'type': '8F1I01.BA2B.xxxx-1',
   'description': 'ACOPOStrak curve segment B'},
  {'name': 'gLoop1_006',
   'length': 660,
   'type': '8F1I01.AA66.xxxx-1',
   'description': 'ACOPOStrak straight segment'},
  {'name': 'gLoop1_007',
   'length': 450,
   'type': '8F1I01.AB2B.xxxx-1',
   'description': 'ACOPOStrak curve segment A'},
  {'name': 'gLoop1_008',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_009',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_010',
   'length': 240,
   'type': '8F1I01.BB4B.xxxx-1',
   'description': 'ACOPOStrak circular arc segment'},
  {'name': 'gLoop1_011',
   'length': 450,
   'type': '8F1I01.BA2B.xxxx-1',
   'description': 'ACOPOStrak curve segment B'},
  {'name': 'gLoop1_012',
   'length': 660,
   'type': '8F1I01.AA66.xxxx-1',
   'description': 'ACOPOStrak straight segment'}]}
```

Or could show the compacted version by passing the `compact` optional argument:

```
import pyacptrak as at
l1 = at.Loop(3,1, seg_prefix='gLoop1_')
l2 = at.Loop(seg_prefix='gLoop2_')
asm = at.Assembly([l1,l2])
asm.track[0].info(compact = True)
```

This will print the main track information and the number of segments in the track:

```
{'seg_prefix': 'gLoop1_',
 'seg_offset': 1,
 'length': 4560,
 'segment': 'The track has 12 segments'}
```

### Configure the plot settings

It is possible to configure the SVG settings (Starting with v0.0.6)

```
import pyacptrak as at

at.Loop(3,1).plot(angle=20, show_id=True, seg_body_fill='#ff8800', seg_border_stroke='#0000ff', seg_id_stroke='#ff0000')
```

![image](https://user-images.githubusercontent.com/101816677/174421293-f234ee90-e321-41f5-95e9-a43d58baa4b4.png)

---
## License

Copyright © Jorge Centeno

Licensed under the [GNU GPLv3 license](LICENSE).

---

## Changes
### v0.0.6 (Latest release)
> #### General changes
> - Change: The library `svgutils` has been removed and replaced with `svgwrite`.
> - Change: The SVG resources installed with `pyacptrak` are now removed.
> - New feature: All SVG images are now generated from scratch, this allows the library to modify the color of the elements and insert text (Like segment ID). This also expands the posibility to implement new features or add elements to the SVG images in future versions.
> - New feature: All `plot()` methods have the following optional arguments to configure the SVG image:
>   - show_id: bool = False: Show or hide the segment id.
>   - seg_body_fill: str = None: Configure the fill color of the segment, accepts a hexadecimal color code. The default value is '#EEEEEE'.
>   - seg_body_stroke: str = None: Configure the stroke (Edge) color of the segment body, acceptas a hexadecimal color code. The default value is '#A9A9A9'.
>   - seg_border_stroke: str = None: Configure the stroke color of the segment border (The work area), accepts a hexadecimal color code. The default value is '#FF8800'.
>   - seg_dir_fill: str = None: Configure the fill color of the arrow that represents the segment encoder direction, accepts a hexadecimal color code. The default value is '#CCCCCC'.
>   - seg_dir_stroke: str = None: Configure the stroke (Edge) color of the segment direction arrow, accepts a hexadecimal color code. The default value is '#CCCCCC'.
>   - seg_id_fill: str = None: Configure the fill color of the segment ID text, accepts a hexadecimal color code. The default value is '#BBBBBB'.
>   - seg_id_stroke: str = None: Configure the stroke (Edge) color of the segment id, accepts a hexadecimal color code. The default value is '#BBBBBB'.
>   - seg_id_stroke_width: float = None: Configure the width of the segment id stroke. The default value is '0.15'

### v0.0.5
> #### General changes:
> - Bug fix: Removed unecessary packages from `install_requires`. The combination some module versions generated the following error when `pyacptrak` was installed in Python 3.9:
>```
> × python setup.py egg_info did not run successfully.
> │ exit code: 1
> ╰─> [1 lines of output]
>       ERROR: Can not execute `setup.py` since setuptools is not available in the build environment.
>       [end of output]
>```
> - New feature: When the shuttle type and/or the controller configuration changes via the `PARAM` class, the PID controller parameters will be automatically calculated based on the recomended values from Automation Help.
> - New feature: The `info()` method of the Track, Loop and Assembly classes may now receive an optional argument `compact` (The default value is False).

> #### Assembly class:
> - New feature: the export method is available, it will automatically create the assembly configuration file `AsmCfg.assembly` and the shuttle stereotype file `ShCfg.shuttlestereotype`. Both files will be generated in the same folder where the python program is running and could be imported (Or copy/pasted) into the Automation Studio project.
> - New feature: The `name` argument is available to configure a name for the assembly, the default value is "gAssembly_1".

> #### Track class:
> - New feature: The `seg_prefix` argument is available to configure a prefix for the segment variable names, the default value is "gSeg_".
> - New feature: The `seg_offset` argument is available to configure an offset for the segment variable names, the default value is "1".

### v0.0.4
> #### General changes:
> - Bug fix: As a result of moving the "img" folder location in v0.0.3 the SVG images were not installed with the package, now this works correctly and the images are installed together with the package.

### v0.0.3
> #### General changes:
> - License changed from MIT to GNU GPLv3.
> - Added TypeError for addition and multiplication operators.
> - Added `typeguard` and `typing` packages to typecheck the methods.
> - Added `xmltodict` package to create the xml configuration files for the AS project.
> - Added `PARAM` variable to configure the exported files.
> - Reduced the size of SVG files.

> #### Segment class:
> - Change: Removed the `info` attribute.
> - New feature: The `info()` method was added to get the segment information.
> - Bug fix: Multiplying a segment object by an integer "n" would create a Track class object with "n" segments all pointing to the same segment object.

> #### Track class:
> - New feature: The `seg_prefix` argument (Optional) was added to the `Track` class to create the segment variable. The default value is "gSeg_".
> - New feature: The `seg_offset` argument (Optional) was added to the `Track` class to configure an offset for the segment variable. The default value is "1".
> - New feature: The `info()` method was added to get the track information.
> - Bug fix: Adding or multiplying Track objects would create a Track class object with elements pointing to the same segment objects.

> #### Loop class:
> - New feature: Added addition and multiplication operators, the result will return an `Assembly` object.
> - Bug fix: The inherited `length()` method didn't work because the `Loop` class had a `length` attribute that was overwritting the method `length()` of the parent class `Track`.

> #### Assembly class:
> - New feature: Class added to the package.
> - New feature: The `export()` method was added.
>   - The assembly configuration file (AsmCfg.assembly) will be generated.
>   - The shuttle stereotype file (ShCfg.shuttlestereotype) will be generated.