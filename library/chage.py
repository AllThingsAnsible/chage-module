#!/usr/bin/python

# Copyright: (c) 2021, Daniel VonMoser <dgvonmoser@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: chage

This module makes working with the chage command a little easier.

version: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str

    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool

    last_pass_changed:
        description: Identify user and set option to True in order to determine the date of the last time the password was changed.
        required: false
        type: bool

    set_amount_days:
        description: Select username and set the amount of days the current password will expire in.
        required: false
        type: str

    pass_expires:
        description: Select user and set option to true in order to see the amount of days remaining until current password expires.
        required: false
        type: bool

extends_documentation_fragment:
    - chage

author:
    - Daniel VonMoser (DannyV99@github.git)
'''

EXAMPLES = r'''

- name: List the amount of days until password expires for any particular user.
  chage:
    name: user
    pass_expires: True

- name: List the last date of the last password change
  chage:
    name: user    
    last_pass_change: True

- name: Chnage the amount of days until password expires 
  chage:
    name: user
    set_amount_days: '100'
'''

RETURN = r'''

"msg": {
        "changed": false,
        "failed": false,
        "name": "user"
    }

"msg": {
        "changed": false,
        "failed": false,
        "name": "user",
        "you set the password to expire in": "100"
    }


"msg": {
        "Number of days until expiration": "90",
        "changed": false,
        "failed": false,
        "name": "user"
    }

'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False),
        last_pass_change=dict(type='bool', required=False, default=False),
        set_amount_days=dict(type='str', required=False),
        pass_expires=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)


    import subprocess
    import re
    import time
    import math

    chage=subprocess.run(['chage','-l',module.params['name']], stdout=subprocess.PIPE)
    results=chage.stdout.decode('utf-8')

    def chageFlag(entry):
      for item in results.split("\n"):
        if entry in item:
          length = len(item.split(" "))
          if (item.split(" ")[length-1]) == 'never':
            return "never"
          else:
            x = (re.search("\w*[A-Z][a-z]{1,3}.[0-9]{2},.[0-9]{1,4}",item))
            y = x.group(0).replace(",", "")
            z = y.split(" ")
            return y


    def myFunc(y):

      z = y.split(" ")
    
      if z[0] == 'Jan':
       month = '01'
      elif z[0] == 'Feb':
       month = '02'
      elif z[0] == 'Mar':
       month = '03'
      elif z[0] == 'Apr':
       month = '04'
      elif z[0] == 'May':
       month = '05'
      elif z[0] == 'Jun':
       month = '06'
      elif z[0] == 'Jul':
       month = '07'
      elif z[0] == 'Aug':
       month = '08'
      elif z[0] == 'Sep':
       month = '09'
      elif z[0] == 'Oct':
       month = '10'
      elif z[0] == 'Nov':
       month = '11'
      elif z[0] == 'Dec':
       month = '12'
      else:
       pass
       
      day = z[1]
      year = z[2]
  
      current_epoch_time = math.floor(time.time())
      date_time = str(day) + '.' + month + '.' + str(year)
      pattern = '%d.%m.%Y'
      epoch = int(time.mktime(time.strptime(date_time, pattern)))
      boobz = str(math.floor((epoch-current_epoch_time)/86400))

      return boobz


    if module.params['name']:
        result['name'] = module.params['name']

    if module.params['last_pass_change'] == True:
        result['name'] = module.params['name']
        result['Last password change'] = chageFlag('Last password change')

    if module.params['name'] and module.params['pass_expires']:
        
        result['name'] = module.params['name']
        result['Number of days until expiration'] = myFunc(chageFlag('Password expires'))

    if module.params['name'] and module.params['set_amount_days']:
        
        begin=subprocess.run(['chage','-M',module.params['set_amount_days'],module.params['name']], stdout=subprocess.PIPE)
        begin.stdout.decode('utf-8')
        
        result['name'] = module.params['name']
        result['you set the password to expire in'] = module.params['set_amount_days']


    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
