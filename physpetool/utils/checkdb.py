# ########################## Copyrights and License #############################
#                                                                               #
# Copyright 2016 Yang Fang <yangfangscu@gmail.com>                              #
#                                                                               #
# This file is part of PhySpeTree.                                              #
# https://xiaofeiyangyang.github.io/physpetools/                                #
#                                                                               #
# PhySpeTree is free software: you can redistribute it and/or modify it under   #
# the terms of the GNU Lesser General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)     #
# any later version.                                                            #
#                                                                               #
# PhySpeTree is distributed in the hope that it will be useful, but WITHOUT ANY #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS     #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                      #
#                                                                               #
# You should have received a copy of the GNU Lesser General Public License      #
# along with PhySpeTree. If not, see <http://www.gnu.org/licenses/>.            #
#                                                                               #
# ###############################################################################


"""
The module for check highly conserved proteins will be prepared.
"""

from physpetool.phylotree.retrieveprotein import getcolname, getspecies, hcp_name
from physpetool.utils.checkinputfile import checkFile, readIputFile, checkKeggOrganism
import os


def check_ehcp(input, output):
    """
    Check the highly conserved proteins will be prepared.
    :param input: the species abbreviated names
    :param output: a directory contain check result
    """
    # prepare a file write result
    if not os.path.exists(output):
        os.makedirs(output)
    fw_name = "PhySpeTree_echp_extend.txt"
    open_path = os.path.join(output, fw_name)
    fw = open(open_path, 'wb')

    # check input names
    input_path = checkFile(input)
    input_list = readIputFile(input_path)
    colname = getcolname()
    relist, match_ko = getspecies(input_list, colname)
    p = 1
    for line in match_ko:
        hcpname = hcp_name(line.strip())
        massage = "'{0}' ----------------------------------> p{1}.fasta\n".format(hcpname, str(p))
        print(massage)
        fw.write(massage)
        p += 1
    print("Checked extend highly conserved proteins is completed.\n")
    print("Checked result was store in {0}".format(open_path))
    fw.close()


def check_hcp(input, output):
    """
    Check whether the input species in the hcp database
    :param input: the species names
    :param output: the directory contains check result
    """
    if not os.path.exists(output):
        os.makedirs(output)
    fw_name = "PhySpeTree_hcp_checked.txt"
    open_path = os.path.join(output, fw_name)
    fw = open(open_path, 'wb')

    input_path = checkFile(input)
    input_list = readIputFile(input_path)
    input_checked = checkKeggOrganism(input_list)

    no_match = list(set(input_list).difference(set(input_checked)))

    if no_match.__len__() == 0:
        fw.write("All species are match in HCP DATABASE")
    else:
        fw.write("The follow species are not support in HCP DATABASE:\n")
        for line in no_match:
            fw.write(line + "\n")

    print("Checked  whether the input species names in HCP DATABASE completed.\n")
    print("Checked result is store in {0}".format(open_path))
    fw.close()
