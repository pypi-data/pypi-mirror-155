import svgwrite
import xmltodict
import numpy as np
from svgwrite import mm
from typeguard import typechecked
from IPython.display import display
from importlib.metadata import distribution
from typing import Final, List, Dict, TypeVar, Type, Sequence

version = distribution('pyacptrak').version

_TSegment = TypeVar("_TSegment", bound = "Segment")
_TTrack = TypeVar("_TTrack", bound = "Track")
_TST = TypeVar('_TST', _TSegment, _TTrack)
_TAssembly = TypeVar("_TAssembly", bound = "Assembly")

#@typechecked
#def get_resource(module: str, name: str):
#    return resources.files(module).joinpath(name)

# Define global configuration class
@typechecked
class _Config(object):
    def __init__(self):
        self.gap: float = 0.5
        self.devMode: bool = False
        
    def __str__(self):
        return get_class_elements(self)
    
    @property
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, v: float):
        if not (0 < v <= 2): raise Exception('The value must be between (0, 2]')
        self._gap = v
    
    @property
    def devMode(self):
        return self._devMode

    @devMode.setter
    def devMode(self, v: bool):
        self._devMode = v

# define global configuration variable
_config = _Config()

def get_class_elements(obj, extra: str = '    '):
    #if globals()['_developerMode']:
    if _config.devMode:
        return str(obj.__class__) + '\n' + '\n'.join(
            (extra + (str(item) + ' = ' +
                      (get_class_elements(obj.__dict__[item], extra + '    ') if hasattr(obj.__dict__[item], '__dict__') else str(
                          obj.__dict__[item])))
             for item in sorted(obj.__dict__)))
    else:
        return str(obj.__class__) + '\n' + '\n'.join(
            (extra + (str(item) + ' = ' +
                      (get_class_elements(obj.__dict__[item], extra + '    ') if hasattr(obj.__dict__[item], '__dict__') else str(
                          obj.__dict__[item])))
             for item in sorted(obj.__dict__) if not item.startswith('_')))

@typechecked
def set_option(variable :str, value) -> None:
    if hasattr(_config, variable):
        setattr(_config, variable, value)

#Segment class
@typechecked
class Segment(object):
    def __init__(self, s: str) -> None:
        self._s = s.lower()
        
        # Segment AA
        if (self._s == 'aa'):
            self._info = {
                'name': None,
                'id': None,
                'node': None,
                'length': 660,
                'type': '8F1I01.AA66.xxxx-1',
                'description': 'ACOPOStrak straight segment'
            }

            self._svg = {
                            'w': 66.0,
                            'h': 10.074,
                            'rs': 0.0,
                            're': 0.0,
                            'svg': {
                                'body': {
                                    'points' : [[16.624056, 0.496246],
                                                [24.812025, 0.496246],
                                                [32.999993, 0.496246],
                                                [41.187961, 0.496246],
                                                [49.375929, 0.496246],
                                                [57.563898, 0.496246],
                                                [65.751866, 0.496246],
                                                [65.751866, 9.8255674],
                                                [0.24812, 9.8255674],
                                                [0.24812, 0.496246],
                                                [8.4360882, 0.496246]],
                                    'fill': '#eeeeee',
                                    'stroke': '#a9a9a9',
                                    'stroke_width': 0.492512,
                                },
                                'border': {
                                    'points': [[0.24812, 0.4962459999999993],
                                               [8.43608825, 0.4962459999999993],
                                               [16.6240565, 0.4962459999999993],
                                               [24.81202475, 0.4962459999999993],
                                               [32.999992999999996, 0.4962459999999993],
                                               [41.187961249999994, 0.4962459999999993],
                                               [49.3759295, 0.4962459999999993],
                                               [57.563897749999995, 0.4962459999999993],
                                               [65.75186599999999, 0.4962459999999993]],
                                    'fill': '#eeeeee',
                                    'stroke': '#ff8800',
                                    'stroke_width': 0.985023,
                                },
                                'direction': {
                                    'points': [[2.233082, 2.3621103],
                                               [2.233082, 7.9597031],
                                               [4.218044, 5.1609067]],
                                    'fill': '#cccccc',
                                    'stroke': '#cccccc',
                                    'stroke_width': 0,
                                }
                            }
                        }
            
        # Segment AB
        elif (self._s == 'ab'):
            self._info = {
                'name': None,
                'id': None,
                'node': None,
                'length': 450,
                'type': '8F1I01.AB2B.xxxx-1',
                'description': 'ACOPOStrak curve segment A'
            }

            self._svg = {
                            'w': 44.6,
                            'h': 12.523,
                            'rs': 0.0,
                            're': 22.5,
                            'svg': {
                                'body': {
                                    'points' : [[27.98617, 0.69384411],
                                                [33.517333, 1.1193844],
                                                [38.986245, 2.0383348],
                                                [44.269779, 3.7118311],
                                                [40.726738, 12.266472],
                                                [0.246234, 9.7518438],
                                                [0.246234, 0.492402],
                                                [5.7947334, 0.492402],
                                                [11.343331, 0.492402],
                                                [16.891831, 0.4965392],
                                                [22.440133, 0.5363351]],
                                    'fill': '#eeeeee',
                                    'stroke': '#a9a9a9',
                                    'stroke_width': 0.492512,
                                },
                                'border': {
                                    'points': [[0.24623400000000117, 0.49240199999999845],
                                               [5.794733367000006, 0.49240199999999845],
                                               [11.343331233900003, 0.49240199999999845],
                                               [16.891830600899993, 0.4965391973999971],
                                               [22.440132968099988, 0.5363350961999913],
                                               [27.986169837600002, 0.6938441114999989],
                                               [33.51733322220001, 1.1193844154999937],
                                               [38.98624466999999, 2.0383347618000016],
                                               [44.269779306000004, 3.7118311100999932]],
                                    'fill': '#eeeeee',
                                    'stroke': '#ff8800',
                                    'stroke_width': 0.985023,
                                },
                                'direction': {
                                    'points': [[2.216232, 2.3442904],
                                               [2.216232, 7.8999554],
                                               [4.18623, 5.1221229]],
                                    'fill': '#cccccc',
                                    'stroke': '#cccccc',
                                    'stroke_width': 0,
                                }
                            }
                        }
            
        # Segment BA
        elif (self._s == 'ba'):
            self._info = {
                'name': None,
                'id': None,
                'node': None,
                'length': 450,
                'type': '8F1I01.BA2B.xxxx-1',
                'description': 'ACOPOStrak curve segment B'
            }

            self._svg = {
                            'w': 44.6,
                            'h': 12.523,
                            'rs': 22.5,
                            're': 0.0,
                            'svg': {
                                'body': {
                                    'points' : [[22.159756, 0.53639704],
                                                [27.70807, 0.496603],
                                                [33.25658, 0.492466],
                                                [38.80516, 0.492466],
                                                [44.3537, 0.492466],
                                                [44.3537, 9.7514754],
                                                [3.8734094, 12.265986],
                                                [0.33016381, 3.7117448],
                                                [5.6139062, 2.0383266],
                                                [11.082533, 1.1194191],
                                                [16.613708, 0.6938987]],
                                    'fill': '#eeeeee',
                                    'stroke': '#a9a9a9',
                                    'stroke_width': 0.492512,
                                },
                                'border': {
                                    'points': [[0.3301638061000034, 3.711744768300008],
                                               [5.613906170299998, 2.038326569399999],
                                               [11.082533222199999, 1.1194191364999995],
                                               [16.613707837600003, 0.6938987045000005],
                                               [22.159755968100004, 0.5363970445999939],
                                               [27.708069600900004, 0.49660300419999714],
                                               [33.2565802339, 0.4924660000000074],
                                               [38.805159816970004, 0.4924660000000074],
                                               [44.35369999999996, 0.4924660000000074]],
                                    'fill': '#eeeeee',
                                    'stroke': '#ff8800',
                                    'stroke_width': 0.985023,
                                },
                                'direction': {
                                    'points': [[2.8588584, 4.6686732],
                                               [4.984786, 9.801218],
                                               [5.7418578, 6.4810751]],
                                    'fill': '#cccccc',
                                    'stroke': '#cccccc',
                                    'stroke_width': 0,
                                }
                            }
                        }
            
        # Segment BB
        elif (self._s == 'bb'):
            self._info = {
                'name': None,
                'id': None,
                'node': None,
                'length': 240,
                'type': '8F1I01.BB4B.xxxx-1',
                'description': 'ACOPOStrak circular arc segment'
            }

            self._svg = {
                            'w': 23.2,
                            'h': 13.081,
                            'rs': 22.5,
                            're': 22.5,
                            'svg': {
                                'body': {
                                    'points' : [[14.488988, 0.62517295],
                                                [17.351025, 1.0496071],
                                                [20.156149, 1.7528172],
                                                [22.880244, 2.7270865],
                                                [18.690886, 12.840194],
                                                [4.508613, 12.840194],
                                                [0.3197376, 2.7270865],
                                                [3.0433506, 1.7528172],
                                                [5.8493425, 1.0496071],
                                                [8.7107037, 0.62517295],
                                                [11.599942, 0.48337337]],
                                    'fill': '#eeeeee',
                                    'stroke': '#a9a9a9',
                                    'stroke_width': 0.492512,
                                },
                                'border': {
                                    'points': [[0.31973760030000165, 2.72708646400001],
                                               [3.0433506408, 1.7528172340000054],
                                               [5.849342485500003, 1.0496070670000108],
                                               [8.710703690399995, 0.6251729469999958],
                                               [11.599942499999997, 0.48337336600000924],
                                               [14.488988384999999, 0.6251729469999958],
                                               [17.351024826000014, 1.0496070670000108],
                                               [20.15614851000001, 1.7528172340000054],
                                               [22.880243861999986, 2.72708646400001]],
                                    'fill': '#eeeeee',
                                    'stroke': '#ff8800',
                                    'stroke_width': 0.985023,
                                },
                                'direction': {
                                    'points': [[5.4532683, 10.079443],
                                               [5.9789878, 6.307767],
                                               [2.9398466, 4.0119643]],
                                    'fill': '#cccccc',
                                    'stroke': '#cccccc',
                                    'stroke_width': 0,
                                }
                            }
                        }
        
        else:
            raise ValueError('Segment not supported. Supported segments "AA", "AB", "BA" or "BB"')
        
        #self._g = self._create_group(self._svg)
        
    def _group(self, constructor, angle: float = 0, show_id: bool = False, seg_body_fill: str = None, seg_body_stroke: str = None, seg_border_stroke: str = None, seg_dir_fill: str = None, seg_dir_stroke: str = None, seg_id_fill: str = None, seg_id_stroke: str = None, seg_id_stroke_width: float = None):
        # Get constructor variables
        name = self._info['name'] if self._info['name'] is not None else 'gSegAB'
        
        seg_body_points = constructor['svg']['body']['points']
        seg_body_fill = constructor['svg']['body']['fill'] if seg_body_fill is None else seg_body_fill
        seg_body_stroke = constructor['svg']['body']['stroke'] if seg_body_stroke is None else seg_body_stroke
        seg_body_stroke_width = constructor['svg']['body']['stroke_width']
        
        seg_border_points = constructor['svg']['border']['points']
        seg_border_fill = constructor['svg']['body']['fill'] if seg_body_fill is None else seg_body_fill
        seg_border_stroke = constructor['svg']['border']['stroke'] if seg_border_stroke is None else seg_border_stroke
        seg_border_stroke_width = constructor['svg']['border']['stroke_width']
        
        seg_dir_points = constructor['svg']['direction']['points']
        seg_dir_fill = constructor['svg']['direction']['fill'] if seg_dir_fill is None else seg_dir_fill
        seg_dir_stroke = constructor['svg']['direction']['stroke'] if seg_dir_stroke is None else seg_dir_stroke
        seg_dir_stroke_width = constructor['svg']['direction']['stroke_width']
        
        seg_id_fill = '#bbbbbb' if seg_id_fill is None else seg_id_fill
        seg_id_stroke = '#bbbbbb' if seg_id_stroke is None else seg_id_stroke
        seg_id_stroke_width = 0.15 if seg_id_stroke_width is None else seg_id_stroke_width
        
        style=f'font-size:5;font-family:Arial;font-weight:none;fill:{seg_id_fill};stroke:{seg_id_stroke};stroke-width:{seg_id_stroke_width};text-anchor:middle;dominant-baseline:middle'
        
        g = svgwrite.container.Group(id = name, style=style)
        seg_body = svgwrite.shapes.Polygon(seg_body_points, fill=seg_body_fill, stroke=seg_body_stroke, stroke_width=seg_body_stroke_width)
        seg_border = svgwrite.shapes.Polyline(seg_border_points, fill=seg_border_fill, stroke=seg_border_stroke, stroke_width=seg_border_stroke_width)
        seg_dir = svgwrite.shapes.Polygon(seg_dir_points, fill=seg_dir_fill, stroke=seg_dir_stroke, stroke_width=seg_dir_stroke_width)
        
        g.add(seg_body)
        g.add(seg_border)
        g.add(seg_dir)
        
        if show_id:
            rot = -angle
            center = (constructor['w']/2)
            middle = (constructor['h']/2)
            seg_id = svgwrite.text.Text(self._info['id'] if self._info['id'] is not None else '1' , insert = (center, middle), transform = 'rotate(%s ,%s, %s)' % (rot, center, middle))
            g.add(seg_id)
        return g
    
    def info(self) -> Dict[str, any]:
        return {k: v for k, v in self._info.items() if v is not None}

    def plot(self, angle: float = 0, show_id: bool = False, seg_body_fill: str = None, seg_body_stroke: str = None, seg_border_stroke: str = None, seg_dir_fill: str = None, seg_dir_stroke: str = None, seg_id_fill: str = None, seg_id_stroke: str = None, seg_id_stroke_width: float = None) -> _TSegment:
        # Limit angle between [0°, 360°)
        angle %= 360.0
        
        # Get with and height
        w = self._svg['w']
        h = self._svg['h']
        
        # Calculate new with and height
        nw = (abs(w*np.cos(np.deg2rad(angle))) + abs(h*np.cos(np.deg2rad(90+angle)))).round(3)
        nh = (abs(w*np.sin(np.deg2rad(angle))) + abs(h*np.sin(np.deg2rad(90+angle)))).round(3)
        
        # Calculate translation in x and y
        nx = (nw - ((w*np.cos(np.deg2rad(angle))) + (h*np.cos(np.deg2rad(90+angle)))).round(3))/2
        ny = (nh - ((w*np.sin(np.deg2rad(angle))) + (h*np.sin(np.deg2rad(90+angle)))).round(3))/2
        
        # Create group
        g = self._group(self._svg, angle, show_id, seg_body_fill, seg_body_stroke, seg_border_stroke, seg_dir_fill, seg_dir_stroke, seg_id_fill, seg_id_stroke, seg_id_stroke_width)
        
        # Apply translation and rotation to the group
        g.translate(nx,ny)
        g.rotate(angle)
        
        # Create drawing and append the group
        self._dwg = svgwrite.Drawing(profile='tiny', viewBox = f'0 0 {nw} {nh}', size = (nw*mm, nh*mm))
        self._dwg.add(g)
        
        # Display the drawing
        display(self._dwg)
        
        return self
    
    def save(self, name: str = 'Segment.svg') -> None:
        self._dwg.saveas(name)
    
    def __add__(self, other: _TST) -> _TTrack:
        if isinstance(other, Segment):
            return Track([self, other])
        elif isinstance(other, Track):
            new_track = [self]
            new_track += other.segment.copy()
            return Track(new_track)
        else:
            raise TypeError('Segments can only be added to  Segment or Track objects')
    
    def __mul__(self, other: int) -> _TTrack:
        if isinstance(other, int):
            if other < 0:
                raise TypeError('Segments can only be multiplied by positive integers')
            l = list()
            for i in range(other):
                l.append(self.__class__(self._s))
            return Track(l)
        else:
            raise TypeError('Segments can only be multiplied by positive integers')
    
    __rmul__ = __mul__
    
#Track class
@typechecked
class Track(object):
    def __init__(self, segments: List[Segment], seg_prefix: str = 'gSeg_', seg_offset: int = 1):
        if seg_offset < 0:
            raise TypeError('The "seg_offset" argument must be a positive integer')

        self.segment = [Segment(seg._s) for seg in segments]
        self.seg_prefix = seg_prefix
        self.seg_offset = seg_offset

        for i, s in enumerate(self.segment):
            s._info['name'] = self.seg_prefix + str(i + self.seg_offset).zfill(3)
            s._info['id'] = self.seg_offset + i
        
    def __add__(self, other: _TST) -> _TTrack:
        new_track = self.segment.copy()
        if isinstance(other, Segment):
            new_track.append(other)
        elif isinstance(other, Track):
            other_track = self.__class__(other.segment, other.seg_prefix, other.seg_offset)
            new_track = new_track + other_track.segment
        else:
            raise TypeError('Tracks can only be added to Segment or Track objects')
        return Track(new_track)
    
    def __mul__(self, other: int) -> _TTrack:
        if isinstance(other, int):
            if other < 0:
                raise TypeError('Tracks can only be multiplied by positive integers')
            new_track = self.segment.copy()
            new_track = new_track * other
            return Track(new_track)
        else:
            raise TypeError('Tracks can only be multiplied by positive integers')
    
    def __len__(self) -> int:
        return len(self.segment)
    
    def info(self, compact: bool = False) -> Dict[str, any]:
        return {
            'seg_prefix': self.seg_prefix,
            'seg_offset': self.seg_offset,
            'length': sum(s._info['length'] for s in self.segment),
            'segment': [s._info for s in self.segment] if not compact else f'The track has {len(self.segment)} segments',
        }
    
    def plot(self, angle: float = 0, show_id: bool = False, seg_body_fill: str = None, seg_body_stroke: str = None, seg_border_stroke: str = None, seg_dir_fill: str = None, seg_dir_stroke: str = None, seg_id_fill: str = None, seg_id_stroke: str = None, seg_id_stroke_width: float = None) -> _TTrack:
        # Limit angle between [0°, 360°)
        angle %= 360.0
        
        xabs = self.segment[0]._svg['svg']['border']['points'][0][0]
        yabs = self.segment[0]._svg['svg']['border']['points'][0][1]
        
        rot = angle
        gap = _config.gap
        xmax = 0.0
        ymax = 0.0
        xmin = 0.0
        ymin = 0.0
        
        #track = []
        # Create drawing and append the group
        self._dwg = svgwrite.Drawing(profile='tiny')
        
        for i, seg in enumerate(self.segment):
            rot += seg._svg['rs']
            tl = seg._svg['svg']['border']['points'][0]
            tr = seg._svg['svg']['border']['points'][-1]
            
            xabs += (tl[1] * np.sin(np.deg2rad(rot)))
            yabs -= (tl[1] * np.cos(np.deg2rad(rot)))
            
            w = seg._svg['w']
            h = seg._svg['h']
            nw = [(w*np.cos(np.deg2rad(rot))).round(3), (h*np.cos(np.deg2rad(90+rot))).round(3)]
            nh = [(w*np.sin(np.deg2rad(rot))).round(3), (h*np.sin(np.deg2rad(90+rot))).round(3)]
            
            xmax = max(xmax, xabs, xabs + sum(x for x in nw if x > 0))
            ymax = max(ymax, yabs, yabs + sum(y for y in nh if y > 0))
            xmin = min(xmin, xabs, xabs + sum(x for x in nw if x < 0))
            ymin = min(ymin, yabs, yabs + sum(y for y in nh if y < 0))
            
            # Create group
            g = seg._group(seg._svg, rot, show_id, seg_body_fill, seg_body_stroke, seg_border_stroke, seg_dir_fill, seg_dir_stroke, seg_id_fill, seg_id_stroke, seg_id_stroke_width)
            
            # Apply translation and rotation to the group
            g.translate(round(xabs, 3), round(yabs, 3))
            g.rotate(round(rot, 3))
            
            self._dwg.add(g)
            
            xabs += ((tr[0] * np.cos(np.deg2rad(rot))) + (tr[1] * np.cos(np.deg2rad(rot + 90))) + (gap * np.cos(np.deg2rad(rot))))
            yabs += ((tr[0] * np.sin(np.deg2rad(rot))) + (tr[1] * np.sin(np.deg2rad(rot + 90))) + (gap * np.sin(np.deg2rad(rot))))
            rot +=  seg._svg['re']
        
        nw = (abs(xmax) + abs(xmin))
        nh = (abs(ymax) + abs(ymin))
        nx = abs(xmin)
        ny = abs(ymin)
        
        self._dwg.viewbox(-nx, -ny, nw, nh)
        self._dwg['width'] = nw*mm
        self._dwg['height'] = nh*mm

        display(self._dwg)
        
        return self
    
    def save(self, name: str = 'Track.svg') -> None:
        self._dwg.saveas(name)
    
    __rmul__ = __mul__
    
#Loop class
@typechecked
class Loop(Track):
    def __init__(self, l: int = 2, w: int = 1) -> None:
        self._l = l
        self._w = w

        if (self._l < 2):
            raise ValueError('The length of the loop must be at least 2')
        elif (self._w < 1):
            raise ValueError('The width of the loop must be at least 1')
        else:
            if (self._w == 1):
                self._track = TRACK180 + ((self._l - 2) * TRACK0) + TRACK180 + ((self._l - 2) * TRACK0)
            else:
                self._track = TRACK90 + ((self._w - 2) * TRACK0) + TRACK90 + ((self._l - 2) * TRACK0) + TRACK90 + ((self._w - 2) * TRACK0) + TRACK90 + ((self._l - 2) * TRACK0)
        super().__init__(self._track.segment)

    def __add__(self, other: _TST) -> _TAssembly:
        if isinstance(other, Segment):
            new_track = Track([other])
            return Assembly([self, new_track])
        elif isinstance(other, Track):
            return Assembly([self, other])

    def __mul__(self, other: int) -> _TAssembly:
        l = [self]
        return Assembly([ item for item in l for _ in range(other) ])

    __rmul__ = __mul__

    def save(self, name: str = 'Loop.svg') -> None:
        self.dwg.saveas(name)

#Assembly class
@typechecked
class Assembly(object):
    def __init__(self, tracks: List[Track], name: str = 'gAssembly_1') -> None:
        self.name = name
        self.track = list()
        
        old_prefix = None
        for track in tracks:
            if old_prefix != track.seg_prefix:
                t_len = track.seg_offset
            self.track.append(Track(track.segment, track.seg_prefix, t_len))
            t_len += len(track)
            old_prefix = track.seg_prefix
    
    def info(self, compact: bool = False) -> Dict[str, any]:
        return {
            'name': self.name,
            'length': sum(t.info()['length'] for t in self.track),
            'track': [t.info() for t in self.track] if not compact else f'The assembly has {len(self.track)} tracks',
        }
    
    def export(self):
        _grp_track = _mk_track_dict(self)
        _grp_segment = _mk_seg_dict()
        _grp_shuttle = _mk_sh_dict()
        _grp_visu = _mk_visu_dict()
        
        _asm_cfg = {
                        'Configuration': {
                            'Element': {
                                '@ID': self.name,
                                '@Type': 'assembly',
                                'Group': [
                                    _grp_track,
                                    _grp_segment,
                                    _grp_shuttle,
                                    _grp_visu,
                                ],
                                'Selector': {
                                    '@ID': 'Alarms',
                                    '@Value': 'None'
                                }
                            }
                        }
                    }
        
        _asm_cfg_tree = xmltodict.unparse(_asm_cfg, pretty=True, full_document=False)

        _asm_cfg_file = 'AsmCfg.assembly'
        with open(_asm_cfg_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<?AutomationStudio FileVersion="4.9"?>\n')
            f.write(b'<?pyacptrak version="'+ version + b'" author="Jorge Centeno"?>\n')
            f.write(_asm_cfg_tree.encode('utf-8'))
        
        print(f'{_asm_cfg_file} created successfully')
        
        _sh_cfg = _mk_sh_stereotype()
        _sh_cfg_tree = xmltodict.unparse(_sh_cfg, pretty=True, full_document=False)
        _sh_cfg_file = 'ShCfg.shuttlestereotype'
        with open(_sh_cfg_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<?AutomationStudio FileVersion="4.9"?>\n')
            f.write(b'<?pyacptrak version="'+ version + b'" author="Jorge Centeno"?>\n')
            f.write(_sh_cfg_tree.encode('utf-8'))
        
        print(f'{_sh_cfg_file} created successfully')

#Controller parameter internal class for segment internal class
class _control_par(object):
    def __init__(self):
        self.pos_proportional_gain = 150
        self.speed_proportional_gain = 120
        self.ff_total_mass = 0.7
        self.ff_force_pos = 1.5
        self.ff_force_neg = 1.5
        self.ff_speed_force_factor = 1.4
    
    def __str__(self):
        return get_class_elements(self)

#Segment internal class for parameter class
class _segment(object):
    def __init__(self, sh):
        self.simulation = 'Off'
        self.elongation = 'Inactive'
        self.stop_reaction = 'Induction Halt'
        self.speed_filter = 'Not Used'
        self._controller = 'Medium'
        self._sh = sh
        self._sh.bind_to(self._update_control_par)
        self.control_par = _control_par()
    
    def __str__(self):
        return get_class_elements(self)
    
    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self, value):
        self._controller = value
        self._update_control_par(self._sh.model)
    
    def _update_control_par(self, model):
        _controller = ['soft', 'medium', 'hard']
        if self._controller.lower() not in _controller:
            raise ValueError(f'The controller mode is not valid, please configure one of the following values: {_controller}')
        
        if ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.102.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        elif ((model == '8F1SA.100.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.5
            self.control_par.ff_force_neg = 1.5
            self.control_par.ff_speed_force_factor = 1.4
        
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.106.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 200
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.5
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 150
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        elif ((model == '8F1SA.104.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 200
            self.control_par.speed_proportional_gain = 150
            self.control_par.ff_total_mass = 0.7
            self.control_par.ff_force_pos = 1.2
            self.control_par.ff_force_neg = 1.2
            self.control_par.ff_speed_force_factor = 1.0
        
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.203.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 180
            self.control_par.ff_total_mass = 0.8
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 80
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 120
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        elif ((model == '8F1SA.201.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 300
            self.control_par.speed_proportional_gain = 180
            self.control_par.ff_total_mass = 1.2
            self.control_par.ff_force_pos = 2.0
            self.control_par.ff_force_neg = 2.0
            self.control_par.ff_speed_force_factor = 2.0
        
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'soft')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 200
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'medium')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 300
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
        elif ((model == '8F1SA.308.xxxxxx-x') and (self._controller.lower() == 'hard')):
            self.control_par.pos_proportional_gain = 600
            self.control_par.speed_proportional_gain = 400
            self.control_par.ff_total_mass = 2.5
            self.control_par.ff_force_pos = 3.0
            self.control_par.ff_force_neg = 3.0
            self.control_par.ff_speed_force_factor = 1.1
            
        else:
            raise ValueError(f'There is no shuttle with those characteristics: model = {model}, controller = {self._controller.capitalize()}')
        
        print('The control parameters have been updated')

#Shuttle stereotype internal class for shuttle class
class _sh_stereotype_par(object):
    def __init__(self):
        self.velocity = 4.0
        self.acceleration = 50.0
        self.deceleration = 50.0
        self.jerk = 0.02
        self.user_data = 0
        self.recontrol = 'Active'
    
    def __str__(self):
        return get_class_elements(self)

#Shuttle internal class for parameter class
class _shuttle(object):
    def __init__(self):
        self.count = 10
        self.convoy = 'Inactive'
        self.collision_distance = 0.002
        self.error_stop = 0.006
        self.stereotype = 'ShuttleStereotype_1'
        self.stereotype_par = _sh_stereotype_par()
        self._size = 50
        self._magnet_plate = 2
        self._magnet_type = 'Straight'
        self.model = '8F1SA.100.xxxxxx-x'
        self.collision_strategy = 'Constant'
        self.extent_front = 0.025
        self.extent_back = 0.025
        self.width = 0.046
        self._observers = []
        self.auto_dimensions = True
    
    def __str__(self):
        return get_class_elements(self)
        
    @property
    def size(self):
        return self._size
    
    @property
    def magnet_plate(self):
        return self._magnet_plate
    
    @property
    def magnet_type(self):
        return self._magnet_type
    
    @size.setter
    def size(self, value):
        _size = [50, 100, 244]
        if value not in _size:
            raise ValueError(f'The shuttle size is not valid, please configure one of the following values: {_size}')
            
        self._size = value
        self._update_model()
        
    @magnet_plate.setter
    def magnet_plate(self, value):
        _magnet_plate = [1, 2]
        if value not in _magnet_plate:
            raise ValueError(f'The magnet plate is not valid, please configure one of the following values: {_magnet_plate}')
        
        self._magnet_plate = value
        self._update_model()
        
    @magnet_type.setter
    def magnet_type(self, value):
        _magnet_type = ['straight', 'skewed']
        if value.lower() not in _magnet_type:
            raise ValueError(f'The magnet type is not valid, please configure one of the following values: {_magnet_type}')
        
        self._magnet_type = value
        self._update_model()
    
    def _update_model(self):
        if ((self.size == 50) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.03
            self.model = '8F1SA.102.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.046
            self.model = '8F1SA.100.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'skewed')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.03
            self.model = '8F1SA.106.xxxxxx-x'
        elif ((self._size == 50) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'skewed')):
            if self.auto_dimensions:
                self.extent_front = 0.025
                self.extent_back = 0.025
                self.width = 0.046
            self.model = '8F1SA.104.xxxxxx-x'
        elif ((self._size == 100) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.05
                self.extent_back = 0.05
                self.width = 0.03
            self.model = '8F1SA.203.xxxxxx-x'
        elif ((self._size == 100) and (self.magnet_plate == 2) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.05
                self.extent_back = 0.05
                self.width = 0.046
            self.model = '8F1SA.201.xxxxxx-x'
        elif ((self._size == 244) and (self.magnet_plate == 1) and (self.magnet_type.lower() == 'straight')):
            if self.auto_dimensions:
                self.extent_front = 0.122
                self.extent_back = 0.122
                self.width = 0.03
            self.model = '8F1SB.308.xxxxxx-x'
        else:
            raise ValueError(f'There is no shuttle with those characteristics size: {self._size}, magnetic plate: {self.magnet_plate}, magnet type {self.magnet_type}')
        
        for callback in self._observers:
            callback(self.model)
        
        if self.auto_dimensions:
            print(f'The shuttle model and dimensions have been updated: {self.model}')
        else:
            print(f'The shuttle model has been updated: {self.model}')
            
    def bind_to(self, callback):
        self._observers.append(callback)

#Visualization internal class for parameter class
class _visu(object):
    def __init__(self):
        self.task = 4

#Parameter internal class
class _param(object):
    def __init__(self):
        self.shuttle = _shuttle()
        self.segment = _segment(self.shuttle)
        self.visu = _visu()
        
    def __str__(self):
        return get_class_elements(self)
    
#Constant definition
PARAM: Final = _param()
TRACK0: Final = Track([Segment('aa')])
TRACK45: Final = Track([Segment('ab'), Segment('ba')])
TRACK90: Final = Track([Segment('ab'), Segment('bb'), Segment('ba')])
TRACK135: Final = Track([Segment('ab'), Segment('bb'), Segment('bb'), Segment('ba')])
TRACK180: Final = Track([Segment('ab'), Segment('bb'), Segment('bb'), Segment('bb'), Segment('ba')])

#Create track group dictionary
def _mk_track_dict(asm: Assembly):
    grp = []
    for i, track in enumerate(asm.track):
        if i < 1:
            selector = {
                            '@ID': 'Position',
                            '@Value': 'Absolute',
                            'Property': {
                                        '@ID': 'SegmentCountDirection',
                                        '@Value': 'RightToLeft'
                                    },
                            'Group': [
                                        {
                                            '@ID': 'Translation',
                                            'Property': [
                                                {
                                                    '@ID': 'X',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Y',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Z',
                                                    '@Value': '0.0'
                                                }
                                            ]
                                        },
                                        {
                                            '@ID': 'Orientation',
                                            'Property': [
                                                {
                                                    '@ID': 'Angle1',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Angle2',
                                                    '@Value': '0.0'
                                                },
                                                {
                                                    '@ID': 'Angle3',
                                                    '@Value': '0.0'
                                                }
                                            ]
                                        }
                                    ]
                        }
        else:
            selector = {
                            '@ID': 'Position',
                            '@Value': 'RelativeToOne',
                            'Group': [
                                    {
                                        '@ID': 'TrackSegmentPosition',
                                        "Property": [
                                            {
                                                '@ID': 'SegmentRef',
                                                '@Value': ''
                                            },
                                            {
                                                '@ID': 'PositionRelativeTo',
                                                '@Value': 'FromEnd'
                                            }
                                        ]
                                    },
                                    {
                                        '@ID': 'Base',
                                        'Property': {
                                            '@ID': 'SegmentRef',
                                            '@Value': ''
                                        }
                                    }
                                ]
                        }
        
        
        grp.append({
                    '@ID': 'Track['+ str(i+1) +']',
                    'Group': {
                                '@ID': 'Segments',
                                'Property': []
                             },
                    'Selector': selector,
                    })
        for j, seg in enumerate(track.info()['segment']):
            grp[i]['Group']['Property'].append({
                                        '@ID': 'SegmentRef[' + str(j+1) + ']',
                                        '@Value': seg['name'],
                                    })
        
    
    tracks = {
                '@ID': 'Tracks',
                    'Property': {
                        '@ID': 'TrackSeparation',
                        '@Value': '0.030'
                    },
                    'Group': grp}
    return tracks

#Create segment group dictionary
@typechecked
def _mk_seg_dict(param: _segment = PARAM.segment):
    _simulation = ['off', 'on']
    _elongation = ['inactive', 'active']
    _stop_reaction = ['induction halt']
    _speed_filter = ['not used']
    
    if param.simulation.lower() not in _simulation:
        raise ValueError(f'The segment simulation is not valid, please configure one of the following values: {_simulation}')
    
    if param.elongation.lower() not in _elongation:
        raise ValueError(f'The segment elongation is not valid, please configure one of the following values: {_elongation}')
    
    if param.stop_reaction.lower() not in _stop_reaction:
        raise ValueError(f'The segment stop reaction is not valid, please configure one of the following values: {_stop_reaction}')
    
    if param.speed_filter.lower() not in _speed_filter:
        raise ValueError(f'The segment speed filter is not valid, please configure one of the following values: {_speed_filter}')
    
    return {
                "@ID": "CommonSegmentSettings",
                "Property": [
                    {
                        "@ID": "SegmentSimulationOnPLC",
                        "@Value": param.simulation.capitalize()
                    },
                    {
                        "@ID": "ElongationCompensation",
                        "@Value": param.elongation.capitalize()
                    },
                    {
                        "@ID": "ScopeOfErrorReaction",
                        "@Value": "Assembly"
                    },
                    {
                        "@ID": "ShuttleIdentificationTime",
                        "@Value": "0"
                    }
                ],
                "Selector": [
                    {
                        "@ID": "StopReaction",
                        "@Value": ''.join(x for x in param.stop_reaction.title() if not x.isspace()),
                    },
                    {
                        "@ID": "SpeedFilter",
                        "@Value": ''.join(x for x in param.speed_filter.title() if not x.isspace()),
                    }
                ],
                "Group": {
                    "@ID": "ControllerParameters",
                    "Group": {
                        "@ID": "DefaultParameter",
                        "Group": [
                            {
                                "@ID": "Controller",
                                "Group": [
                                    {
                                        "@ID": "Position",
                                        "Property": {
                                            "@ID": "ProportionalGain",
                                            "@Value": str(param.control_par.pos_proportional_gain),
                                        }
                                    },
                                    {
                                        "@ID": "Speed",
                                        "Property": [
                                            {
                                                "@ID": "ProportionalGain",
                                                "@Value": str(param.control_par.speed_proportional_gain),
                                            },
                                            {
                                                "@ID": "IntegrationTime",
                                                "@Value": "0.0"
                                            }
                                        ]
                                    },
                                    {
                                        "@ID": "FeedForward",
                                        "Property": [
                                            {
                                                "@ID": "TotalMass",
                                                "@Value": str(param.control_par.ff_total_mass),
                                            },
                                            {
                                                "@ID": "ForcePositive",
                                                "@Value": str(param.control_par.ff_force_pos),
                                            },
                                            {
                                                "@ID": "ForceNegative",
                                                "@Value": str(param.control_par.ff_force_neg),
                                            },
                                            {
                                                "@ID": "SpeedForceFactor",
                                                "@Value": str(param.control_par.ff_speed_force_factor),
                                            },
                                            {
                                                "@ID": "ForceLoad",
                                                "@Value": "0.0"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "@ID": "MovementErrorLimits",
                                "Property": [
                                    {
                                        "@ID": "PositionError",
                                        "@Value": "0.005"
                                    },
                                    {
                                        "@ID": "VelocityError",
                                        "@Value": "5.0"
                                    }
                                ]
                            },
                            {
                                "@ID": "Diverter",
                                "Property": {
                                    "@ID": "ForceOverride",
                                    "@Value": "1.0"
                                }
                            }
                        ]
                    },
                    "Selector": {
                        "@ID": "AdditionalParameterSets",
                        "@Value": "NotUsed"
                    }
                }
            }

def _mk_sh_stereotype(param: _shuttle = PARAM.shuttle):
    return {
                    'Configuration': {
                        'Element': {
                            '@ID': param.stereotype,
                            '@Type': 'shuttlestereotype',
                            'Property': [
                                {
                                    '@ID': 'MeasurementUnit',
                                    '@Value': '5067858'
                                },
                                {
                                    '@ID': 'MeasurementResolution',
                                    '@Value': '0.00001'
                                }
                            ],
                            'Selector': [
                                {
                                    '@ID': 'MovementLimits',
                                    '@Value': 'Internal',
                                    'Property': [
                                        {
                                            '@ID': 'VelocityIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'AccelerationIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'DecelerationIsReadOnly',
                                            '@Value': '0'
                                        },
                                        {
                                            '@ID': 'UpdateMode',
                                            '@Value': 'Immediately'
                                        }
                                    ],
                                    'Selector': [
                                        {
                                            '@ID': 'Velocity',
                                            'Property': {
                                                '@ID': 'Velocity',
                                                '@Value': str(param.stereotype_par.velocity)
                                            }
                                        },
                                        {
                                            '@ID': 'Acceleration',
                                            'Property': {
                                                '@ID': 'Acceleration',
                                                '@Value': str(param.stereotype_par.acceleration)
                                            }
                                        },
                                        {
                                            '@ID': 'Deceleration',
                                            'Property': {
                                                '@ID': 'Deceleration',
                                                '@Value': str(param.stereotype_par.deceleration)
                                            }
                                        }
                                    ]
                                },
                                {
                                    '@ID': 'JerkFilter',
                                    '@Value': 'Used',
                                    'Property': {
                                        '@ID': 'JerkTime',
                                        '@Value': str(param.stereotype_par.jerk)
                                    }
                                }
                            ],
                            'Group': [
                                {
                                    '@ID': 'UserData',
                                    'Property': {
                                        '@ID': 'Size',
                                        '@Value': str(param.stereotype_par.user_data)
                                    }
                                },
                                {
                                    '@ID': 'StateTransitions',
                                    'Property': {
                                        '@ID': 'AutomaticRecontrol',
                                        '@Value': param.stereotype_par.recontrol
                                    }
                                }
                            ]
                        }
                    }
                }

#Create shuttle group dictionary
@typechecked
def _mk_sh_dict(param: _shuttle = PARAM.shuttle):
    _convoy = ['inactive', 'active']
    _collision_strategy = ['constant', 'variable', 'advanced constant', 'advanced variable']
    
    if param.convoy.lower() not in _convoy:
        raise ValueError(f'The convoy is not valid, please configure one of the following values: {_convoy}')
    
    if param.collision_strategy.lower() not in _collision_strategy:
        raise ValueError(f'The collision strategy is not valid, please configure one of the following values: {_collision_strategy}')
        
    return {
                "@ID": "Shuttles",
                "Property": [
                    {
                        "@ID": "MaxShuttleCount",
                        "@Value": str(param.count),
                    },
                    {
                        "@ID": "MaxShuttleCommandCount",
                        "@Value": "0"
                    },
                    {
                        "@ID": "UseConvoys",
                        "@Value": param.convoy.capitalize(),
                    }
                ],
                "Group": [
                    {
                        "@ID": "DistanceReserve",
                        "Property": [
                            {
                                "@ID": "Collision",
                                "@Value": str(param.collision_distance),
                            },
                            {
                                "@ID": "ErrorStop",
                                "@Value": str(param.error_stop),
                            }
                        ]
                    },
                    {
                        "@ID": "ShuttleStereotypes",
                        "Property": {
                            "@ID": "ShuttleStRef[1]",
                            "Value": param.stereotype,
                        }
                    },
                    {
                        "@ID": "MagnetPlateConfigurations",
                        "Selector": {
                            "@ID": "ShuttleType[1]",
                            "@Value": param.model,
                        }
                    },
                    {
                        "@ID": "CollisionAvoidance",
                        "Selector": {
                            "@ID": "Strategy",
                            "@Value": ''.join(x for x in param.collision_strategy.title() if not x.isspace()),
                        },
                        "Group": {
                            "@ID": "MaximumModelDimensions",
                            "Group": [
                                {
                                    "@ID": "Length",
                                    "Property": [
                                        {
                                            "@ID": "ExtentToFront",
                                            "@Value": str(param.extent_front),
                                        },
                                        {
                                            "@ID": "ExtentToBack",
                                            "@Value": str(param.extent_back),
                                        }
                                    ]
                                },
                                {
                                    "@ID": "Width",
                                    "Property": {
                                        "@ID": "Width",
                                        "@Value": str(param.width),
                                    }
                                }
                            ]
                        }
                    }
                ]
            }

#Create visualization group dictionary
@typechecked
def _mk_visu_dict(param: _visu = PARAM.visu):
    _task = [1, 2, 3, 4, 5, 6, 7, 8]
    
    if param.task not in _task:
        raise ValueError(f'The task class is not valid, please configure one of the following values: {_task}')
        
    return {
                "@ID": "Visualization",
                "Property": [
                    {
                        "@ID": "MonitoringPv",
                        "@Value": "::Vis:Mon"
                    },
                    {
                        "@ID": "ProcessingTaskClass",
                        "@Value": str(param.task),
                    }
                ]
            }