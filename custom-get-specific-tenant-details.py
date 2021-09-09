#!/usr/bin/env python

import json
from sys import exit
from acitoolkit.acitoolkit import *
from credentials import *

def as_dict(object_list):
    # Helper function to create a name-indexed dictionary
    # from a list of objects returned by acitoolkit get functions
    objects_dict = {}
    for obj in object_list:
        objects_dict[obj.name] = obj
    return objects_dict


tenant_name = "Marketing"
vrf_name = "Marketing_VRF"
bridge_domain_name = "Marketing_BD"
application_profile_name = "Marketing_APP"
contract_name = "Portal"


session = Session(APIC_HOST, APIC_USERNAME, APIC_PASSWORD)
session.login()

tenants = as_dict(Tenant.get(session))

# print("All tenants: {}".format(tenants.keys()))

if tenants.get(tenant_name) is None:
    print("Couldn't find tenant {} on the APIC.".format(tenant_name))
    exit(1)

tenant = tenants.get(tenant_name)
print("=============== Tenant ================")
print("Tenant '{}' exists with DN:- {}!\n".format(tenant.name, tenant.dn))

vrfs = as_dict(Context.get(session, tenant))
if vrf_name in vrfs:
    print("=============== VRF ================")
    print("'{}' exists with DN:- {}\n".format(vrf_name, vrfs[vrf_name].dn))
else:
    print("Couldn't find VRF {} under tenant {}.".format(vrf_name, tenant.name))

bridge_domains = as_dict(BridgeDomain.get(session, tenant))
if bridge_domain_name in bridge_domains:
    bd = bridge_domains[bridge_domain_name]
    print("=============== BD ================")
    print("'{}' exists with DN:- {}\n".format(bd.name, bd.dn))
    print("=============== Subnet ================")
    print("It has the following subnets:")

    for subnet in Subnet.get(session, bd, tenant):
        print(subnet.get_addr())
else:
    print("Couldn't find BD {} under tenant {}.".format(bridge_domain_name, tenant.name))



application_profiles = as_dict(AppProfile.get(session, tenant))
if application_profile_name in application_profiles:
    app = application_profiles[application_profile_name]
    print("\n=============== APP Profile ================")
    print("'{}' exists with DN:- {}\n".format(app.name, app.dn))
    print("=============== EPGs ================")
    print("It has the following EPGs:")

    for epg in EPG.get(session, app, tenant):
        print("-    '{}' exists with DN:- {}\n".format(epg.name, epg.dn))
else:
    print("Couldn't find APP {} under tenant {}.".format(application_profile_name, tenant.name))    



contracts = as_dict(Contract.get(session, tenant))
if contract_name in contracts:
    contract = contracts[contract_name]
    print("=============== Contract ================")
    print("Contract '{}' exists with DN:- {}\n".format(contract.name, contract.dn))    
    print("Exit-Bye\n")

else:
    print("Couldn't find APP {} under tenant {}.".format(application_profile_name, tenant.name))    
