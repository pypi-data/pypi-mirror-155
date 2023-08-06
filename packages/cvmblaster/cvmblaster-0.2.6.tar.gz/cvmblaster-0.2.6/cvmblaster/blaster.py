import os
import sys
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML

# from Bio.Blast import NCBIWWW
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline


class Blaster():
    def __init__(self, inputfile, database, output, threads, minid=90, mincov=60):
        self.inputfile = os.path.abspath(inputfile)
        self.database = database
        self.minid = int(minid)
        self.mincov = int(mincov)
        self.temp_output = os.path.join(os.path.abspath(output), 'temp.xml')
        self.threads = threads

    def biopython_blast(self):
        hsp_results = {}
        cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no',
                                      evalue=1E-20, out=self.temp_output, outfmt=5,
                                      perc_identity=self.minid, max_target_seqs=50000,
                                      num_threads=self.threads)
        # print(cline)
        # print(self.temp_output)

        stdout, stderr = cline()

        result_handler = open(self.temp_output)

        blast_records = NCBIXML.parse(result_handler)
        df_final = pd.DataFrame()

        for blast_record in blast_records:

            # if blast_record.alignments:
            #     print("QUERY: %s" % blast_record.query)
            # else:
            #     for alignment in blast_record.alignments:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    strand = 0
                    query_name = blast_record.query
                    # print(query_name)
                    target_gene = alignment.title.split(' ')[1]

                    # Get gene name and accession number from target_gene
                    gene = target_gene.split('_')[0]
                    accession = target_gene.split('_')[2]

                    # print(target_gene)
                    sbjct_length = alignment.length  # The length of matched gene
                    # print(sbjct_length)
                    sbjct_start = hsp.sbjct_start
                    sbjct_end = hsp.sbjct_end
                    gaps = hsp.gaps  # gaps of alignment
                    query_string = str(hsp.query)  # Get the query string
                    identities_length = hsp.identities  # Number of indentity bases
                    # contig_name = query.replace(">", "")
                    query_start = hsp.query_start
                    query_end = hsp.query_end
                    # length of query sequence
                    query_length = len(query_string)

                    # calculate identities
                    perc_ident = (int(identities_length)
                                  / float(query_length) * 100)
                    IDENTITY = "%.2f" % perc_ident
                    # print("Identities: %s " % perc_ident)

                    # coverage = ((int(query_length) - int(gaps))
                    #             / float(sbjct_length))
                    # print(coverage)

                    perc_coverage = (((int(query_length) - int(gaps))
                                      / float(sbjct_length)) * 100)
                    COVERAGE = "%.2f" % perc_coverage
                    # print("Coverage: %s " % perc_coverage)

                    # cal_score is later used to select the best hit
                    cal_score = perc_ident * perc_coverage

                    # Calculate if the hit is on minus strand
                    if sbjct_start > sbjct_end:
                        temp = sbjct_start
                        sbjct_start = sbjct_end
                        sbjct_end = temp
                        strand = 1
                        query_string = str(
                            Seq(str(query_string)).reverse_complement())

                    if strand == 0:
                        strand_direction = '+'
                    else:
                        strand_direction = '-'

                    if perc_coverage >= self.mincov:
                        hit_id = "%s:%s_%s:%s" % (
                            query_name, query_start, query_end, target_gene)
                        # hit_id = query_name
                        # print(hit_id)
                        best_result = {
                            'FILE': os.path.basename(self.inputfile),
                            'SEQUENCE': query_name,
                            'GENE': gene,
                            'START': query_start,
                            'END': query_end,
                            'SBJSTART': sbjct_start,
                            'SBJEND': sbjct_end,
                            'STRAND': strand_direction,
                            # 'COVERAGE':
                            'GAPS': gaps,
                            "%COVERAGE": COVERAGE,
                            "%IDENTITY": IDENTITY,
                            # 'DATABASE':
                            'ACCESSION': accession,
                            'QUERY_SEQ': query_string,
                            'cal_score': cal_score,
                            'remove': 0
                            # 'PRODUCT': target_gene,
                            # 'RESISTANCE': target_gene
                        }
                    if best_result:
                        save = 1

                        if hsp_results:
                            tmp_results = hsp_results
                            save, hsp_results = Blaster.filter_results(
                                save, best_result, tmp_results)

                    if save == 1:
                        hsp_results[hit_id] = best_result
        # close file handler, then remove temp file
        result_handler.close()
        os.remove(self.temp_output)
        # print(self.inputfile)
        df = Blaster.resultdict2df(hsp_results)
        return df, hsp_results

    @staticmethod
    def filter_results(save, best_result, tmp_results):
        """
        remove the best hsp with coverage lt mincov
        参考bn的耐药基因过滤
        """

        new_query_name = best_result['SEQUENCE']
        new_query_start = best_result['START']
        new_query_end = best_result['END']
        new_sbjct_start = best_result['SBJSTART']
        new_sbjct_end = best_result['SBJEND']
        coverage = best_result['%COVERAGE']
        new_cal_score = best_result['cal_score']
        keys = list(tmp_results.keys())

        for hit in keys:
            remove_old = 0
            hit_data = tmp_results[hit]
            old_query_name = hit_data['SEQUENCE']
            if new_query_name == old_query_name:
                old_query_start = hit_data['START']
                old_query_end = hit_data['END']
                old_sbjct_start = hit_data['SBJSTART']
                old_sbjct_end = hit_data['SBJEND']
                old_cal_score = hit_data['cal_score']
                hit_union_length = (max(old_query_end, new_query_end)
                                    - min(old_query_start, new_query_start))
                hit_lengths_sum = ((old_query_end - old_query_start)
                                   + (new_query_end - new_query_start))
                overlap_len = (hit_lengths_sum - hit_union_length)

                if overlap_len <= 0:  # two genes without overlap, save all of them
                    continue

                if (old_query_start == new_query_start) and (old_query_end == new_query_end):
                    if new_cal_score > old_cal_score:
                        remove_old = 1
                    else:
                        save = 0
                elif (old_query_start != new_query_start) or (old_query_end != new_query_end):
                    if new_cal_score > old_cal_score:
                        remove_old = 1
                    else:
                        save = 0
                else:
                    pass
            if remove_old == 1:
                del tmp_results[hit]
        return save, tmp_results

    @staticmethod
    def resultdict2df(result_dict):
        df_final = pd.DataFrame()
        col_dict = {'FILE': '',
                    'SEQUENCE': '',
                    'GENE': '',
                    'START': '',
                    'END': '',
                    'SBJSTART': '',
                    'SBJEND': '',
                    'STRAND': '',
                    'GAPS': '',
                    "%COVERAGE": '',
                    "%IDENTITY": '',
                    'ACCESSION': '',
                    'QUERY_SEQ': '',
                    'cal_score': '',
                    'remove': ''}
        if len(result_dict.keys()) == 0:
            df_final = pd.DataFrame.from_dict(col_dict, orient='index')
        else:
            for key in result_dict.keys():
                hit_data = result_dict[key]
                df_tmp = pd.DataFrame.from_dict(hit_data, orient='index')
                df_final = pd.concat([df_final, df_tmp], axis=1)
        df_result = df_final.T
        df_result = df_result.drop(
            labels=['QUERY_SEQ', 'cal_score', 'remove'], axis=1)
        return df_result

    @staticmethod
    def makeblastdb(file, name):
        cline = NcbimakeblastdbCommandline(
            dbtype="nucl", out=name, input_file=file)
        print("Making reference database...")
        stdout, stderr = cline()
        print('Finish')

    @staticmethod
    def get_nucl_seq(result_dict, out_path):
        arg_records = []
        if len(result_dict.keys()) == 0:
            print('No ARGs were found...')
        else:
            for key in result_dict.keys():
                hit_data = result_dict[key]
                file = os.path.splitext(str(hit_data['FILE']))[0]
                outfile = os.path.join(
                    out_path, file + str('_ARGs_nucl.fasta'))
                id = str(hit_data['SEQUENCE'] +
                         '_' + hit_data['GENE']) + str('_' + hit_data['ACCESSION'])
                name = str(hit_data['ACCESSION'])
                record = SeqRecord(Seq(hit_data['QUERY_SEQ']),
                                   id=id,
                                   name=name,
                                   description='')
            arg_records.append(record)
            SeqIO.write(arg_records, outfile, 'fasta')

    @staticmethod
    def get_prot_seq(result_dict, out_path):
        arg_records = []
        if len(result_dict.keys()) == 0:
            print('No ARGs were found...')
        else:
            for key in result_dict.keys():
                hit_data = result_dict[key]
                file = os.path.splitext(str(hit_data['FILE']))[0]
                outfile = os.path.join(
                    out_path, file + str('_ARGs_prot.fasta'))
                trim = Seq(hit_data['QUERY_SEQ']) % 3
                prot_seq = Seq(hit_data['QUERY_SEQ'][:-trim])
                id = str(hit_data['SEQUENCE'] +
                         '_' + hit_data['GENE']) + str('_' + hit_data['ACCESSION'])
                name = str(hit_data['ACCESSION'])
                record = SeqRecord(prot_seq.translate(),
                                   id=id,
                                   name=name,
                                   description='')
            arg_records.append(record)
            SeqIO.write(arg_records, outfile, 'fasta')
