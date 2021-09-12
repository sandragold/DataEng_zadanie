"""
Task 4 code
"""
import pandas as pd

INDELS = "./T1_vs_N1_head.strelka.somatic.indels.norm.vcf"
SNVS = "./T1_vs_N1_head.strelka.somatic.snvs.norm.vcf"
TAR_POS = 1
TIR_POS = 2


def get_vcf_names(vcf_path):
    with open(vcf_path, "rt") as file:
        for line in file:
            if line.startswith("#CHROM"):
                vcf_names = [x.strip("\n") for x in line.split('\t')]
                break
    return vcf_names


def get_ref_counts(row):
    try:
        return int(row.FORMAT.split(":").index(row.REF+"U")) - 3
    except AttributeError:
        return None


def get_alt_counts(row):
    try:
        return int(row.FORMAT.split(":").index(row.ALT+"U")) - 3
    except AttributeError:
        return None


def get_tier1_ref_counts(row, group="NORMAL"):
    try:
        return row[group].split(",")[0].split(":")[int(row["refCounts"])]
    except AttributeError:
        return None


def get_tier1_alt_counts(row, group="NORMAL"):
    try:
        return row[group].split(",")[0].split(":")[int(row["altCounts"])]
    except AttributeError:
        return None


def get_vaf_score(row, group="NORMAL"):
    try:
        return int(row[f"tier1AltCounts_{group}"])/ (int(row[f"tier1AltCounts_{group}"]) + int(row[f"tier1RefCounts_{group}"]))
    except (AttributeError, ZeroDivisionError, TypeError):
        return None


def get_somatic_vaf(df):
    """
    refCounts = Value of FORMAT column $REF + “U” (e.g. if REF="A" then use the value in FOMRAT/AU)
    altCounts = Value of FORMAT column $ALT + “U” (e.g. if ALT="T" then use the value in FOMRAT/TU)
    tier1RefCounts = First comma-delimited value from $refCounts
    tier1AltCounts = First comma-delimited value from $altCounts
    Somatic allele freqeuncy (VAF) is $tier1AltCounts / ($tier1AltCounts + $tier1RefCounts)
    """
    df['refCounts'] = df.apply(lambda row: get_ref_counts(row), axis=1)
    df['altCounts'] = df.apply(lambda row: get_alt_counts(row), axis=1)
    df['tier1RefCounts_NORMAL'] = df.apply(lambda row: get_tier1_ref_counts(row), axis=1)
    df['tier1AltCounts_NORMAL'] = df.apply(lambda row: get_tier1_alt_counts(row), axis=1)
    df['VAF_NORMAL'] = df.apply(lambda row: get_vaf_score(row), axis=1)
    df['tier1RefCounts_TUMOR'] = df.apply(lambda row: get_tier1_ref_counts(row, group="TUMOR"), axis=1)
    df['tier1AltCounts_TUMOR'] = df.apply(lambda row: get_tier1_alt_counts(row, group="TUMOR"), axis=1)
    df['VAF_TUMOR'] = df.apply(lambda row: get_vaf_score(row, group="TUMOR"), axis=1)


def get_tier1_ref_counts_indels(row, group="NORMAL"):
    try:
        return row[group].split(",")[0].split(":")[TAR_POS]
    except AttributeError:
        return None


def get_tier1_alt_counts_indels(row, group="NORMAL"):
    try:
        return row[group].split(",")[0].split(":")[TIR_POS]
    except AttributeError:
        return None


def get_indels_vaf(df):
    """
    tier1RefCounts = First comma-delimited value from FORMAT/TAR
    tier1AltCounts = First comma-delimited value from FORMAT/TIR
    Somatic allele frequency is (VAF) $tier1AltCounts / ($tier1AltCounts + $tier1RefCounts)
    """
    df["tier1RefCounts_NORMAL"] = df.apply(lambda row: get_tier1_ref_counts_indels(row), axis=1)
    df["tier1AltCounts_NORMAL"] = df.apply(lambda row: get_tier1_alt_counts_indels(row), axis=1)
    df['VAF_NORMAL'] = df.apply(lambda row: get_vaf_score(row), axis=1)

    df["tier1RefCounts_TUMOR"] = df.apply(lambda row: get_tier1_ref_counts_indels(row, group="TUMOR"), axis=1)
    df["tier1AltCounts_TUMOR"] = df.apply(lambda row: get_tier1_alt_counts_indels(row, group="TUMOR"), axis=1)
    df['VAF_TUMOR'] = df.apply(lambda row: get_vaf_score(row, group="TUMOR"), axis=1)


def main():
    """ Main script module """
    # load files
    names = get_vcf_names(INDELS)
    indels = pd.read_csv(INDELS, comment='#', delim_whitespace=True, header=None, names=names)

    names = get_vcf_names(SNVS)
    snvs = pd.read_csv(SNVS, comment='#', delim_whitespace=True, header=None, names=names)

    # compute VAF for indels
    get_indels_vaf(indels)
    indels.to_csv(INDELS+".vaf", sep="\t", index=False)

    # compute VAF for somatics
    get_somatic_vaf(snvs)
    snvs.to_csv(SNVS+".vaf", sep="\t", index=False)


if __name__ == "__main__":
    main()
