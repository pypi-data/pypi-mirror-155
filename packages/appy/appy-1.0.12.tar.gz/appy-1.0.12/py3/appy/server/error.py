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
from http import HTTPStatus

from appy.px import Px
from appy.ui.js import Quote
from appy.utils import Traceback
from appy.ui.template import Template
from appy.utils import MessageException

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Error:
    '''Represents a server error'''

    byCode = {
     # Error 404: page not found
     404: {'label': 'not_found', 'px':
       Px('''<div>::msg</div>
             <div if="not isAnon and not popup">
              <a href=":tool.computeHomePage()">:_('app_home')</a>
             </div>''', template=Template.px, hook='content')},

     # Error 403: unauthorized
     403: {'label': 'unauthorized', 'px':
       Px('''<div><img src=":svg('password')" class="iconERR"/>
                  <x>::msg</x></div>''', template=Template.px, hook='content')},

     # Error 500: server error
     500: {'label': 'server_error', 'px':
       Px('''<div><img src=":svg('warning')" class="iconERR"/>
                  <x>::msg</x></div>''', template=Template.px, hook='content')},

     # Error 503: service unavailable. This error code is used by Appy when, due
     # to too many conflict errors (heavy load), the server cannot serve the
     # request.
     503: {'label': 'conflict_error',
           'px': Px('''<div>::msg</div>''',
                    template=Template.px, hook='content')},

     # Return code 200: a logical error rendering a nice translated message to
     # the user, but not considered being an error at the HTTP level.
     200: {'px': Px('''<img src=":svg('warning')" class="iconERR"/>
                       <x>::msg</x>''', template=Template.px, hook='content')}
    }

    @classmethod
    def getContent(class_, traversal, code, error):
        '''Get the textual content to render in the error page'''
        # Dump a traceback for a Manager
        if traversal.user.hasRole('Manager') and code != 200:
            r = Traceback.get(html=True)
        else:
            if isinstance(error, MessageException):
                r = str(error)
            else:
                _ = traversal.handler.tool.translate
                r = _(Error.byCode[code]['label'])
                if error:
                    text = str(error).strip()
                    if text:
                        r += '<div class="discreet">%s</div>' % text
        return r

    @classmethod
    def get(class_, resp, traversal, error=None):
        '''A server error just occurred. Try to return a nice error page. If it
           fails (ie, the error is produced in the main PX template), dump a
           simple traceback.'''
        # When managing an error, ensure no database commit will occur
        handler = traversal.handler
        handler.commit = False
        # Log the error
        code = resp.code if resp.code in Error.byCode else 500
        # Message exceptions are special errors being 200 at the HTTP level
        is200 = code == 200
        message = '%d on %s' % (code, handler.path)
        if error and error.args:
            message = '%s - %s' % (message, str(error))
        handler.log('app', 'warning' if is200 else 'error', message=message)
        if code in (500, 503):
            handler.log('app', 'error', Traceback.get().strip())
        # Compute the textual content that will be shown
        content = Error.getContent(traversal, code, error)
        # If we are called by an Ajax request, return only the error message,
        # and set the return code to 200; else, browsers will complain.
        context = traversal.context
        if context and context.ajax:
            resp.code = HTTPStatus.OK
            return '<p>%s</p>' % content
        # Return the PX corresponding to the error code. For rendering it, get
        # the last PX context, or create a fresh one if there is no context.
        if not context:
            # Remove some variables from the request to minimise the possibility
            # that an additional error occurs while creating the PX context.
            req = handler.req
            if 'search' in req: del(req.search)
            traversal.context = context = traversal.createContext()
        else:
            # Reinitialise PX counts. Indeed, we have interrupted a "normal"
            # page rendering that has probably already executed a series of PXs.
            # Without reinitialising counts, Appy will believe these PXs were
            # already executed and will not include CSS and JS code related to
            # these PXs.
            context['_rt_'] = {}
        context.msg = content
        try:
            return Error.byCode[code]['px'](context)
        except Exception as err:
            return '<p>%s</p>' % content
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
