# Author: Lalitha Viswanathan
# Quality Score Distribution Utilities
import string
import picardparserutilities as ppu
from typing import Dict, Any, Union, Optional

#########################################################################
def qualityscoredistribution(filename) -> Union[
    dict[str, Union[list, dict, tuple[str, Optional[str]]]], dict[str, Union[list, list[str]]]]:
    """
    :rtype: object
    """
    genericdict: Union[
        dict[str, Union[list, dict, tuple[str, Optional[str]
        ]
        ]
        ], dict[str, Union[list, list[str]]]] = ppu.genericparser(
        filename)
    if not genericdict:
        raise Exception("Quality Score Distribution not generated successfully")
    return genericdict
