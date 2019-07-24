"""This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

The core loader module defines an abstract loader. Loaders take in 
some source data and convert them into DARelations
"""
import truthdb.exec.rel 

class Loader(object):
    """Loader Abstract Class
    """

    def __init__(self, params):
        """Constructor

         Args:
            params (Dict): The input dictionary describing the loader parameters
        """

        self.params = params
        
        if not self._check_params():
            raise ValueError("Inconsistent Params: " + str(params))


    def _check_params(self):
        raise NotImplemented("Every loader must implement _check_params")

    def _load(self):
        raise NotImplemented("Every loader must implement _load()")

    def load(self):
        darel = self._load()

        if not isinstance(darel, truthdb.exec.rel.DARelation):
            raise TypeError("The output of _load is not a DARelation")
        else:
            return darel



