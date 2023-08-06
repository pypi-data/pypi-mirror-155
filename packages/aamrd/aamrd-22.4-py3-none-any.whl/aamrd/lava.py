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
# lava.py -- openlava/LSF compatible scheduler

from dmprj.engineering.hpcluster import Scheduler


class LavaScheduler(Scheduler):
    '''
    openlava
    '''

    CHAR_BJOB_DELIM = ','

    def _get_bsub_template(self):
        FMT = [
            'bsub',
            '{dependency}',
            '-q {queue_name}',
            '-J {job_name}',
            '-cwd {job_dir}',
            '{walltime} {concurrency} {checkpoint}',
            '-e {job_dir}/log.err',
            '-o {job_dir}/log.out',
            '{script}',
        ]
        return FMT

    def _bsub_run(self, command):
        '''
        process command line for bsub

        :param command: (obj)

        :return: final command (string)
        '''
        d = {
            'job_name': command.job_name,
            'job_dir': command.job_dir,
            'script': command.job_script_fullpath,
            #
            'dependency': '-w "done({j})"'.format(j=command.depend_on_job) if command.depend_on_job else '',
            'queue_name': command.queue_name,
            'concurrency': '-n {n}'.format(n=command.n_thread) if command.n_thread else '',
            'walltime': '-W {wt}'.format(wt=command.wall_time) if command.wall_time else '',
            'checkpoint': '-k {cpdir}'.format(cpdir=command.checkpoint_dir) if command.checkpoint_dir else '',
            'priority': '-R "order[!slots] span[hosts=1]" -sp {p}'.format(p=command.priority) if command.priority else '',
        }
        return (' '.join(self._get_bsub_template())).format(**d)

    def bsub_submission_step(self, job_def):
        '''
        `bsub` job submission steps

        :param job_def: (obj)

        :return: HPC job id (string or none)
        '''
        output = None
        try:
            self.execute_command(
                self._bsub_run(job_def.preexec_command)
            )
            output = self.execute_command(
                self._bsub_run(job_def.main_command)
            )
            self.execute_command(
                self.checkpoint_registration_command(job_def)
            )
            self.execute_command(
                self._bsub_run(job_def.postexec_command)
            )
        except Exception as e:
            self.on_error_action(e)

        return self.bsub_output_process(output)

    def checkpoint_registration_command(self, job_def):
        '''
        :param job_def: (obj)

        :return: (string)
        '''
        reg_cmd = 'bchkpnt -p {cp_interval} -J {job_name}'.format(
            cp_interval=10,
            job_name=job_def.main_command.job_name
        )
        return reg_cmd

    def bsub_output_process(self, value):
        '''
        extract HPC job id from `bsub` return value

        :param value: `bsub` command output (string)

        :return: HPC job id (string or none)
        '''
        ret = None
        if value is not None:
            ret = value.split('<')[1].split('>')[0]
        return ret

    def bjob_command_line(self):
        '''
        :return: (string)
        '''
        FMT = 'bjobs -o {double_quote}{col} delimiter={single_quote}{delim}{single_quote}{double_quote}'
        COL_NAMES = ('id', 'user', 'stat', 'queue', 'exit_code', 'exit_reason', 'name',)
        d = {
            'single_quote': "'",
            'double_quote': '"',
            #
            'delim': self.CHAR_BJOB_DELIM,
            'col': ' '.join(COL_NAMES)
        }
        return FMT.format(**d)

    def bjob_output_process(self, value):
        '''
        :param value: `bjob` command output (string)

        :return: (obj)
        '''
        ret = None

        if not value.startswith('No unfinished job found'):
            # parse the response
            total = value.splitlines()
            ret = [ line.split(self.CHAR_BJOB_DELIM) for line in total[1:] if len(line) > 2 ]
        return ret
