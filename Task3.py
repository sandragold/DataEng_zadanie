'''
Provided file called CPCT02220079.annotated.processed.vcf doesn't consist any data for chromosomes etc.
 Therefore only the commands which would be used are written
'''

import allel
import matplotlib.pyplot as plt

#with open('CPCT02220079.annotated.processed.vcf', mode='r') as vcf:
#    print(vcf.read())


callset = allel.read_vcf('CPCT02220079.annotated.processed.vcf', region='12:112204691-112247789')
chrom = callset['variants/CHROM']
print(chrom)

'''Getting: Traceback (most recent call last):
  File "/PycharmProjects/MNM/Task3.py", line 15, in <module>
    chrom = callset['variants/CHROM']
TypeError: 'NoneType' object is not subscriptable'''

output = open("output.vcf", "w")
output.write(chrom)

'''It is also possible to use pysam for this:
from pysam import VariantFile

vcf_in = VariantFile("CPCT02220079.annotated.processed.vcf")  # auto-detect input format
vcf_out = VariantFile('-', 'w', header=vcf_in.header)

for rec in vcf_in.fetch('chr12', 112204691, 112247789):
    vcf_out.write(rec)'''




'''Draw histograms of the insertion and deletion lengths in the input file for each of the chromosomes. 
Place the drawing and table in the repository.


To count insertions and deletions from vcf file the BEDOPS 2.4 (https://github.com/bedops/bedops) program was installed and run with following commands
in the bash terminal:

(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --snvs < /Users/sandra.goldowska/MNM/CPCT02220079.annotated.processed.vcf | wc -l
       0
(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --insertions < /Users/sandra.goldowska/MNM/CPCT02220079.annotated.processed.vcf > insertions.bed | wc -l
       0
(base) MacBook-Pro-6:~ sandra.goldowska$ vcf2bed --deletions < /Users/sandra.goldowska/MNM/CPCT02220079.annotated.processed.vcf > deletions.bed | wc -l
       0
       
There is also a possibility to use a vcfstats method from vcflib.
'''

#To draw histograms
# x = [insertions, value2, value3,....]
# # plt.hist(x, bins = 10)
# # plt.show()
