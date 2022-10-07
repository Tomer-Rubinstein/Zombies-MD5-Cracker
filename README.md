# Zombies-MD5-Cracker
> zCracker uses a [network of zombies](https://en.wikipedia.org/wiki/Botnet) to divide the bruteforcing work of traditional MD5 cracking (wordlist-based) between different CPUs.

```
$ python zCracker.py --help

usage: zCracker.py [-h] [--port PORT] [--connlim CONNLIM] --hash HASH --wordlist WORDLIST

zCracker is a multi-client threaded server software to decode a MD5 hash using a botnet.
Source: https://github.com/Tomer-Rubinstein/Zombies-MD5-Cracker

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Port to bind the server to
  --connlim CONNLIM    Limit the no. of zombies in the botnet.
  --hash HASH          Target MD5 Hash to decrypt.
  --wordlist WORDLIST  Path to a wordlist file with words seperated by newlines.
```