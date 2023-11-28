
# python scripts/figures/scatter-energy.py $(pwd)
# python scripts/figures/plot-lattices.py $(pwd)
# python scripts/figures/plot-meshgrid.py $(pwd)

cd output/figures
# convert -delay 60 -loop 0 -deconstruct lattices/*.png lattice.gif
gifsicle --resize 800x_ --colors 32 lattice.gif > _lattice.gif
