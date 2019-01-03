from ruamel.yaml import YAML
import json
import requests
import argparse
import sys
import os
import logging
import pprint

# Change working directory to landscape.py location always
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

yaml=YAML(typ='safe')
yaml.default_flow_style = False
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="invoked_command")


create = subparser.add_parser("create", help="Create new Packet architecture")
create.add_argument("-s", "--state", help="state file")

# read = subparser.add_parser("read", help="List current Packet architecture")
# read.add_argument("-f", "--file", help="state file")
#
# update = subparser.add_parser("update", help="Update current Packet architecture")
# update.add_argument("-f", "--file", help="state file")
#
delete = subparser.add_parser("delete", help="Destroy current Packet architecture")
delete.add_argument("-s", "--state", help="state file")

# test = subparser.add_parser("delete", help="Self test - setup host, run commands and check output")
# test.add_argument("-f", "--file", help="state file")

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

# Print out help if no arguments are given
# Why isn't this default python behaviour???
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

# Set up logging
log_level = "DEBUG"

if args.verbose == True:
    log_level = "DEBUG"
else:
    log_level = "WARN"

logging.basicConfig(level = log_level, format="%(asctime)s %(levelname)-8s %(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

if args.invoked_command == "create":
    # Get current devices
    current_devices_response = requests.get("https://api.packet.net/projects/ca73364c-6023-4935-9137-2132e73c20b4/devices", \
    headers={"X-Auth-Token": os.environ.get("LANDSCAPE_API_KEY")})
    logging.info(current_devices_response)
    current_devices = json.loads(current_devices_response.text)

    try:
        with open(args.state or "main.ls") as f:
            state_list = yaml.load(f)
            logging.info("Requested state: %s", state_list)

            save_states = []

            for state in state_list:
                # Add ssh key if set
                if "ssh_key" in state:
                    ssh_key_create_response = requests.post('https://api.packet.net/projects/ca73364c-6023-4935-9137-2132e73c20b4/ssh-keys', \
                    headers={"X-Auth-Token": os.environ.get("LANDSCAPE_API_KEY")}, json={"key" : state["ssh_key"], "label" : "Created by landscape" })
                    logging.info(ssh_key_create_response)

                    ssh_key_search_response = requests.get('https://api.packet.net/projects/ca73364c-6023-4935-9137-2132e73c20b4/ssh-keys', \
                    headers={"X-Auth-Token": os.environ.get("LANDSCAPE_API_KEY")})
                    logging.info(ssh_key_search_response)
                    ssh_key_search = json.loads(ssh_key_search_response.text)

                    # Doesn't work for some reason

                    # ssh key reverse lookup
                    # for key_data in ssh_key_search["ssh_keys"]:
                    #     if key_data["key"] == state[0]["ssh_key"]:
                    #         state[0]["project_ssh_keys"] = key_data["id"]
                    #         break



                # Warn if hostname in use
                for device in current_devices["devices"]:
                    if device["hostname"] == state["hostname"]:
                        logging.warn("Hostname in use!")

                # Make new device
                new_device_json_stripped = state
                try:
                    del new_device_json_stripped["ssh_key"]
                except KeyError:
                    pass
                logging.info(new_device_json_stripped)

                # Actually create new device
                create_device_response = requests.post("https://api.packet.net/projects/ca73364c-6023-4935-9137-2132e73c20b4/devices", \
                headers={"X-Auth-Token": os.environ.get("LANDSCAPE_API_KEY")}, json=new_device_json_stripped)
                create_device = create_device_response.text
                logging.info(create_device_response)

                create_device_object = json.loads(create_device)
                save_state = {  "id" : create_device_object["id"],
                                "hostname"  : create_device_object["hostname"],
                                "facility"  : create_device_object["facility"]["code"],
                                "plan"      : create_device_object["plan"]["slug"],
                                "operating_system"      : create_device_object["operating_system"]["slug"]
                                }

                save_states.append(save_state)

            try:
                with open((args.state or "main")+".lsstate", "w+") as current_state:
                    yaml.dump(save_states, current_state)
                    logging.info("Current state: %s", save_state)
                    current_state.close()

            except IOError as error:
                logging.error("Could not open lsstate file!")
                sys.exit(1)

    except IOError as error:
        logging.error("Error: file \"{0}\" does not exist!".format(args.state or "main.ls"))
        sys.exit(1)

elif args.invoked_command == "delete":

    # Delete all IDs specified

    try:
        with open((args.state or "main")+".lsstate") as f:
            state_list = yaml.load(f)
            for state in state_list:
                delete_device_response = requests.delete("https://api.packet.net/devices/{0}".format(state["id"]), \
                headers={"X-Auth-Token": os.environ.get("LANDSCAPE_API_KEY")})
                delete_device = delete_device_response.text
                if 200 <= delete_device_response.status_code <= 299:
                    logging.info("Device {0} successfully deleted".format(state["hostname"]))
                logging.info(delete_device_response)
            f.close()

        os.remove((args.state or "main")+".lsstate")

    except IOError as error:
        print("Error: No .lsstate file found!")
        sys.exit(1)





    # ssh_key_response = requests.post('https://api.packet.net/project/{id}/devices'.format())

    #


    # Return created device
