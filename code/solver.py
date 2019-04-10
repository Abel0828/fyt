import pickle
import numpy as np

f=open('./all_important_inter.pickle', 'rb')

index_table = pickle.load(f)
A = pickle.load(f)
T = pickle.load(f)
N = pickle.load(f)
P = pickle.load(f)
# mat_A = pickle.load(f, protocol=4)
c = pickle.load(f)
pos = pickle.load(f)

f.close()


mat_A=np.zeros((len(pos), len(pos)),dtype=np.float32)
for pos1, row in A.items():
    for pos2, a in row.items():
        mat_A[pos1, pos2]=a
print('mat_A.shape: ', mat_A.shape)
print('mat_A head 3', mat_A[:3,:3])

for i in range(len(pos)):
    mat_A[i, i]= 1-mat_A[i,i]

print('Start solving x')
x=np.linalg.solve(mat_A, c)
print('x[:10]: ', x[:10])

f=open('./x.pickle', 'wb')
pickle.dump(x, f)
f.close()