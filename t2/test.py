#!/bin/python

from classifiers import *
from utils import *
data = load("datasets/generoIris2D.csv")[1:]

def test(classifier):
  ibl = classifier(data)
  print(ibl.descriptor)

test(IBL3)
