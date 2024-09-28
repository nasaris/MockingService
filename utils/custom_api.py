import random
import ipaddress
from faker import Faker

fake = Faker()

# Definition von ASSET_TYPES
ASSET_TYPES = {
    "Information": "Information Asset",
    "Physical Assets": "Physical Asset",
    "Software": "Software Asset",
    "Services": "Service Asset",
    "Networks and Communications": "Network Asset",
    "Human Resources": "Human Resource Asset",
    "Financial Resources": "Financial Asset",
    "Reputation": "Reputation Asset",
    "Documented Procedures": "Procedure Asset"
}

# Hersteller-Listen
SOFTWARE_MANUFACTURERS = [
    "Microsoft", "Adobe", "Oracle", "VMware", "Red Hat", "SAP", "Salesforce", 
    "Intuit", "Autodesk", "Slack", "Dropbox", "Atlassian", "Symantec", 
    "McAfee", "Trend Micro", "Zoom", "Trello", "Asana", "MongoDB", 
    "JetBrains", "Unity Technologies", "GitHub", "GitLab", "MySQL", 
    "PostgreSQL", "Splunk", "ServiceNow", "TIBCO", "Informatica", 
    "Citrix", "Zendesk"
]

HARDWARE_MANUFACTURERS = [
    "Cisco", "Dell", "HP", "Lenovo", "Apple", "IBM", "Fujitsu", 
    "Supermicro", "Huawei", "Asus", "Acer", "Toshiba", "Panasonic", 
    "Sony", "Samsung", "LG", "HPE (Hewlett Packard Enterprise)", 
    "Intel", "AMD", "Nvidia", "Western Digital", "Seagate", "Hitachi", 
    "QNAP", "Synology", "NetApp", "EMC", "Juniper", "Arista Networks", 
    "Avaya", "Palo Alto Networks"
]

NETWORK_MANUFACTURERS = [
    "Cisco", "Juniper Networks", "Netgear", "Huawei", "Ubiquiti", 
    "Arista Networks", "Fortinet", "Palo Alto Networks", "MikroTik", 
    "TP-Link", "D-Link", "Extreme Networks", "Avaya", "Zyxel", 
    "Dell EMC", "Hewlett Packard Enterprise", "Ruckus Wireless", 
    "Nokia", "Ericsson", "Samsung Networks", "Linksys", "Alcatel-Lucent", 
    "Cambium Networks", "ADTRAN", "Radwin", "SonicWall", "WatchGuard", 
    "Ciena", "Riverbed", "Silver Peak"
]

SERVICE_PROVIDERS = [
    "Amazon Web Services", "Microsoft Azure", "Google Cloud", "IBM Cloud", 
    "Oracle Cloud", "Salesforce", "Alibaba Cloud", "DigitalOcean", 
    "Heroku", "Rackspace", "Vultr", "Linode", "OVHcloud", "Tata Communications", 
    "CenturyLink", "Equinix", "Interoute", "Akamai", "Fastly", 
    "Cloudflare", "Verizon Cloud", "SAP Cloud Platform", "Zoho", 
    "Dropbox", "Box", "iCloud", "Tencent Cloud", "Huawei Cloud", 
    "Nextiva", "GoDaddy", "Bluehost"
]

# Funktion zum Generieren einer Semantic Version
def generate_semver():
    return f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(0, 999)}"

# Zufällige IP-Adresse generieren
def generate_ip():
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

# Assets generieren
def generate_asset(asset_type):
    if asset_type == "Information":
        return {
            "name": fake.file_name(),
            "classification": random.choice(["Public", "Internal", "Confidential", "Secret"]),
            "storage_location": random.choice(["Cloud", "On-premise", "External Backup", "Data Center"])
        }
    elif asset_type == "Physical Assets":
        return {
            "name": fake.hostname(),
            "location": random.choice(["Data Center", "Office", "Cloud"]),
            "condition": random.choice(["New", "Used", "Deprecated"]),
            "manufacturer": random.choice(HARDWARE_MANUFACTURERS)
        }
    elif asset_type == "Software":
        return {
            "name": fake.company() + " App",
            "version": generate_semver(),  # Hier verwenden wir unsere eigene Funktion
            "license_type": random.choice(["Open-source", "Commercial", "Proprietary"]),
            "manufacturer": random.choice(SOFTWARE_MANUFACTURERS)
        }
    elif asset_type == "Human Resources":
        return {
            "name": fake.name(),
            "role": random.choice(["Admin", "User", "Consultant", "External"]),
            "access_level": random.choice(["Full Access", "Read Access", "Restricted"])
        }
    elif asset_type == "Services":
        return {
            "name": fake.company() + " Service",
            "availability": random.choice(["99.99%", "99.9%", "99.5%"]),
            "provider": random.choice(SERVICE_PROVIDERS),
            "manufacturer": random.choice(SERVICE_PROVIDERS)
        }
    elif asset_type == "Networks and Communications":
        return {
            "ip_address": generate_ip(),
            "bandwidth": random.choice(["100 Mbit/s", "1 Gbit/s", "10 Gbit/s"]),
            "protocol": random.choice(["TLS", "SSL", "IPsec", "WPA3"]),
            "manufacturer": random.choice(NETWORK_MANUFACTURERS)
        }
    elif asset_type == "Financial Resources":
        return {
            "name": "Budget " + fake.year(),
            "budget_type": random.choice(["Operational", "Capital Investment"]),
            "value": f"{random.randint(100000, 1000000)} EUR"
        }
    elif asset_type == "Reputation":
        return {
            "name": "Reputation of " + fake.company(),
            "public_perception": random.choice(["Positive", "Neutral", "Negative"]),
            "risk_level": random.choice(["High", "Medium", "Low"])
        }
    elif asset_type == "Documented Procedures":
        return {
            "name": random.choice(["Security Policy", "Procedure", "Guideline"]),
            "document_type": random.choice(["Security Policy", "Procedure", "Guideline"]),
            "last_reviewed": fake.date_this_decade()
        }

# Generiere eine Liste von Assets
def generate_assets(n, asset_type=None):
    assets = []
    for _ in range(n):
        if asset_type:
            assets.append({
                "asset_type": asset_type,
                "details": generate_asset(asset_type)
            })
        else:
            random_asset_type = random.choice(list(ASSET_TYPES.keys()))
            assets.append({
                "asset_type": random_asset_type,
                "details": generate_asset(random_asset_type)
            })
    return assets
