"""Electricity-network power-flow problems."""
import numpy as np


def get_transmission_dc(sus_mat, delta):
    """ Compute the transmission matrix from the susceptance
    matrix and the phases computed beforehand from the DC approximation
    of the power flow.

    :param sus_mat: Susceptance matrix,
      i.e. the imaginary part of the admittance matrix.
    :param delta: Phase at each node.
    :type sus_mat: :py:obj:`numpy.array`
    :type delta: :py:obj:`numpy.array`

    :returns: Transmission matrix.
    :rtype: :py:obj:`numpy.array`
    """
    n_reg = sus_mat.shape[0]
    trans_mat = np.zeros((n_reg, n_reg))
    for i in np.arange(n_reg):
        for j in np.arange(i + 1, n_reg):
            trans_mat[i, j] = (delta[i] - delta[j]) * sus_mat[i, j]
            trans_mat[j, i] = -trans_mat[i, j]

    return trans_mat


def get_power_flow_dc(power_trans, sus_mat):
    """ Solve the power flow problem using the DC approximation.

    :param power_trans: Power to be transmitted at each node of the network.
    :param sus_mat: The susceptance matrix (S),
      i.e. the imaginary part of the admittance matrix).
    :type power_trans: :py:obj:`numpy.array`
    :type sus_mat: :py:obj:`numpy.array`

    :returns: A tuple containing:

      * The transmission between each pair of node.
      * The phase at each node.

    :rtype: tuple

    .. note::
      Node one is taken as slack node. All the other nodes are
      considered generation nodes.

    .. see also::
      * Grainger, J., Stevenson, Jr. W., 1994, *Power System Analysis*,
        McGraw-Hill, New York.
      * Glover, J. D., Sarma, M. S., Overbye, T., 2012,
        *Power System Analysis and Design*, CENGAGE Learning.
    """
    nt, n_reg = power_trans.shape

    # Solve the power flow for each time step
    delta = np.zeros((nt, n_reg))
    trans = np.empty((nt, n_reg, n_reg))
    for t in np.arange(nt):
        # Solve the power flow to find the phases
        delta[t, 1:] = np.linalg.solve(-sus_mat[1:, 1:], power_trans[t, 1:])

        # Compute the resulting transmission between each pair of node.
        trans[t] = get_transmission_dc(sus_mat, delta[t])

    return trans, delta
