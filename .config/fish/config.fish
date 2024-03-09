set -x EDITOR "helix"
set -x TERM "alacritty"
set -x JAVA_HOME "/usr/lib/jvm/java-19-openjdk"


# util
alias clipboard='xclip -sel c'
alias redshift='redshift -l 36:174'
alias ls='exa --color=always --group-directories-first'

# laptop
alias brightness='doas vim /sys/class/backlight/intel_backlight/brightness'

# dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# programming
alias gcc='gcc -Wall'
alias ssh-it='eval "$(ssh-agent -c)"'
alias matlab='matlab -nodesktop -nosplash'
alias capslockfix="xmodmap -e 'clear Lock' -e 'keycode 0x42 = Escape'"

# text editor
alias hx='helix'

function typstc 
    # echo 'typst compile --root . $argv.typ $argv.pdf'
    command typst compile --root . $argv.typ $argv.pdf
    command zathura $argv.pdf &
    command typst watch --root . $argv.typ $argv.pdf
end

if status is-interactive
    # Commands to run in interactive sessions can go here

    starship init fish | source
    zoxide init fish | source
end
