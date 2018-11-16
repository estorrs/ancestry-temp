# ancestry-temp

## With Docker
docker pull estorrs/ancestry-tool

docker run -it --cpus 10 -v /host/data/folder:/app/data -v /host/output/folder:/app/outputs estorrs/ancestry-tool

$ python main.py --vcf data/path/to/vcf --position-filter data/path/to/position-filter --variant-filter data/path/to/variants-filter --out output-prefix

### to run with test example
$ python main.py --vcf tests/data/example.vcf --position-filter tests/data/example-positions.tsv --variant-filter tests/data/example-variant-filter.tsv --out example

