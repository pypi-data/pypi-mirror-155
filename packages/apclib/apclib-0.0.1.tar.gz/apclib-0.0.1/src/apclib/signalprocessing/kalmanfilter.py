# Matrix operation functions
if 1:
    def identity(n, v):
        m=[[0 for x in range(n)] for y in range(n)]
        for i in range(0,n):
            m[i][i] = v
        return m
    
    def matmult(a, b):
        if    len(a) == 1 and len(a[0]) == 1:
            zip_b = zip(*b)
            zip_b = list(zip_b)
            return [[el*a[0][0] for el in row] for row in b]
    
        elif len(b) == 1 and len(b[0]) == 1: 
            zip_a = zip(*a)
            zip_a = list(zip_a)
            return [[el*b[0][0] for el in row] for row in a]
    
        else:
            zip_b = zip(*b)
            zip_b = list(zip_b)
            return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
                     for col_b in zip_b] for row_a in a]
    
    def matadd(a, b):
        res = []
        for i in range(len(a)):
            row = []
            for j in range(len(a[0])):
                row.append(a[i][j]+b[i][j])
            res.append(row)
        return res
    
    def matsubtract(a, b):
        res = []
        for i in range(len(a)):
            row = []
            for j in range(len(a[0])):
                row.append(a[i][j]-b[i][j])
            res.append(row)
        return res
    
    def mattranspose(a):
        return list(map(list, zip(*a)))
    
    def matminor(m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]
    
    def matdeternminant(m):  
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    
        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*matdeternminant(matminor(m,0,c))
        return determinant
    
    def matinverse(m):
        #base case for 1x1 matrix
        if len(m) == 1:
            return [[1./m[0][0]]]
            
        determinant = matdeternminant(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]]
    
        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = matminor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * matdeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = mattranspose(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors

class KF:

    def __init__(self, X, U, A, B, H, q, r):
        '''
        X = AX + BU
        Y = HX
        '''
        self.q = q                               # Expected variance/error in model
        self.r = r                               # Expected variance/error in measurement
        
        # Matrices
        self.X = X                               # Mean state estimate of the previous step (k -1)
        self.U = U                               # Model Input
        self.A = A                               # State transition nxn matrix: Relates state in previous time-step to state in current time-step
        self.B = B                               # Input effect matrix:         Relates the input to the states
        self.H = H                               # Relates the measurement y to the states
        self.Q = identity(len(self.A[0]),self.q) # Process noise covariance matrix:     Expected variance/error in model
        self.R = identity(len(self.H   ),self.r) # Measurement noise covariance matrix: Expected variance/error in measurement
        self.P = identity(len(self.A[0]), 1)     # State covariance of previous step (k -1)
        
    def predict(self,U): 
        self.U = U
        self.X = matadd(matmult(self.A,self.X), matmult(self.B,self.U))
        self.P = matadd(matmult(self.A, matmult(self.P, mattranspose(self.A))),self.Q)

    def update(self, y):
        Y      = [[y]]
        IM     = matmult    (self.H, self.X)
        IS     = matadd     (self.R, matmult(self.H, matmult(self.P, mattranspose(self.H))))
        K      = matmult    (self.P, matmult(mattranspose(self.H), matinverse (IS)))
        self.X = matadd     (self.X, matmult(K, matsubtract(Y, IM)))
        self.P = matsubtract(self.P, matmult(K, matmult (IS, mattranspose(K))))