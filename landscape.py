from ruamel.yaml import YAML
import requests
import argparse
import sys

yaml=YAML(typ='safe')
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="invoked_command")


create = subparser.add_parser("create", help="Create new Packet architecture")
create.add_argument("-s", "--state", help="state file")
# create.set_defaults(selected="create")

# read = subparser.add_parser("read", help="List current Packet architecture")
# read.add_argument("-f", "--file", help="state file")
#
# update = subparser.add_parser("update", help="Update current Packet architecture")
# update.add_argument("-f", "--file", help="state file")
#
# delete = subparser.add_parser("delete", help="Destroy current Packet architecture")
# delete.add_argument("-f", "--file", help="state file")

# test = subparser.add_parser("delete", help="Self test")
# test.add_argument("-f", "--file", help="state file")

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")



if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()
# print(args.file)
# print(args.selected)
print(args)
# print(parser.parse_args(["all"]))

if args.invoked_command == "create":
    # Get current devices

    # Make new device

    # Return created device
