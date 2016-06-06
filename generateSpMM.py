from scipy import sparse
from scipy import *
from array import *
import numpy
import random

def generate_sparse_matrix(m,n,c):
    matrix = numpy.zeros((n, n))
    offset = (m-c)/(m-1) * m
    for i in range(n):
        for j in range(m):
            matrix[i][(offset*i+j)%n] = random.random()
    #print sparse.csr_matrix(matrix)
    return sparse.csr_matrix(matrix)

def generate_sparse_array(m,n,c):
    matrix = numpy.zeros((n, n))
    offset = (m-c)/(m-1) * m
    for i in range(n):
        for j in range(m):
            matrix[i][(offset*i+j)%n] = random.random()
    #print sparse.csr_matrix(matrix)
    return matrix

def run():
    number_of_nnz_per_row = m = 3 ; #alias m
    size_of_matrix = n = 10; # alias n (square matrices only.)   m << n
    compression_ratio = c = 1; #varies from 1 to m
    generate_sparse_matrix(m, n, c)

run()