
import requests

from os import environ
from socket import AF_INET, SOCK_DGRAM, socket, gethostbyname

from construct import Int8ub, PaddedString, Struct, VarInt
from shodan.cli.helpers import get_api_key

# Configure logging if the end-user wants to debug potential issues w/ Chrono
import logging
log = logging.getLogger("chrono")
log.addHandler(logging.NullHandler())


DATA_REQUEST = Struct(
    "api_version" / Int8ub,
    "timeseries_id" / PaddedString(16, "ascii"),
    "value" / VarInt,
)
COLLECTOR_HOSTNAME = "collector.chrono.shodan.io"
COLLECTOR_PORT = 443


class progress(object):
    def __init__(self, title: str, total: int = -1, api_key: str = None):
        self.collector_ip = None
        self.ts = None
        self.title = title
        self.total = total
        self.processed = 0
        self.sock = socket(SOCK_DGRAM, AF_INET)

        # Use the provided API key if the user gives it
        if api_key:
            self.api_key = api_key
        else:
            # See if we can grab the Shodan API key from the environment or other locations
            if "SHODAN_API_KEY" in environ:
                self.api_key = environ["SHODAN_API_KEY"]
            else:
                try:
                    self.api_key = get_api_key()
                except Exception:
                    pass

        # Error out if we don't have an API key
        if not self.api_key:
            log.critical('API key not found. Specify the Shodan API key in the "api_key" parameter.')

    def __enter__(self) -> "progress":
        try:
            self.ts = requests.post(
                f"https://chrono.shodan.io/api/timeseries?key={self.api_key}",
                {
                    "title": self.title,
                    "total": self.total,
                },
            ).json()

            # Lookup the IP for the collector once
            self.collector_ip = gethostbyname(COLLECTOR_HOSTNAME)
        except Exception:
            pass
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.ts:
            try:
                requests.put(f'https://chrono.shodan.io/api/timeseries/{self.ts["id"]}/done/{self.processed}?key={self.api_key}')
            except Exception:
                pass

    def update(self, value: int = 1):
        if self.ts and self.collector_ip:
            data = DATA_REQUEST.build({"api_version": 1, "timeseries_id": self.ts["id"], "value": value})
            self.sock.sendto(data, (self.collector_ip, COLLECTOR_PORT))

        # Keep track of how many records have been processed if we know the total
        # This way we can tell the API at the end how many records were processed
        # according to the client in case the Chrono collector didn't get all the messages.
        if self.total > 0:
            self.processed += value
