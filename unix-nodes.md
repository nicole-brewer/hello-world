

# UNIX

### Git authentication warning: cannot open display

`unset SSH_ASKPASS`
`git config —global user.email "my@email.com"`

### scp

Secure copy (remote file copy program) - scp copies files between hosts on a network. It uses ssh for data 
transfer, and uses the same authentication and provides the same security as ssh.

Transfer to remote host:

```bash
scp /home/user/location/of/file username@host:/home/user/destination/directory/
```

Get files from remote host:

```bash
scp /home/user/destination/directory/ username@host:/home/user/location/of/file
```



### screen

[How is screen different than & for running commands in the background?](https://superuser.com/questions/488434/running-linux-commands-in-the-background-ampersand-or-screen)

Use the command `screen` to launch and `screen -r` to reattach.

Every other `screen` command begins with `Ctrl-a`.

| `Ctrl-a c`           | Create new window ([shell](https://kb.iu.edu/d/agvf))    |
| -------------------- | -------------------------------------------------------- |
| `Ctrl-a k`           | Kill the current window                                  |
| `Ctrl-a w`           | List all windows (the current window is marked with "*") |
| `Ctrl-a 0-9`         | Go to a window numbered 0-9                              |
| `Ctrl-a n`           | Go to the next window                                    |
| `Ctrl-a` `Ctrl-a `   | Toggle between the current and previous window           |
| `Ctrl-a [`           | Start copy mode                                          |
| `Ctrl-a ]`           | Paste copied text                                        |
| `Ctrl-a ?`           | Help (display a list of commands)                        |
| `Ctrl-a` `Ctrl-\`    | Quit `screen`                                            |
| `Ctrl-a D` (Shift-d) | Power detach and logout                                  |
| `Ctrl-a d`           | Detach but keep shell window open                        |



### iptables

sudo iptables -I INPUT -s 149.165.170.36 -p tcp --dport 8445 -j ACCEPT

-I is for --insert to add another rule to the INPUT chain
-s specifies that 149.165.170.36 is the incoming ip address
-p specifies that tcp is the protocol used
--dport specifies that 8445 is the port being connected to
and -j  or --jump specifies the target for that rule

So when this server (129...) attempts to connect over tcp to port 8445, the connection will be allowed.

## Fixing tabs in vim

Change settings in vim: 

```bash
set tabstop=4 shiftwidth=4 expandtab
```

Fix already existing tabs:

```bash
:retab
```