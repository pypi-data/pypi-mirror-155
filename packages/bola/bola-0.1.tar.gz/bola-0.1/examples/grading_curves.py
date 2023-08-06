from bola import psd

import matplotlib
import matplotlib.pyplot as plt


def main():

    N_classes = 5
    d_max = 16

    gcs = [
        psd.GradingCurves.A16,
        psd.GradingCurves.B16,
        psd.GradingCurves.C16,
        psd.GradingCurves.fuller(0.25, 16, 0.5),
    ]
    gcs = [psd.n_largest(gc, N_classes) for gc in gcs]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
    factors = (2, 3, 5, 10)

    for ax, factor in zip(axes.flat, factors):
        ax.set_title("sampled in V = ({} * d_max)**3".format(factor))
        ax.set_xlabel("particle diameter")
        ax.set_ylabel("particle mass CDF")

        V_box = (factor * d_max) ** 3

        for gc in gcs:
            radii = psd.sample_grading_curve(gc, V_box)
            d, v = zip(*gc)
            ax.semilogx(d, v, ":kx", label="target")
            ax.semilogx(*psd.build_grading_curve(radii, V_box), "-r", label="sampled")

        ax.set_xticks(d)
        ax.xaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,g}"))

    plt.show()


if __name__ == "__main__":
    main()
