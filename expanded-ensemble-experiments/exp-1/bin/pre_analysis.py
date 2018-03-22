#!/usr/bin/env python

__author__    = "Vivek <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2014, http://radical.rutgers.edu"
__license__   = "MIT"

from copy import deepcopy

from radical.entk import NoKernelConfigurationError
from radical.entk import KernelBase

# ------------------------------------------------------------------------------
# 
_KERNEL_INFO = {
            "name":         "pre_analysis",
            "description":  "Analysis kernel",
            "arguments":   {"--template=":     
                        {
                            "mandatory": True,
                            "description": "Template filename"
                        },
                        "--newname=":     
                        {
                            "mandatory": True,
                            "description": "New mdp filename"
                        },
                        "--wldelta=":
                        {
                            "mandatory": True,
                            "description": "Topology file"
                        },
                        "--equilibrated=":
                        {
                            "mandatory": True,
                            "description": "Index file"
                        },
                        "--lambda_state=":
                        {
                            "mandatory": True,
                            "description": "Output file"
                        },
                        "--seed=":
                        {
                            "mandatory": True,
                            "description": "Output file"
                        }
                    },
            "machine_configs": 
            {
                "*": {
                    "environment"   : None,
                    "pre_exec"      : None,
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "xsede.stampede":{
                    "environment"   : None,
                    "pre_exec"      : ['module load python'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "xsede.comet":{
                    "environment"   : None,
                    "pre_exec"      : ['. /usr/share/Modules/init/sh','module load python'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "xsede.supermic":{
                    "environment"   : None,
                    "pre_exec"      : ['module load python'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "local.localhost":{
                    "environment"   : None,
                    "pre_exec"      : ['export PYTHONPATH=$PYTHONPATH:/home/vivek/.local/lib/python2.7/site-packages'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                }
            }
    }


# ------------------------------------------------------------------------------
# 
class pre_analysis_kernel(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(pre_analysis_kernel, self).__init__(_KERNEL_INFO)


    # --------------------------------------------------------------------------
    #
    def _bind_to_resource(self, resource_key):
        """(PRIVATE) Implements parent class method. 
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        executable = cfg['executable']
        arguments  = [  'analysis_1.py',
                        '--template', self.get_arg("--template="), 
                        '--newname', self.get_arg("--newname="), 
                        '--wldelta', self.get_arg("--wldelta="), 
                        '--equilibrated', self.get_arg("--equilibrated="), 
                        '--lambda_state', self.get_arg("--lambda_state="), 
                        '--seed', self.get_arg("--seed="),
                    ]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]

