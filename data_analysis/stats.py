import matplotlib.pyplot as plt
import pandas as pd

items_column = pd.read_csv('mapped_team_data.csv').iloc[:, 0]
print(items_column)