import snakemake.utils  # Load snakemake API
import os               # Operating system operations
import sys              # System related operations

# Python 3.7 is required
if sys.version_info < (3, 7):
    raise SystemError("Please use Python 3.7 or later.")

# Snakemake 5.8.0 at least is required
snakemake.utils.min_version("5.8.0")

include: "rules/common.smk"
include: "rules/copy.smk"
# include: "rules/samtools.smk"
include: "rules/msisensor.smk"

workdir: config.get("workdir", os.getcwd())
image = config.get(
    "singularity_docker_image",
    "docker://continuumio/miniconda3:4.4.10"
)

singularity: image
localrules: copy_bams, copy_ref

rule target:
    input:
        **target_dict
    message:
        "Finishing the MSI-sensor pipeline"
