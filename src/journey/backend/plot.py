import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay


def plot_decision_boundary(
    X,
    y,
    ax=None,
    disp: None | DecisionBoundaryDisplay = None,
    title=None,
):
    if ax is None and disp is None:
        _, ax = plt.subplots()
    else:
        assert disp is not None
        ax = disp.ax_

    cmap = ListedColormap(disp.multiclass_colors_) # type: ignore

    ax.scatter(
        X.iloc[:, 0],
        X.iloc[:, 1],
        c=y,
        cmap=cmap,
        s=20,
        edgecolor="k",
    )

    ax.set_xlim(
        X.iloc[:, 0].min(),
        X.iloc[:, 0].max()
    )

    ax.set_ylim(
        X.iloc[:, 1].min(),
        X.iloc[:, 1].max()
    )

    if title:
        ax.set_title(title)

    return ax


def plot(
    X, y, title, disp,
    figsize=(12, 6),
):
    plot_decision_boundary(
        X=X,
        y=y,
        title=title,
        disp=disp
    )