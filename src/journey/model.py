# exmaple from sklearn website

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from journey.dataLoader import DataLoader
from journey.plot import *
from journey.preprocessing import DataProcessor

data_set = DataLoader().load_sklearn_sample_dateset()

processor = DataProcessor(data_set._data_set) # splits the data Automatically


X_plot = data_set._data_set.data[["proline", "hue"]]

scaler = StandardScaler()

X_plot_scaled = pd.DataFrame(
    scaler.fit_transform(X_plot),
    columns=X_plot.columns,
    index=X_plot.index,
)

y = data_set._data_set.data['target']

model = KNeighborsClassifier(n_neighbors=20).fit(X_plot_scaled, y)
disp = DecisionBoundaryDisplay.from_estimator(
        model,
        X_plot_scaled,
        response_method="predict",
        alpha=0.5,
    )

plot(
    X = X_plot_scaled,
    y = y,
    title = "KNN with scaling",
    disp=disp
)

plt.show()