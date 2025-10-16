def set_style(plt):
    #plt.style.use('dark_background')
    bgcolor = '#262c33'
    plt.rcParams.update({
        "figure.facecolor": bgcolor,
        "axes.facecolor": bgcolor,
        "savefig.facecolor": bgcolor,
        "text.color": "white",
        "axes.labelcolor": "white",
        "axes.edgecolor": "#A9A9A9",
        "xtick.color": "white",
        "ytick.color": "white",
        "grid.color": "#444444",
        "grid.linestyle": "--",
        "legend.facecolor": "#282C34",
        "legend.edgecolor": "#A9A9A9",
        "legend.labelcolor": "white",
        "lines.color": "#61AFEF",
        "lines.linewidth": 2
    })