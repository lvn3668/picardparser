# Author: Lalitha Viswanathan
# Utility to parse GC Bias Metrics results from Picard
# Parses summary GC Bias metrics (number of nr reads, window size,
# aligned reads used to compute gc bias,
# calculating at dropout / gc dropout (for gc = 0-50, find
# bins where %ref - %reads is positive and summing;
# repeat for gc vals = 50..100)
# normalized coverage over gc content quintile ranging over 0-100
# in bins of 20
#########################################################################
import picardparserutilities as ppu
from typing import Any, Union

def gcbiasmetrics(filename) -> tuple[
    dict[str, Union[dict[str, Union[Union[list, dict], Any]], dict[str, Union[list, list[str]]]]], dict]:
    """

    :rtype: object
    :param filename:
    :return: dict
    """
    results = {'picard_gc_bias_metrics': ppu.genericparser(filename)}
    gc_bias_metrics: dict = {}
    # The indices from which we wish to extract data
    # [picard_gc_bias_metrics][3] is the dataset from which we wish to extract rows 3 and 4 as results
    indices: list[int] = [3, 4]
    for index in indices:
        if results["picard_gc_bias_metrics"]["rows"][3][index]:
            gc_bias_metrics[results['picard_gc_bias_metrics']['header'][index]] = \
                results['picard_gc_bias_metrics']['rows'][3][index]

    if not gc_bias_metrics:
        raise Exception('GCBiasMetrics not generated successfully')
    return results, gc_bias_metrics
#########################################################################
