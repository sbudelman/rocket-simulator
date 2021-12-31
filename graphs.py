import matplotlib.pyplot as plt
import numpy as np


class GraphHandler:
    def __init__(self, n_plots, **kwargs):
        self.rows = n_plots
        self.cols = 1
        self.data_size = kwargs.get('size', [0, 0])
        self.data_array = np.zeros((self.data_size[1], self.data_size[0]))
        
        self.fig, self.axs = plt.subplots(self.rows, self.cols)
        self.fig.subplots_adjust(hspace=1.5)

        self._current_idx = 0
        self._plot_idx = 0

    def collect(self, array):
        self.data_array[self._current_idx] = array
        self._current_idx += 1

    def define_plot(self, x_col, y_col, **kwargs):
        ax = self.axs[self._plot_idx]
        # We use self._current_idx - 1 to remove initialized rows that weren't used
        ax.plot(self.data_array[:self._current_idx - 1,x_col], self.data_array[:self._current_idx - 1,y_col])
        ax.set_xlabel(kwargs.get('xlabel', ''))
        ax.set_ylabel(kwargs.get('ylabel', ''))
        ax.set_title(kwargs.get('title', ''))
        ax.grid(True)
        self._plot_idx += 1
        return ax

    def show(self):
        plt.show()
