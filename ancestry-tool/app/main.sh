#!/bin/bash

# do filtering
# filter for chr and pos
vcftools --vcf $INPUT_VCF --positions $FILTER_POSITIONS --recode --recode-INFO-all --out outputs/$OUTPUT_PREFIX.filtered

# filter for right variants

# do pca
./../plink --vcf outputs/$OUTPUT_PREFIX.filtered.recode.vcf --pca --maf $MAF --out outputs/$OUTPUT_PREFIX
