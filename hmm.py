import numpy as np
from hmmlearn import hmm

states = ["Vehicle", "Stoplight"]
n_states = len(states)

observations = ["Stop", "Go", "LeftSeep", "RightSeep", "1-Left", "1-Right"]
n_observations = len(observations)


state_probability = np.array([0.9,0.1])

transition_probability = np.array([
    [0.791,0.209],
    [0.933,0.067]
])

emission_probability= np.array([
    [0.002,0.221,0.143,0.172,0.225,0.237],
    [0.944,0.056,0,0,0,0]
])

model = hmm.CategoricalHMM(n_components=n_states, n_features=n_observations)
model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability

from labelencoding import final_sequence, final_v_sequences

observations_sequence = final_sequence.reshape(-1, 1)
model.fit(observations_sequence)
model.predict(observations_sequence)
print(model.score(observations_sequence,[14,11,28,43,46,37,119,27,89]))
print(model.score(final_v_sequences.reshape(-1,1),[27,84,111,42]))

print(model.transmat_)
print(model.emissionprob_)

#Transmat: [V->V, V->S] [S->V, S->S] 
#Emission: V[Stop, Go, LS, RS, 1L, 1R] S[Stop, Go, LS, RS, 1L, 1R]
