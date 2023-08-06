import os

base_path = os.path.join(os.path.dirname(__file__), 'Tor')
tor_path = os.path.join(base_path, 'tor.exe')
tor_geo_ip_file_path = os.path.join(base_path, 'Data/geoip')
tor_geo_ipv6_file_path = os.path.join(base_path, 'Data/geoip6')