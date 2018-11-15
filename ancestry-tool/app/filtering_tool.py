#!/bin/python

import argparse

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("vcf_filepath", type=str, help='The vcf file to be filtered')
parser.add_argument("filter_filepath", type=str,
        help='The alleles file to be used during filtering\n\nFile contains tab seperated values in the following format: <CHROM>\t<POS>\t<REF>\t<ALT>\n\nThe file should have no header')
parser.add_argument("-o", "--out", type=str, help='output file prefix')

args = parser.parse_args()

def get_vcf_df(vcf_fn):
    f = open(vcf_fn)
    header = ''
    vcf_header = ''

    for line in f:
        vcf_header += line
        if 'CHROM\tPOS\tID' in line:
            header = line
            break

    df = pd.read_csv(f, delimiter='\t', header=None)

    # do headers
    headers = header.split('\t')
    # remove # if necessary
    if headers[0][0] == '#':
        headers[0] = headers[0][1:]
    df.columns = headers

    return df, vcf_header

def main():
    vcf_df, vcf_header = get_vcf_df(args.vcf_filepath)
    filter_df = pd.read_csv(open(args.filter_filepath), delimiter='\t', header=None)

    # maybe avoid hardcoding here?
    filter_df.columns = ['CHROM', 'POS', 'REF', 'ALT']

    df = pd.merge(filter_df, vcf_df, how='inner', on=list(filter_df.columns))

    # back into vcf format
    df_str = df.to_csv(None, header=None, index=None, sep='\t')
    vcf_str = vcf_header + df_str

    if args.out:
        f = open(args.out, 'w')
    else:
        f = open(args.vcf_filepath + '.filtered.vcf', 'w')

    f.write(vcf_str)
    f.close()


if __name__ == '__main__':
    main()
