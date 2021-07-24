#!/usr/bin/env python3
# Author: Lalitha Viswanathan
# Picard Metrics parser

import re, os, json
import string
from argparse import ArgumentParser
import picardparserutilities as ppu
from pprint import pprint
import alignmentsummarymetricsutilities as alignsummetricsutils
import GCBiasMetricsParserutilities as gcbiasmetricsutils
import insertsizemetricsutilities as insertszmetrics
import qualityscoredistutilities as qsd
#########################################################################
# global variable for all picard results


#########################################################################
def picard_parser_wrapper(alignment_summarymetrics_file: string, insertsize_metrics_file: string,
                          gcbiasmetrics_file: string, meanqualitybycycle_file: string,
                          qualityscoredistribution_file: string, picardparserresults : dict) -> str:
    """

    :param insertsize_metrics_file:
    :param meanqualitybycycle_file:
    :param gcbiasmetrics_file:
    :param qualityscoredistribution_file:
    :type alignment_summarymetrics_file: object
    """
    # noinspection PyBroadException
    try:
        picard_parser_file(alignment_summarymetrics_file, 'alignmentsummarymetricsfunction')
        picard_parser_file(gcbiasmetrics_file, 'gcbiasmetricsfunction')
        picard_parser_file(meanqualitybycycle_file, 'meanqualitybycyclefunction')
        picard_parser_file(insertsize_metrics_file, 'insertsizemetrics')
        picard_parser_file(qualityscoredistribution_file, 'qualitydistributionfunction')
    except Exception:
        print
        "Picard Parser failed"

    if ppu.is_json(json.dumps(picardparserresults)):
        return json.dumps(picardparserresults)
    else:
        raise Exception("Picard Parser has generated invalid JSON")


#########################################################################
def picard_parser_file(picardoutputfilename: string, parsertype: string):
    """

    :param parsertype:
    :type picardoutputfilename: object
    :rtype: object
    """
    parsefxn: None = None
    picardparserresults = {}
    if parsertype == 'alignmentsummarymetricsfunction':
        parsefxn = alignsummetricsutils.alignmentsummarymetrics
    if parsertype == 'gcbiasmetricsfunction':
        parsefxn = gcbiasmetricsutils.gcbiasmetrics
    if parsertype == 'insertsizemetrics':
        parsefxn = insertszmetrics.insertsizemetrics
    if parsertype == 'meanqualitybycyclefunction':
        parsefxn = ppu.genericparser
    if parsertype == 'qualitydistributionfunction':
        parsefxn = qsd.qualityscoredistribution

    if "gcbiasmetrics" in parsefxn.__name__:
        tmpgcbiasmetrics: dict
        (results, tmpgcbiasmetrics) = parsefxn(picardoutputfilename)
        picardparserresults['picard_gcbiasmetrics'] = tmpgcbiasmetrics

    if "alignmentsummarymetrics" in parsefxn.__name__:
        tmpalnsummarymetrics: dict
        (results, tmpalnsummarymetrics) = parsefxn(picardoutputfilename)
        picardparserresults['picard_alignmentsummarymetrics'] = tmpalnsummarymetrics

    if "insertsizemetrics" in parsefxn.__name__:
        insertsizemetricsresults: dict
        (results, insertsizemetricsresults) = parsefxn(picardoutputfilename)
        picardparserresults['picard_insertsizemetrics'] = insertsizemetricsresults

    if "qualityscoredistribution" in parsefxn.__name__:
        qualityscoredistributionresults: dict
        qualityscoredistributionresults = qsd.qualityscoredistribution(picardoutputfilename)
        del qualityscoredistributionresults['rows']
        del qualityscoredistributionresults['header'][0]
        del qualityscoredistributionresults['header'][1]
        picardparserresults['picard_qualityscoredistribution'] = qualityscoredistributionresults

    if "genericparser" in parsefxn.__name__:
        tmpreturnvalue: dict
        tmpreturnvalue = ppu.genericparser(picardoutputfilename)
        # delete the rows; retain only the intervals
        # delete the first 2 lines of the header
        del tmpreturnvalue['rows']
        del tmpreturnvalue['header'][0]
        del tmpreturnvalue['header'][1]
        picardparserresults['picard_meanqualitybycycle'] = tmpreturnvalue


#########################################################################
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('picardoutputfilename')
    parser.add_argument('sampleid')
    parser.add_argument('runid')
    parser.add_argument('parsertype')
    args = parser.parse_args()
    parsefxn: None = None

    if args.parsertype == 'alignmentsummarymetrics':
        parsefxn =  alignsummetricsutils.alignmentsummarymetrics
    if args.parsertype == 'gcbiasmetrics':
        parsefxn = gcbiasmetricsutils.gcbiasmetrics
    if args.parsertype == 'insertsizemetrics':
        parsefxn = insertszmetrics.insertsizemetrics
    if args.parsertype == 'meanqualitybycycle':
        parsefxn = ppu.genericparser
    if args.parsertype == 'qualityscoredistribution':
        parsefxn = qsd.qualityscoredistribution
