"""Snakemake script for MSISensor Scan"""

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
    "msisensor scan "   # Tool and its sub-command
    "-d {input} "       # Path to fasta file
    "-o {output} "      # Path to output file
    "{params.extra} "   # Optional extra parameters
    "{log}"             # Logging behavior
)
