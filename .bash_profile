if [[ -f ~/.bashrc ]]; then
  source ~/.bashrc
fi

#!/bin/bash
if [ -e $HOME/.logon_script_done ]
then
  echo "No actions to do"
  else
  eval ssh-agent bash
  ssh-add ~/.ssh/id_ed25519
  kinit -f franklin

  # echo "First run of the script. Performing some actions" >> $HOME/run-once.txt
  touch $HOME/.logon_script_done
fi

### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
export PATH="/home/franklin/.rd/bin:$PATH"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)
