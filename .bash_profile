# this is required to set up oh my bash
#. ~/.bashrc
if [[ -f ~/.bashrc ]]; then
  source ~/.bashrc
fi

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/usr/local/share/google-cloud-sdk/path.bash.inc' ]; then . '/usr/local/share/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/usr/local/share/google-cloud-sdk/completion.bash.inc' ]; then . '/usr/local/share/google-cloud-sdk/completion.bash.inc'; fi

### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
export PATH="/Users/fdiaz/.rd/bin:$PATH"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)
