"""
While other .smk files contains rules and pure snakemake instructions, this
one gathers all the python instructions surch as config mappings or input
validations.
"""

import pandas as pd


from snakemake.utils import validate

from typing import Any, Dict

my_snw = "https://raw.githubusercontent.com/tdayris-perso/snakemake-wrappers"
swv = "0.50.3"


configfile: "config.yaml"
validate(config, schema="../schemas/config.schemas.yaml")

design = pd.read_csv(
    config["design"],
    sep="\t",
    header=0,
    index_col=None,
    dtype=str
)
design.set_index(design["Sample_id"])
validate(design, schema="../schemas/design.schemas.yaml")

report: "../report/general.rst"


def get_bam_from_path() -> Dict[str, str]:
    """
    This function gives the correspondancy between real bam paths, and the
    ones used in this pipeline. It returns a dictionnary:

    {sample1_N: real_path to normal sample,
     sample1_T: real_path to tumor  sample, ...}

    Input paths are not predictable, besides in design file.
    All output bams, will be in raw_data/{sample_id}.bam
    """
    result = {}

    design_iterator = zip(
        design["Sample_id"],
        design["Normal_Bam"],
        design["Tumor_Bam"]
    )

    for sample, normal, tumor in design_iterator:
        result[f"{sample}_N"] = normal
        result[f"{sample}_T"] = tumor

    return result


def get_bam_pairs() -> Dict[str, Dict[str, str]]:
    """
    This function gives the correspondancy between sample id and bam pairs.
    It returns a dictionnary:

    {sample_id: {normal: bam_normal, tumor: bam_tumor}, ...}
    """
    return {
        sample: {
            "normal": f"raw_data/{sample}_N.bam",
            "tumor": f"raw_data/{sample}_T.bam"
        }
        for sample in design["Sample_id"]
    }


def get_bam_pair_w(wildcards: Any) -> Dict[str, Dict[str, str]]:
    """
    This function returns a single pair of normal/tumor bams from a given
    sample id, as a dictionnary:
    {normal: bam_normal, tumor: bam_tumor}
    """
    return bam_pairs_dict[wildcards.sample]


def get_bam_index_pairs_w(wildcards: Any) -> Dict[str, Dict[str, str]]:
    """
    This function returns a single pair of normal/tumor bams from a given
    sample id, as a dictionnary:
    {normal: bam_normal, tumor: bam_tumor}
    """
    return {
        f"{k}_idx": f"{v}.bai"
        for k, v in bam_pairs_dict[wildcards.sample].items()
    }


def get_target_dict() -> Dict[str, Any]:
    """
    This function calls all important output
    """
    return {
        "msi_scores": expand(
            "msisensor/msi/{sample}",
            sample=bam_pairs_dict.keys()
        ),
        "read_count": expand(
            "msisensor/msi/{sample}_dis",
            sample=bam_pairs_dict.keys()
        ),
        "somatic_sites": expand(
            "msisensor/msi/{sample}_somatic",
            sample=bam_pairs_dict.keys()
        ),
        "germline_sites": expand(
            "msisensor/msi/{sample}_germline",
            sample=bam_pairs_dict.keys()
        )
    }


fasta_path = f"genome/{os.path.basename(config['fasta'])}"
bam_path_dict = get_bam_from_path()
bam_pairs_dict = get_bam_pairs()
target_dict = get_target_dict()
