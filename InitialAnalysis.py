import scipy.sparse
import scipy.io
from scipy.sparse import diags
import plotly
import generateSpMM
import numpy as np
from numpy import random
from numpy import linalg as LA
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.plotly as py
import plotly.graph_objs as go

def build_rand_sparse_mat_and_multiply():
    sparse_matrix = scipy.sparse.rand(25,25,density=0.1)
    #sparse_matrix = generateSpMM.generate_sparse_matrix(3,10,1)
    scipy.sparse.rand()
    array = sparse_matrix.toarray()
    array_as_list = array.tolist()
    heat_map_data1 = [go.Heatmap(z=array_as_list)]
    heat_map_data2 = [go.Heatmap(z=(LA.matrix_power(array, 10)).tolist())]
    plot_url = plotly.offline.plot(heat_map_data1, filename='basic-heatmap1.html')
    plot_url = plotly.offline.plot(heat_map_data2, filename='basic-heatmap2.html')

def build_rand_sparse_diag_mat_and_multiply():
    array = diags(random.random_sample(25).tolist(), 0).toarray()
    #print array
    heat_map_data1 = [go.Heatmap(z=np.flipud(array).tolist())]
    heat_map_data2 = [go.Heatmap(z=np.flipud((LA.matrix_power(array, 2))).tolist())] #multiply with itself.
    plot_url = plotly.offline.plot(heat_map_data1, filename='basic-heatmap1.html')
    plot_url = plotly.offline.plot(heat_map_data2, filename='basic-heatmap2.html')

def build_rand_sparse_mat_with_compression_ratio_and_multiply():
    #array = diags(random.random_sample(25).tolist(), 0).toarray()
    #print array
    array = generateSpMM.generate_sparse_array(3,25,1)
    scipy.io.mmwrite("syn_mat.mtx",scipy.sparse.csr_matrix(array),field = 'real')
    #heat_map_data1 = [go.Heatmap(z=np.flipud(array).tolist())]
    #heat_map_data2 = [go.Heatmap(z=np.flipud((LA.matrix_power(array, 2))).tolist())] #multiply with itself.
    #plot_url = plotly.offline.plot(heat_map_data1, filename='basic-heatmap1.html')
    #plot_url = plotly.offline.plot(heat_map_data2, filename='basic-heatmap2.html')

def run():
    build_rand_sparse_mat_with_compression_ratio_and_multiply()

run()