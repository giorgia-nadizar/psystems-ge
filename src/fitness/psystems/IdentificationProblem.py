from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff
from psystems.Membrane import Membrane
from psystems.Rule import Rule
from utilities.fitness.get_data import get_compressed_dataset


class IdentificationProblem(base_ff):
    """
    Basic fitness function template for writing new fitness functions. This
    basic template inherits from the base fitness function class, which
    contains various checks and balances.

    Note that all fitness functions must be implemented as a class.

    Note that the class name must be the same as the file name.

    Important points to note about base fitness function class from which
    this template inherits:

      - Default Fitness values (can be referenced as "self.default_fitness")
        are set to NaN in the base class. While this can be over-written,
        PonyGE2 works best when it can filter solutions by NaN values.

      - The standard fitness objective of the base fitness function class is
        to minimise fitness. If the objective is to maximise fitness,
        this can be over-written by setting the flag "maximise = True".

    """

    # The base fitness function class is set up to minimise fitness.
    # However, if you wish to maximise fitness values, you only need to
    # change the "maximise" attribute here to True rather than False.
    # Note that if fitness is being minimised, it is not necessary to
    # re-define/overwrite the maximise attribute here, as it already exists
    # in the base fitness function class.
    maximise = False

    def __init__(self):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """

        # Initialise base fitness function class.
        super().__init__()

        # Get training set
        self.problem = params['EXPERIMENT_NAME']
        self.train_set = get_compressed_dataset(params['DATASET_TRAIN'].replace('EXPERIMENT_NAME', self.problem))

    def evaluate(self, ind, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.

        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.

        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """
        ruleset = [Rule.from_string(r) for r in ind.phenotype.split('; ')]

        # Evaluate the fitness of the phenotype
        return self.compute_error(self.train_set, ruleset, verbose=False)

    @staticmethod
    def compute_error(train_set, ruleset, verbose=True):
      err = 0
      n = len(train_set)
      for before, after in train_set:
        b = Membrane.clone(before)
        b.apply(ruleset, verbose=verbose)
        d = Membrane.distance(b, after)
        if verbose:
          print(f'Input: {before}\tObtained: {b}\tExpected: {after}\tDist={d}\n')
        err += d
      return err / n
