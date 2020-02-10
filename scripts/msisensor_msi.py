"""Snakemake script for MSISensor msi"""

__author__ = "Thibault Dayris"
__copyright__ = "Copyright 2020, Dayris Thibault"
__email__ = "thibault.dayris@gustaveroussy.fr"
__license__ = "MIT"

from snakemake.shell import shell
from snakemake.utils import makedirs

# STDout contains the vcf file, it shall not be captured
log = snakemake.log_fmt_shell(stdout=True, stderr=True)

# Extra parameters default value is an empty string
extra = snakemake.params.get("extra", "")

shell(
    "msisensor msi"         # Tool and its sub-command
    " -d {snakemake.input.index}"     # Path to indexed fasta file
    " -n {snakemake.input.normal}"    # Path to normal bam
    " -t {snakemake.input.tumor}"  # Path to tumor bam
    " -o {snakemake.params.prefix}"  # Path to output distribution file
    " -b {snakemake.threads}"         # Maximum number of threads used
    " {extra}"       # Optional extra parameters
    " {log}"                # Logging behavior
)
