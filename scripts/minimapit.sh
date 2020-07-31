#!/bin/bash

acc=$1
index=$2

esearch -db assembly -query ${acc} | elink -target nucleotide -name \
        assembly_nuccore_refseq | efetch -format fasta > ${acc}.fa

minimap2 -d ${index} ${acc}.fa

rm ${acc}.fa