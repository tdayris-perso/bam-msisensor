Material and Methods:
#####################

Fasta-formatted reference genome was scanned using `MSIsensor <https://www.ncbi.nlm.nih.gov/pubmed/24371154>`_ . Scanned homopolymers and microsatellites were then scored within tumor/normal pairs. The whole pipeline is powered by both `Snakemake <https://snakemake.readthedocs.io>`_ , and `SnakemakeWrappers <https://snakemake-wrappers.readthedocs.io/>`_ .

* MSIsensor scan optional arguments: `{{snakemake.config.params.msi_scan_extra}}`
* MSIsensor msi optional arguments: `{{snakemake.config.params.msi_extra}}`


Citations:
##########

This pipeline stands on best practices found in multiple high impact papers, published in Nature, Cell, Bioinformatics, and others.

MSIsensor:
  Niu, Beifang, et al. "MSIsensor: microsatellite instability detection using paired tumor-normal sequence data." Bioinformatics 30.7 (2014): 1015-1016.

  Why MSIsensor? MSIsensor has been cited 149 times since 2016, including Nature, Nature medecine, Cell, and others. It's main feature relays on the analysis of cancer data, from cell lines to larger groups of patients.

  https://github.com/ding-lab/msisensor


Snakemake
  Köster, Johannes and Rahmann, Sven. “Snakemake - A scalable bioinformatics workflow engine”. Bioinformatics 2012.

  Why Snakemake? Snakemake is a very popular workflow manager in data science and bioinformatics. It has about three new citations per week within the scopes of biology, medicine and bioinformatics.

  https://snakemake.readthedocs.io/
  https://snakemake-wrappers.readthedocs.io/
