Material and Methods:
#####################

Fasta-formatted reference genome was scanned using `MSIsensor <https://www.ncbi.nlm.nih.gov/pubmed/24371154>`_ . Scanned homopolymers and microsatellites were then scored within tumor/normal pairs.


* MSIsensor scan optional arguments: `{{snakemake.config.params.msi_scan_extra}}`
* MSIsensor msi optional arguments: `{{snakemake.config.params.msi_extra}}`

The whole pipeline is powered by both `Snakemake <https://snakemake.readthedocs.io>`_ , and `SnakemakeWrappers <https://snakemake-wrappers.readthedocs.io/>`_ .


Citations:
##########

MSIsensor:
  Niu, Beifang, et al. "MSIsensor: microsatellite instability detection using paired tumor-normal sequence data." Bioinformatics 30.7 (2014): 1015-1016.

  https://github.com/ding-lab/msisensor


Snakemake
  Köster, Johannes and Rahmann, Sven. “Snakemake - A scalable bioinformatics workflow engine”. Bioinformatics 2012.

  https://snakemake.readthedocs.io/
  https://snakemake-wrappers.readthedocs.io/
