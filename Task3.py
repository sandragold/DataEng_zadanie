'''
Provided file called CPCT02220079.annotated.processed.vcf doesn't consist any data for chromosomes etc.
 Therefore only the commands which would be used are written
'''

import allel
import matplotlib.pyplot as plt
import numpy as np

#with open('CPCT02220079.annotated.processed.vcf', mode='r') as vcf:
#    print(vcf.read())

#Read the VCF file, using needed parameters: chromosom 12, positions 112204691-112247789
callset = allel.read_vcf('CPCT02220079.annotated.processed.vcf', region='12:112204691-112247789')
chrom = callset['variants/CHROM']
print(chrom)

'''Getting: Traceback (most recent call last):
  File "/PycharmProjects/MNM/Task3.py", line 15, in <module>
    chrom = callset['variants/CHROM']
TypeError: 'NoneType' object is not subscriptable'''

#To create a vcf file and save the variants
output = open("output.vcf", "w")
output.write(chrom)

'''It is also possible to use pysam for this:
from pysam import VariantFile

vcf_in = VariantFile("CPCT02220079.annotated.processed.vcf")  # auto-detect input format
vcf_out = VariantFile('-', 'w', header=vcf_in.header)

for rec in vcf_in.fetch('chr12', 112204691, 112247789):
    vcf_out.write(rec)'''



'''
To count insertions and deletions from vcf file the BEDOPS 2.4 (https://github.com/bedops/bedops) program was installed and run with following commands
in the bash terminal:

(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --snvs < CPCT02220079.annotated.processed.vcf | wc -l
       0
(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --insertions < CPCT02220079.annotated.processed.vcf > insertions.bed | wc -l
       0
(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --deletions < CPCT02220079.annotated.processed.vcf > deletions.bed | wc -l
       0
       
The result is as follow because of the content of the file. There is also a possibility to use a vcfstats method from vcflib.
'''

#To draw histograms for an example (randomly generated) data because of luck of yours
indels = np.random.randn(10000)
plt.hist(indels, histtype='bar', bins=50)
plt.xlabel("Indel size (bp)")
plt.ylabel("Number of indels")
plt.show()
