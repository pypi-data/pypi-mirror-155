rootpw = "nothing"
acess = 0

unvar= ""

def setrootpw(customrootpw):
    global rootpw
    rootpw = customrootpw
    return customrootpw

def acess_fn1():
    global acess
    acess = 1

def acess_fn():
    global acess
    acess = 2
pwn = 0

def rootlogin():
    rootpass = input("root password:")

    if rootpass == rootpw: {
        acess_fn()
    }
    return "sucessful"


userlist = [
    "user",
    "user1",
    "user2"
]
passlist = [
    "user@1234"
    "user1@9876",
    "user2@321"
]
def pwn_setup():
    global pwn
    pwn = userlist.index(unvar)
def login(un,up):
    pwn = 0
    global unvar
    unvar = un
    global userlist, passlist
    for un in userlist : {
        pwn_setup()
    }
    if up == passlist[pwn]:{
        acess_fn1()
    }

def useradd():
    global userlist,passlist
    uname = input("username to be added")
    upass = input("password of the new user that to be added")
    if acess < 2 :{
        print("you are not root")
    }
    elif acess == 2:{
        userlist.append(uname),
        passlist.append(upass)
    }
