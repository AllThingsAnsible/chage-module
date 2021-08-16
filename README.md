ansible-chage-module

A full example playbook can be found in main.yml.

Example Playbook with options:


---
  - name: Test the module
    hosts: localhost
    become: yes
    tasks:
      - name: Test the chage module
        chage:
          name: user
          last_pass_change: True
          pass_expires: True
          set_amount_days: '100'
        no_log: True
        register: output
      - debug:
          msg: "{{ output }}"
