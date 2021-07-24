#########################################################################
import json
from typing import re

import numpy as np
from numpy import ndarray


def is_json(picardjsonoutput: json) -> bool:
    """

    :type picardjsonoutput: object
    """
    try:
        json_object = json.loads(picardjsonoutput)
    except ValueError as e:
        print('invalid json: %s' % e)
        return False
    return True


def genericparser(filename: str) -> dict:
    """

    :rtype: object
    """
    resultsdata = {
        'rows': []
    }
    genericdict = {
        'header': [],
        'rows': {},
        'intervals1': {},
        'intervals2': {},
        'intervals3': {},
    }
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line: break

            if line.startswith('## METRICS'):
                # Skip line
                # Save next line as header
                line = f.readline()
                resultsdata['header'] = line.rstrip().split()

            if line.startswith('picard.analysis'):
                line = f.readline()
                resultsdata['header'] = line.rstrip().split()

            headerpattern = re.compile('^\D+.*$')
            valuespattern = re.compile('^\d+.+\d+$')

            # Get rows
            line = f.readline().rstrip()
            if headerpattern.match(line):
                genericdict['header'].append(line.rstrip().split())
            while line:
                resultsdata['rows'].append(line.rstrip().split())
                # For insert size metrics and quality score distribution
                if valuespattern.match(line):
                    vals = line.strip().split('\t')
                    if '>>' not in vals[0]:
                        genericdict['rows'][int(vals[0])] = float(vals[1])
                        # print "Genericdict rows " ,genericdict['rows']
                try:
                    line = f.readline().rstrip()
                    if headerpattern.match(line):
                        genericdict['header'].append(line.rstrip().split())
                except StopIteration:
                    break

    if genericdict and 'CollectAlignmentSummaryMetrics' not in genericdict['header'][0][1] and \
            'CollectGcBiasMetrics' not in genericdict['header'][0][1] and \
            'CollectInsertSizeMetrics' not in genericdict['header'][0][1]:
        # For Mean Quality by Cycle and Quality Score Distribution
        sum: ndarray = np.sum(genericdict['rows'].values())
        # rewrite the values as percentages
        counter = 0
        for key in genericdict['rows'].keys():
            genericdict['rows'][key] = (genericdict['rows'][key] / sum) * 100
        # 3 intervals
        for list in np.array_split(genericdict['rows'].keys(), 3):
            counter += 1
            subdict: dict = {y: genericdict['rows'][y] for y in list if y in genericdict['rows']}
            for key in subdict.keys():
                genericdict['intervals' + str(counter)][key] = subdict[key]
                genericdict['interval' + str(counter) + 'avg'] = np.average(subdict.values())
        if not genericdict:
            raise Exception('Dictionary not created successfully: Picard Parser')
        return genericdict
        # Both original values and intervals are returned

    if 'CollectGcBiasMetrics' in genericdict['header'][0][1]:
        return resultsdata

    if 'CollectAlignmentSummaryMetrics' in genericdict['header'][0][1]:
        return resultsdata

    if 'CollectInsertSizeMetrics' in genericdict['header'][0][1]:
        return resultsdata

