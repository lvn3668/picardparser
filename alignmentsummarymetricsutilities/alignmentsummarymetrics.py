# Author: Lalitha Viswanathan
# Utility to parse alignment summary results from Picard
########################################################################
import string
import picardparserutilities as ppu
from typing import Dict, Any, Union, Optional
# extracts percentage pass filter reads, aligned reads (including that dont pass Illumina's filters),
# aligned reads that pass Illumina's filters
# percentage of bases mismatching with reference for all bases aligned to reference
# strand imbalance
def alignmentsummarymetrics(filename: string) -> tuple[
    dict[str, Union[
        dict[str, Union[list, dict, tuple[str, Optional[str]]]], dict[str, Union[list[str], list[str]]]]], dict]:
    results = {'picard_alignment_summary_metrics': ppu.genericparser(filename)}
    modified_alignment_summary_metrics: tuple[dict[str, Union[dict[str, Union[list, dict,
                                                                              tuple[str, Optional[str]]]],
                                                              dict[str, Union[
                                                                  list[str], list[str]]]]], dict] = {}
    # These are the indices corresponding to which we wish to extract data
    indicesfrompicardalignmentsummarymetricsfiles: list[int] = [3, 6, 10, 13, 14, 15, 17, 19]
    for index in indicesfrompicardalignmentsummarymetricsfiles:
        if results['picard_alignment_summary_metrics']['rows'][5][index]:
            modified_alignment_summary_metrics[results['picard_alignment_summary_metrics']['rows'][5][0] + "_" +
                                               results['picard_alignment_summary_metrics']['header'][index]] = \
                results['picard_alignment_summary_metrics']['rows'][5][index]

    if not modified_alignment_summary_metrics:
        raise Exception('Alignment Summary Metrics not generated successfully')
    return results, modified_alignment_summary_metrics
#########################################################################