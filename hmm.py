import numpy as np
from hmmlearn import hmm

states = ["Vehicle", "Stoplight"]
n_states = len(states)

observations = ["Stop", "Go", "LeftSeep", "RightSeep", "1-Left", "1-Right"]
n_observations = len(observations)


state_probability = np.array([0.9,0.1])

transition_probability = np.array([
    [32/35,3/35],
    [0.4,0.6]
])

emission_probability= np.array([
    [0,0,1/6,1/4,1/3,1/4],
    [0.5,0.5,0,0,0,0]
])

model = hmm.CategoricalHMM(n_components=n_states, n_features=n_observations)
model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability

observations_sequence = np.array([0,1,4,3,2,0,1,0,1,2,3,3,4,4,3,4,5,5,3,0,1,4,4,4,5,4,4,5,5,5,2,2,3,3,2,5,3,4,4,5,4,5,0,1,2,3]).reshape(-1, 1)
observations_sequence
model.fit(observations_sequence)
model.predict(observations_sequence)

print(model.transmat_)
print(model.emissionprob_)

#Transmat: [V->V, V->S] [S->V, S->S] 
#Emission: V[Stop, Go, LS, RS, 1L, 1R] S[Stop, Go, LS, RS, 1L, 1R]
