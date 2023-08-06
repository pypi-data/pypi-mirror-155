import requests
import json
from certbot import errors
from certbot.plugins import dns_common


class RoxApi:
    _token = ""
    _url = ""
    _verify_ssl = True

    def __init__(self, token, url, verify_ssl=True):
        self._token = token
        self._url = url
        self._verify_ssl = verify_ssl

    def _header(self):
        return {
            'X-AUTH-TOKEN': self._token
        }

    def _getTxtEntries(self, zonename, record_name):
        tmp = []
        response = requests.get(self._url + "/api/dns/zone/" + zonename,
                                headers=self._header(),
                                verify=self._verify_ssl)

        if 400 <= response.status_code <= 599:
            raise errors.PluginError(response.text)

        zone = json.loads(response.content)
        rrsets = zone["rrsets"]
        for rrset in rrsets:
            if rrset["name"] == record_name and rrset["type"] == "TXT":
                records = rrset["records"]
                for record in records:
                    tmp.append(record["content"].strip('"'))
        return tmp

    def add_txt_record(self, zonename, record_name, record_content, record_ttl=60):

        records = []
        entries = self._getTxtEntries(zonename, record_name)
        entries.append(record_content)
        for entry in entries:
            record = {
                "content": "\"" + entry + "\""
            }
            if not (record in records):
                records.append(record)

        record = {
            "name": record_name,
            "type": "TXT",
            "ttl": record_ttl,
            "changetype": "REPLACE",
            "records": records
        }

        response = requests.patch(self._url + "/api/dns/zone/" + zonename,
                                  data=json.dumps(record),
                                  verify=self._verify_ssl,
                                  headers=self._header())

        if 200 <= response.status_code < 300:
            return

        raise errors.PluginError('Error while creating dns records: {}.'.format(response.text))

    def del_txt_record(self, zonename, record_name, record_content, record_ttl=60):

        records = []
        entries = self._getTxtEntries(zonename, record_name)
        entries.append(record_content)
        for entry in entries:
            record = {
                "content": "\"" + entry + "\""
            }
            if not (record in records) and entry != record_content:
                records.append(record)

        if len(records) > 0:
            changetype = "REPLACE"
        else:
            changetype = "DELETE"

        record = {
            "name": record_name,
            "type": "TXT",
            "ttl": record_ttl,
            "changetype": changetype,
            "records": records
        }

        response = requests.patch(self._url + "/api/dns/zone/" + zonename,
                                  data=json.dumps(record),
                                  verify=self._verify_ssl,
                                  headers=self._header())

        if 200 <= response.status_code < 300:
            return

        raise errors.PluginError('Error removing dns records: {}.'.format(response.text))

    def get_base_domain(self, subdomain):
        subdomain_parts = dns_common.base_domain_name_guesses(subdomain)

        for subdomain_part in subdomain_parts:
            response = requests.get(self._url + "/api/dns/zone/" + subdomain_part + '.',
                                    headers=self._header(),
                                    verify=self._verify_ssl)

            if 500 <= response.status_code <= 599:
                raise errors.PluginError(response.text)

            if response.status_code == 200:
                return subdomain_part

        # should not occur
        return subdomain
