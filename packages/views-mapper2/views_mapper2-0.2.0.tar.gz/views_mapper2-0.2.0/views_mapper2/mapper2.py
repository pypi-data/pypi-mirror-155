from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as ctx


from views_mapper2 import color
from views_mapper2 import utils


class Mapper2:
    """
    Modified version of Mapper1.
    `Map` takes basic properties and allows the user to consecutively add
    layers to the Map object. This makes it possible to prepare mapping
    "presets" at any level of layeredness that can be built on further.

    Mapper2 allows for the customizable addition of scaling to the map.
    Map scale sets the scales to a custom range, displays values of the variable as is.
    Map dictionary sets both scale and labels to custom.
    Map dictionary writer can be used to create dictionaries from scale values.
    Background allows for Background map and labels sandwiching of the map using the Standard Stamen Design tiles
    from  Open Street Map project.

    Attributes
    ----------
    width: Integer value for width in inches.
    height: Integer value for height in inches.
    bbox: List for the bbox per [xmin, xmax, ymin, ymax].
    frame_on: Bool for whether to draw a frame around the map.
    title: Optional default title at matplotlib's default size.
    figure: Optional tuple of (fig, size) to use if you want to plot into an
        already existing fig and ax, rather than making a new one.
    """

    def __init__(
            self,
            width,
            height,
            bbox=None,
            cmap=None,
            frame_on=True,
            title="",  # Default title without customization. (?)
            figure=None,
    ):
        self.width = width
        self.height = height
        self.bbox = bbox  # xmin, xmax, ymin, ymax
        self.cmap = cmap
        if figure is None:
            self.fig, self.ax = plt.subplots(figsize=(self.width, self.height))
        else:
            self.fig, self.ax = figure
        self.texts = []
        self.ax.set_title(title)

        if frame_on:  # Remove axis ticks only.
            self.ax.tick_params(
                top=False,
                bottom=False,
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
            )
        else:
            self.ax.axis("off")

        if bbox is not None:
            self.ax.set_xlim((self.bbox[0], self.bbox[1]))
            self.ax.set_ylim((self.bbox[2], self.bbox[3]))

    def add_layer(self, gdf, map_scale=False, map_dictionary=None, background=None, cmap=None, **kwargs):
        """Add a geopandas plot to a new layer.

        Parameters
        ----------
        gdf: Geopandas GeoDataFrame to plot.
        cmap: Optional matplotlib colormap object or string reference
            (e.g. "viridis"). Defaults to rainbow if not specified.
        map_scale: set a manual scale for the map. If missing defaults to the Remco procedure.
        map_dictionary: set manual labels for the map. If missing defaults to Remco procedure
        note preferentially looking for map_dictionary, then map_scale, and then Remco default
        no need to use ticklabel and tickvalue commands as the code is subsumed within Mapper2
        Refer to dictionary writer for easy code for
        **kwargs: Geopandas `.plot` keyword arguments.
        """
        if "color" in kwargs:
            colormap = None
        else:
            colormap = 'rainbow' if cmap is None else cmap
            if "column" in kwargs:
                if hasattr(self, "cax"):
                    self.cax.remove()
                if "vmin" not in kwargs:
                    self.vmin = gdf[kwargs["column"]].min()
                else:
                    self.vmin = kwargs["vmin"]
                if "vmax" not in kwargs:
                    self.vmax = gdf[kwargs["column"]].max()
                else:
                    self.vmax = kwargs["vmax"]

                if map_dictionary is not None:
                    Mapper2.add_colorbar(self, colormap, min(map_dictionary.values()), max(map_dictionary.values()),
                                         tickparams=map_dictionary)
                else:
                    try:
                        Mapper2.add_colorbar(self, colormap, min(map_scale), max(map_scale))
                    except:
                        Mapper2.add_colorbar(self, colormap, self.vmin, self.vmax)

        if map_dictionary is not None:
            self.ax = gdf.plot(ax=self.ax, cmap=colormap, vmin=min(map_dictionary.values()),
                               vmax=max(map_dictionary.values()), **kwargs)
        else:
            try:
                self.ax = gdf.plot(ax=self.ax, cmap=colormap, vmin=min(map_scale), vmax=max(map_scale), **kwargs)
            except:
                self.ax = gdf.plot(ax=self.ax, cmap=colormap, **kwargs)

        if background is not None:
            Mapper2.add_background(self, gdf, background)

        return self

    def add_colorbar(
            self,
            cmap,
            vmin,
            vmax,
            location="right",
            size="5%",
            pad=0.1,
            alpha=1,
            labelsize=16,
            tickparams=None,
    ):
        """Add custom colorbar to Map.

        Needed since GeoPandas legend and plot axes do not align, see:
        https://geopandas.readthedocs.io/en/latest/docs/user_guide/mapping.html

        Parameters
        ----------
        cmap: Matplotlib colormap object or string reference (e.g. "viridis").
        vmin: Minimum value of range colorbar.
        vmax: Maximum value of range colorbar.
        location: String for location of colorbar: "top", "bottom", "left"
            or "right".
        size: Size in either string percentage or number of pixels.
        pad: Float for padding between the plot's frame and colorbar.
        alpha: Float for alpha to apply to colorbar.
        labelsize: Integer value for the text size of the ticklabels.
        tickparams: Dictionary containing value-label pairs. For example:
            {0.05: "5%", 0.1: "10%"}
        """
        norm = plt.Normalize(vmin, vmax)
        if isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)
        cmap = color.force_alpha_colormap(cmap=cmap, alpha=alpha)
        scalar_to_rgba = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        divider = make_axes_locatable(self.ax)
        self.cax = divider.append_axes(location, size, pad)
        self.cax.tick_params(labelsize=labelsize)

        tickvalues = (
            list(tickparams.values()) if tickparams is not None else None
        )
        self.cbar = plt.colorbar(
            scalar_to_rgba, cax=self.cax, ticks=tickvalues
        )
        if tickparams is not None:
            self.cbar.set_ticklabels(list(tickparams.keys()))
        return self

    def save(
            self, path, dpi=200, **kwargs
    ):  # Just some defaults to reduce work.
        """Save Map figure to file.
        Parameters
        ----------
        path: String path, e.g. "./example.png".
        dpi: Integer dots per inch. Increase for higher resolution figures.
        **kwargs: Matplotlib `savefig` keyword arguments.
        """
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
        plt.close(self.fig)

    def add_views_textbox(self, text, textsize=15):
        """Add ViEWS textbox to figure. Logo and url are hardcoded.
        Parameters
        ----------
        text: String text. Note that newlines can be used, for example:
            "Model A\nr_2021_12_01"
        textsize: Integer for textsize.
        """
        utils.add_textbox_to_ax(self.fig, self.ax, text, textsize)
        return self

    def add_background(self, gdf, background):
        # this uses the Stamen build in maps
        if background == 'grey':
            ctx.add_basemap(self.ax, crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLite)
            ctx.add_basemap(self.ax, crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLabels)
        if background == 'color':
            ctx.add_basemap(self.ax, crs=gdf.crs.to_string(), source=ctx.providers.Stamen.Watercolor)
            ctx.add_basemap(self.ax, crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLabels)