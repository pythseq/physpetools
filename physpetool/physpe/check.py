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
The arguments parse module for check module.

"""

import os
from physpetool.utils.checkdb import check_ehcp, check_hcp, check_srna

APP_DESC = ""


def start_args(input):
    """
Arguments parse
    :param input:  Arguments
    """

    annotation_args = input.add_argument_group("CHECK OPTIONS")
    annotation_args.add_argument('-i', action='store', dest="inputfile",
                                 help="Input organisms names file, which use to reconstructed \
                              phylogenetic tree.")
    annotation_args.add_argument('-o', action='store', dest="outputfile",
                                 default='check', help="It's a directory name contain check result. The default is \
                                name is check")
    annotation_args.add_argument('--hcp', action='store_true', dest="checkhcp",
                                 default=False, help="Check organisms whether supported by KEGG database.")
    annotation_args.add_argument('--ehcp', action='store_true', dest="checkehcp",
                                 default=False, help="Check the organisms highly conserved proteins, which users should \
                                prepared for extend highly conserved protein method.")
    annotation_args.add_argument('--srna', action='store_true', dest="checksrna",
                                 default=False, help="Check organisms whether supported by SILVA database.")


def starting(args):
    """
Staring run combine
    :param args: arguments
    """
    pwd = os.getcwd()

    out_put = os.path.join(pwd, args.outputfile)
    if args.checkehcp:
        check_ehcp(args.inputfile, out_put)
    if args.checkhcp:
        check_hcp(args.outputfile, out_put)
    if args.checksran:
        check_srna(args.outputfile, out_put)
