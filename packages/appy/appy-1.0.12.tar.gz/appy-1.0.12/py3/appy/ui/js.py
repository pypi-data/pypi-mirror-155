'''Module implementing Javascript-related functionality'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2022 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import re

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Quote:
    '''This class escapes strings to be integrated as Javascript string literals
       in Javascript code, and, once escaped, quotes them.'''
    # The "escaping" part of this class is inspired by class appy/xml/Escape
    rex = re.compile("[\n\t\r']")
    blanks = {'\n': '', '\t':'', '\r':''}
    # There are 2 ways to escape a single quote
    values = {True: {"'": '&apos;'}, False: {"'": "\\'"}}
    for d in values.values(): d.update(blanks)

    @staticmethod
    def js(s, withEntity=True):
        '''Escapes blanks and single quotes in string p_s. Single quotes are
           escaped with a HTML entity if p_withEntity is True or with a quote
           prefixed with a "backslash" char else. Returns p_s, escaped and
           quoted.'''
        s = s if isinstance(s, str) else str(s)
        fun = lambda match: Quote.values[withEntity][match.group(0)]
        return "'%s'" % Quote.rex.sub(fun, s)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
