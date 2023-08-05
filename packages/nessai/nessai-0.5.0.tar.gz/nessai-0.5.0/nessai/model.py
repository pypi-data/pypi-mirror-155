# -*- coding: utf-8 -*-
"""
Object for defining the use-defined model.
"""
from abc import ABC, abstractmethod
import datetime
import logging
import numpy as np

from .livepoint import (
    parameters_to_live_point,
    numpy_array_to_live_points,
    get_dtype,
    DEFAULT_FLOAT_DTYPE,
    LOGL_DTYPE,
)
from .utils.multiprocessing import (
    get_n_pool,
    log_likelihood_wrapper,
)


logger = logging.getLogger(__name__)


class OneDimensionalModelError(Exception):
    """Exception raised when the model is one-dimensional"""
    pass


class Model(ABC):
    """Base class for the user-defined model being sampled.

    The user must define the attributes ``names`` ``bounds`` and the methods
    ``log_likelihood`` and ``log_prior``.

    The user can also define the reparemeterisations here instead of in
    the keyword arguments passed to the sampler.
    """

    _names = None
    _bounds = None
    reparameterisations = None
    """
    dict
        Dictionary of reparameterisations that overrides the values specified.
    """
    likelihood_evaluations = 0
    """
    int
        Number of likelihood evaluations.
    """
    likelihood_evaluation_time = datetime.timedelta()
    """
    :py:obj:`datetime.timedelta()`
        Time spent evaluating the likelihood.
    """
    _lower = None
    _upper = None
    pool = None
    """
    obj
        Multiprocessing pool for evaluating the log-likelihood.
    """
    allow_vectorised = True
    """
    bool
        Allow the model to use a vectorised likelihood. If True, nessai will
        try to check if the model is vectorised and use call the likelihood
        as a vectorised function. If False, nessai won't check and, even if the
        likelihood is vectorised, it will only evaluate the likelihood one
        sample at a time.
    """
    _vectorised_likelihood = None

    @property
    def names(self):
        """List of the names of each parameter in the model."""
        if self._names is None:
            raise RuntimeError('`names` is not set!')
        return self._names

    @names.setter
    def names(self, names):
        if not isinstance(names, list):
            raise TypeError('`names` must be a list')
        elif not names:
            raise ValueError('`names` list is empty!')
        elif len(names) == 1:
            raise OneDimensionalModelError(
                'names list has length 1. '
                'nessai is not designed to handle one-dimensional models due '
                'to limitations imposed by the normalising flow-based '
                'proposals it uses. Consider using other methods instead of '
                'nessai.'
            )
        else:
            self._names = names

    @property
    def bounds(self):
        """Dictionary with the lower and upper bounds for each parameter."""
        if self._bounds is None:
            raise RuntimeError('`bounds` is not set!')
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        if not isinstance(bounds, dict):
            raise TypeError('`bounds` must be a dictionary.')
        elif len(bounds) == 1:
            raise OneDimensionalModelError(
                'bounds dictionary has length 1. '
                'nessai is not designed to handle one-dimensional models due '
                'to limitations imposed by the normalising flow-based '
                'proposals it uses. Consider using other methods instead of '
                'nessai.'
            )
        elif not all([len(b) == 2 for b in bounds.values()]):
            raise ValueError('Each entry in `bounds` must have length 2.')
        else:
            self._bounds = {p: np.asarray(b) for p, b in bounds.items()}

    @property
    def dims(self):
        """Number of dimensions in the model"""
        d = len(self.names)
        if d == 0:
            d = None
        return d

    @property
    def lower_bounds(self):
        """Lower bounds on the priors"""
        if self._lower is None:
            bounds_array = np.array(list(self.bounds.values()))
            self._lower = bounds_array[:, 0]
            self._upper = bounds_array[:, 1]
        return self._lower

    @property
    def upper_bounds(self):
        """Upper bounds on the priors"""
        if self._upper is None:
            bounds_array = np.array(list(self.bounds.values()))
            self._lower = bounds_array[:, 0]
            self._upper = bounds_array[:, 1]
        return self._upper

    @property
    def vectorised_likelihood(self):
        """Boolean to indicate if the likelihood is vectorised or not.

        Checks that the values returned by computing the likelihood for
        individual samples matches those return by evaluating the likelihood
        in a batch. If a TypeError or ValueError are raised the likelihood is
        assumed to be vectorised.

        This check can be prevented by setting
        :py:attr:`nessai.model.Model.allowed_vectorised` to ``False``.
        """
        if self._vectorised_likelihood is None:
            if self.allow_vectorised:
                x = self.new_point(N=10)
                target = np.fromiter(map(self.log_likelihood, x), LOGL_DTYPE)
                try:
                    batch = self.log_likelihood(x)
                except (TypeError, ValueError):
                    logger.debug(
                        'Evaluating a batch of points returned an error. '
                        'Assuming the likelihood is not vectorised.'
                    )
                    self._vectorised_likelihood = False
                else:
                    if np.array_equal(batch, target):
                        logger.debug(
                            'Individual and batch likelihoods are equal.'
                        )
                        logger.info('Likelihood is vectorised')
                        self._vectorised_likelihood = True
                    else:
                        logger.debug(
                            'Individual and batch likelihoods are not equal.'
                        )
                        logger.debug(target)
                        logger.debug(batch)
                        self._vectorised_likelihood = False
            else:
                self._vectorised_likelihood = False
        return self._vectorised_likelihood

    @vectorised_likelihood.setter
    def vectorised_likelihood(self, value):
        """Manually set the value for vectorised likelihood."""
        self._vectorised_likelihood = value

    def configure_pool(self, pool=None, n_pool=None):
        """Configure a multiprocessing pool for the likelihood computation.

        Parameters
        ----------
        pool :
            User provided pool. Must call
            :py:func:`nessai.utils.multiprocessing.initialise_pool_variables`
            before creating the pool or pass said function to the initialiser
            with the model.
        n_pool : int
            Number of threads to use to create an instance of
            :py:obj:`multiprocessing.Pool`.
        """
        self.pool = pool
        self.n_pool = n_pool
        if self.pool:
            logger.info('Using user specified pool')
            n_pool = get_n_pool(self.pool)
            if n_pool is None and not self.n_pool:
                logger.warning(
                    'Could not determine number of processes in pool and '
                    'user has not specified the number. Likelihood '
                    'vectorisation will be disabled.'
                )
                self.allow_vectorised = False
            elif n_pool:
                self.n_pool = n_pool
                logger.debug(f'User pool has {n_pool} processes')
        elif self.n_pool:
            logger.info(
                f'Starting multiprocessing pool with {n_pool} processes'
            )
            import multiprocessing
            from nessai.utils.multiprocessing import initialise_pool_variables
            self.pool = multiprocessing.Pool(
                processes=self.n_pool,
                initializer=initialise_pool_variables,
                initargs=(self,)
            )
        else:
            logger.info('pool and n_pool are none, no multiprocessing pool')

    def close_pool(self, code=None):
        """Close the the multiprocessing pool"""
        if getattr(self, "pool", None) is not None:
            logger.info("Starting to close worker pool.")
            if code == 2:
                self.pool.terminate()
            else:
                self.pool.close()
            self.pool.join()
            self.pool = None
            logger.info("Finished closing worker pool.")

    def new_point(self, N=1):
        """
        Create a new LivePoint, drawn from within bounds.

        See `new_point_log_prob` if changing this method.

        Parameters
        ----------
        N : int, optional
            Number of points to draw. By default draws one point. If N > 1
            points are drawn using a faster method.

        Returns
        -------
        ndarray
            Numpy structured array with fields for each parameter
            and log-prior (logP) and log-likelihood (logL)
        """
        if N > 1:
            return self._multiple_new_points(N)
        else:
            return self._single_new_point()

    def new_point_log_prob(self, x):
        """
        Computes the proposal probability for a new point.

        This does not assume the that points will be drawn according to the
        prior. If `new_point` is redefined this method must be updated to
        match.

        Parameters
        ----------
        x : ndarray
            Points in a structured array

        Returns
        -------
        ndarray
            Log proposal probability for each point
        """
        return np.zeros(x.size)

    def _single_new_point(self):
        """
        Draw a single point within the prior

        Returns
        -------
        ndarray
            Numpy structured array with fields for each parameter
            and log-prior (logP) and log-likelihood (logL)
        """
        logP = -np.inf
        while (logP == -np.inf):
            p = parameters_to_live_point(
                    np.random.uniform(self.lower_bounds, self.upper_bounds,
                                      self.dims),
                    self.names)
            logP = self.log_prior(p)
        return p

    def _multiple_new_points(self, N):
        """
        Draw multiple points within the prior. Draws N points and accepts
        only those for which log-prior is finite.

        Parameters
        ----------
        N : int
            Number of points to draw

        Returns
        -------
        np.ndarray
            Numpy structured array with fields for each parameter
            and log-prior (logP) and log-likelihood (logL)
        """
        new_points = np.array([], dtype=get_dtype(self.names,
                                                  DEFAULT_FLOAT_DTYPE))
        while new_points.size < N:
            p = numpy_array_to_live_points(
                    np.random.uniform(self.lower_bounds, self.upper_bounds,
                                      [N, self.dims]),
                    self.names)
            logP = self.log_prior(p)
            new_points = np.concatenate([new_points, p[np.isfinite(logP)]])
        return new_points

    def in_bounds(self, x):
        """Check if a set of live point are within the prior bounds.

        Parameters
        ----------
        x : :obj:`numpy.ndarray`
            Structured array of live points. Must contain all of the parameters
            in the model.

        Returns
        -------
        Array of bool
            Array with the same length as x where True indicates the point
            is within the prior bounds.
        """
        return ~np.any([(x[n] < self.bounds[n][0]) | (x[n] > self.bounds[n][1])
                        for n in self.names], axis=0)

    def sample_parameter(self, name, n=1):
        """Draw samples for a specific parameter from the prior.

        Should be implemented by the user and return a numpy array of length
        n. The array should NOT be a structured array. This method is not
        required for standard sampling with nessai. It is intended for use
        with :py:class:`nessai.conditional.ConditionalFlowProposal`.

        Parameters
        ----------
        name : str
            Name for the parameter to sample
        n : int, optional
            Number of samples to draw.
        """
        raise NotImplementedError('User must implement this method!')

    def parameter_in_bounds(self, x, name):
        """
        Check if an array of values for specific parameter are in the prior \
            bounds.

        Parameters
        ----------
        x : :obj:`numpy:ndarray`
            Array of values. Not a structured array.

        Returns
        -------
        Array of bool
            Array with the same length as x where True indicates the value
            is within the prior bounds.
        """
        return (x >= self.bounds[name][0]) & (x <= self.bounds[name][1])

    @abstractmethod
    def log_prior(self, x):
        """
        Returns log-prior, must be defined by the user.
        """
        raise NotImplementedError

    @abstractmethod
    def log_likelihood(self, x):
        """
        Returns the log-likelihood, must be defined by the user.
        """
        raise NotImplementedError

    def evaluate_log_likelihood(self, x):
        """
        Evaluate the log-likelihood and track the number of calls.

        Returns
        -------
        float
            Log-likelihood value

        """
        self.likelihood_evaluations += 1
        return self.log_likelihood(x)

    def batch_evaluate_log_likelihood(self, x):
        """Evaluate the likelihood for a batch of samples.

        Uses the pool if available.

        Parameters
        ----------
        x : :obj:`numpy.ndarray`
            Array of samples

        Returns
        -------
        :obj:`numpy.ndarray`
            Array of log-likelihood values
        """
        st = datetime.datetime.now()
        if self.pool is None:
            logger.debug('Not using pool to evaluate likelihood')
            if self.allow_vectorised and self.vectorised_likelihood:
                log_likelihood = self.log_likelihood(x)
            else:
                log_likelihood = \
                    np.fromiter(map(self.log_likelihood, x), LOGL_DTYPE)
        else:
            logger.debug('Using pool to evaluate likelihood')
            if self.allow_vectorised and self.vectorised_likelihood:
                log_likelihood = np.concatenate(
                    self.pool.map(
                        log_likelihood_wrapper,
                        np.array_split(x, self.n_pool)
                    )
                )
            else:
                log_likelihood = np.array(
                    self.pool.map(log_likelihood_wrapper, x)
                ).flatten()
        self.likelihood_evaluations += x.size
        self.likelihood_evaluation_time += (datetime.datetime.now() - st)
        return log_likelihood

    def verify_model(self):
        """
        Verify that the model is correctly setup. This includes checking
        the names, bounds and log-likelihood.
        """
        if not isinstance(self.names, list):
            raise TypeError('`names` must be a list')

        if not isinstance(self.bounds, dict):
            raise TypeError('`bounds` must be a dictionary')

        if not self.names:
            raise ValueError(
                f'`names` is not set to a valid value: {self.names}'
            )
        if not self.bounds or not isinstance(self.bounds, dict):
            raise ValueError(
                f'`bounds` is not set to a valid value: {self.bounds}'
            )

        if self.dims == 1:
            raise OneDimensionalModelError(
                'model is one-dimensional. '
                'nessai is not designed to handle one-dimensional models due '
                'to limitations imposed by the normalising flow-based '
                'proposals it uses. Consider using other methods instead of '
                'nessai.'
            )

        for n in self.names:
            if n not in self.bounds.keys():
                raise RuntimeError(f'Missing bounds for {n}')

        if (np.isfinite(self.lower_bounds).all() and
                np.isfinite(self.upper_bounds).all()):
            logP = -np.inf
            counter = 0
            while (logP == -np.inf) or (logP == np.inf):
                x = numpy_array_to_live_points(
                        np.random.uniform(self.lower_bounds, self.upper_bounds,
                                          [1, self.dims]),
                        self.names)
                logP = self.log_prior(x)
                counter += 1
                if counter == 1000:
                    raise RuntimeError(
                        'Could not draw valid point from within the prior '
                        'after 10000 tries, check the log prior function.')
        else:
            logger.warning('Model has infinite bounds(s)')
            logger.warning('Testing with `new_point`')
            try:
                x = self.new_point(1)
                logP = self.log_prior(x)
            except Exception as e:
                raise RuntimeError(
                    'Could not draw a new point and compute the log prior '
                    f'with error: {e}. \n Check the prior bounds.')

        if self.log_prior(x) is None:
            raise RuntimeError('Log-prior function did not return '
                               'a prior value')
        if self.log_likelihood(x) is None:
            raise RuntimeError('Log-likelihood function did not return '
                               'a likelihood value')

    def __getstate__(self):
        state = self.__dict__.copy()
        state['pool'] = None
        return state
