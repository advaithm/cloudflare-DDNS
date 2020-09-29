import yaml, logging
from cloudflare_ddns.internals import read_data,write_data

# nosec is for bandit as it flags input as a vunriblity siting python 2 issues
def gen_settings():
    """function to genrate the settings.yaml
    :return: None
    """
    api_key = input("input api key: ").strip().replace(" ", "")  # nosec
    domain = input("input root domain: ").strip().replace(" ", "")  # nosec
    zone_id = input("input zone id: ").strip().replace(" ", "")  # nosec
    check = int(input("input number of subdomains: "))  # nosec
    if check == 0:
        creds = {"api_key": api_key, "domain": domain, "zone_id": zone_id}
    else:
        subdomains = []
        for i in range(0, check):
            x = input("input subdomain: ").strip().replace(" ", "")  # nosec
            subdomains.append(x)
        creds = {
            "api_key": api_key,
            "domain": domain,
            "zone_id": zone_id,
            "subdoamins": subdomains,
        }
    x = yaml.dump(creds)
    logging.info(creds)
    with open(f"settings.yml", "w") as f:
        f.write(x)
        f.close()


def edit():
    data = read_data()
    print(f"1. {data['domain']}")
    n=2
    for domain in data["subdoamins"]:
        print(f"{n}. {domain}")
        n+=1
    edit_choice = input("enter number of record to edit: ")  # nosec
    if edit_choice ==1:
        data['domain']=input("update root domain: ")
    else:
        data['subdoamins'][int(edit_choice)-2]=input("update subdomain: ")
        write_data(data)