How to run ansible playbook:



$ ansible-playbook web.yml -e 'uservar=root'

## run init tags:
$ ansible-playbook web.yml -e 'uservar=root' --tags init

