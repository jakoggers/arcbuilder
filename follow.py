import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors

data = np.array(
    [
        ["Pointy", "Round", "Present", 1],
        ["Floppy", "Not round", "Present", 1],
        ["Floppy", "Round", "Absent", 0],
        ["Pointy", "Not round", "Present", 0],
        ["Pointy", "Round", "Present", 1],
        ["Pointy", "Round", "Absent", 1],
        ["Floppy", "Not round", "Absent", 0],
        ["Pointy", "Round", "Absent", 1],
        ["Floppy", "Round", "Absent", 0],
        ["Floppy", "Round", "Absent", 0],
    ]
)

X, Y = data[:, :-1], data[:, -1]
Y = Y.reshape((-1,1))
print(Y)

class Node:
	def __init__(self, data=None, children=None, split_on=None, pred_class=None, is_leaf = False):

		"""
	Parameters
	----------
	data: numpy.ndarray, default=None
		The dataset includes X and Y
	children: dict(feat_value: Node), default=None
		Dict of children
	split_on: int, default=None
		Index of the feature that node was split on that
	pred_class : str, default=None
		The predicted class for the node (only applicable to leaf nodes)
	is_leaf: bool, default=False
		Determine whether the node is leaf or not

	Examples
	--------
	>>> feat_index = 0     # Ear Shape
	>>> root = Node(data=all_data, split_on=feat_index)
	>>> pointy_node = Node(data=pointy_data, is_leaf=True)
	>>> floppy_node = Node(data=floppy_data, is_leaf=True)
	>>> root.children = {"Pointy": pointy_node, "Floppy": floppy_node}

	Visualization
	-------------
						  root  (data = all_data, split_on = 0, is_leaf=False)
						/    \
						/      \
						/        \
						/          \
					pointy_node     floppy_node
	(data=pointy_data, is_leaf=True)    (data=floppy_data, is_leaf=True)
	"""
		self.data = data
		self.children = children
		self.split_on = split_on
		self.pred_class = pred_class
		self.is_leaf = is_leaf

	def __init__(self):
		self.root = Node()

	def calculate_entropy(Y):
		"""
		Parameters:
		-----------
		Y: numpy.ndarray
			The labels array.

		Returns:
		-----------
		entropy: flaot
			The entropy value of the given labels.

		Examples:
		----------
		>>> Y_1 = np.array([[1], [1], [0], [0]])
		>>> DecisionTreeClassifier.calculate_entropy(Y_1)
		1.0
		>>> Y_2 = np.array([[1], [1], [1], [1]])
		>>> DecisionTreeClassifier.calculate_entropy(Y_2)
		0.0
		"""
		_, label_counts = np.unique(Y, return_counts=True)
		total_instances = len(Y)
		entropy = sum([label_count / total_instances * np.log2( 1 / (label_count / total_instances)) for label_count in label_counts])
		return entropy
	
