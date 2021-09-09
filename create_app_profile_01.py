"""
create_app_profile.py
This is the full Tenant model, including two EPGs in the same Bridge Domain and VRF, with a Contract allowing HTTP traffic between them.
Script either creates the full Tenant Model or removes it.
"""
import json
from sys import exit
from acitoolkit.acitoolkit import *
from credentials import *

tenant_name = "Marketing"
vrf_name = "Marketing_VRF"
bridge_domain_name = "Marketing_BD"
bridge_domain_subnet = "192.168.21.1/24"
bridge_domain_subnet_name = "Marketing_Subnet"
app_prof_name = "Marketing_APP"
epg_portal_name = "Portal_EPG"
epg_users_name = "Users_EPG"

# Create Tenant
tenant = Tenant(tenant_name)

# Create VRF
vrf = Context(vrf_name, tenant)

# Create Bridge Domain
bridge_domain = BridgeDomain(bridge_domain_name, tenant)
bridge_domain.add_context(vrf)

# Create public subnet and assign gateway
subnet = Subnet(bridge_domain_subnet_name, bridge_domain)
subnet.set_scope("public")
subnet.set_addr(bridge_domain_subnet)

# Create http filter and filter entry
filter_http = Filter("http", tenant)
filter_entry_tcp80 = FilterEntry(
    "tcp-80", filter_http, etherT="ip", prot="tcp", dFromPort="http", dToPort="http"
)

# Create Portal contract and use http filter
contract_portal = Contract("Portal", tenant)
contract_subject_http = ContractSubject("http", contract_portal)
contract_subject_http.add_filter(filter_http)

# Create Application Profile
app_profile = AppProfile(app_prof_name, tenant)

# Create Portal EPG and associate bridge domain and contracts
epg_portal = EPG(epg_portal_name, app_profile)
epg_portal.add_bd(bridge_domain)
epg_portal.provide(contract_portal)

# Create Users EPG and associate bridge domain and contracts
epg_users = EPG(epg_users_name, app_profile)
epg_users.add_bd(bridge_domain)
epg_users.consume(contract_portal)

print("Candidate Tenant configuration as JSON payload:\n {}".format(tenant.get_json()))


# Connect and push configuration to APIC

session = Session(APIC_HOST, APIC_USERNAME, APIC_PASSWORD)
session.login()

choice = input("Would you like to delete the Tenant? (y/N): ")

if choice.lower().strip() == 'y':
    tenant.mark_as_deleted()
    # Push configuration to APIC
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
else:
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

if not resp.ok:
    print("API return Failure code {} with message {}".format(resp.status_code, resp.text))
    exit(1)
else:
    print("API return Success code {} with message {}".format(resp.status_code, resp.text))

