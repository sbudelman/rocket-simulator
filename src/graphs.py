import matplotlib.pyplot as plt
import numpy as np
import math as m

MAX_ROWS = 3

class GraphHandler:
    def __init__(self, **kwargs):
        self.data_size = kwargs.get('size', [0, 0])
        self._max_rows = MAX_ROWS
        self.rows = min(self.data_size[0], self._max_rows) 
        self.cols = m.ceil(self.data_size[0]/self._max_rows)
        self.data_array = np.zeros((self.data_size[1], self.data_size[0]))
        self.fig, self.axs = plt.subplots(self.rows, self.cols)
        self.fig.subplots_adjust(hspace=1.5)

        self._current_idx = 0
        self._plot_idx = 0

    def collect(self, array):
        self.data_array[self._current_idx] = array
        self._current_idx += 1

    def define_plot(self, x_col, y_col, **kwargs):
        plot_row = m.floor(self._plot_idx / self.cols)
        plot_col = self._plot_idx % self.cols
        ax = self.axs[plot_row][plot_col]
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
