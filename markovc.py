import numpy.linalg
import numpy.random
import scipy.stats
import scipy.io
import argparse
import numpy
import math
import sys
import os

import os.path

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


sys.path.append("./module")
import mainmkvcmp
import basicutils

parser = argparse.ArgumentParser()

parser.add_argument("-m","--rmat-filename", help="Transition probability matrix filename", \
        type=str, required=True, dest="rmatfilename")
parser.add_argument("-b", "--imat-filename", help="Rewards matrix filename", \
        type=str, required=True, dest="imatfilename")
parser.add_argument("-s", "--step", help="Bin width ", \
        type=float, required=False, default=0.25, dest="step")
parser.add_argument("-t", "--time-prev", help="Forecasted period ", \
        type=int, required=False, default=37, dest="tprev")
parser.add_argument("-n", "--max-run", help="Monte carlo iterations ", \
        type=int, required=True, dest="maxrun")
parser.add_argument("-M", "--name-of-matrix", help="Name of the probability matrix ", \
        type=str, required=False, default="ms", dest="nameofmatrix")
parser.add_argument("-B", "--name-of-bpmatrix", help="Name of the rewards matrix ", \
        type=str, required=False, default="i_r", dest="nameofbpmatrix")
parser.add_argument("-v", "--verbose", help="increase output verbosity", \
        default=False, action="store_true")
parser.add_argument("-S", "--seed", help="Using a seed for the random generator", \
        default=False, action="store_true", dest="seed")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

namebp = args.nameofbpmatrix
verbose = args.verbose
filename1 = args.rmatfilename
filename2 = args.imatfilename
step = args.step
tprev = args.tprev
numofrun = args.maxrun
namems = args.nameofmatrix

errmsg = []

if not (os.path.isfile(filename1)):
    print("File " + filename1 + " does not exist ")
    exit(1)

if not (os.path.isfile(filename2)):
    print("File " + filename2 + " does not exist ")
    exit(1)

msd = scipy.io.loadmat(filename1)
bpd = scipy.io.loadmat(filename2)

if not(namems in msd.keys()):
    print ("Cannot find " + namems + " in " + filename1)
    print (msd.keys())
    exit(1)

if not(namebp in bpd.keys()):
    print ("Cannot find " + namebp + " in " + filename2)
    print (bpd.keys())
    exit(1)

if msd[namems].shape[0] != bpd[namebp].shape[0]:
    print ("wrong dim of the input matrix")
    exit(1)

ms = msd[namems]
i_r = bpd[namebp]

entropia = numpy.zeros(tprev, dtype='float64')
var = numpy.zeros((tprev), dtype='float64')

rating = numpy.max(ms)

meanval = []
stdeval = []
 
allratings = []
allratingsnins = []

time = ms.shape[1]
pr = numpy.zeros((rating,rating,time), dtype='float64')
if not mainmkvcmp.main_mkc_comp_cont (ms, i_r, timeinf, step, tprev, \
        numofrun, verbose, True, args.seed, errmsg, entropia, \
        var, allratings, allratingsnins, pr, meanval, stdeval):
    for m in errmsg:
        print (m)
    exit(1)
