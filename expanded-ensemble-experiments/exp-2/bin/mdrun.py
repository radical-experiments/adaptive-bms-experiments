#!/usr/bin/env python

"""A kernel that writes Hello World to a file.
"""

__author__    = "Vivek <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2014, http://radical.rutgers.edu"
__license__   = "MIT"

from copy import deepcopy

from radical.entk import NoKernelConfigurationError
from radical.entk import KernelBase

# ------------------------------------------------------------------------------
# 
_KERNEL_INFO = {
            "name":         "mdrun",
            "description":  "Writes Hello World to a file",
            "arguments":   {"--nt=":     
                        {
                            "mandatory": True,
                            "description": "Number of threads"
                        },
                        "--tag=":     
                        {
                            "mandatory": True,
                            "description": "Tag of filename"
                        },
                        "--out=":
                        {
                            "mandatory": True,
                            "description": "Output filename"
                        },
                    },
            "machine_configs": 
            {
                "*": {
                    "environment"   : None,
                    "pre_exec"      : None,
                    "executable"    : "mdrun",
                    "uses_mpi"      : False
                },
                "xsede.stampede":{
                    "environment"   : None,
                    "pre_exec"      : ['. /opt/apps/lmod/lmod/init/sh','module restore','module load cxx11','module load python','source /work/02734/vivek91/gromacs-patched/bin/GMXRC.bash'],
                    "executable"    : "gmx mdrun",
                    "uses_mpi"      : False
                },
                "xsede.supermic":{
                    "environment"   : None,
                    "pre_exec"      : ['source /home/trje3733/pkgs/gromacs/5.1.3.wlmod/bin/GMXRC.bash'],
                    "executable"    : "gmx mdrun",
                    "uses_mpi"      : False
                },
                "local.localhost":{
                    "environment"   : None,
                    "pre_exec"      : ['export PATH=$PATH:/home/vivek/Research/modules/gromacs-5.1.3/build/bin'],
                    "executable"    : "gmx mdrun",
                    "uses_mpi"      : False
                },
                "xsede.comet":{
                    "environment"   : None,
                    "pre_exec"      : ['. /usr/share/Modules/init/sh','export PATH=$PATH:/home/vivek91/modules/gromacs/gromacs-5.1.3/build/bin'],
                    "executable"    : "gmx mdrun",
                    "uses_mpi"      : False
                }
            }
    }


# ------------------------------------------------------------------------------
# 
class mdrun_kernel(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(mdrun_kernel, self).__init__(_KERNEL_INFO)


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
        arguments  = [  '-nt', self.get_arg("--nt="), 
                        '-deffnm', self.get_arg("--tag="), 
                        '-dhdl', self.get_arg("--out="), 
                    ]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]

