import subprocess

from physpetool.softwares.path import getlocalpath


def docontree(input, output):
    """
Combine tree
    :param input: input files
    :param output: output directory
    """
    #get raxml path
    raxmlpath = getlocalpath()
    #run
    consensuseCmd = raxmlpath + "/raxmlHPC-PTHREADS-AVX " + " -J MR -m GTRCAT -z " + input + " -w " + output + " -n T1"
    subprocess.call(consensuseCmd, shell=True)
