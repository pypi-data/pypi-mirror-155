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
# slurm.py -- SLURM compatiable scheduler

from dmprj.engineering.hpcluster import SLURM


class SlurmScheduler(SLURM):
    '''
    SLURM
    '''

    def _ssub_run(self, command):
        '''
        process command line for ssub

        :param command: (obj)

        :return: final command (string)
        '''
        d = {
            'job_name': command.job_name,
            'job_dir': command.job_dir,
            'script': command.job_script_fullpath,
            #
            'dependency': '--dependency=afterany:{j}'.format(j=command.depend_on_job_id) if command.depend_on_job else '',
            'queue_name': command.queue_name,
            'concurrency': '-S {n}'.format(n=command.n_thread) if command.n_thread else '',
            'walltime': '-t {wt}'.format(wt=command.wall_time) if command.wall_time else '',
            'checkpoint': '--checkpoint={cp_interval} --checkpoint-dir={cpdir}'.format(cp_interval=self.CHECKPOINT_INTERVAL, cpdir=command.checkpoint_dir) if command.checkpoint_dir else '',
            'priority': '' if command.priority else '',
        }
        return (' '.join(self.get_sbatch_template())).format(**d)

    def slurm_submission_step(self, job_def):
        '''
        `ssub` job submission steps

        :param job_def: (obj)

        :return: HPC job id (string or none)
        '''
        output = None
        try:
            a_out = self.execute_command(
                self._ssub_run(job_def.preexec_command)
            )
            main = job_def.main_command
            main.depend_on_job_id = self.sbatch_output_process(a_out)
            b_out = self.execute_command(
                self._ssub_run(main)
            )
            output = self.sbatch_output_process(b_out)
            post = job_def.postexec_command
            post.depend_on_job_id = output
            self.execute_command(
                self._ssub_run(post)
            )
        except Exception as e:
            self.on_error_action(e)

        return output

    def sjob_command_line(self):
        '''
        :return: (string)
        '''
        FMT = 'squeue -h -a -S "P,i" -t all -o "{col}"'
        COL_NAMES = ('%A', '%u', '%T', '%P', '%t', '%r', '%j')
        d = {
            'col': self.CHAR_SQUEUE_FIELD_SEP.join(COL_NAMES),
        }
        return FMT.format(**d)

    def sjob_output_process(self, value):
        '''
        :param value: `sjob` command output (string)

        :return: (obj)
        '''
        ret = None

        if value:
            # parse the response
            total = value.splitlines()
            ret = [ line.split(self.CHAR_SQUEUE_FIELD_SEP) for line in total if len(line) > 2 ]
        return ret
