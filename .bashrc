#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Environment Variables
export EDITOR=vim

# Aliases

# essentials
alias ls='ls --color=auto'
alias mv='mv -i'
alias rm='rm -i'
alias cls='clear'

# colour tests
alias colours8='(x=`tput op` y=`printf %76s`;for i in {0..256};do o=00$i;echo -e
${o:${#o}-3:3} `tput setaf $i;tput setab $i`${y// /=}$x;done)'

# dumb art stuff
alias vibe='cat /home/domidoodle/Art/ansi-art/brycewave.ans'
alias washere='cat /home/domidoodle/Art/ansi-art/domihere.ans'

# dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# Other
PS1='\W \$ '
