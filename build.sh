
module load gnu10
module load python
export PYTHONPATH=~/lib/python:$PYTHONPATH

cd ~/projects/magnetization/potts/
python setup.py build_ext --inplace

module unload gnu10
module unload python
