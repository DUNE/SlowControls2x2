"""
    Script to automatically ramp down all the TTis

    Last modification:  2025-09-28
    by:                 Nicolas Sallin, nicolas.sallin@unibe.ch
"""
import argparse
import sys
import subprocess
import json
import os

TTI_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(TTI_path)

from Source.tti_library_old import ttiPsu
from Source.tti_control import ramp_down, ramp_up

from Source.test_source import print_in_source

CONFIG_PATH = os.path.join(TTI_path, "CONFIG/")

def _check_args(modules):
    # Delete the duplicate and check that the correct number were given
    set_modules = set(modules)
    if not set_modules.issubset({0, 1, 2, 3}):
        raise ValueError("Wrong modules number provided. Accepted values are 0,1,2 and/or 3")

    return list(set_modules)

def _get_confirmation_proceed(modules, command):
    prompt = f"TTIs {modules} will be ramped {command}. The monitoring will be temporarily turned off, are the concerned people informed? (y/n): "
    while True:
        reply = input(prompt).strip().lower()
        if reply in ("y", "yes"):
            return 0
        elif reply in ("n", "no"):
            print("Then please inform the concerned people and run the script when it is done.")
            sys.exit(0)
        else:
            print("Please answer with 'y' or 'n'.")


def _turn_off_monitoring(): 
    try:
        subprocess.run(["podman", "stop", "tti-monitoring"], check=True)
        print("\ntti-monitoring stopped successfully.")
    except subprocess.CalledProcessError as e:
        raise e(f"\nError: failed to stop tti-monitoring.")
    
    return 0

def _turn_on_monitoring(): 
    try:
        subprocess.run(["./run.sh"], check=True)
        print("\nExecuted ./run.sh successfully. Monitoring is back on")
    except subprocess.CalledProcessError:
        print("\nError: ./run.sh failed. Monitoring was not restored")
        return 1

    return 0


def _ramp_down(module):
    print(f"\nInitialization ramp down of module {module}")
    
    # Get the ip of the TTI
    config_file = os.path.join(CONFIG_PATH, f'module{module}.json')
    with open(config_file, "r") as f:
        config = json.load(f)
    ip_tti = config[f"module{module}"][f"TTI{module}"]["ip"]

    print(f"Ip address found: {ip_tti}")

    tti = ttiPsu(ip_tti,1)
    #   Start voltage so that if connection is lost things dont blow up 
    V_start = tti.readOutputVolts()
    status = tti.getOutputIsEnabled()
    max_amp = tti.getMaxAmps()
    # V_start = "v_start"
    # status = False
    # max_amp = "max_amp"

    if status == True:
        status = "Enabled"
    elif status == False:
        status = "Disabled"
    else:
        raise ValueError(f"Unexpected status returned for TTI {module}: {status}")
    print(f"The current voltage on the TTI is: {V_start}\t V\nCurrently the output status is (True/enabled): {status}\nThe current limit on the TTI is: {max_amp}")
    # Ramp down
    ramp_down(ip_tti)

    return 0

def _ramp_up(module):
    print(f"\nInitialization ramp up of module {module}")
    
    # Get the ip of the TTI
    config_file = os.path.join(CONFIG_PATH, f'module{module}.json')
    with open(config_file, "r") as f:
        config = json.load(f)
    ip_tti = config[f"module{module}"][f"TTI{module}"]["ip"]

    print(f"Ip address found: {ip_tti}")

    tti = ttiPsu(ip_tti,1)
    #   Start voltage so that if connection is lost things dont blow up 
    V_start = tti.readOutputVolts()
    status = tti.getOutputIsEnabled()
    max_amp = tti.getMaxAmps()
    # V_start = "v_start"
    # status = True
    # max_amp = "max_amp"

    if status == True:
        status = "Enabled"
    elif status == False:
        status = "Disabled"
    else:
        raise ValueError(f"Unexpected status returned for TTI {module}: {status}")
    print(f"The current voltage on the TTI is: {V_start}\t V\nCurrently the output status is: {status}\nThe current limit on the TTI is: {max_amp}")

    # Ramp down
    ramp_up(ip,0,100)

    return 0

def main(command, modules):
    """
    Main funciton of the script:
        1. Check the arguments
        2. Ask the safety questions
        3. Turn off the TTIs monitoring
        4. Ramp the TTIs
        5. Turn on the TTIs monitoring again
    """

    #####
    #       1. Check the args
    ####
    modules = _check_args(modules)

    #####
    #       2. Confirm the action of the user and make sure he noticed the concerned persons
    #####
    _get_confirmation_proceed(modules, command)

    #####
    #       3. Turn off the TTIs monitoring
    ####
    _turn_off_monitoring()

    #####
    #       4. Ramp down the TTIs
    #####
    ramp_status = []
    for module in modules:
        ramp_status.append(1)
        if command == "down":
            ramp_status[-1] = _ramp_down(module)

        elif command == "up":
            ramp_status[-1] = _ramp_up(module)
    if 1 in ramp_status:
        print("\nNot all TTIs were ramped. The statues are (0/success, 1/error): {ramp_status}")
    else:
        print("\nThe TTIs were ramped down.")

    #####
    #       5. Turn the monitoring back on
    #####
    status_monitoring = _turn_on_monitoring()
    if status_monitoring == 0:
        print("\nThe monitoring of the TTIs was restored, don't forget to notify the concerned person")
    else:
        print("\nThe monitoring of the TTIs was NOT restored, please restore it my hand or inform the concerned persons")

    return 0


if __name__ == '__main__':
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Ramp the 2x2 TTIs", usage="%(prog)s [-h] COMMAND [--modules i_module j_module ...]")
    parser.add_argument("command", choices=["up", "down"],metavar="COMMAND", type=str.lower, help="Ramp the power up or down. {up, down}")
    parser.add_argument("--modules", nargs='+', default=[0,1,2,3], type=int, help="TTIs numbers to ramp, default: 0 1 2 3")
    # parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    # parser.add_argument("--log_level", default=None, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Level of the logger")
    
    args = parser.parse_args()
    main(args.command, args.modules)
