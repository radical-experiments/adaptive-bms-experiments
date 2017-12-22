__author__ = "Vivek Balasubramanian <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2016, http://radical.rutgers.edu"
__license__ = "MIT"

from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager

import argparse
import os
import re
import pprint
import glob


# USER PARS
ENSEMBLE_SIZE = int(os.environ.get('ENSEMBLE_SIZE', None))
NS = int(os.environ.get('NS', None))
TOTAL_ITERS = int(os.environ.get('TOTAL_ITERS', None))


def get_pipeline():

    p = Pipeline()
    it_task_uids = []
    for it in range(TOTAL_ITERS):

        s1 = Stage()
        s1_task_uids = []
        for e in range(ENSEMBLE_SIZE):
            t = Task()
            t.pre_exec = [  'export PATH=/home/vivek91/miniconda2/bin:$PATH',
                            'source activate openmm_env',
                            'export OPENMM_CPU_THREADS=20']
            t.executable = ['python']
            t.cores = 20
            t.arguments = ['simulate.py', '--ns', NS]
            if it == 0:
                t.link_input_data = ['$SHARED/ala2.pdb', '$SHARED/simulate.py']
            else:
                t.link_input_data = [   '$SHARED/simulate.py',
                                        '%s/ala2-%s.pdb > ala2.pdb' %(it_task_uids[it-1]['msm'], e)
                                    ]

            s1.add_tasks(t)
            s1_task_uids.append('$Pipeline_%s_Stage_%s_Task_%s'%(p.uid, s1.uid, t.uid))

        p.add_stages(s1)
        it_task_uids.append({'openmm': s1_task_uids})

        s2 = Stage()        
        s2_task_uid = list()

        t = Task()
        t.pre_exec = [  'export PATH=/home/vivek91/miniconda2/bin:$PATH',
                        'source activate openmm_env']
        t.executable = ['python']
        t.arguments = [ 'analyze.py',
                        '--lag', '2',
                        '--clusters', '100',
                        '--pdb', 'ala2.pdb',
                        '--components', '4',
                        '--stride', '10' ]
        t.cores = 1

        t.link_input_data = ['$SHARED/ala2.pdb', '$SHARED/analyze.py']
        t.download_output_data = [ 'microstate_info.txt > dur-%s-ensemble-%s-iters-%s/microstate_info-%s.txt' % (NS, ENSEMBLE_SIZE, TOTAL_ITERS, it),
                                    'macrostate_info.txt > dur-%s-ensemble-%s-iters-%s/macrostate_info-%s.txt' % (NS, ENSEMBLE_SIZE, TOTAL_ITERS, it)]

        for i in range(it):
            for j in range(ENSEMBLE_SIZE):
                t.link_input_data += ['%s/trajectory.dcd > trajectory-%s_%s.dcd' %(it_task_uids[i]['openmm'][j], i, j)]

        s2_task_uid.append('$Pipeline_%s_Stage_%s_Task_%s'%(p.uid,s2.uid, t.uid))
        s2.add_tasks(t)
        p.add_stages(s2)

        it_task_uids[it]['msm'] = s2_task_uid

    return p

if __name__ == '__main__':

    pipelines_set = set()

    pipelines_set.add(get_pipeline())

    total_cores = ENSEMBLE_SIZE*20

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'xsede.supermic',
            'walltime': 15,
            'cores': total_cores,
            'project': 'TG-MCB090174',
            'access_schema': 'gsissh'
    }

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)
    # Data common to multiple tasks -- transferred only once to common staging area
    rman.shared_data = [ './ala2.pdb','./simulate.py','./analyze.py' ]

    # Create Application Manager
    appman = AppManager(port=32781)
    #appman = AppManager(port=) # if using docker, specify port here.

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(pipelines_set)

    # Run the Application Manager
    appman.run()
