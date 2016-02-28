from colorama import init, Style, Fore, Back

def printmsg(line,file,msg,fg=Fore.GREEN,bg=Back.RED,style=Style.BRIGHT):
    init(autoreset=True)
    #Comment testing fast-forward-update to git
    print (fg + bg + style + '{line:0>5d} : {file:<20s} -> {msg}'.format(line=line, file=file, msg=msg))
