# SPDX-FileCopyrightText: 2022 Gregory Clunies <greg@reflekt-ci.com>
#
# SPDX-License-Identifier: Apache-2.0

import re


def segment_2_snake(in_str: str) -> str:
    """Converts a planCase/PlanCase/PLanCase string to snake_case. Inserts
    underscore only where casing switches from lower to UPPER, lower() entire
    string, replace period with with underscore, replace space with underscore.

    Examples:
        planCase --> plan_case
        PlanCase --> plan_case
        PLanCase --> plan_case

    This function is useful when dealing with column names from Segment
    tracking plans.
    """
    temp = re.sub("([a-z])([A-Z]+)", r"\1_\2", in_str)
    temp2 = temp.lower()
    warehouse_case = (
        temp2.replace(".", "_").replace(" ", "_").replace("_-_", "_").replace("/", "_")
    )
    return warehouse_case
