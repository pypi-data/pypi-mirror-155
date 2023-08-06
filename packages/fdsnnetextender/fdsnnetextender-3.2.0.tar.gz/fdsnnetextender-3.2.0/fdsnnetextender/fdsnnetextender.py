from datetime import date, datetime
from functools import lru_cache
from urllib.request import urlopen
import re
import logging
import json

class FdsnNetExtender():
    """
    Toolbox to manage the correspondance between a short network code and an extended network code.
    Correspondance is made using the metadata
    """
    def __init__(self, base_url="http://www.fdsn.org/ws/networks/1"):
        """
        param: base_url is the base url for getting metadata. Default is ws.
        """
        # we can guess that a network is temporary from this regex:
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.tempo_network_re = '^[0-9XYZ][0-9A-Z]$'
        self.base_url = base_url
        self.date_format = '%Y-%m-%d'

    @lru_cache(maxsize=1000)
    def extend(self, net, date_string):
        """
        Given a short code and a year
        Param date_string can be a year or a date string like 2022-01-01
        Returns the corresponding extended network code for temporary networks
        """
        extnet = net
        # Only extend temporary networks
        if re.match(self.tempo_network_re, net):
            # Normalize the start year from date_string
            try:
                # Can I cast it to an integer ? ie. is date_string just the year ?
                dateparam = date(year=int(date_string), month=1, day=1)
            except ValueError:
                self.logger.debug("Parameter %s is not a year. Trying to guess the date in iso format", date_string )
                try:
                    dateparam = datetime.strptime(date_string, self.date_format).date()
                except ValueError as err:
                    raise ValueError("date argument is not in format YYYY-MM-DD. Expected like 2022-01-01.") from err
            # Now that we have a start date :
            self.logger.debug("Trying to extend %s for %s", net, dateparam)
            found = False
            request = f"{self.base_url}/query?fdsn_code={net}"
            try:
                with urlopen(request) as metadata:
                    networks = {'networks': []}
                    if metadata.status == 200:
                        networks = json.loads(metadata.read().decode('utf-8'))
                    elif metadata.status == 204:
                        raise ValueError(f"No metadata for request {request}")
                    for n in networks['networks']:
                        logging.debug(net)
                        if dateparam >= datetime.strptime(n['start_date'], self.date_format).date() and dateparam <= datetime.strptime(n['end_date'], self.date_format).date():
                            extnet = n['fdsn_code'] + n['start_date'][0:4]
                            found = True
                            break
            except Exception as err:
                self.logger.error(err)
                raise err
            if not found:
                raise ValueError(f"No temporary network found for {net} at {date_string}")
        return extnet
