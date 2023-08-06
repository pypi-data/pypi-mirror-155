# -*- python -*-
#
# Copyright (C) 2014-2016 Liang Chen
# Copyright (C) 2016-2022 Xingeng Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# hpc.py -- HPC operation abstraction

import os.path
from dmprj.engineering.remote import SSHAction

from aamrd.slurm import SlurmScheduler
from aamrd.lava import LavaScheduler


__all__ = [ 'Task', 'HPC', 'SlurmScheduler', 'LavaScheduler' ]


class SSH(SSHAction):
    '''
    SSH interface for communication abstraction
    '''

    CHAR_HOST_PATH_PIVOT = ':'

    SPEC_FILE_PATH_WITH_HOST = 'host:/path/to/file'

    @classmethod
    def split_host_filepath(cls, remote_path):
        '''
        split host name and filepath

        :spec: input string format "host:/path/to/file"
        :note: rvalue 'host' field may be host name string or None; 'file.path' field is the file path on the server.

        :param remote_path: (string)

        :return: {'host':host_name_string_or_none, 'file.path':file_path_string} (dict)
        '''
        ret = {
            'host': None,
            'file.path': None,
        }

        token = remote_path.split(cls.CHAR_HOST_PATH_PIVOT, 1)
        if len(token) > 1:
            ret['file.path'] = token[1]
            if len(token[0].strip()) > 0:
                ret['host'] = token[0]
        else:
            ret['file.path'] = remote_path

        return ret

    def download_single_file(self, src, target):
        '''
        SFTP download

        :param src: file path on remote SSH server (string)
        :param target: local directory for storing the transferred file (string)

        :return: (obj or none)
        '''
        ret = {
            'success': False,
            'message': '',
        }

        _remote_f = self.split_host_filepath(src)
        # check if the given file path contains host name;
        if _remote_f['host'] is not None:
            # TODO: handle the host name in _remote_f['host']
            pass
        remote_path = _remote_f['file.path']

        local_dir = target if os.path.isdir(target) else os.path.dirname(target)

        _ret = self.get_backend().get(remote_path, local_dir)
        ret['success'] = _ret.succeeded
        return ret

    def upload_single_file(self, src, target):
        '''
        SFTP upload

        :param src: local file path (string)
        :param target: remote file path (string)

        :return: (obj or none)
        '''
        ret = {
            'success': False,
            'message': '',
        }

        local_path = src

        _remote_f = self.split_host_filepath(target)
        # check if the given file path contains host name;
        if _remote_f['host'] is not None:
            # TODO: handle the host name in _remote_f['host']
            pass
        remote_path = _remote_f['file.path']

        _ret = self.get_backend().put(local_path, remote_path)
        ret['success'] = _ret.succeeded
        return ret

    def execute_command(self, command_line):
        '''
        :param command_line: (string)
        '''
        retcode = self.get_backend().run(command_line)
        return retcode

    def get_backend(self):
        '''
        sub-class should override this method to provide the actual backend
        '''
        return None


class Task(object):
    '''
    abstraction of dispatched tasks
    '''

    CODE_QUEUED = 0
    CODE_STARTED = 1
    CODE_FAILED = 2
    CODE_COMPLETED = 4

    def parse_hpc_code(self, val):
        '''
        :param val: (string)
        '''
        ret = None

        STATUS_MAP = {
            self.CODE_QUEUED: {
                'PENDING', 'PD',
                'PEND',
            },
            self.CODE_STARTED: {
                'RUNNING', 'R',
                'RUN',
            },
            self.CODE_FAILED: {
                'FAILED', 'F',
                'EXIT'
            },
            self.CODE_COMPLETED: {
                'COMPLETED', 'CD',
                'DONE'
            },
        }
        for code in STATUS_MAP.keys():
            if val in STATUS_MAP[ code ]:
                ret = code
                break
        return ret


class HPC(SSH):
    '''
    abstraction of HPC
    '''

    def on_error_action(self, error):
        '''
        sub-class may override this method
        '''
        return None

    def get_task_list(self, val, cls=Task):
        pool = list()
        for item in val:
            pool.append(cls(item))
        return pool
