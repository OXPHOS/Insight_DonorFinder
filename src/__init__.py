#!/usr/bin/env python


class ProgressBar(object):
    __progress_bar__ = True

    @classmethod
    def set_progress_bar(cls, val):
        cls.__progress_bar__ = val

    @classmethod
    def get_progress_bar(cls):
        return cls.__progress_bar__

from src.find_political_donors import *
from src.stream_input import *
from src.AVLTree import *
from src.InfoTable import *
from src.LinkedListNode import *
