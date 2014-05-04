"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import cvxpy.utilities as u
import cvxpy.lin_ops.lin_utils as lu
from cvxpy.utilities import bool_mat_utils as bu
from cvxpy.atoms.affine.generic_stack import GenericStack
from cvxpy.atoms.affine.index import index
import numpy as np

class vstack(GenericStack):
    """ Vertical concatenation """
    # Returns the vstack of the values.
    @GenericStack.numpy_numeric
    def numeric(self, values):
        return np.vstack(values)

    # The shape is the common width and the sum of the heights.
    def shape_from_args(self):
        cols = self.args[0].size[1]
        rows = sum(arg.size[0] for arg in self.args)
        return u.Shape(rows, cols)

    # All arguments must have the same width.
    def validate_arguments(self):
        arg_cols = [arg.size[1] for arg in self.args]
        if max(arg_cols) != min(arg_cols):
            raise TypeError( ("All arguments to vstack must have "
                              "the same number of columns.") )

    # Vertically concatenates sign and curvature as dense matrices.
    def sign_curv_from_args(self):
        return super(vstack, self).sign_curv_from_args(bu.vstack)

    @staticmethod
    def graph_implementation(arg_objs, size, data=None):
        """Stack the expressions vertically.

        Parameters
        ----------
        arg_objs : list
            LinExpr for each argument.
        size : tuple
            The size of the resulting expression.
        data :
            Additional data required by the atom.

        Returns
        -------
        tuple
            (LinOp for objective, list of constraints)
        """
        X = lu.create_var(size)
        constraints = []
        # Create an equality constraint for each arg.
        offset = 0
        for arg in arg_objs:
            index.block_eq(X, arg, constraints,
                           offset, arg.size[0] + offset,
                           0, size[1])
            offset += arg.size[0]
        return (X, constraints)
