#!/usr/bin/env python
import os
import requests

amberc_template = """
Name = {name}
Institution = {institution}
City =  {city}
State or Province = {state_or_province}
Country = {country}
"""

AMBERTOOLS_VERSION='16'
# REGISTRATION_TEMPLATE = "http://ambermd.org/cgi-bin/AmberTools{version}-get.pl?Conda=true&&Name={name}&Institution={institution}&City={city}&State={state_or_province}&Country={country}"
REGISTRATION_TEMPLATE = "http://localhost:8000/conda/registration/name/{name}/institution/{institution}"
required_fields = ['name', 'institution', 'city', 'state_or_province', 'country']

def main():
    base = '.amberrc'
    home = os.getenv('HOME', '')
    
    user_dict = {'name': '', 'institution': '',
                 'city': '', 'state_or_province': '',
                  'country': ''}
    interactive = True
    print('-'*100)
    print("Looking for $HOME/.amberrc or .amberrc registration file\n")
    if os.path.exists('.amberrc'):
        amberrc_file = base
        interactive = False 
    elif os.path.exists(os.path.join(home, base)):
        amberrc_file = os.path.join(home, base)
        interactive = False 
    else:
        print("Can not find registration file")
        print("We are asking users to fill out the simple form below, \n"
              "so that we can justify our existence by having a record of who is using the code")
        print('-'*100)
        print("Please enter your info")
        while not user_dict['name']:
            value = input("Please put your name here: ")
            user_dict['name'] = value
        while not user_dict['institution']:
            value = input("Please put your institution here: ")
            user_dict['institution'] = value
        while not user_dict['city']:
            value = input("Please put your city here: ")
            user_dict['city'] = value
        while not user_dict['state_or_province']:
            value = input("Please put your state or province here: ")
            user_dict['state_or_province'] = value
        while not user_dict['country']:
            value = input("Please put your country here: ")
            user_dict['country'] = value
        print("Note: You can avoid interactive registration by making $HOME/.amberrc file")
    if not interactive:
        print("Detecting user information from")
        print(os.path.abspath(amberrc_file))
        with open(amberrc_file) as fh: 
            for line in fh.readlines():
                key, val = line.split('=')
                if key and val.strip():
                    user_dict[key.strip().lower().replace(' ', '_')] = val.strip()
        for field in required_fields:
            assert field in user_dict, 'Must follow \n{}'.format(amberc_template)

    print("For the future deployment, please create $HOME/.amberrc file with below content")
    print(amberc_template.format(**user_dict))

    user_dict['version'] = AMBERTOOLS_VERSION
    user_info = REGISTRATION_TEMPLATE.format(**user_dict)
    # requests.post(user_info, timeout=10.)
    print("Enjoy. Happy computing")

if __name__ == '__main__':
    main()
