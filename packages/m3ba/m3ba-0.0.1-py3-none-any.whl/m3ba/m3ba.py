"""
Python library to perform plots and analysis on MD data.

----------------
Version history:
- Version 0.0.1 - 15/06/2022 : The very beginning

"""

__version__ = '0.0.1'
__author__ = 'M3B'


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm
from scipy.stats import shapiro
import os
import seaborn as sns

default_colors = ['k', 'r', 'g', 'b', 'c', 'm', 'y' ]

def plot_compare(sims, xlabel=None, ylabel=None, title=None, ylim=None, xlim=None, subplot=False, fig=None, axs=None, ax=0, colors=None, timeseries=True, xcol=0, ycol=1):
    """
    Function to plot the comparison among different data
    ;sims is a list of arrays containing the data to be plotted
    """

    if timeseries:
        k = 1000 # data are supposed to be in ps; in this way the x axis should be in ns
    else:
        k = 1

    if not colors:
        colors = default_colors[:len(sims)]

    # in case of standartd plot
    if not subplot:
        for cnt, sim in enumerate(sims):
            plt.plot(sim[:,xcol]/k,  sim[:,ycol],  color=colors[cnt])

            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)

            if ylim:
                plt.ylim(ylim)

            if xlim:
                plt.xlim(xlim)

    # in case of subplot
    else:
        for cnt, sim in enumerate(sims):
            axs[ax].plot(sim[:,xcol]/k,  sim[:,ycol],  color=colors[cnt])

            axs[ax].set_xlabel(xlabel)
            axs[ax].set_ylabel(ylabel)
            axs[ax].set_title(title)

        if ylim:
            axs[ax].set_ylim(ylim)

        if xlim:
            axs[ax].set_xlim(xlim)


if __name__ == "__main__":
#run as stand alone script
    print ("hello")
