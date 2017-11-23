# (C) 2012, Michael DeHaan, <michael.dehaan@gmail.com>

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import time
import json

from ansible.utils.unicode import to_bytes
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    logs playbook status, per play, in $PWD/status
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'sync_result'
    #CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT="%b %d %Y %H:%M:%S"
    MSG_FORMAT="%(now)s - %(category) - %(data)s\n"
    LOG_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../")

    def __init__(self):

        super(CallbackModule, self).__init__()

        if not os.path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

    def log(self, category, data):
        path = os.path.join(self.LOG_PATH, "status")
        now = time.strftime(self.TIME_FORMAT, time.localtime())

        msg = json.dumps({'time': now, 'category': category, 'stutus': data}, separators=(',',':'))
        with open(path, "ab") as fd:
            fd.write(msg)
            fd.write("\n")

    def v2_playbook_on_setup(self):
        self.log("playbook", "starting...")

    def v2_playbook_on_play_start(self, play):
        self.log(play.name, "starting {0} ...".format(play.name))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.log(task.name, "starting {0} ...".format(task.name))
