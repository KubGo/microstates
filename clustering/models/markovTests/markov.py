import numpy as np
from scipy.stats import chi2


class MarkovTest:
    """
    Markov test builder for 0,1,2 order tests
    for checking of the Markovianity of the
    chain
    """
    def __init__(self, x: list, n_clusters, alpha: float):
        """
        Instantiate MarkovTest with correct order
        Args:
            x: list
            Chain of states
            n_clusters: int
            Number of clusters
            alpha: float
            Significance level
        """
        self.x = x
        self.n_clusters = n_clusters
        self.alpha = alpha

    def test_markov(self, order: int):
        """
        Test Markovianity of the sequence
        Returns:
            p: p-value of the Chi2 test for independence
        """

        function = select_function(order)
        return function(self.x, self.n_clusters, self.alpha)


def test_markov_0(x, n_clusters, alpha):
    """Test zero-order Markovianity of symbolic sequence x with ns symbols.
    Null hypothesis: zero-order MC (iid) <=>
    p(X[t]), p(X[t+1]) independent
    cf. Kullback, Technometrics (1962)

    Args:
        x: symbolic sequence, symbols = [0, 1, 2, ...]
        n_clusters: number of symbols
        alpha: significance level
    Returns:
        p: p-value of the Chi2 test for independence
    """
    n = len(x)
    f_ij = np.zeros((n_clusters, n_clusters))
    f_i = np.zeros(n_clusters)
    f_j = np.zeros(n_clusters)
    # calculate f_ij p( x[t]=i, p( x[t+1]=j ) )
    for t in range(n - 1):
        i = x[t]
        j = x[t + 1]
        f_ij[i, j] += 1.0
        f_i[i] += 1.0
        f_j[j] += 1.0
    T = 0.0  # statistic
    for i, j in np.ndindex(f_ij.shape):
        f = f_ij[i, j] * f_i[i] * f_j[j]
        if f > 0:
            num_ = n * f_ij[i, j]
            den_ = f_i[i] * f_j[j]
            T += (f_ij[i, j] * np.log(num_ / den_))
    T *= 2.0
    df = (n_clusters - 1.0) * (n_clusters - 1.0)
    p = chi2.sf(T, df, loc=0, scale=1)
    return p


def test_markov_1(x, n_clusters, alpha):
    """Test first-order Markovianity of symbolic sequence X with ns symbols.
    Null hypothesis:
    first-order MC <=>
    p(X[t+1] | X[t]) = p(X[t+1] | X[t], X[t-1])
    cf. Kullback, Technometrics (1962), Tables 8.1, 8.2, 8.6.

    Args:
        x: symbolic sequence, symbols = [0, 1, 2, ...]
        n_clusters: number of symbols
        alpha: significance level
    Returns:
        p: p-value of the Chi2 test for independence
    """

    n = len(x)
    f_ijk = np.zeros((n_clusters, n_clusters, n_clusters))
    f_ij = np.zeros((n_clusters, n_clusters))
    f_jk = np.zeros((n_clusters, n_clusters))
    f_j = np.zeros(n_clusters)
    for t in range(n - 2):
        i = x[t]
        j = x[t + 1]
        k = x[t + 2]
        f_ijk[i, j, k] += 1.0
        f_ij[i, j] += 1.0
        f_jk[j, k] += 1.0
        f_j[j] += 1.0
    T = 0.0
    for i, j, k in np.ndindex(f_ijk.shape):
        f = f_ijk[i][j][k] * f_j[j] * f_ij[i][j] * f_jk[j][k]
        if f > 0:
            num_ = f_ijk[i, j, k] * f_j[j]
            den_ = f_ij[i, j] * f_jk[j, k]
            T += (f_ijk[i, j, k] * np.log(num_ / den_))
    T *= 2.0
    df = n_clusters * (n_clusters - 1) * (n_clusters - 1)
    p = chi2.sf(T, df, loc=0, scale=1)
    return p


def test_markov_2(x, ns, alpha):
    """Test second-order Markovianity of symbolic sequence X with ns symbols.
    Null hypothesis:
    first-order MC <=>
    p(X[t+1] | X[t], X[t-1]) = p(X[t+1] | X[t], X[t-1], X[t-2])
    cf. Kullback, Technometrics (1962), Table 10.2.

    Args:
        x: symbolic sequence, symbols = [0, 1, 2, ...]
        ns: number of symbols
        alpha: significance level
    Returns:
        p: p-value of the Chi2 test for independence
    """
    n = len(x)
    f_ijkl = np.zeros((ns, ns, ns, ns))
    f_ijk = np.zeros((ns, ns, ns))
    f_jkl = np.zeros((ns, ns, ns))
    f_jk = np.zeros((ns, ns))
    for t in range(n - 3):
        i = x[t]
        j = x[t + 1]
        k = x[t + 2]
        l = x[t + 3]
        f_ijkl[i, j, k, l] += 1.0
        f_ijk[i, j, k] += 1.0
        f_jkl[j, k, l] += 1.0
        f_jk[j, k] += 1.0
    T = 0.0
    for i, j, k, l in np.ndindex(f_ijkl.shape):
        f = f_ijkl[i, j, k, l] * f_ijk[i, j, k] * f_jkl[j, k, l] * f_jk[j, k]
        if f > 0:
            num_ = f_ijkl[i, j, k, l] * f_jk[j, k]
            den_ = f_ijk[i, j, k] * f_jkl[j, k, l]
            T += (f_ijkl[i, j, k, l] * np.log(num_ / den_))
    T *= 2.0
    df = ns * ns * (ns - 1) * (ns - 1)
    p = chi2.sf(T, df, loc=0, scale=1)
    return p


def select_function(order: int):
    """
    Select right function for Markov test calculations
    Args:
        order: int
        Order of Markov chain
    Returns:
        function: Function to calculate order of 0,1 or 2
    """
    if order <= 0:
        if order < 0:
            print("Order cannot be lower than 0, using 0 order")
        return test_markov_0
    elif order == 1:
        return test_markov_1
    if order > 2:
        print("Order cannot be higher than 2, using 2 order")
    return test_markov_2