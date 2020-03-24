"""
This rule scans a fasta file and searches homopolymers and microsatellites.
More information at:
https://github.com/ding-lab/msisensor
"""
rule msi_scan:
    input:
        fasta_path
    output:
        temp("msisensor/scan/homopolymers_micosats.msi")
    message:
        "Scanning homopolymers and microsatellites"
    threads:
        1
    resources:
        mem_mb = (
            lambda wildcards, attempt: min(attempt * 4096, 20480)
        ),
        time_min = (
            lambda wildcards, attempt: min(attempt * 60, 380)
        )
    log:
        "logs/msisensor/scan.logs"
    params:
        extra = config["params"].get("msi_scan_extra", "")
    wrapper:
        f"{swv}/bio/msisensor/scan"

"""
This rule scans both tumor and normal bam pairs in search for msi
More information at: https://github.com/ding-lab/msisensor
"""
rule msi:
    input:
        unpack(get_bam_pair_w),
        unpack(get_bam_index_pairs_w),
        microsat = "msisensor/scan/homopolymers_micosats.msi"
    output:
        msi_scores = report(
            "msisensor/msi/{sample}",
            caption="../report/msi.rst",
            category="MSI"
        ),
        read_count = report(
            "msisensor/msi/{sample}_dis",
            caption="../report/read_count.rst",
            category="Read Count"
        ),
        somatic_sites = report(
            "msisensor/msi/{sample}_somatic",
            caption="../report/somatic.rst",
            category="Somatic"
        ),
        germline_sites = report(
            "msisensor/msi/{sample}_germline",
            caption="../report/germline.rst",
            category="Germline"
        )
    message:
        "Scanning {wildcards.sample} in search for MSI"
    threads:
        min(config["threads"], 8)
    resources:
        mem_mb = (
            lambda wildcards, attempt: min(attempt * 8192, 20480)
        ),
        time_min = (
            lambda wildcards, attempt: min(attempt * 40, 380)
        )
    log:
        "logs/msisensor/msi/{sample}.logs"
    wildcard_constraints:
        sample = r"[^/]+"
    params:
        extra = config["params"].get("msi_extra", ""),
        prefix = (lambda w: f"msisensor/msi/{w.sample}")
    wrapper:
        f"{swv}/bio/msisensor/msi"
