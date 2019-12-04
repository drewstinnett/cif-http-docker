#!/usr/bin/env python3

import sys
import os
import requests
import subprocess

def main():
    user_mapping = {
        'hunter': {},
        'admin': {},
        'smrt': {},
        'httpd': {},
    }

    es_node = os.environ['CIF_STORE_NODES']

    for username, values in user_mapping.items():

        existing_count = requests.get("http://%s/tokens/_search?q=username=%s" % (es_node, username)).json()['hits']['total']
        if existing_count > 0:
            print("Already have a token for %s, skipping" % username)
        else:
            print("No token found for %s, creating" % username)
            subprocess.check_call([
                "cif-store", "-d", "--store", "elasticsearch",
                "--nodes",es_node, "--token-groups", "everyone",
                "--token-create-%s" % user_mapping[username].get('user', username),
                "--token", os.environ['CIF_TOKEN_%s' % username.upper()]
            ])

    return 0

if __name__ == "__main__":
    sys.exit(main())
