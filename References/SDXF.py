# (c)www.stani.be

__version__ = """v1.1.2 (07/06/12)"""
__author__ = "www.stani.be"
__license__ = "GPL"
__url__ = "https://github.com/nycresistor/SDXF"
"""SDXF - Stani's DXF
Python library to generate dxf drawings

Copyright %s
Version %s
License %s
Homepage %s

Library by Stani, whose website is now defunct.
Now on github, loosely maintained by Kellbot (http://www.kellbot.com)
""" % (__author__, __version__, __license__, __url__)

import copy

####1) Private (only for developers)
_HEADER_POINTS = ['insbase', 'extmin', 'extmax']


# ---helper functions


def _point(x, index=0):
    """Convert tuple to a dxf point"""
    return '\n'.join(['%s\n%s' % ((i + 1) * 10 + index, x[i])
                      for i in range(len(x))])


def _points(p):
    """Convert a list of tuples to dxf points"""
    return [_point(p[i], i) for i in range(len(p))]


# ---base classes


class _Call:
    """Makes a callable class."""

    def copy(self):
        """Returns a copy."""
        return copy.deepcopy(self)

    def __call__(self, **attrs):
        """Returns a copy with modified attributes."""
        copied = self.copy()
        for attr in attrs:
            setattr(copied, attr, attrs[attr])
        return copied


class _Entity(_Call):
    """Base class for _common group codes for entities."""

    def __init__(self, color=None, extrusion=None, layer='0',
                 lineType=None, lineTypeScale=None, lineWeight=None,
                 thickness=None, parent=None):
        """None values will be omitted."""
        self.color = color
        self.extrusion = extrusion
        self.layer = layer
        self.lineType = lineType
        self.lineTypeScale = lineTypeScale
        self.lineWeight = lineWeight
        self.thickness = thickness
        self.parent = parent

    def _common(self):
        """Return common group codes as a string."""
        parent = self.parent if self.parent else self
        result = '8\n%s' % parent.layer
        if parent.color is not None:
            result += '\n62\n%s' % parent.color
        if parent.extrusion is not None:
            result += '\n%s' % _point(parent.extrusion, 200)
        if parent.lineType is not None:
            result += '\n6\n%s' % parent.lineType
        if parent.lineWeight is not None:
            result += '\n370\n%s' % parent.lineWeight
        if parent.lineTypeScale is not None:
            result += '\n48\n%s' % parent.lineTypeScale
        if parent.thickness is not None:
            result += '\n39\n%s' % parent.thickness
        return result


class _Entities:
    """Base class to deal with composed objects."""

    def __dxf__(self):
        return []

    def __str__(self):
        return '\n'.join([str(x) for x in self.__dxf__()])


class _Collection(_Call):
    """Base class to expose entities methods to main object."""

    def __init__(self, entities=None):
        self.entities = copy.copy(entities or [])
        # link entities methods to drawing
        for attr in dir(self.entities):
            if attr[0] != '_':
                attrObject = getattr(self.entities, attr)
                if callable(attrObject):
                    setattr(self, attr, attrObject)


####2) Constants
# ---color values
BYBLOCK = 0
BYLAYER = 256

# ---block-type flags (bit coded values, may be combined):

# This is an anonymous block generated by hatching, associative
# dimensioning, other internal operations, or an application
ANONYMOUS = 1
# This block has non-constant attribute definitions (this bit is not set if
# the block has any attribute definitions that are constant, or has no
# attribute definitions at all)
NON_CONSTANT_ATTRIBUTES = 2
XREF = 4  # This block is an external reference (xref)
XREF_OVERLAY = 8  # This block is an xref overlay
EXTERNAL = 16  # This block is externally dependent
# This is a resolved external reference, or dependent of an external
# reference (ignored on input)
RESOLVED = 32
# This definition is a referenced external reference (ignored on input)
REFERENCED = 64

# ---mtext flags
# attachment point
TOP_LEFT, TOP_CENTER, TOP_RIGHT = 1, 2, 3
MIDDLE_LEFT, MIDDLE_CENTER, MIDDLE_RIGHT = 4, 5, 6
BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT = 7, 8, 9
# drawing direction
LEFT_RIGHT = 1
TOP_BOTTOM = 3
# the flow direction is inherited from the associated text style
BY_STYLE = 5
# line spacing style (optional):
AT_LEAST = 1  # taller characters will override
EXACT = 2  # taller characters will not override

# ---polyline flags
# This is a closed polyline (or a polygon mesh closed in the M direction)
CLOSED = 1
CURVE_FIT = 2  # Curve-fit vertices have been added
SPLINE_FIT = 4  # Spline-fit vertices have been added
POLYLINE_3D = 8  # This is a 3D polyline
POLYGON_MESH = 16  # This is a 3D polygon mesh
CLOSED_N = 32  # The polygon mesh is closed in the N direction
POLYFACE_MESH = 64  # The polyline is a polyface mesh
# The linetype pattern is generated continuously around the vertices of this
# polyline
CONTINOUS_LINETYPE_PATTERN = 128

# ---text flags
# horizontal
LEFT, CENTER, RIGHT = 0, 1, 2
ALIGNED, MIDDLE, FIT = 3, 4, 5  # if vertical alignment = 0
# vertical
BASELINE, BOTTOM, MIDDLE, TOP = 0, 1, 2, 3


####3) Classes
# ---entitities


class Arc(_Entity):
    """Arc, angles in degrees."""

    def __init__(self, center=(0, 0, 0), radius=1,
                 startAngle=0.0, endAngle=90, **common):
        """Angles in degrees."""
        _Entity.__init__(self, **common)
        self.center = center
        self.radius = radius
        self.startAngle = startAngle
        self.endAngle = endAngle

    def __str__(self):
        return '0\nARC\n%s\n%s\n40\n%s\n50\n%s\n51\n%s' % \
               (self._common(), _point(self.center),
                self.radius, self.startAngle, self.endAngle)


class Circle(_Entity):
    """Circle"""

    def __init__(self, center=(0, 0, 0), radius=1, **common):
        _Entity.__init__(self, **common)
        self.center = center
        self.radius = radius

    def __str__(self):
        return '0\nCIRCLE\n%s\n%s\n40\n%s' % \
               (self._common(), _point(self.center), self.radius)


class Face(_Entity):
    """3dface"""

    def __init__(self, points, **common):
        _Entity.__init__(self, **common)
        self.points = points

    def __str__(self):
        return '\n'.join(['0\n3DFACE', self._common()] +
                         _points(self.points))


class Insert(_Entity):
    """Block instance."""

    def __init__(self, name, point=(0, 0, 0),
                 xscale=None, yscale=None, zscale=None,
                 cols=None, colspacing=None, rows=None, rowspacing=None,
                 rotation=None, **common):
        _Entity.__init__(self, **common)
        self.name = name
        self.point = point
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.cols = cols
        self.colspacing = colspacing
        self.rows = rows
        self.rowspacing = rowspacing
        self.rotation = rotation

    def __str__(self):
        result = '0\nINSERT\n2\n%s\n%s\n%s' % (self.name, self._common(),
                                               _point(self.point))
        if self.xscale is not None:
            result += '\n41\n%s' % self.xscale
        if self.yscale is not None:
            result += '\n42\n%s' % self.yscale
        if self.zscale is not None:
            result += '\n43\n%s' % self.zscale
        if self.rotation:
            result += '\n50\n%s' % self.rotation
        if self.cols is not None:
            result += '\n70\n%s' % self.cols
        if self.colspacing is not None:
            result += '\n44\n%s' % self.colspacing
        if self.rows is not None:
            result += '\n71\n%s' % self.rows
        if self.rowspacing is not None:
            result += '\n45\n%s' % self.rowspacing
        return result


class Line(_Entity):
    """Line"""

    def __init__(self, points, **common):
        _Entity.__init__(self, **common)
        self.points = points

    def __str__(self):
        return '\n'.join(['0\nLINE', self._common()] + _points(self.points))


class LwPolyLine(_Entity):
    """This is a LWPOLYLINE. I have no idea how it differs from a normal
    PolyLine"""

    def __init__(self, points, flag=0, width=None, **common):
        _Entity.__init__(self, **common)
        self.points = points
        self.flag = flag
        self.width = width

    def __str__(self):
        result = '0\nLWPOLYLINE\n%s\n70\n%s' % (self._common(), self.flag)
        result += '\n90\n%s' % len(self.points)
        for point in self.points:
            result += '\n%s' % _point(point)
        if self.width:
            result += '\n40\n%s\n41\n%s' % (self.width, self.width)
        return result


class PolyLine(_Entity):
    # TODO: Finish polyline (now implemented as a series of lines)
    def __init__(self, points, flag=0, width=None, **common):
        _Entity.__init__(self, **common)
        self.points = points
        self.flag = flag
        self.width = width

    def __str__(self):
        result = '0\nPOLYLINE\n%s\n70\n%s' % (self._common(), self.flag)
        for point in self.points:
            result += '\n0\nVERTEX\n%s' % _point(point)
            if self.width:
                result += '\n40\n%s\n41\n%s' % (self.width, self.width)
        result += '\n0\nSEQEND'
        return result


class Point(_Entity):
    """Colored solid fill."""

    def __init__(self, points=None, **common):
        _Entity.__init__(self, **common)
        self.points = points

    def __str__(self):
        result = '0\nPOINT\n%s' % (self._common())
        result += '\n%s' % _point(self.points)
        return result


class Solid(_Entity):
    """Colored solid fill."""

    def __init__(self, points=None, **common):
        _Entity.__init__(self, **common)
        self.points = points

    def __str__(self):
        return '\n'.join(['0\nSOLID', self._common()] +
                         _points(self.points[:2] + [self.points[3], self.points[2]]))


class Text(_Entity):
    """Single text line."""

    def __init__(self, text='', point=(0, 0, 0), alignment=None,
                 flag=None, height=1, justifyhor=None, justifyver=None,
                 rotation=None, obliqueAngle=None, style=None, xscale=None,
                 **common):
        _Entity.__init__(self, **common)
        self.text = text
        self.point = point
        self.alignment = alignment
        self.flag = flag
        self.height = height
        self.justifyhor = justifyhor
        self.justifyver = justifyver
        self.rotation = rotation
        self.obliqueAngle = obliqueAngle
        self.style = style
        self.xscale = xscale

    def __str__(self):
        result = '0\nTEXT\n%s\n%s\n40\n%s\n1\n%s' % (self._common(),
                                                     _point(self.point), self.height, self.text)
        if self.rotation:
            result += '\n50\n%s' % self.rotation
        if self.xscale:
            result += '\n41\n%s' % self.xscale
        if self.obliqueAngle:
            result += '\n51\n%s' % self.obliqueAngle
        if self.style:
            result += '\n7\n%s' % self.style
        if self.flag:
            result += '\n71\n%s' % self.flag
        if self.justifyhor:
            result += '\n72\n%s' % self.justifyhor
        if self.alignment:
            result += '\n%s' % _point(self.alignment, 1)
        if self.justifyver:
            result += '\n73\n%s' % self.justifyver
        return result


class Mtext(Text):
    """Surrogate for mtext, generates some Text instances."""

    def __init__(self, text='', point=(0, 0, 0), width=250,
                 spacingFactor=1.5, down=0, spacingWidth=None, **options):
        Text.__init__(self, text=text, point=point, **options)
        if down:
            spacingFactor *= -1
        self.spacingFactor = spacingFactor
        self.spacingWidth = spacingWidth
        self.width = width
        self.down = down

    def __str__(self):
        texts = self.text.replace('\r\n', '\n').split('\n')
        if not self.down:
            texts.reverse()
        result = ''
        x = y = 0
        if self.spacingWidth:
            spacingWidth = self.spacingWidth
        else:
            spacingWidth = self.height * self.spacingFactor
        for text in texts:
            while text:
                result += '\n%s' % Text(text[:self.width],
                                        point=(self.point[0] + x * spacingWidth,
                                               self.point[1] + y * spacingWidth,
                                               self.point[2]),
                                        alignment=self.alignment, flag=self.flag,
                                        height=self.height,
                                        justifyhor=self.justifyhor, justifyver=self.justifyver,
                                        rotation=self.rotation, obliqueAngle=self.obliqueAngle,
                                        style=self.style, xscale=self.xscale, parent=self)
                text = text[self.width:]
                if self.rotation:
                    x += 1
                else:
                    y += 1
        return result[1:]


##class _Mtext(_Entity):
##    """Mtext not functioning for minimal dxf."""
##    def __init__(self,text='',point=(0,0,0),attachment=1,
##                 charWidth=None,charHeight=1,direction=1,height=100,rotation=0,
##                 spacingStyle=None,spacingFactor=None,style=None,width=100,
##                 xdirection=None,**common):
##        _Entity.__init__(self,**common)
##        self.text=text
##        self.point=point
##        self.attachment=attachment
##        self.charWidth=charWidth
##        self.charHeight=charHeight
##        self.direction=direction
##        self.height=height
##        self.rotation=rotation
##        self.spacingStyle=spacingStyle
##        self.spacingFactor=spacingFactor
##        self.style=style
##        self.width=width
##        self.xdirection=xdirection
##    def __str__(self):
##        input=self.text
##        text=''
##        while len(input)>250:
##            text+='\n3\n%s'%input[:250]
##            input=input[250:]
##        text+='\n1\n%s'%input
##        result= '0\nMTEXT\n%s\n%s\n40\n%s\n41\n%s\n71\n%s\n72\n%s%s\n43\n%s\n50\n%s'%\
##                (self._common(),_point(self.point),self.charHeight,self.width,
##                 self.attachment,self.direction,text,
##                 self.height,
##                 self.rotation)
##        if self.style:result+='\n7\n%s'%self.style
##        if self.xdirection:result+='\n%s'%_point(self.xdirection,1)
##        if self.charWidth:result+='\n42\n%s'%self.charWidth
##        if self.spacingStyle:result+='\n73\n%s'%self.spacingStyle
##        if self.spacingFactor:result+='\n44\n%s'%self.spacingFactor
##        return result

# ---tables


class Block(_Collection):
    """Use list methods to add entities, eg append."""

    def __init__(self, name, layer='0', flag=0, base=(0, 0, 0), entities=[]):
        self.entities = copy.copy(entities)
        _Collection.__init__(self, entities)
        self.layer = layer
        self.name = name
        self.flag = 0
        self.base = base

    def __str__(self):
        e = '\n'.join([str(x) for x in self.entities])
        return '0\nBLOCK\n8\n%s\n2\n%s\n70\n%s\n%s\n3\n%s\n%s\n0\nENDBLK' % (
            self.layer, self.name.upper(), self.flag, _point(self.base),
            self.name.upper(), e)


class Layer(_Call):
    """Layer"""

    def __init__(self, name='pydxf', color=7, lineType='continuous',
                 flag=64):
        self.name = name
        self.color = color
        self.lineType = lineType
        self.flag = flag

    def __str__(self):
        return '0\nLAYER\n2\n%s\n70\n%s\n62\n%s\n6\n%s' % (self.name.upper(),
                                                           self.flag, self.color, self.lineType)


class LineType(_Call):
    """Custom linetype"""

    def __init__(self, name='continuous', description='Solid line',
                 elements=[], flag=64):
        # TODO: Implement lineType elements
        self.name = name
        self.description = description
        self.elements = copy.copy(elements)
        self.flag = flag

    def __str__(self):
        return '0\nLTYPE\n2\n%s\n70\n%s\n3\n%s\n72\n65\n73\n%s\n40\n0.0' % (
            self.name.upper(), self.flag, self.description,
            len(self.elements))


class Style(_Call):
    """Text style"""

    def __init__(self, name='standard', flag=0, height=0, widthFactor=40,
                 obliqueAngle=50, mirror=0, lastHeight=1, font='arial.ttf',
                 bigFont=''):
        self.name = name
        self.flag = flag
        self.height = height
        self.widthFactor = widthFactor
        self.obliqueAngle = obliqueAngle
        self.mirror = mirror
        self.lastHeight = lastHeight
        self.font = font
        self.bigFont = bigFont

    def __str__(self):
        return ('0\nSTYLE\n2\n%s\n70\n%s\n40\n%s\n41\n%s\n50\n%s\n71'
                '\n%s\n42\n%s\n3\n%s\n4\n%s' % (self.name.upper(),
                                                self.flag, self.flag,
                                                self.widthFactor, self.obliqueAngle, self.mirror,
                                                self.lastHeight, self.font.upper(), self.bigFont.upper()))


class View(_Call):
    def __init__(self, name, flag=0, width=1, height=1, center=(0.5, 0.5),
                 direction=(0, 0, 1), target=(0, 0, 0), lens=50,
                 frontClipping=0, backClipping=0, twist=0, mode=0):
        self.name = name
        self.flag = flag
        self.width = width
        self.height = height
        self.center = center
        self.direction = direction
        self.target = target
        self.lens = lens
        self.frontClipping = frontClipping
        self.backClipping = backClipping
        self.twist = twist
        self.mode = mode

    def __str__(self):
        return ('0\nVIEW\n2\n%s\n70\n%s\n40\n%s\n%s\n41\n%s\n%s\n%s\n42\n%s'
                '\n43\n%s\n44\n%s\n50\n%s\n71\n%s' % (self.name,
                                                      self.flag, self.height, _point(self.center), self.width,
                                                      _point(self.direction, 1), _point(self.target, 2),
                                                      self.lens, self.frontClipping, self.backClipping,
                                                      self.twist, self.mode))


def ViewByWindow(name, leftBottom=(0, 0), rightTop=(1, 1), **options):
    width = abs(rightTop[0] - leftBottom[0])
    height = abs(rightTop[1] - leftBottom[1])
    center = ((rightTop[0] + leftBottom[0]) * 0.5,
              (rightTop[1] + leftBottom[1]) * 0.5)
    return View(name=name, width=width, height=height, center=center,
                **options)


# ---drawing


class Drawing(_Collection):
    """Dxf drawing. Use append or any other list methods to add objects."""

    def __init__(self, insbase=(0.0, 0.0, 0.0), extmin=(0.0, 0.0),
                 extmax=(0.0, 0.0), layers=[Layer()], linetypes=[LineType()],
                 styles=[Style()], blocks=[], views=[], entities=None,
                 fileName='test.dxf'):
        # TODO: replace list with None,arial
        entities = entities or []
        _Collection.__init__(self, entities)
        self.insbase = insbase
        self.extmin = extmin
        self.extmax = extmax
        self.layers = copy.copy(layers)
        self.linetypes = copy.copy(linetypes)
        self.styles = copy.copy(styles)
        self.views = copy.copy(views)
        self.blocks = copy.copy(blocks)
        self.fileName = fileName
        # private
        self.acadver = '9\n$ACADVER\n1\nAC1006'

    def _name(self, x):
        """Helper function for self._point"""
        return '9\n$%s' % x.upper()

    def _point(self, name, x):
        """Point setting from drawing like extmin,extmax,..."""
        return '%s\n%s' % (self._name(name), _point(x))

    def _section(self, name, x):
        """Sections like tables,blocks,entities,..."""
        if x:
            xstr = '\n' + '\n'.join(x)
        else:
            xstr = ''
        return '0\nSECTION\n2\n%s%s\n0\nENDSEC' % (name.upper(), xstr)

    def _table(self, name, x):
        """Tables like ltype,layer,style,..."""
        if x:
            xstr = '\n' + '\n'.join(x)
        else:
            xstr = ''
        return '0\nTABLE\n2\n%s\n70\n%s%s\n0\nENDTAB' % (name.upper(),
                                                         len(x), xstr)

    def __str__(self):
        """Returns drawing as dxf string."""
        header = [self.acadver] + [self._point(attr, getattr(self, attr))
                                   for attr in _HEADER_POINTS]
        header = self._section('header', header)
        tables = [self._table('ltype', [str(x) for x in self.linetypes]),
                  self._table('layer', [str(x) for x in self.layers]),
                  self._table('style', [str(x) for x in self.styles]),
                  self._table('view', [str(x) for x in self.views])]
        tables = self._section('tables', tables)
        blocks = self._section('blocks', [str(x) for x in self.blocks])
        entities = self._section('entities', [str(x) for x in self.entities])
        return '\n'.join([header, tables, blocks, entities, '0\nEOF\n'])

    def saveas(self, fileName):
        self.fileName = fileName
        self.save()

    def save(self):
        test = open(self.fileName, 'w')
        test.write(str(self))
        test.close()


# ---extras
class Rectangle(_Entity):
    """Rectangle, creates lines."""

    def __init__(self, point=(0, 0, 0), width=1, height=1, solid=None,
                 line=1, **common):
        _Entity.__init__(self, **common)
        self.point = point
        self.width = width
        self.height = height
        self.solid = solid
        self.line = line

    def __str__(self):
        result = ''
        points = [self.point,
                  (self.point[0] + self.width, self.point[1], self.point[2]),
                  (self.point[0] + self.width, self.point[1] + self.height,
                   self.point[2]),
                  (self.point[0], self.point[1] + self.height, self.point[2]),
                  self.point]
        if self.solid:
            result += '\n%s' % Solid(points=points[:-1], parent=self.solid)
        if self.line:
            for i in range(4):
                result += '\n%s' % Line(points=[points[i], points[i + 1]],
                                        parent=self)
        return result[1:]


class LineList(_Entity):
    """Like polyline, but built of individual lines."""

    def __init__(self, points=[], closed=0, **common):
        _Entity.__init__(self, **common)
        self.closed = closed
        self.points = copy.copy(points)

    def __str__(self):
        if self.closed:
            points = self.points + [self.points[0]]
        else:
            points = self.points
        result = ''
        for i in range(len(points) - 1):
            result += '\n%s' % Line(points=[points[i], points[i + 1]],
                                    parent=self)
        return result[1:]


PolyLine = LineList


# ---test


def main():
    # Blocks
    b = Block('test')
    b.append(Solid(points=[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
                   color=1))
    b.append(Arc(center=(1, 0, 0), color=2))

    # Drawing
    d = Drawing()
    # tables
    d.blocks.append(b)  # table blocks
    d.styles.append(Style())  # table styles
    d.views.append(View('Normal'))  # table view
    d.views.append(ViewByWindow('Window', leftBottom=(1, 0),
                                rightTop=(2, 1)))  # idem

    # entities
    d.append(Circle(center=(1, 1, 0), color=3))
    d.append(Face(points=[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
                  color=4))
    d.append(Insert('test', point=(3, 3, 3), cols=5, colspacing=2))
    d.append(Line(points=[(0, 0, 0), (1, 1, 1)]))
    d.append(Mtext('Click on Ads\nmultiple lines with mtext',
                   point=(1, 1, 1), color=5, rotation=90))
    d.append(Text('Please donate!', point=(3, 0, 1)))
    d.append(Rectangle(point=(2, 2, 2), width=4, height=3, color=6,
                       solid=Solid(color=2)))
    d.append(Solid(points=[(4, 4, 0), (5, 4, 0), (7, 8, 0), (9, 9, 0)],
                   color=3))
    d.append(PolyLine(points=[(1, 1, 1), (2, 1, 1), (2, 2, 1), (1, 2, 1)],
                      closed=1, color=1))

    d.saveas('test.dxf')


if __name__ == '__main__':
    main()
