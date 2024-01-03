w0 = 1.5
w1 = w2 = w3 = 0
w1 = w2 = w3 = 0.5
x1 = -2
x2 = 1
x3 = 2
nA = w0 + w1 * x1 + w2 * x2 + w3 * x3
nB = w0 + w1 * x1 + w2 * x2 + w3 * x3

def ReQU(x):
    if x < 0:
        return 0
    else:
        return x**2
    

nA_ats = ReQU(nA)
nB_ats = ReQU(nB)
print(nA_ats, nB_ats)


nD_ats = ReQU((nA_ats*w1)+(nB_ats*w2)+w0)
nC_ats = ReQU((nA_ats*w1)+(nB_ats*w2)+w0)
nU_ats = ReQU((nA_ats*w1)+x2*w2+(nD_ats*w3)+w0)
print(f"D:{nD_ats}, C:{nC_ats}, U:{nU_ats}")