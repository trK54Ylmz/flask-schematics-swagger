from dataclasses import dataclass


@dataclass(frozen=True)
class Security:
    BASIC = 'basic'
    APIKEY = 'apiKey'
    OAUTH2 = 'oauth2'
