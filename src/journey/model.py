# exmaple from sklearn website

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from journey.dataLoader import DataLoader
from journey.preprocessing import DataProcessor

data = DataLoader()
data.load_sklearn_sample_dateset()

processor = DataProcessor(data._data_set) # splits the data Automatically


X_plot = data._data_set.data[["proline", "hue"]]

scaler = StandardScaler()

X_plot_scaled = pd.DataFrame(
    scaler.fit_transform(X_plot),
    columns=X_plot.columns,
    index=X_plot.index,
)

y = data._data_set.data['target']
clf = KNeighborsClassifier(n_neighbors=20)


def fit_and_plot_model(X_plot, y, clf, ax):
    clf.fit(X_plot, y)
    disp = DecisionBoundaryDisplay.from_estimator(
        clf,
        X_plot,
        response_method="predict",
        alpha=0.5,
        ax=ax,
    )
    cmap = ListedColormap(disp.multiclass_colors_) # type: ignore
    disp.ax_.scatter(
        X_plot["proline"], X_plot["hue"], c=y, cmap=cmap, s=20, edgecolor="k"
    )
    disp.ax_.set_xlim((X_plot["proline"].min(), X_plot["proline"].max()))
    disp.ax_.set_ylim((X_plot["hue"].min(), X_plot["hue"].max()))
    return disp.ax_


fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))

fit_and_plot_model(X_plot, y, clf, ax1)
ax1.set_title("KNN without scaling")

fit_and_plot_model(X_plot_scaled, y, clf, ax2)
ax2.set_xlabel("scaled proline")
ax2.set_ylabel("scaled hue")
_ = ax2.set_title("KNN with scaling")

plt.show()