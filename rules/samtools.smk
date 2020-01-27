rule index_bam:
    input:
        "raw_data/{sample}.bam"
    output:
        "raw_data/{sample}.bam.bai"
    message:
        "Indexing bam for msisensor msi"
    threads:
        1
    resources:
        mem_mb = 1536,
        time_min = 35
    log:
        "logs/samtools/index.{sample}.log"
    params:
        ""
    wrapper:
        f"{swv}/bio/samtools/index"
