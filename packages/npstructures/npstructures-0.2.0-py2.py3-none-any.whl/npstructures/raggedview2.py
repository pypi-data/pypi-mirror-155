import numpy as np
from numbers import Number
from dataclasses import dataclass


@dataclass
class RaggedView2:
    starts: np.ndarray
    lengths: np.ndarray
    col_step: int = 1
    _dtype: int = np.int64

    def __post_init__(self):
        self.starts = np.atleast_1d(self.starts)
        self.lengths = np.atleast_1d(self.lengths)

    @property
    def n_rows(self):
        if isinstance(self.starts, Number):
            return 1
        return len(self.starts)

    def row_slice(self, row_slice):
        return self.__class__(self.starts[row_slice], self.ends[row_slice], self.col_step)

    def col_slice(self, col_slice):
        if isinstance(col_slice, Number):
            idx = col_slice
            if idx >= 0:
                return self.__class__(self.starts + idx,
                                      np.ones_like(self.lengths))
            return self.__class__(self.ends + idx, np.ones_like(self.lengths))

        starts, lengths, col_step = (self.starts, self.lengths, self.col_step)
        ends = self.ends
        default_forward = (self.starts, self.ends)
        default_reverse = (starts + (self.lengths-1)*col_step,
                           starts)
        if col_slice.step is not None:
            if col_slice.step < 0:
                starts = starts+(self.lengths-1)*col_step
                ends = self.starts-1
            col_step = col_step*col_slice.step
            lengths = lengths // np.abs(col_step)
        if col_slice.start is not None:
            if col_slice.start >= 0:
                starts = self.starts + col_slice.start*self.col_step
            else:
                starts = self.starts + (self.lengths+col_slice.start)*self.col_step
        if col_slice.stop is not None:
            if col_slice.stop >= 0:
                ends = self.starts + col_slice.stop*self.col_step
            else:
                ends = self.starts + (self.lengths+col_slice.stop)*self.col_step
        lengths = (ends-starts)//col_step
        lengths = np.maximum(np.minimum(self.lengths, lengths), 0)
        return self.__class__(starts, lengths, col_step)

    def get_shape(self):
        return RaggedShape(np.atleast_1d(self.lengths))

    @property
    def ends(self):
        return self.starts + (self.lengths-1)*self.col_step+1

    def get_flat_indices(self):
        """Return the indices into a flattened array

        Return the indices of all the elements in all the
        rows in this view

        Returns
        -------
        array
        """
        print("#####", self)
        if not self.n_rows:
            return np.ones(0, dtype=self._dtype), self.get_shape()
        shape = self.get_shape()
        step = 1 if self.col_step is None else self.col_step
        index_builder = np.full(shape.size + 1, step, dtype=self._dtype)
        index_builder[shape.ends[::-1]] = 1 - self.ends[::-1]
        index_builder[0] = 0
        index_builder[shape.starts] += self.starts
        np.cumsum(index_builder, out=index_builder)
        return index_builder[:-1], shape
