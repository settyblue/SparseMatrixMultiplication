from scipy.sparse import coo_matrix
import random


def create_matrix_market_file(values,col_idx,row_ptr, nnz_per_row, nrows, skip_length = 0, scattered = False,\
                              symmetric = False, dtype = 'float', prefix = '', total_nnz = 0):
    if skip_length >=0 :
        filename = 'syn_mat_'+str(nnz_per_row)+'_'+str(nrows)+'_'+str(skip_length)
    else:
        filename = 'syn_mat_'+str(nnz_per_row)+'_'+str(nrows)

    if scattered:
        filename = prefix+filename + 's.mtx'
    else:
        filename = prefix+filename + '.mtx'
    print filename
    matrix_market_file = open(filename,'w')
    matrix_market_file.write("%%MatrixMarket matrix coordinate real general\n")
    matrix_market_file.write("%nnz_per_row = "+str(nnz_per_row)+"\n")
    matrix_market_file.write("%nrows = "+str(nrows)+"\n")
    matrix_market_file.write("%skip/shift length = "+str(skip_length)+"\n")
    matrix_market_file.write("%scattered = "+str(scattered)+"\n")
    matrix_market_file.write("%indexing starts from 1.\n")
    matrix_market_file.write(str(nrows)+" "+str(nrows)+" "+str(total_nnz)+"\n")
    for i in range(nrows):
        for j in range(row_ptr[i],row_ptr[i+1]):
            matrix_market_file.write(str(i+1)+" "+str(col_idx[j]+1)+" "+str(values[j])+"\n")
    matrix_market_file.close()


def generate_sparse_matrix(nnz_per_row=4, nrows = 10, skip_length = 2, scattered = False, both = False, prefix = ''):
    row_ptr = [0]
    row_idx = []
    col_idx = []
    values = []
    nnz_so_far = 0
    prev_row_start_point = 0
    for i in range(nrows):
        nnz_so_far += nnz_per_row
        row_ptr.append(nnz_so_far)
        if i == 0:
            start_col_index = 0
            prev_row_start_point = 0
        else:
            start_col_index  = prev_row_start_point + skip_length
            prev_row_start_point = start_col_index
        for j in range(nnz_per_row):
            row_idx.append(i)
            col_idx.append((start_col_index+j)%nrows)
            values.append(random.random())

    if not scattered or both:
        create_matrix_market_file(values,col_idx,row_ptr, nnz_per_row, nrows, skip_length, False, prefix=prefix, total_nnz=nnz_per_row*nrows)

    if scattered or both:
        # code to scatter the matrix.
        new_row_map = {}
        for i in range(nrows):
            new_row_map[i] = i

        for i in range(nrows):
            x = random.randint(0,nrows-1)
            y = random.randint(0,nrows-1)
            new_row_map[x], new_row_map[y] = new_row_map[y], new_row_map[x]

        for j in range(len(values)):
            row_idx[j] = new_row_map[row_idx[j]]
            col_idx[j] = new_row_map[col_idx[j]]

        mat = coo_matrix((values,(row_idx,col_idx)),shape=(nrows,nrows))
        mat = mat.tocsr()
        values = mat.data
        col_idx = mat.indices
        row_ptr = mat.indptr
        create_matrix_market_file(values,col_idx,row_ptr, nnz_per_row, nrows, prefix=prefix, total_nnz=nnz_per_row*nrows)


def generate_band_sparse_matrix(nnz_per_row = 5, nrows = 10, prefix = ''):
    row_ptr = [0]
    col_idx = []
    values = []

    start_col_index = 0
    nnz_so_far = 0
    nnz_this_row = int(nnz_per_row/2) + 1
    mid_value = nnz_this_row
    prev_row_start_point = 0
    for rowid in range(nrows):
        for j in range(nnz_this_row):
            col_idx.append((start_col_index+j)%nrows)
            values.append(random.random())
        nnz_so_far += nnz_this_row
        row_ptr.append(nnz_so_far)

        if rowid < mid_value-1:
            nnz_this_row += 1
        elif rowid < nrows - mid_value:
            nnz_this_row = nnz_per_row
            start_col_index += 1
        else:
            nnz_this_row -= 1
            start_col_index += 1
    create_matrix_market_file(values,col_idx,row_ptr, nnz_per_row, nrows, -1, prefix=prefix, total_nnz=nnz_so_far)


def run():
    skip_mat = [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                 [0, 1, 2, 4, 5, 6, 8, 9, 10],
                 [0, 1, 3, 5, 7, 9, 11, 13, 14],
                 [0, 3, 6, 9, 10, 12, 15, 18, 21],
                 [0, 3, 5, 10, 15, 18, 20, 25, 30],
                 [0, 4, 8, 12, 16, 20, 26, 34, 40]]

    for i,j,k in zip([8,10,14,21,30,40],[1024000,512000,512000,256000,256000,128000], skip_mat):
        for l in k:
            generate_sparse_matrix(nnz_per_row = i, nrows = j, skip_length = l, scattered=True, both=False)


def run2():
    generate_sparse_matrix(scattered=True)


def run3():
    generate_sparse_matrix(nnz_per_row = 8, nrows = 1024000, skip_length = 0, scattered=True, both=False)


def run4():
    skip_mat = [[0, 4, 8],
                 [0, 5, 10],
                 [0, 7, 14],
                 [0, 12, 21],
                 [0, 15, 30],
                 [0, 20, 40]]

    for i,j,k in zip([8,10,14,21,30,40],[1024,512,512,256,256,256], skip_mat):
        for l in k:
            generate_sparse_matrix(nnz_per_row = i, nrows = j, skip_length = l, scattered=True, both=True, \
                                   prefix='small_')


def run5():
    generate_band_sparse_matrix(nrows=256,nnz_per_row=7,prefix='Test_')


def run6():
    for i in [1024*1024]:
        for j in [7, 15, 31, 63, 127, 255]:
            generate_band_sparse_matrix(nrows=i,nnz_per_row=j, prefix='band_')


run6()
