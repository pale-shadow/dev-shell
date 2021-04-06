import re
import time
import getpass
import logging
from datetime import datetime
from panos import panorama, policies, base
from panos.policies import SecurityRule, PreRulebase, PostRulebase, Rulebase

'''Global variables'''
current_dg = 'On_Premises'
source_zones = ['GAMING', 'GAME_CLIENTS', 'ANY']
destination_zones = ['GAMING', 'GAME_CLIENTS', 'ANY']
targets = ['007901000537', '007901003306']
new_tags = ['Gaming_Legacy']
new_dg = 'Gaming'
strip_vsys = True

'''Setup logging'''
time_now = datetime.now().strftime("%m-%d-%y_%H%M%S")
logging.basicConfig(
    level=logging.DEBUG,
    filename=f'gaming_migration_{time_now}.log',
    filemode='w',
    format='%(asctime)s %(levelname)s: %(message)s'
)
logging.getLogger("panorama").setLevel(logging.DEBUG)


def get_pan_addr():
    """
    Prompt the user to enter an address, then checks it's validity

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """
    while True:
        pan_addr = input('\nPlease enter Panorama IP or FQDN: ')
        ipr = re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                       pan_addr)
        fqdnr = re.match(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', pan_addr)
        if ipr:
            break
        elif fqdnr:
            break
        else:
            print("\nThere was something wrong with your entry. Please try again...\n")
    return pan_addr


def get_creds():
    """
    Prompt the user to enter a username and password

    Authenticate user
    pan_addr = get_pan_addr()

    Args: variable (type): description

    Returns:
        string: username
        string: password

    Raises: Exception: description
    """
    while True:
        username = input("Please enter your user name: ")
        usernamer = re.match(r"^[\w-]{3,24}$", username)
        if usernamer:
            password = getpass.getpass("Please enter your password: ")
            break
        else:
            print("\nThere was something wrong with your entry. Please try again...\n")
    return username, password


def get_rulebase(device, devicegroup):
    """
    Search for specific rules based on match criteria provided.

    A bit longer description.

    Args:
        variable (type):
        device
        devicegroup

    Returns:
        rulebase: description

    Raises:
        Exception: description
    """
    # Build the rulebase
    if isinstance(device, panorama.Panorama):
        dg = panorama.DeviceGroup(devicegroup)
        device.add(dg)
        rulebase = policies.PreRulebase()
        dg.add(rulebase)
    else:
        return False
    policies.SecurityRule.refreshall(rulebase)
    return rulebase


def copy_rulebase(device, devicegroup, rules):
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """
    if isinstance(device, panorama.Panorama):
        dg = panorama.DeviceGroup(devicegroup)
        device.add(dg)
        prb = dg.add(PreRulebase())
        for rule in rules.children:
            rule.tag = new_tags
            rule.target = []
            prb.add(rule)
        prb.apply()
    else:
        return False
    policies.SecurityRule.refreshall(prb)
    return prb


def tag_rules(device, devicegroup, rules):
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """
    if isinstance(device, panorama.Panorama):
        dg = panorama.DeviceGroup(devicegroup)
        device.add(dg)
        prb = dg.add(PreRulebase())
        for rule in SecurityRule.refreshall(prb):
            for specific_rule in rules.children:
                if rule.name == specific_rule.name:
                    if rule.tag is not None:
                        rule.tag = rule.tag + new_tags
                    else:
                        rule.tag = new_tags
                    prb.add(rule)
        prb.apply()
    else:
        return False
    policies.SecurityRule.refreshall(prb)
    return prb


if __name__ == '__main__':
    username, password = get_creds()
    pan_addr = 'awspanorama.psolabs.com'
    '''Create the device with the appropriate pandevice type'''
    device = base.PanDevice.create_from_device(
        pan_addr, username, password
    )
    rules = get_rulebase(device, current_dg)
    rulelist = rules.children
    hitbase = policies.Rulebase()
    loose_match = True
    for rule in rulelist:
        hitlist = []
        if source_zones:
            source_zone_match = False
            if loose_match and "any" in rule.fromzone:
                source_zone_match = True
            else:
                for object_string in rule.fromzone:
                    if object_string in source_zones:
                        source_zone_match = True
            # Parse Targets
            if targets:
                target_match = False
                if source_zone_match is True:
                    if rule.target is not None:
                        for object_string in rule.target:
                            if object_string in targets:
                                target_match = True
                    else:
                        logging.info('rule name: ' + rule.name + ' - has no target set')
                        target_match = True
            hitlist.append(target_match)
        # Add to hit rulebase
        if False not in hitlist:
            hitbase.add(rule)
        # OR Destination Zone Add
        if destination_zones:
            destination_zone_match = False
            if loose_match and "any" in rule.tozone:
                destination_zone_match = True
            else:
                for object_string in rule.tozone:
                    if object_string in destination_zones:
                        destination_zone_match = True
            # Parse Targets
            if targets:
                target_match = False
                if destination_zone_match is True:
                    if rule.target is not None:
                        for object_string in rule.target:
                            if object_string in targets:
                                target_match = True
                    else:
                        logging.info('rule name: ' + rule.name + ' - has no target set')
                        target_match = True
            hitlist.append(target_match)
        # Add to hit rulebase
        if False not in hitlist:
            hitbase.add(rule)
    # Remove duplicates
    updated_hitbase = policies.Rulebase()
    for rule in hitbase.children:
        if rule in updated_hitbase.children:
            logging.warning('rule: ' + rule.name + ' already exists, will not update to rulebase')
        else:
            updated_hitbase.add(rule)
    # copy_rulebase(device, new_dg, updated_hitbase)
    ## TAG Existing Rules with
    tag_rules(device, current_dg, updated_hitbase)


"""
# Script:       gaming_migration.py

# Author:       Anton Coleman <acoleman@paloaltonetworks.com>

# Description:  Copy specific rules from the On Premises to the 'Gaming' device
#               group. This is done one rule at a time. A log of all actions to the rulebase is saved to the
#               working directory.

# Usage:        gaming_migration.py

# Requirements: pan-os-python

# Python:       Version 3

# License:      © 2021 Palo Alto Networks, Inc. All rights reserved.
                Licensed under SCRIPT SOFTWARE AGREEMENT, Palo Alto Networks,
                Inc., at https://www.paloaltonetworks.com/legal/script-software-license-1-0.pdf
"""
