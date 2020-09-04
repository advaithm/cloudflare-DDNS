#!/usr/bin/python
import requests
import json
import yaml
import argparse
from sys import exit


def update(domain, zone_id, record_id, api_key):
    dynamic_ip = requests.get("http://ip.42.pl/raw").text
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {
        "type": "A",
        "name": f"{domain}",
        "content": f"{dynamic_ip}",
        "ttl": 1,
        "proxied": True,
    }
    data = json.dumps(data)
    response = requests.put(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        headers=headers,
        data=data,
    )
    response_status = response.json()["success"]
    if response_status:
        print("updated")
    else:
        print(
            "there was a error in the update the response may help debug it\n",
            response,
            "\n",
            response.json(),
        )


def ddns():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        record_id = settings["record_id"]
        f.close()
        update(domain, zone_id, record_id, api_key)


def get_record_id():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        f.close()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        headers=headers,
    )
    data = response.json()
    data = data["result"]
    for record in data:
        if record["zone_id"] == zone_id:
            record_id = record["id"]
            with open("settings.yml", "w") as f:
                data = {
                    "api_key": api_key,
                    "domain": domain,
                    "zone_id": zone_id,
                    "record_id": record_id,
                }
                data = yaml.dump(data)
                f.write(data)
                f.close()


parser = argparse.ArgumentParser()
parser.add_argument("--ddns", type=bool, help="update dns records")
x = parser.parse_args()
if x.ddns:
    ddns()
else:
    get_record_id()
    ddns()