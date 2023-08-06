import subprocess

from celescope.tools import utils
from celescope.tools.mkref import Mkref, super_opts
from celescope.__init__ import HELP_DICT


class Mkref_rna(Mkref):
    """
    ## Features
    - Create a genome reference directory.

    ## Output

    - STAR genome index files

    - Genome refFlat file

    - Genome config file
    ```
    $ cat celescope_genome.config
    [genome]
    genome_name = Homo_sapiens_ensembl_99
    genome_type = rna
    fasta = Homo_sapiens.GRCh38.dna.primary_assembly.fa
    gtf = Homo_sapiens.GRCh38.99.gtf
    refflat = Homo_sapiens_ensembl_99.refFlat
    ```
    """

    def __init__(self, genome_type, args, files=(), non_files=()):
        super().__init__(genome_type, args, files, non_files)
        self.refflat = f'{self.genome_name}.refFlat'

        self.gtf_temp = f'{self.genome_name}.gtf.temp'

    @utils.add_log
    def build_rna_star_index(self):
        cmd = (
            f'STAR \\\n'
            f'--runMode genomeGenerate \\\n'
            f'--runThreadN {self.thread} \\\n'
            f'--genomeDir ./ \\\n'
            f'--genomeFastaFiles {self.fasta} \\\n'
            f'--sjdbGTFfile {self.gtf} \\\n'
            f'--sjdbOverhang 100 \\\n'
        )
        if self.STAR_param:
            cmd += (" " + self.STAR_param)
        self.build_star_index.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)


    @utils.add_log
    def build_refflat(self):
        # remove lines without gene_id
        cmd = f"grep 'gene_id' {self.gtf} > {self.gtf_temp}"
        self.build_refflat.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)

        # ignore all errors
        cmd = (
            'gtfToGenePred -genePredExt -allErrors -ignoreGroupsWithoutExons \\\n'
            f'{self.gtf_temp} /dev/stdout | \\\n'
            'awk \'{print $12"\\t"$1"\\t"$2"\\t"$3"\\t"$4"\\t"$5"\\t"$6"\\t"$7"\\t"$8"\\t"$9"\\t"$10}\' \\\n'
            f'> {self.refflat} \\\n'
        )
        self.build_refflat.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)

        # remove temp file
        cmd = f"rm {self.gtf_temp}"
        self.build_refflat.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)

    def set_config_dict(self):
        super().set_config_dict()
        self.config_dict['refflat'] = self.refflat

    @staticmethod
    def parse_genomeDir(genomeDir):
        return Mkref.parse_genomeDir(genomeDir, files=('gtf', 'refflat', 'mt_gene_list'))


    @utils.add_log
    def run(self):
        super().run()
        self.build_refflat()
        self.build_star_index()



def mkref(args):
    genome_type = 'rna'
    # files do not contain refflat because refflat is not input argument
    with Mkref_rna(genome_type, args, files=('gtf', 'mt_gene_list'), non_files=('genomeSAindexNbases',)) as runner:
        runner.run()


def get_opts_mkref(parser, sub_program):
    super_opts(parser, sub_program)
    if sub_program:
        parser.add_argument(
            "--gtf",
            help="Required. Genome gtf file. Use absolute path or relative path to `genomeDir`.",
            required=True
        )
        parser.add_argument(
            "--mt_gene_list",
            help="""Mitochondria gene list file. Use absolute path or relative path to `genomeDir`.
It is a plain text file with one gene per line. 
If not provided, will use `MT-` and `mt-` to determine mitochondria genes.""",
            default="None"
        )
        parser.add_argument("--genomeSAindexNbases", help=HELP_DICT['genomeSAindexNbases'], default=14)
