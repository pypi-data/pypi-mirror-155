#!/usr/bin/env python3

#
###############################################################################
# The MIT License (MIT)

# Copyright (c)  2022 Philip Heringlake

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################


from inspect import isfunction
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from matplotlib.widgets import Slider
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

try:
    import ipywidgets as widgets
except:
    ImportError("Could not import ipywidgets. Can not be used in jupyter notebook")

slider_height_inches = 0.1


class lineplot(object):
    """Single line plot instance"""

    def __init__(self, ax, x, data, parameters,fix_lim=False, **kwargs):
        """

        Arguments:
        - `ax`: axis instance
        - `x`: x values
        - `data`: data array to be sliced
        - `parameters`: dimension parameters (len = ndim-1)
        - `fix_lim` (False) : wether to update the axes' limits or keep them fixed
        - `kwargs` : keyword arguments to pass to plot function
        """
        self._ax = ax
        self._data = data
        self._dimvar = {}
        self._parameters = parameters
        self.fix_lim=fix_lim
        self._kwargs=kwargs

        self._datisfun = isfunction(data)

        if not isfunction(data) and len(data.shape) - 1 != len(parameters):
            raise (Exception("not enough dimension parameters "))

        self._vnames = [v.name for v in parameters]
        for v in parameters:
            self._dimvar[v.name] = v

        (self.line,) = self._ax.plot(x, self.get_line(), **kwargs)

    def get_line(self):
        if self._datisfun:
            vdict = {}
            for v in self._parameters:
                vdict[v.name] = v.value
            return self._data(**vdict)
        else:
            idx = tuple([v.value for v in self._parameters])
            return self._data[idx]

    def vchanged(self):
        for v in self._parameters:
            if v.changed():
                return True
        return False

    def plot(self):
        if self.vchanged():
            self.line.set_ydata(self.get_line())
            if self.fix_lim:
                return
            self._ax.relim()
            self._ax.autoscale_view()
        return


class plot2d(object):
    """"""

    def __init__(self, ax, cax, x, y, data, parameters, **kwargs):
        """

        Arguments:
        - `ax`:
        - `x`:
        - `y`:
        - `data`:
        - `parameters`:
        - `**kwargs`:
        """
        self._ax = ax
        self._x = x
        self._y = y
        self._data = data
        self._parameters = parameters
        self._dimvar = {}

        if len(data.shape) - 2 != len(parameters):
            raise (Exception("not enough or too many dimension parameters "))

        self._vnames = [v.name for v in parameters]
        for v in parameters:
            self._dimvar[v.name] = v

        if not "origin" in kwargs:
            kwargs["origin"] = "lower"
        self.im = self._ax.imshow(
            self.get_map(), extent=[x.min(), x.max(), y.min(), y.max()], **kwargs
        )
        self.cb = plt.colorbar(self.im, cax=cax)

    def get_map(self):
        idx = tuple([v.value for v in self._parameters])
        ldat = self._data[idx]
        return ldat

    def vchanged(self):
        for v in self._parameters:
            if v.changed():
                return True
        return False

    def plot(self):
        if self.vchanged():
            data = self.get_map()
            self.im.set_data(data)
            self._ax.relim()
            self.im.set_clim(data.min(), data.max())
            self._ax.autoscale_view()
        return


class dimvar(object):
    """Manipulatable variable"""

    def __init__(self, name, vmin=0, vmax=None, vstep=1):
        """

        Arguments:
        - `name`:
        - `vmin`:
        - `vmax`:
        """
        self.name = name
        self.vmin = vmin
        self.vmax = vmax
        self.vstep = vstep
        self._value = 0
        self._slider = None
        self._changed = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.vmin < new_value < self.vmax:
            print("Value invalid")
            return
        else:
            self._value = new_value

    def add_slider(self, slider):
        self._slider = slider

    def get_changed(self):
        if isinstance(self._slider, Slider):
            new_val = self._slider.val  # matplotlib
        else:
            new_val = self._slider.value  # ipywidget
        if new_val != self._value:
            self._value = new_val
            self._changed = True
        else:
            self._changed = False

    def changed(self):
        return self._changed


class ifigure(object):
    """Interactive figure instance

    Create a collection of subplots arranged with GridSpec that update
    automatically when using the sliders in the bottom part of the figure.
    """

    def __init__(self, rows, columns, jupyterwidget=False,**kwargs):
        """

        Arguments:
        - `rows`: Number of plot rows (as for GridSpec)
        - `columns`: Number of plot columns
        - `**kwargs`: keyword arguments:
                    `jupyterwidget` (boolean) -- If true create slider as jupyter widgets instead of
                                                 using matplotlib sliders
        """
        self._rows = rows
        self._columns = columns
        self._kwargs = kwargs
        self._jw = jupyterwidget

        self.fg = plt.figure(constrained_layout=True,**kwargs)
        if not self._jw:
            self.gs0 = GridSpec(2, 1, figure=self.fg, height_ratios=[4, 1])
            self.gs = GridSpecFromSubplotSpec(
                rows, columns, subplot_spec=self.gs0[0, :]
            )
            self.gss = GridSpecFromSubplotSpec(1, 1, subplot_spec=self.gs0[1, :])
        else:
            self.gs0 = None
            self.gs = GridSpec(rows, columns, figure=self.fg)
            self.gss = None
        self.axs = dict()
        self.parameters = dict()
        self.plots = []
        self._axpos = []
        self.saxs = []

    def add_plot(self, axpos, x, data, parameters, plot_ax=0, twinx=False, **kwargs):
        """Add a single line plot to one of the figures axis
        Keyword Arguments:
        axpos     -- list indicating the axis position (e.g. [0,0] for the upper left plot)/
                     Use numpys indexing syntax to span multiple rows/columns as::
                        np.s_[:,0]
        x         -- x values for line plot, a list of two 1d arrays [x,y] for a 2d plot
        data      -- data to plot. Either a multidimensional array with ndim=len(parameters)+1
                     for a lineplot (+2 for 2d plot), or a function returning either a line or 2d data.
        parameters -- list of the parameters to change. A variable can either be a single string
                     or a list containing name,minimum value(default 0), maximum value (default size
                     of data for the corresponding dimension when array, 1 when data is function),
                     step size (default 1).
        plot_ax (0) -- Axis to cut along. If data is a function returning a 2D array,
                       plot_ax needs to be a list of length 2 in order to create a 2d plot.
        **kwargs  -- keyword arguments to pass to the plot function

        Returns:
        ax  -- Matplotlib subplot axis instance where plot is created.
        """

        axposn = f"{axpos}"
        axposn += "y" if twinx else ""
        is2d = isinstance(plot_ax, list) and len(plot_ax) > 1
        if not axposn in self.axs:
            if twinx and not axposn[:-1] in self.axs:
                return self.add_plot(
                    axpos, x, data, parameters, plot_ax, False, **kwargs
                )
            elif twinx:
                ax = self.axs[axposn[:-1]].twinx()
            else:
                if not is2d:
                    ax = self.fg.add_subplot(self.gs[tuple(axpos)])
                else:
                    subgs = GridSpecFromSubplotSpec(
                        1, 2, self.gs[tuple(axpos)], width_ratios=[15, 1]
                    )
                    ax = self.fg.add_subplot(subgs[:, 0])
                    cax = self.fg.add_subplot(subgs[:, 1])
            self.axs[axposn] = ax
            if is2d:
                self.axs[axposn + "cax"] = cax
        else:
            ax = self.axs[axposn]
            if is2d:
                cax = self.axs[axposn + "cax"]

        ## Bring data in right shape and create list of scan parameters
        ##

        datisfun = isfunction(data)
        if not datisfun:
            if is2d:
                data = np.moveaxis(
                    data, plot_ax, (len(data.shape) - 2, len(data.shape) - 1)
                )
            else:
                data = np.moveaxis(data, plot_ax, len(data.shape) - 1)
        varlist = []
        for ii, v in enumerate(parameters):
            vmin = 0
            vmax = data.shape[ii] - 1 if not datisfun else 1
            vstep = 1
            name = ""
            if isinstance(v, list):
                name = v[0]
                if len(v) >= 2:
                    vmin = v[1]
                if len(v) >= 3:
                    vmax = v[2]
                if len(v) >= 4:
                    vstep = v[3]
            elif isinstance(v, str):
                name = v
            self._add_var(name, vmin, vmax, vstep=vstep)
            varlist.append(self.parameters[name])

        if is2d:
            self.plots.append(plot2d(ax, cax, x[0], x[1], data, varlist, **kwargs))
        else:
            self.plots.append(lineplot(ax, x, data, varlist, **kwargs))
        return ax

    def _add_var(self, vname, vmin, vmax, vstep):
        if not vname in self.parameters.keys():
            self.parameters[vname] = dimvar(vname, vmin, vmax, vstep)
            fs = self.fg.get_size_inches()
            self.fg.set_size_inches([fs[0], fs[1] + slider_height_inches])

    def show(self):
        """Create the figure and display it

        Needs to be called after all plots are added to the figure, as this is
        where all sliders are created and the size of the final plot can be adapted.

        """
        vlen = len(self.parameters)

        if not self._jw:
            self.gss = GridSpecFromSubplotSpec(vlen, 1, self.gs0[1, 0])

        for i, v in enumerate(self.parameters.items()):
            if not self._jw:
                ax = self.fg.add_subplot(self.gss[i, :])
                self.saxs.append(ax)
                sl = Slider(
                    ax,
                    v[0],
                    v[1].vmin,
                    v[1].vmax,
                    valinit=v[1].vmin,
                    valstep=v[1].vstep,
                )
                sl.on_changed(self.update)
            else:
                if v[1].vstep == 1:
                    sl = widgets.IntSlider(
                        min=v[1].vmin, max=v[1].vmax, step=v[1].vstep, description=v[0]
                    )
                else:
                    sl = widgets.FloatSlider(
                        min=v[1].vmin, max=v[1].vmax, step=v[1].vstep, description=v[0]
                    )
                sl.observe(self.update, names="value")
                display(sl)
            v[1].add_slider(sl)
        # self.fg.subplots_adjust(left=0.15, bottom=0.25)
        plt.show()

    def update(self, val):
        for v in self.parameters.values():
            v.get_changed()
        for plot in self.plots:
            plot.plot()
        self.fg.canvas.draw()
