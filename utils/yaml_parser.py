#######################################################################################
## Author:          Phan Thanh Trung, Phan Ngoc Hung, Pham Nguyen Quang Khanh
##                  Tran Minh Quang, Dang Lam Tung
## Project:         [BGSV-HR-Chatbot]-Develop Chatbot for HR support
## Version:         4.0.0
## Maintainer:      Phan Ngoc Hung, Pham Nguyen Quang Khanh, Tran Minh Quang, Dang Lam Tung
## Status:          Work in Development and Maintenance
## Last modified:   March 17, 2022
## License:     
##    Copyright 2022, Robert Bosch Engineering & Business Solutions (RBVH)
## 
##    Licensed under the Apache License, Version 2.0 (the "License");
##    you may not use this file except in compliance with the License.
##    You may obtain a copy of the License at
## 
##        http://www.apache.org/licenses/LICENSE-2.0
##
##    Unless required by applicable law or agreed to in writing, software
##    distributed under the License is distributed on an "AS IS" BASIS,
##    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##    See the License for the specific language governing permissions and
##    limitations under the License.
#######################################################################################

import yaml

## define custom tag handler
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

def parse_cfg_file(path_to_file):

    # Add a joiner to concatenate string in yaml file
    yaml.add_constructor('!join', join)

    try:
        cfg_file = open(path_to_file,'r')
        cfg = yaml.load(cfg_file, yaml.FullLoader)
        
        # # Convert list() into tuple() for cbox configs
        # cfg_cbox_checker = cfg['detector']['cbox_detector']
        # for key in cfg_cbox_checker:
        #     if isinstance(cfg_cbox_checker[key], list):
        #         cfg_cbox_checker[key] = tuple(cfg_cbox_checker[key])

        return cfg

    except FileNotFoundError:
        print("Error occured in config file: Wrong file or Incorrect file path")

