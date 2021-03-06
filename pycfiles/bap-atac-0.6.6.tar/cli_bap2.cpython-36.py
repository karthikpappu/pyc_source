# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clareau/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/cli_bap2.py
# Compiled at: 2019-11-09 17:28:16
# Size of source mod 2**32: 14310 bytes
import click, os, os.path, sys, shutil, yaml, random, string, itertools, time, pysam
from pkg_resources import get_distribution
from subprocess import call, check_call
from .bapHelp import *
from .bap2ProjectClass import *
from ruamel import yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString as sqs

@click.command()
@click.version_option()
@click.argument('mode', type=(click.Choice(['bam', 'check', 'support'])))
@click.option('--input', '-i', help='Input for bap2-- a .bam file with an index.')
@click.option('--output', '-o', default='bap_out', help='Output directory for analysis; this is where everything is housed.')
@click.option('--name', '-n', default='default', help='Name for all of the output files (default: uses the .bam prefix)')
@click.option('--ncores', '-c', default='detect', help='Number of cores to run the main job in parallel.')
@click.option('--reference-genome', '-r', default='hg19', help='Specifcy supported reference genome. Check `bap2 support` for a list')
@click.option('--cluster', default='', help='Message to send to Snakemake to execute jobs on cluster interface; see Snakemake documentation.')
@click.option('--jobs', default='0', help='Max number of jobs to be running concurrently on the cluster interface; see Snakemake documentation.')
@click.option('--peak-file', '-pf', default='', help='If supplied, compute FRIP (in QC stats) and generate Summarized Experiment (not required)')
@click.option('--barcode-prior', '-bp', default='', help='If supplied, a two-column file that imposes barcode merges to occur within a prior annotation (e.g. donor or hash).')
@click.option('--minimum-barcode-fragments', '-bf', default=0, help='Minimum number of fragments to be thresholded for doublet merging; by default, determines a threshold via knee-calling')
@click.option('--barcode-whitelist', '-w', default='', help='File path of a whitelist of bead barcodes (one per line) to be used in lieu of a fixed threshold.')
@click.option('--minimum-jaccard-index', '-ji', default=0.0, help='Minimum jaccard index for collapsing bead barcodes to cell barcodes')
@click.option('--nc-threshold', '-nc', default=6, help='Number of barcodes that a paired-end read must be observed for the read to be filtered.')
@click.option('--regularize-threshold', '-rt', default=4, help='Minimum number of inserts two barcodes must share to be counted per-chromosome. Anything less than this number will be shrunk to 0.')
@click.option('--one-to-one', '-oo', is_flag=True, help='Enforce that each bead barcode maps to one unique drop barcode (cancels the merging)')
@click.option('--barcoded-tn5', is_flag=True, help='Process data knowing that the barcodes were generated with a barcoded Tn5; assumes that the last 6 characters of the barcode sequence correspond to the barcoded Tn5 sequence.')
@click.option('--keep-read-names', is_flag=True, help='Retain the read namems that correspond to the final fragment assemebled in the final output.')
@click.option('--extract-mito', '-em', is_flag=True, help='Extract mitochondrial DNA and annotate with droplet barcodes.')
@click.option('--keep-temp-files', '-z', is_flag=True, help='Keep all intermediate files.')
@click.option('--snakemake-stdout', '-ss', is_flag=True, help='Write what would typically go in the snakemake log file into stdout.')
@click.option('--mapq', '-mq', default=30, help='Minimum mapping quality to keep read for downstream analyses')
@click.option('--max-insert', '-mi', default=2000, help='Max insert size to keep fragment for downstream analysis')
@click.option('--all-pairs', '-ap', is_flag=True, help='Include all read pairs when assembling fragments (not just proper pairs, which is the default)')
@click.option('--bedtools-genome', '-bg', default='', help='Path to bedtools genome file; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--blacklist-file', '-bl', default='', help='Path to bed file of blacklist; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--tss-file', '-ts', default='', help='Path bed file of transcription start sites; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--mito-chromosome', '-mc', default='default', help='Name of the mitochondrial chromosome; only necessary to specify if the reference genome is unknown but will overwrite default if necessary')
@click.option('--r-path', default='', help='Path to R; by default, assumes that R is in PATH')
@click.option('--bedtools-path', default='', help='Path to bedtools; by default, assumes that bedtools is in PATH')
@click.option('--samtools-path', default='', help='Path to samtools; by default, assumes that samtools is in PATH')
@click.option('--bgzip-path', default='', help='Path to bgzip; by default, assumes that bgzip is in PATH')
@click.option('--tabix-path', default='', help='Path to tabix; by default, assumes that tabix is in PATH')
@click.option('--snakemake-path', default='', help='Path to snakemake; by default, assumes that snakemake is in PATH')
@click.option('--drop-tag', '-dt', default='DB', help='New tag in the .bam file(s) that will be the name of the droplet barcode.')
@click.option('--bead-tag', '-bt', default='XB', help='Tag in the .bam file(s) that points to the bead barcode (should already exist).')
def main(mode, input, output, name, ncores, reference_genome, cluster, jobs, peak_file, barcode_prior, minimum_barcode_fragments, barcode_whitelist, minimum_jaccard_index, nc_threshold, regularize_threshold, one_to_one, barcoded_tn5, keep_read_names, extract_mito, keep_temp_files, snakemake_stdout, mapq, max_insert, all_pairs, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path, snakemake_path, drop_tag, bead_tag):
    """
        bap2: ~improved~ Bead-based scATAC-seq data Processing 

        Caleb Lareau, clareau <at> broadinstitute <dot> org 

        
        mode = ['bam', 'check', 'support']

        """
    __version__ = get_distribution('bap-atac').version
    script_dir = os.path.dirname(os.path.realpath(__file__))
    click.echo(gettime() + 'Starting bap2 pipeline v%s' % __version__)
    output = output.rstrip('/')
    rawsg = os.popen('ls ' + script_dir + '/anno/bedtools/*.sizes').read().strip().split('\n')
    supported_genomes = [x.replace(script_dir + '/anno/bedtools/chrom_', '').replace('.sizes', '') for x in rawsg]
    if ncores == 'detect':
        ncores = str(available_cpu_count())
    else:
        ncores = str(ncores)
    snakeclust = ''
    njobs = int(jobs)
    if njobs > 0:
        if cluster != '':
            snakeclust = ' --jobs ' + str(jobs) + " --cluster '" + cluster + "' "
            click.echo(gettime() + 'Recognized flags to process jobs on a cluster.')
    else:
        if mode == 'support':
            click.echo(gettime() + 'List of built-in genomes supported in bap:')
            click.echo(gettime() + str(supported_genomes))
            sys.exit(gettime() + 'Specify one of these genomes or provide your own files (see documentation).')
        if reference_genome in ('hg19-mm10', 'hg19_mm10_c', 'hg19-mm10_nochr'):
            speciesMix = True
        else:
            speciesMix = False
    p = bap2Project(script_dir, supported_genomes, mode, input, output, name, ncores, reference_genome, cluster, jobs, peak_file, barcode_prior, minimum_barcode_fragments, barcode_whitelist, minimum_jaccard_index, nc_threshold, regularize_threshold, one_to_one, barcoded_tn5, keep_read_names, extract_mito, keep_temp_files, snakemake_stdout, mapq, max_insert, all_pairs, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path, snakemake_path, drop_tag, bead_tag, speciesMix)
    if mode == 'bam':
        click.echo(gettime() + 'Attempting to parse supplied .bam files for analysis.')
        if not os.path.exists(input):
            sys.exit('Cannot parse supplied .bam file in --input')
        if not os.path.exists(input + '.bai'):
            sys.exit('Index supplied .bam before proceeding')
        idxstats = pysam.idxstats(input)
        chrs_bam = [x.split('\t')[0] for x in idxstats.split('\n')]
        chrs_ref = []
        with open(p.bedtoolsGenomeFile) as (f):
            for line in f:
                if line.rstrip():
                    chrs_ref.append(line.split('\t')[0])

        chrs_both = intersection(chrs_bam, chrs_ref)
        if len(chrs_both) > 0:
            click.echo(gettime() + 'Found ' + str(len(chrs_both)) + ' chromosomes for analysis (including mitochondria).')
        else:
            sys.exit('Found no overlapping chromosomes between bam and reference. Check reference genome specification with the --reference-genome flag.')
        of = output
        logs = of + '/logs'
        logs_bedpe = logs + '/frag'
        fin = of + '/final'
        mito = of + '/mito'
        temp = of + '/temp'
        temp_filt_split = temp + '/filt_split'
        temp_frag_overlap = temp + '/frag_overlap'
        knee = of + '/knee'
        temp_drop_barcode = temp + '/drop_barcode'
        folders = [
         of, logs, logs_bedpe, fin, mito, temp,
         temp_filt_split, temp_frag_overlap, temp_drop_barcode, knee,
         of + '/.internal/parseltongue', of + '/.internal/samples']
        mkfolderout = [make_folder(x) for x in folders]
        if not os.path.exists(of + '/.internal/README'):
            with open(of + '/.internal/README', 'w') as (outfile):
                outfile.write("This folder creates important (small) intermediate; don't modify it.\n\n")
        if not os.path.exists(of + '/.internal/parseltongue/README'):
            with open(of + '/.internal/parseltongue/README', 'w') as (outfile):
                outfile.write("This folder creates intermediate output to be interpreted by Snakemake; don't modify it.\n\n")
        if not os.path.exists(of + '/.internal/samples/README'):
            with open(of + '/.internal' + '/samples' + '/README', 'w') as (outfile):
                outfile.write("This folder creates samples to be interpreted by Snakemake; don't modify it.\n\n")
        click.echo(gettime() + 'Splitting input bam files by chromosome for parallel processing.')
        click.echo(gettime() + 'User specified ' + ncores + ' cores for parallel processing.')
        line1 = 'python ' + script_dir + '/bin/python/20_names_split_filt.py --input ' + p.bamfile
        line2 = ' --name ' + p.name + ' --output ' + temp_filt_split + ' --barcode-tag '
        line3 = p.bead_tag + ' --bedtools-reference-genome ' + p.bedtoolsGenomeFile
        line4 = ' --mito-chr ' + p.mitochr + ' --ncores ' + str(ncores) + ' --mapq ' + str(mapq)
        filt_split_cmd = line1 + line2 + line3 + line4
        os.system(filt_split_cmd)
        click.echo(gettime() + 'Processing bam file using a Snakemake workflow. This is the most computationally intensive step.')
        y_s = of + '/.internal/parseltongue/bap.object.bam.yaml'
        with open(y_s, 'w') as (yaml_file):
            yaml.dump((dict(p)), yaml_file, default_flow_style=False, Dumper=(yaml.RoundTripDumper))
        os.system('cp ' + y_s + ' ' + logs + '/' + p.name + '.parameters.txt')
        snake_stats = logs + '/' + p.name + '.snakemake.stats'
        snake_log = logs + '/' + p.name + '.snakemake.log'
        if snakemake_stdout:
            snake_log_preference = ''
        else:
            snake_log_preference = ' &>' + snake_log
        snakecmd_chr = p.snakemake + snakeclust + ' --snakefile ' + script_dir + '/bin/snake/Snakefile.bap2.chr --cores ' + ncores + ' --config cfp="' + y_s + '" --stats ' + snake_stats + snake_log_preference
        os.system(snakecmd_chr)
        finalBamFile = p.output + '/final/' + p.name + '.bap.bam'
        if os.path.exists(finalBamFile):
            click.echo(gettime() + 'Finished processing via Snakemake.')
        else:
            sys.exit(gettime() + 'ERROR: Snakemake execution failed. Check ' + snake_log + ' file for more information. If blank, try allocating more memory.')
        if extract_mito:
            click.echo(gettime() + 'Creating a new .bam file for mitochondria.')
            dict_file = fin + '/' + p.name + '.barcodeTranslate.tsv'
            line1 = 'python ' + script_dir + '/bin/python/17_processMito.py --input ' + p.bamfile
            line2 = ' --output ' + mito + '/' + p.name + '.mito.bam' + ' --mitochr ' + p.mitochr
            line3 = ' --bead-barcode ' + p.bead_tag + ' --drop-barcode ' + p.drop_tag + ' --dict-file ' + dict_file
            mito_cmd = line1 + line2 + line3
            os.system(mito_cmd)
        if keep_temp_files:
            click.echo(gettime() + 'Temporary files not deleted since --keep-temp-files was specified.')
        else:
            byefolder = of
            shutil.rmtree(byefolder + '/.internal')
            shutil.rmtree(byefolder + '/temp')
            os.remove(fin + '/' + p.name + '.basicQC.tsv')
            os.remove(knee + '/' + p.name + '.kneesPlotted.txt')
            if not extract_mito:
                shutil.rmtree(byefolder + '/mito')
            click.echo(gettime() + 'Intermediate files successfully removed.')
    if mode == 'check':
        click.echo(gettime() + 'Dependencies and user-reported file paths OK')
    click.echo(gettime() + 'Complete.')