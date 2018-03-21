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
            "name":         "post_analysis",
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
                            "--dir=":
                            {
                                "mandatory": True,
                                "description": "New mdp filename"
                            },
                            "--run=":
                            {
                                "mandatory": True,
                                "description": "Run number"
                            },
                            "--gen=":
                            {
                                "mandatory": True,
                                "description": "Gen number"
                            },
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
                    "pre_exec"      : ['module load python','export PYTHONPATH=$PYTHONPATH:/home1/02734/vivek91/expanded-ensemble/alchemical_analysis:/home1/02734/vivek91/.local/lib/python2.7/site-packages','sh transfer_local_files.sh'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "xsede.supermic":{
                    "environment"   : None,
                    "pre_exec"      : ['module load python','export PYTHONPATH=/home/vivek91/modules/alchemical-analysis/alchemical_analysis:/home/vivek91/modules/alchemical-analysis:/home/vivek91/.local/lib/python2.7/site-packages:$PYTHONPATH','ln -s ../staging_area data'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
                "local.localhost":{
                    "environment"   : None,
                    "pre_exec"      : ['export PYTHONPATH=$PYTHONPATH:/home/vivek/Research/repos/expanded-ensemble/alchemical_analysis:/home/vivek/.local/lib/python2.7/site-packages'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },                
                "xsede.comet":{
                    "environment"   : None,
                    "pre_exec"      : ['. /usr/share/Modules/init/sh','module load python', 'export PYTHONPATH=$PYTHONPATH:/home/vivek91/expanded-ensemble/alchemical_analysis:/home/vivek91/.local/lib/python2.7/site-packages', 'export LAPACK=/opt/lapack/intel','export BLAS=/opt/lapack/intel', 'export LAPACKHOME=/opt/lapack/intel','export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/lapack/intel/lib','export LIBPATH=$LIBPATH:/opt/lapack/intel/lib'],
                    "executable"    : "python",
                    "uses_mpi"      : False
                },
            }
    }


# ------------------------------------------------------------------------------
# 
class post_analysis_kernel(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(post_analysis_kernel, self).__init__(_KERNEL_INFO)


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
        arguments  = [  'analysis_2.py',
                        '--template', self.get_arg("--template="), 
                        '--newname', self.get_arg("--newname="),
                        '--dir', self.get_arg("--dir="),
                        '--run', self.get_arg("--run="),
                        '--gen', self.get_arg("--gen=")
                    ]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]

