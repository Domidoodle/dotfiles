#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Environment Variables
export EDITOR=vim
export PAGER=vimpager

# power managment
alias slx='systemctl suspend'
alias shd='shutdown now'

# essentials
alias ls='ls --color=auto'
alias mv='mv -i'
alias rm='rm -i'
alias cls='clear'
alias vimp='vimpager'
alias clipboard='xclip -sel c'

# laptop
alias brightness='doas vim /sys/class/backlight/intel_backlight/brightness'

# colour tests
alias colours8='(x=`tput op` y=`printf %76s`;for i in {0..256};do o=00$i;echo -e
${o:${#o}-3:3} `tput setaf $i;tput setab $i`${y// /=}$x;done)'

# art stuff
alias vibe='cat /home/domidoodle/Art/ansi-art/brycewave.ans'
alias washere='cat /home/domidoodle/Art/ansi-art/domihere.ans'

# dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# silly aliases
alias math='qalc'

# aliases
alias matlab='matlab -nodesktop -nosplash'

# Other
PS1='\W \$ '
