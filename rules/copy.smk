"""
This rule copies or soft links the bam files. It handles cold/hot storages
issues on a cluster. More information at:
https://github.com/tdayris-perso/snakemake-wrappers/blob/cp/bio/cp/
"""
rule copy_bams:
    input:
        lambda wildcards: bam_path_dict[wildcards.sample]
    output:
        temp("raw_data/{sample}.bam")
    message:
        "Copy/soft-link {wildcards.sample}"
    threads:
        1
    resources:
        mem_mb = (
            lambda wildcards, attempt: min(attempt * 256, 512)
        ),
        time_min = (
            lambda wildcards, attempt: min(attempt * 45, 180)
        )
    log:
        "logs/cp/{sample}.logs"
    params:
        extra = config["params"].get(
            "copy_extra",
            "--verbose"
        ),
        cold_storage = config.get(
            "cold_storage",
            [" "]
        )
    wrapper:
        f"{my_snw}/cp/bio/cp"


rule copy_bam_indexes:
    input:
        lambda wildcards: f"{bam_path_dict[wildcards.sample]}.bai"
    output:
        temp("raw_data/{sample}.bam.bai")
    message:
        "Copy/soft-link {wildcards.sample}"
    threads:
        1
    resources:
        mem_mb = (
            lambda wildcards, attempt: min(attempt * 256, 512)
        ),
        time_min = (
            lambda wildcards, attempt: min(attempt * 45, 180)
        )
    log:
        "logs/cp/{sample}.logs"
    params:
        extra = config["params"].get(
            "copy_extra",
            "--verbose"
        ),
        cold_storage = config.get(
            "cold_storage",
            [" "]
        )
    wrapper:
        f"{my_snw}/cp/bio/cp"


rule copy_ref:
    input:
        config["fasta"]
    output:
        temp(fasta_path)
    message:
        "Copy/soft-link fasta-formatted reference"
    threads:
        1
    resources:
        mem_mb = (
            lambda wildcards, attempt: min(attempt * 256, 512)
        ),
        time_min = (
            lambda wildcards, attempt: min(attempt * 45, 180)
        )
    log:
        "logs/cp/fasta.logs"
    params:
        extra = config["params"].get(
            "copy_extra",
            "--verbose"
        ),
        cold_storage = config.get(
            "cold_storage",
            [" "]
        )
    wrapper:
        f"{my_snw}/cp/bio/cp"
