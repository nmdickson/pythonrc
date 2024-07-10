'''Various plotting functionalities'''


__all__ = ['add_watermark', 'add_anchor', 'Field', 'SkyField']


# --------------------------------------------------------------------------
# Add pieces to a plot
# --------------------------------------------------------------------------


def add_watermark(fig, text='DRAFT', fs=40):
    '''add a transparent watermark to a figure'''

    return fig.text(0.5, 0.5, text, transform=fig.transFigure,
                    fontsize=fs, color='gray', alpha=0.5,
                    ha='center', va='center', rotation=30)


def add_anchor(ax, text, loc='upper right', *args, **kwargs):
    '''add an anchored textbox to an ax'''
    from matplotlib.offsetbox import AnchoredText

    at = AnchoredText(text, loc=loc, *args, **kwargs)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")

    ax.add_artist(at)

    return at


# --------------------------------------------------------------------------
# Plotting of arbitrary geometries
# --------------------------------------------------------------------------


class Field:

    def __init__(self, coords):
        import numpy as np
        from shapely import ops
        import shapely.geometry as geom

        # ------------------------------------------------------------------
        # Parse the coords argument
        # ------------------------------------------------------------------

        # if already a polygon, assume its already been corrected
        if isinstance(coords, geom.Polygon):
            self._multi = False
        elif isinstance(coords, geom.MultiPolygon):
            self._multi = True
            coords = coords.geoms

        # is a single polygon of coordinates
        elif isinstance(coords, np.ndarray) and coords.ndim == 2:
            self._multi = False
            # coords = (coords << u.Unit(unit)).value

        # assume it's iterable of coords or polygons
        else:
            self._multi = True
            # coords = (coords << u.Unit(unit)).value

        # ------------------------------------------------------------------
        # Set up the polygons
        # ------------------------------------------------------------------

        # Combine and smooth all polygons
        if self._multi:
            self.polygon = ops.unary_union([geom.Polygon(c).buffer(0)
                                            for c in coords])
        else:
            self.polygon = geom.Polygon(coords).buffer(0)

        # Explicitly check the polygons again, as they sometimes change above
        if isinstance(self.polygon, geom.Polygon):
            self._multi = False

        elif isinstance(self.polygon, geom.MultiPolygon):
            self._multi = True

    # ----------------------------------------------------------------------
    # Plotting functionality
    # ----------------------------------------------------------------------

    def _patch(self, *args, **kwargs):
        '''Create a `PathPatch` based on the polygon boundaries'''
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch

        if self.polygon.is_empty:
            raise ValueError("This Field is empty, cannot create patch")

        coords, codes = [], []
        for poly in (self.polygon.geoms if self._multi else [self.polygon]):

            for line in [poly.exterior, *poly.interiors]:

                coords += line.coords

                codes += [Path.MOVETO]
                codes += ([Path.LINETO] * (len(line.coords) - 2))
                codes += [Path.CLOSEPOLY]

        path = Path(coords, codes)

        return PathPatch(path, *args, **kwargs)

    def plot(self, ax, prev_sample=False, adjust_view=True, **kwargs):
        '''Plot this field onto a given ax as a polygonal patch'''

        pt = ax.add_patch(self._patch(**kwargs))

        if adjust_view:
            ax.autoscale_view()

        return pt


class SkyField(Field):

    def __init__(self, wrap=True, **kwargs):
        import numpy as np
        import astropy.units as u
        from astropy.coordinates import SkyCoord

        self.skycoord = SkyCoord(**kwargs)

        self.wrapped = wrap
        # TODO rather than wrapping, should cut at 0,360 and make multi polygon

        frame = self.skycoord.name

        # TODO is there really no better way to get the coords from skycoord?
        if frame == 'icrs':
            x, y = self.skycoord.ra, self.skycoord.dec

        elif frame == 'galactic':
            x, y = self.skycoord.l, self.skycoord.b

        else:
            raise ValueError('idk how to plot this frame, use ra/dec or l/b')

        if wrap:
            x = x.wrap_at(180 * u.deg)

            self.skycoord = ()

        super().__init__(np.c_[x, y].value)
