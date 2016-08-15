import os
import subprocess
import sys

from physpetool.phylotree.domuscle import domuscle_file, domuscle
from physpetool.phylotree.dogblocks import dogblocks
from physpetool.phylotree.doraxml import doraxml
from physpetool.convert.fasta2phy import fasta2phy
from physpetool.convert.concatenate import cocat_path
from physpetool.phylotree.log import getLogging, setlogdir
from physpetool.phylotree.retrieve16srna import retrieve16srna
from physpetool.phylotree.retrieveprotein import doretrieve
import argparse

from physpetool.utils.checkinputfile import checkKeggOrganism, checkSilvaOrganism

"""
the main module as enter point and contain a main() function to invoke other
script same as pipeline.
"""

APP_DESC = "construct"


raxmlpara_pro = "-f a -m PROTGAMMAJTTX  -p 12345 -x 12345 -# 100 -n T1"
raxmlpara_dna = "-f a -m GTRGAMMA  -p 12345 -x 12345 -# 100 -n T1"
musclepara = '-maxiters 100'
gblockspara_pro = '-t=p -e=-gb1'
gblockspara_dna = '-t=d -e=-gb1'


def start_args(input):
    """
Argument parse
    :param input: arguments
    """
    autobuild_args = input.add_argument_group("AUTOBUILD OPTIONS")
    advance_args = input.add_argument_group("ADVANCE OPTIONS")
    autobuild_args.add_argument('-i', nargs='?', dest='spenames', type=argparse.FileType('r'),
                        help='Input file must be contain the species names')
    autobuild_args.add_argument('-o', action='store', dest="outdata",
                        default='Outdata', help='Out file name be string type')
    autobuild_args.add_argument('-t', action='store', dest='thread',
                        type=int, default=1, help='Set the thread')
    autobuild_args.add_argument('--hcp', action='store_true', dest='HCP',
                        default=False, help='Reconstruct phylogenetic tree by highly conserved proteins')
    autobuild_args.add_argument('--srna', action='store_true', dest='ssurna',
                        default=False, help='Reconstruct phylogenetic tree by 16s ran')
    autobuild_args.add_argument('-v', '--version', action='store_true',
                        default=False, help='Version information')
    advance_args.add_argument('--muscle', action='store', dest='muscle',
                        default=musclepara, help='Alignment by muscle')
    advance_args.add_argument('--gblocks', action='store', dest='gblocks',
                        default=gblockspara_pro, help='Use gblock')
    advance_args.add_argument('--raxml', action='store', dest='raxml',
                        default=raxmlpara_pro, help='Build by raxml')


def starting(args):
    """
starting run reconstruct tree
    :param args: arguments
    """
    print "in put fasta file is:"
    print args.spenames
    print "outfile is:"
    print args.outdata + "\n"
    print "now loading data and constructing species phylogenetic tree..."
    print args.thread

    in_put = args.spenames

    pwd = os.getcwd()

    out_put = os.path.join(pwd, args.outdata)
    # reconstruct phylogenetic tree by highly conserved proteins
    if args.HCP:
        setlogdir(out_put)

        hcp_input = checkKeggOrganism(in_put)
        out_retrieve = doretrieve(hcp_input, out_put)
        out_alg = domuscle_file(out_retrieve, out_put, args.muscle)
        out_concat = cocat_path(out_alg)
        out_gblock = dogblocks(out_concat, args.gblocks)
        out_f2p = fasta2phy(out_gblock)
        doraxml(out_f2p, out_put, args.raxml, args.thread)
    # reconstruct phylogenetic tree by ssu RNA
    elif args.ssurna:
        setlogdir(out_put)

        ssu_input = checkSilvaOrganism(in_put)
        out_retrieve = retrieve16srna(ssu_input, out_put)
        out_alg = domuscle(out_retrieve, out_put, args.muscle)
        if args.gblocks is gblockspara_pro:
            args.gblocks = gblockspara_dna
            out_gblock = dogblocks(out_alg, args.gblocks)
        out_f2p = fasta2phy(out_gblock)
        if args.raxml is raxmlpara_pro:
            args.raxml = raxmlpara_dna
            doraxml(out_f2p, out_put, args.raxml, args.thread)

