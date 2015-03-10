{%- raw -%}

#  The ScanCode software is licensed under the Apache License version 2.0.
#  Copyright (c) 2015 nexB Inc. and others. All rights reserved.
#  See http://www.nexb.com/ and http://scancode.io for details.
#  You may not use this software except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# 
# The ScanCode software also embeds several third-party free and open
# source software packages under various licenses. See the thirdparty
# directory for details.
# 
# When publishing or redistributing data generated or collected with
# ScanCode or a ScanCode derivative you must accompany the data with this
# prominent credit notice:
# 
#  Generated with ScanCode WITHOUT WARRANTIES OF ANY KIND.
#  ScanCode is free software by nexB Inc. and others.
#  Visit http://scancode.io for details.

import sys
# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m


def main(argv=()):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    print(argv)
    return 0

if __name__ == "__main__":
    sys.exit(main())
{%- endraw %}
