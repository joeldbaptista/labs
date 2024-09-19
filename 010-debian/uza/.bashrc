[[ $- != *i* ]] && return

# Set vi mode
set -o vi
bind -m vi-command 'Control-l: clear-screen'
bind -m vi-insert 'Control-l: clear-screen'

# Alias
alias ls='ls --color=auto'
