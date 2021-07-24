# Author: Lalitha Viswanathan
# Utility to parse Insert size QC results from Picard
# Parses results from insert_size_metrics.txt
# Outputs read percentages along different orientations FF, FR, RF, RR
# Mean Insert Size
# Median Insert SSize
# Read pairs
# Pair Orientation
# Bin widths centered around median that encompass 10-99% of all read pairs
#########################################################################
import picardparserutilities as ppu
from typing import Dict, Any, Union, Optional

def insertsizemetrics(filename) -> \
        tuple[dict[str, object], dict[Union[str, str], Union[dict, str]]]:
    """

    :rtype: tuple[dict[str, Union[
            dict[str, Union[list, dict, tuple[Any, Optional[Any]]]], dict[str, Union[list, list[str]]]]], dict[
                  str, dict]]
    :param filename:
    :return:
    """
    results = {'picard_insert_size_metrics': ppu.genericparser(filename)}
    insert_size_metrics: dict[Union[str, str], Union[dict[str, str], str]] = dict(picard_insert_size_metrics={})
    tmp_hash: dict = {}
    for counter, key in enumerate(results["picard_insert_size_metrics"]['header']):
        if counter in (0, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17) and \
                results["picard_insert_size_metrics"]["rows"][3][counter]:
            tmp_hash[key] = results["picard_insert_size_metrics"]["rows"][3][counter]

    if not tmp_hash:
        raise Exception("Insert size metrics not generated successfully")

    insert_size_metrics["picard_insert_size_metrics"] = tmp_hash
    return results, insert_size_metrics
#########################################################################

