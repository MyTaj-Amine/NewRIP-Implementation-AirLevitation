import os
import json
import rip
#from urllib import urlencode
#from urllib import urlopen
from xml.etree.ElementTree import parse
from HttpServer import HttpServer

CONFIG_DIR = 'Configuration'
CONFIG_FILE = 'mygadget_conf_AirLevitation.json'
LICENSE_FILE = 'license.json'


def load_config(filename):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    config_dir = os.path.join(base_dir, CONFIG_DIR)
    file_ = os.path.join(config_dir, filename)
    with open(file_) as fp:
        content = json.load(fp)
    return content


def check_license(license):
    licenseid = license['License']['ID']
    licensenumber = license['License']['Number']
    encoded_args = urlencode({'sarlabId': licenseid, 'license': licensenumber})
    response = urlopen('https://irs.nebsyst.com/registrations/checklicense?' + encoded_args)
    response_xml = parse(response)
    licenses = 0
    licenses += int(response_xml.findtext('lite')) + int(response_xml.findtext('full'))
    return 1


if __name__ == "__main__":
    # Just in case
    HttpServer().exit()
    try:
        # Check license with IRS:
        #conf = load_config(LICENSE_FILE)
        #licenses = check_license(conf)
        licenses = 1
        if licenses > 0:
            try:
                # Read config file and start the server and experience
                config = load_config(CONFIG_FILE)
                impl_module = config['control']['impl_module']
                impl_name = config['control'].get('impl_name', impl_module)
                RIPImpl = getattr(rip, impl_module)
                RIPControl = getattr(RIPImpl, impl_name)
                info = config['control']['info']
                control = RIPControl(info)
                HttpServer(
                    host=config['server']['host'],
                    port=config['server']['port'],
                    control=control
                ).start(enable_ssl=False)
            except Exception as e:
                print('Error: could not load control. Please, check mygadget json configuration file.')
                print(e)
                HttpServer().exit()
        else:
            print('Error: license number/id in the license file could not be validated.')
    except:
        print('Error: could not open license file. Make sure the license.json file exists in the Configuration folder.')
