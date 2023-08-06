"""
Copyright © 2022 Jeff Kletsky. All Rights Reserved.

License for this software, part of the pyDE1 package, is granted under
GNU General Public License v3.0 only
SPDX-License-Identifier: GPL-3.0-only

Convert the lazy legacy implementation of profiles into the JSON v2 format

Assumptions are

* It is in
    key value
  form, one pair per line.
* None of the keys are "quoted" and do not contain spaces
* The only quoting mechanism used is {}
* There are no backslash escapes
* No translation of newline, whitespace into single space
"""
from typing import Union, Optional

from pyDE1.exceptions import DE1TypeError


def braced_to_python(braced: Union[str, bytes, bytearray]) \
        -> Optional[Union[str, list]]:
    """
    Converts Tcl-style list into Python list, potentially nested
    Also handles a single argument, converting it into a string
    """
    if braced is None:
        return None

    if isinstance(braced, str):
        pass
    elif isinstance(braced, (bytes, bytearray)):
        braced = braced.decode('utf-8')
    else:
        raise DE1TypeError(
            "braced_to_python() expects a string or bytes-like, "
            f"not {type(braced)}")

    

