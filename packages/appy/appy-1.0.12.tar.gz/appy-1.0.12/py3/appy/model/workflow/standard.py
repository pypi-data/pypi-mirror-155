'''Standard workflows'''

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
from appy.model.workflow import *
from appy.model.workflow.state import State
from appy.model.workflow.transition import Transition

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# WARNING | To be activated, any workflow defined here must be listed in
#         | appy.model.Model.baseWorkflows.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Anonymous:
    '''One-state workflow allowing anyone to consult and Manager + Owner(s) to
       edit.'''

    ma = 'Manager'
    o = 'Owner'
    everyone = (ma, 'Anonymous', 'Authenticated')
    active = State({r:everyone, w:(ma, o), d:(ma, o)}, initial=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Authenticated:
    '''One-state workflow allowing authenticated users to consult and Manager
       to edit.'''

    ma = 'Manager'
    o = 'Owner'
    authenticated = (ma, 'Authenticated')
    active = State({r:authenticated, w:(ma, o), d:(ma, o)}, initial=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Owner:
    '''Workflow allowing only manager and owner to consult and edit'''

    # ~~ Errors ~~~
    ADMIN_DEACTIVATE_ERROR = 'Cannot deactivate admin.'

    # ~~~ Roles in use ~~~
    ma = 'Manager'
    o = 'Owner'

    # ~~~ States ~~~
    active = State({r:(ma, o), w:(ma, o), d:ma}, initial=True)
    inactive = State({r:(ma, o), w:ma, d:ma})

    # ~~~ Transitions ~~~
    def doDeactivate(self, o):
        '''Prevent user "admin" from being deactivated'''
        if (o.class_.name == 'User') and (o.login == 'admin'):
            raise WorkflowException(Owner.ADMIN_DEACTIVATE_ERROR)

    deactivate = Transition( (active, inactive), condition=ma,
                             action=doDeactivate, confirm=True)

    reactivate = Transition( (inactive, active), condition=ma, confirm=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TooPermissive:
    '''If objects of class B must follow the security of their container object,
       of class A, define, on class B, this too permissive workflow. Actual
       security needs to be implemented, on class B, by object methods mayView,
       mayEdit and mayDelete that return what is allowed according to the
       container workflow (A).'''

    # As an example, consult standard class appy/model/document.py that uses
    # this worflow.
    everyone = ('Anonymous', 'Authenticated')
    created = State({r:everyone, w:everyone, d:everyone}, initial=True)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
