import numpy as np
import qiskit
from functools import reduce

################################################################################
## B Tree
arr = [0, 1, 2, 3, 4, 5, 6]

def BTree(N):
    q = []

    def rec(a, b):
        if a == b:
            return

        m = (a+b)   // 2
        l = (a+m-1) // 2
        r = (m+1+b) // 2

        q.append((m, l, r))
        rec(a, m-1)
        rec(m+1, b)

    rec(0, N)

    arr = []
    if len(q) > 0:
        (m, l, r) = q[0]
        arr.append(m)

    for i in range(len(q)):
        (m, l, r) = q[i]
        arr.append(l)
        arr.append(r)

    return arr

################################################################################
## Gen Angles
def gen_angles(x):
  if (len(x) > 1):
    new_N = int(len(x) / 2)
    new_x = [0.] * new_N

    for k in range(new_N):
      new_x[k] = np.sqrt( np.abs(x[2*k])**2 + np.abs(x[2*k+1])**2 )

    inner_angles = gen_angles(new_x)
    angles = [0.] * new_N

    for k in range(new_N):
      if new_x[k] != 0:
        if x[2*k] > 0:
          angles[k] = 2*np.arcsin(x[2*k+1] / new_x[k])
        else:
          angles[k] = 2*np.pi - 2*np.arcsin(x[2*k+1] / new_x[k])
      else:
        angles[k] = 0

    return inner_angles + angles # concat
  else:
    return []

################################################################################
## Gen Circuit
def gen_circuit(angles):
    N = len(angles) + 1
    bt = BTree(N - 2)

    circuit = qiskit.QuantumCircuit(N - 1)

    for k in range(N - 1):
        circuit.ry(angles[k], k)

    parent = lambda i: int((i - .5) / 2)
    left   = lambda i: 2*i + 1
    right  = lambda i: 2*i + 2

    actual = parent(N-2)

    while actual >= 0:
        left_index = left(actual)
        right_index = right(actual)

        while right_index < N - 1:
            circuit.cswap(actual, left_index, right_index)

            left_index = left(left_index)
            right_index = left(right_index)

        actual = actual - 1

    return circuit

v = list(map(lambda a: np.sqrt(a), [.03, .07, .15, .05, .1, .3, .2, .1]))
print( gen_circuit(gen_angles(v)).draw() )
