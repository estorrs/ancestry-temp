#!/bin/python

import argparse
import subprocess

import pandas as pd

OUTPUT_FOLDER = 'outputs/'

parser = argparse.ArgumentParser()

parser.add_argument('--vcf', type=str,
        help='The input vcf file')

parser.add_argument('--gzvcf', type=str,
        help='The compressed input vcf file')

parser.add_argument('--position-filter', type=str,
        help='The alleles file to be used during filtering\n\nFile contains tab seperated values in the following format: <CHROM>\t<POS>\t<REF>\t<ALT>\n\nThe file should have no header')

parser.add_argument('--variant-filter', type=str,
        help='The position file to be used during filtering\n\nFile contains tab seperated values in the following format: <CHROM>\t<POS>\n\nThe file should have no header')

parser.add_argument('--maf', type=int,
        help='The minimum allele frequency threshold')

parser.add_argument("--out", type=str, default='output',
        help='output file prefix')

args = parser.parse_args()


def filter_input_vcf(input_fp, compressed_input, position_filter_fp, variant_filter_fp=None, out_prefix=''):
    tool_args = ['--positions', args.position_filter]

    if compressed_input:
        tool_args += ['--gzvcf', input_fp]
    else:
        tool_args += ['--vcf', input_fp]

    tool_args += ['--out', OUTPUT_FOLDER + out_prefix + '.filtered']
    tool_args += ['--recode', '--recode-INFO-all']

    print('position filter')
    subprocess.check_output(['vcftools'] + tool_args)

    if variant_filter_fp:
        tool_args = [OUTPUT_FOLDER + out_prefix + '.filtered.recode.vcf', variant_filter_fp]
        tool_args += ['--out', OUTPUT_FOLDER + out_prefix + '.variant-filtered.vcf']

        print('variant filter')
        subprocess.check_output(['python', 'filtering_tool.py'] + tool_args)
        
        return OUTPUT_FOLDER + out_prefix + '.variant-filtered.vcf'

    return OUTPUT_FOLDER + out_prefix + '.filtered.recode.vcf'


def perform_pca(input_fp, maf=None, out_prefix=None):
    tool_args = ['--vcf', input_fp]

    if maf:
        tool_args += ['--maf', maf]

    tool_args += ['--out', OUTPUT_FOLDER + out_prefix]
    tool_args += ['--pca']

    print('pca')
    subprocess.check_output(['./../plink'] + tool_args)


def main():
    # is the initial input file compressed or not
    if args.gzvcf:
        compressed_input = True
        input_file = args.gzvcf
    else:
        compressed_input = False
        input_file = args.vcf

    # run through filter is position flag is given
    if args.position_filter:
        input_file = filter_input_vcf(input_file, compressed_input, args.position_filter,
                variant_filter_fp=args.variant_filter, out_prefix=args.out)

    # do pca
    perform_pca(input_file, maf=args.maf, out_prefix=args.out)


if __name__ == '__main__':
    main()
