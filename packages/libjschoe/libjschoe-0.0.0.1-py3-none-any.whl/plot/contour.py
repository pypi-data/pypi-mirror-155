import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# data_url = 'https://raw.githubusercontent.com/alexmill/website_notebooks/master/data/data_3d_contour.csv'


def contour_from_csv(
    file="result.csv",
    title="S-bend 2 stage 2000um-VOA performance",
    x_col="electric power1(mW)",
    y_col="electric power2(mW)",
    z_col="transmitted power(dBm)",
    resolution=50,
    contour_method="linear",
):
    df = pd.read_csv(file)
    x = df[x_col].values
    y = df[y_col].values
    z = df[z_col].values

    X, Y, Z = plot_contour(x, y, z, resolution, contour_method)

    with plt.style.context("seaborn-white"):
        fig, ax = plt.subplots(figsize=(13, 8))
        # ax.scatter(x, y, color="black", linewidth=1, edgecolor="ivory", s=50)
        CS = ax.contourf(X, Y, Z, cmap="viridis",)  # alpha=1)

        ax.set_title(title, fontsize=24)
        ax.set_xlabel(x_col, fontsize=18)
        ax.set_ylabel(y_col, fontsize=18)

        cbar = fig.colorbar(CS)
        cbar.ax.set_ylabel(z_col, fontsize=14)

        plt.show()

    # return X, Y, Z


# contour_data = pd.read_csv("res.csv")

# x = contour_data["electric power1(mW)"].values
# y = contour_data["electric power2(mW)"].values
# z = contour_data["transmitted power(dBm)"].values


def plot_contour(x, y, z, resolution=50, contour_method="linear"):
    resolution = str(resolution) + "j"
    X, Y = np.mgrid[
        min(x) : max(x) : complex(resolution), min(y) : max(y) : complex(resolution)
    ]
    points = [[a, b] for a, b in zip(x, y)]
    Z = griddata(points, z, (X, Y), method=contour_method)
    return X, Y, Z


# X, Y, Z = plot_contour(x, y, z, resolution=50, contour_method="linear")

# with plt.style.context("seaborn-white"):
#     fig, ax = plt.subplots(figsize=(13, 8))
#     CS = ax.contourf(X, Y, Z, cmap="viridis",)

#     ax.set_title("S-bend 2 stage 2000um-VOA performance", fontsize=24)
#     ax.set_xlabel("VOA_1 Electric Power(mW)", fontsize=18)
#     ax.set_ylabel("VOA_2 Electric Power(mW)", fontsize=18)


# cbar = fig.colorbar(CS)
# cbar.ax.set_ylabel("Transmission (dBm)", fontsize=14)

# plt.show()

contour_from_csv(file="res.csv")
