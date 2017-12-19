from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if not os.environ.get('RADICAL_ENTK_VERBOSE'):
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

if not os.environ.get('RADICAL_PILOT_DBURL'):
    os.environ['RADICAL_PILOT_DBURL'] = "mongodb://138.201.86.166:27017/ee_exp_4c"

MAX_STAGES = 2
CUR_STAGE = 1


def generate_pipeline():
    
    def func_condition():

        global CUR_STAGE, MAX_STAGES
    
        if CUR_STAGE < MAX_STAGES:
            CUR_STAGE += 1
            return True

        return False

    def func_on_true():

        global CUR_STAGE

        s = Stage()
        print 'func uid: ', s.uid
        
        t = Task()    
        t.executable = ['/bin/echo']   
        t.arguments = ['This is added stage %s'%CUR_STAGE] 

        # Add the Task to the Stage
        s.add_tasks(t)

        p.add_stages(s)

    def func_on_false():
        print 'Done'

    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object 
    s1 = Stage()
    print 'Main uid: ', s1.uid

    # Create a Task object which creates a file named 'output.txt' of size 1 MB
    t1 = Task()    
    t1.executable = ['/bin/echo']   
    t1.arguments = ['This is the original stage'] 

    # Add the Task to the Stage
    s1.add_tasks(t1)

    # Add post-exec to the Stage
    s1.post_exec = {
                       'condition': func_condition,
                       'on_true': func_on_true,
                       'on_false': func_on_false
                   }

    # Add Stage to the Pipeline
    p.add_stages(s1)    

    return p

if __name__ == '__main__':


    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'xsede.supermic',
            'walltime': 10,
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
