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
from appy.model.fields import Field
from appy.ui.layout import Layout, Layouts

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Info(Field):
    '''An info is a field whose purpose is to present information
       (text, html...) to the user.'''

    class Layouts(Layouts):
        '''Info-specific layouts'''
        b = Layouts(edit='l')
        d = Layouts(edit=Layout('l-d', width=None))
        c = Layouts(edit='l|')
        dc = Layouts(edit='l|-d|')
        do = Layouts(edit='f', view='d') # Description only
        vdc = Layouts(edit='l', view='l|-d|')

        @classmethod
        def getDefault(class_, field):
            '''Default layouts for this Info p_field'''
            return class_.b

    # An info only displays a label: PXs for showing content are empty
    view = edit = cell = buttons = search = ''

    def __init__(self, validator=None, multiplicity=(1,1), show='view',
      renderable=None, page='main', group=None, layouts=None, move=0,
      readPermission='read', writePermission='write', width=None, height=None,
      maxChars=None, colspan=1, master=None, masterValue=None, focus=False,
      historized=False, mapping=None, generateLabel=None, label=None, view=None,
      cell=None, buttons=None, edit=None, xml=None, translations=None):
        # Call the base constructor
        Field.__init__(self, None, (0,1), None, None, show, renderable, page,
          group, layouts, move, False, True, None, None, False, None,
          readPermission, writePermission, width, height, None, colspan, master,
          masterValue, focus, historized, mapping, generateLabel, label, None,
          None, None, None, False, False, view, cell, buttons, edit, xml,
          translations)
        self.validable = False
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
