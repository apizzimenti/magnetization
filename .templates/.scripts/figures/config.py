
from ateams.common import Bunch
import numpy as np


################################################################################
### HELPERS ####################################################################
################################################################################
def xscale(ax, scale, base=10):
	ax.set_xscale(scale, base=base)
	return ax

def xticks(ax, X, labels=[]):
	ax.set_xticks(X)
	ax.set_xticklabels([f"${t}$" for t in X] if len(labels) < 1 else labels)
	return ax

################################################################################
### PLOT DEFAULTS ##############################################################
################################################################################
plot = Bunch()
plot.rcParams = {
	"text.usetex": True,
	"font.family": "Helvetica"
}

plot.figsize = (5,3)
plot.dpi = 1200
plot.bbox_inches = "tight"


################################################################################
### AUTOCORRELATION ############################################################
################################################################################
autocorrelation = Bunch()

############################################
### AUTOCORRELATION.EXPONENTS ##############
############################################
autocorrelation.exponents = Bunch()
autocorrelation.exponents.rcParams = plot.rcParams
autocorrelation.exponents.figsize = plot.figsize

autocorrelation.exponents.scatter = dict(
	marker="s",
	facecolor="w",
	edgecolors="k",
	zorder=10000
)

autocorrelation.exponents.plot = dict(
	color="k"
)

autocorrelation.exponents.fill_between = dict(
	color="k",
	alpha=1/8,
	edgecolor="None"
)

autocorrelation.exponents.xscale = lambda ax: xscale(ax, "log", np.sqrt(2))
autocorrelation.exponents.xticks = lambda ax, X: xticks(ax, X)

autocorrelation.exponents.name = lambda statistic: f"autocorrelation.exponents.{statistic}.png"
autocorrelation.exponents.savefig = dict(
	dpi=plot.dpi,
	bbox_inches=plot.bbox_inches
)


############################################
### AUTOCORRELATION.DECAY ##################
############################################
autocorrelation.decay = Bunch()
autocorrelation.decay.rcParams = plot.rcParams
autocorrelation.decay.figsize = plot.figsize


autocorrelation.decay.scatter = dict(
	marker="x",
	facecolor="red",
	edgecolors="None",
	zorder=1000
)

autocorrelation.decay.plot = dict(
	color="k"
)

autocorrelation.decay.axvspan = dict(
	facecolor="k",
	alpha=1/8,
	edgecolor="None"
)

autocorrelation.decay.xscale = lambda ax: xscale(ax, "log", 10)
autocorrelation.decay.xticks = lambda ax, X: xticks(ax, X)

autocorrelation.decay.name = lambda statistic, L: f"autocorrelation.decay.{statistic}.{L}.png"
autocorrelation.decay.savefig = dict(
	dpi=plot.dpi,
	bbox_inches=plot.bbox_inches
)
