import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_results(csv_path="results/noise_sweep_results.csv"):
    df = pd.read_csv(csv_path)

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 6)
    )

    # Plot 1: Logical Error Rate vs Noise
    for distance in sorted(df["Distance"].unique()):

        subset = (
            df[df["Distance"] == distance]
            .sort_values("Noise")
        )

        ax1.plot(
            subset["Noise"],
            subset["Logical_Error_Rate"],
            marker="o",
            label=f"Distance {distance}",
        )

    ax1.set_xscale("log")
    ax1.set_yscale("log")

    ax1.set_xlabel("Physical Noise Probability")
    ax1.set_ylabel("Logical Error Rate")

    ax1.set_title("Surface Code Performance")

    ax1.grid(
        True,
        which="both",
        ls="--",
        alpha=0.5
    )

    ax1.legend()

    # Plot 2: Decoder Scaling
    noise_subset = (
        df[df["Noise"] == 0.005]
        .sort_values("Detectors")
    )

    speeds = (
        noise_subset["Shots"]
        / noise_subset["Decoding_Time"]
    )

    ax2.plot(
        noise_subset["Detectors"],
        speeds,
        marker="s",
        color="purple",
        linestyle="-",
    )

    ax2.set_xscale("log")
    ax2.set_yscale("log")

    ax2.set_xlabel("Number of Detectors")
    ax2.set_ylabel("Decoding Speed (Shots/Second)")

    ax2.set_title(
        "Sparse Blossom Scaling (p = 0.005)"
    )

    ax2.grid(
        True,
        which="both",
        ls="--",
        alpha=0.5
    )

    plt.tight_layout()

    output_path = (
        "results/reproduction_plots.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Plots saved to '{output_path}'"
    )

    plt.show()


if __name__ == "__main__":
    plot_results()