'''
This file is an abstract class defining the methods
that must be implemented for a view in the SuperConductor
project
'''

from abc import ABCMeta, abstractmethod

class AbstractView(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_control(self, value):
        pass

    @abstractmethod
    def update_value(self, control, track, value):
        pass
    
