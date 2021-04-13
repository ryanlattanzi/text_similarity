import yaml
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def parse_config(config_path):
    config_file = open(config_path, 'r')
    return yaml.load(config_file, Loader=yaml.FullLoader)

def build_retry_strategy(retry_limit):
    retry_strategy = Retry(
        total = 5,
        status_forcelist = [429, 500, 502, 503, 504],
        method_whitelist = ['POST']
    )
    adapter = HTTPAdapter(max_retries = retry_strategy)
    http = requests.Session()
    http.mount('https://', adapter)
    http.mount('http://', adapter)
    return http