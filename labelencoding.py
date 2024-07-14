import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("sequence.csv")
sequences = df['Observations'].apply(lambda x: ['STOP', 'GO', 'LEFT SEEP', 'RIGHT SEEP', '1-LEFT', '1-RIGHT'].index(x))
final_sequence = sequences.to_numpy()
