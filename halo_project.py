# -*- coding: utf-8 -*-
"""halo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sPSwt1NyD8hcjKjIqlvOoGMr4Lk6jqgl
"""

!pip install pennylane

import sys
import pennylane as qml
import numpy as np1
from pennylane import numpy as np

from pennylane.optimize import AdamOptimizer
from pennylane import qaoa

def hamiltonian_coeffs_and_obs(A,c,n):
  obs = []
  coeffs = []
  #cost_function
  for p in range(n):
    for i in range(n):
      for j in range(n):

        
        coeffs.append(c[i,j,p]/4)
        obs.append(qml.Identity(0))
          
        coeffs.append(c[i,j,p]/4)
        obs.append(qml.PauliZ(A[i,p]))
          
        coeffs.append(c[i,j,p]/4)
        obs.append(qml.PauliZ(A[j,p+1]))
          
        coeffs.append(c[i,j,p]/4)
        obs.append(qml.PauliZ(A[i,p]) @ qml.PauliZ(A[j,p+1]))

  #constraint 1 : x0,0=1
  coeffs.append(-1/2)
  obs.append(qml.PauliZ(A[0,0]))

  coeffs.append(1/2)
  obs.append(qml.Identity(0))

  #constraint 2 : x0,n=1
  coeffs.append(-1/2)
  obs.append(qml.PauliZ(A[0,n]))

  coeffs.append(1/2)
  obs.append(qml.Identity(0))

  #constraint 3 : one occurs in a position
  coeffs.append(n+1)
  obs.append(qml.Identity(0))
  

  for p in range(n+1):
    for i in range(n):
      coeffs.append(-1)
      obs.append(qml.Identity(0))

      coeffs.append(-1)
      obs.append(qml.PauliZ(A[i,p]))

      for j in range(n):
        coeffs.append(1/4)
        obs.append(qml.Identity(0))

        coeffs.append(1/4)
        obs.append(qml.PauliZ(A[i,p]))

        coeffs.append(1/4)
        obs.append(qml.PauliZ(A[j,p]))

        
        coeffs.append(1/4)
        if (i==j):
          obs.append(qml.Identity(0))
        else:
          obs.append(qml.PauliZ(A[i,p]) @ qml.PauliZ(A[j,p]))

  return coeffs,obs





def variational_circuit(params, n,H,A,c):

 
  mixer_h=qml.Hamiltonian([1 for i in range(n**2+n)],[qml.PauliX(i) for i in range (n**2+n)])
    
  def qaoa_layer(gamma, alpha):
      qaoa.cost_layer(gamma, H)
      qaoa.mixer_layer(alpha, mixer_h)
        
  depth=4
  for w in range(n**2+n):
    qml.Hadamard(wires=w)
 
  qml.layer(qaoa_layer, depth, params[0], params[1])
  

  


def train_circuit(n, H,A,c):


  dev = qml.device("default.qubit", wires=n**2+n)
  dev1 = qml.device("default.qubit", wires=n**2+n,shots=10)

  @qml.qnode(dev)
  def cost(params):
         
    variational_circuit(params, n,H,A,c)
    return qml.expval(H)


  @qml.qnode(dev1)
  def cost_sample(params):
         
    variational_circuit(params, n,H,A,c)
    return qml.sample()

 
  np.random.seed(0)
    
  params = np.array([[0.1,0.1,0.1,0.1], [0.1,0.1,0.1,0.1]], requires_grad=True)

  opt = qml.AdamOptimizer(0.2)
  epochs = 10
    
  
  for i in range(epochs):
    print(f'start epoch {i}')
    params, E = opt.step_and_cost(cost, params)
    print(f'epoch : {i} | cost : {E}')

  ground_state= cost_sample(params)

  return E,ground_state 

if __name__ == "__main__":

  n=3

  #indexing qubits
  A=np1.zeros((n,n+1),dtype='int')
  for p in range(n+1):
    for i in range(n):
      A[i,p]=p*n+i

  #time dependant weight matrix
  c=np1.random.random((n,n,n))

  coeffs, obs = hamiltonian_coeffs_and_obs(A,c,n)
  H = qml.Hamiltonian(coeffs, obs)

  energy_density,ground_state = train_circuit(n, H,A,c)
  print(f"{energy_density:.6f}")
  
  print(ground_state)