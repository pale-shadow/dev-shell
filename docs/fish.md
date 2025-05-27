
# place this in your fish path
# ~/.config/fish/config.fish

function fish_greeting
        if not type fortune > /dev/null 2>&1
                apt-get install fortune
        end
        if not type cowsay > /dev/null 2>&1
                apt-get install cowsay
        end
        fortune -a | cowsay -f bud-frogs
end

funcsave fish_greeting

