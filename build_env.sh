source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda deactivate
conda env remove --name reulate
conda env create -f env.yml
conda activate reulate
python -m ipykernel install --user --name=reulate