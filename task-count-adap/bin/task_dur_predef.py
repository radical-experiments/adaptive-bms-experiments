from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os, sys

# ------------------------------------------------------------------------------
# Set default verbosity

if not os.environ.get('RADICAL_ENTK_VERBOSE'):
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

if not os.environ.get('RADICAL_PILOT_DBURL'):
    os.environ['RADICAL_PILOT_DBURL'] = "mongodb://entk:entk@ds141406.mlab.com:41406/adap-task-count"

def generate_pipeline():
    
    # Create a Pipeline object
    p = Pipeline()

    for s_cnt in range(STAGES):

        # Create a Stage object 
        s = Stage()

        t = Task()    
        t.pre_exec = ['export PATH=/home/vivek91/tools/stress-ng-0.09.04:$PATH']
        t.executable = ['stress-ng']   
        t.arguments = [ '-c', '1', '-t', str(duration)]  

        # Add the Task to the Stage
        s.add_tasks(t)

        # Add Stage to the Pipeline
        p.add_stages(s)
    return p

if __name__ == '__main__':

    duration = int(sys.argv[1])
    STAGES = int(sys.argv[2])

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'xsede.supermic',
            'walltime': (duration*(STAGES+1)/60) + 40,
            'cores': 21,
            'project': 'TG-MCB090174',
            'access_schema': 'gsissh'
    }

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)

    # Create Application Manager
    appman = AppManager()

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    p = generate_pipeline()
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()
