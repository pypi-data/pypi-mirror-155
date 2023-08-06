from typing import List, Iterable, Type
from time import sleep
import acme.challenges
from acme.challenges import ChallengeResponse, Challenge
from certbot import interfaces
from certbot.achallenges import AnnotatedChallenge
from certbot.plugins import common
from certbot.display import util as display_util
from .rox_api import RoxApi


class Authenticator(common.Plugin, interfaces.Authenticator):
    description = "Obtain certificates using a DNS TXT record (if you are using rockenstein AG " \
                  "for DNS). "

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self._roxApi = RoxApi(self.conf('token'), self.conf('url'), not self.conf('ignore-ssl'))

    def prepare(self) -> None:
        return None

    @classmethod
    def add_parser_arguments(cls, add) -> None:
        super(Authenticator, cls).add_parser_arguments(
            add
        )
        add("token", help="Token for rockenstein API")
        add("url", help="URL for rockenstein API", default="https://api.rox.net")
        add("ignore-ssl", action="store_true", default=False)
        add('propagation-seconds',
            default=120,
            type=int,
            help='The number of seconds to wait for DNS to propagate before asking the ACME server '
                 'to verify the DNS record.')

    def more_info(self) -> str:
        return self.description

    def perform(self, achalls: List[AnnotatedChallenge]) -> List[ChallengeResponse]:
        responses = []
        for achall in achalls:
            domain = achall.domain
            validation_domain_name = achall.validation_domain_name(domain)
            validation = achall.validation(achall.account_key)

            # domains can be subdomains, eg. "abc.example.com" so we have to find out
            # the base domain name
            basedomain = self._roxApi.get_base_domain(domain)

            # make dns entry
            self._roxApi.add_txt_record(basedomain + '.',
                                        validation_domain_name + '.',
                                        validation)

            responses.append(achall.response(achall.account_key))

        # wait for DNS
        display_util.notify("Waiting %d seconds for DNS changes to propagate" %
                            self.conf('propagation-seconds'))
        sleep(self.conf('propagation-seconds'))

        return responses

    def cleanup(self, achalls: List[AnnotatedChallenge]) -> None:
        responses = []
        for achall in achalls:
            domain = achall.domain
            validation_domain_name = achall.validation_domain_name(domain)
            validation = achall.validation(achall.account_key)

            # domains can be subdomains, eg. "abc.example.com" so we have to find out
            # the base domain name
            basedomain = self._roxApi.get_base_domain(domain)

            # delete dns entry
            self._roxApi.del_txt_record(basedomain + '.',
                                        validation_domain_name + '.',
                                        validation)

            responses.append(achall.response(achall.account_key))

    def get_chall_pref(self, domain: str) -> Iterable[Type[Challenge]]:
        return [
            acme.challenges.DNS01
        ]
