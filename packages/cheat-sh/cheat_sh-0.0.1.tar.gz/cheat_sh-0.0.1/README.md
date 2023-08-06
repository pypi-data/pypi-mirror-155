# cheat_sh

the http://cheat.sh non official lightweight wrapper

# example

-   cheat_sh.ask()
```python
import cheat_sh
# ask question
print(cheat_sh.ask('reverse list in python'))
# you can provide the language
print(cheat_sh.ask('reverse list', 'python'))
# by default, colors are removed because it is not helpfull if you dont print it on a terminal
# but you can let them
print(cheat_sh.ask('echo', color=True))
```

-   cheat_sh.learn()
```python
import cheat_sh
# access cheat.sh/lang/:learn
print(cheat_sh.learn('python'))
# same as ask for the colors
print(cheat_sh.learn('python', color=True))
```

-   cheat_sh.get_base_url()
```python
>>> import cheat_sh
>>> cheat_sh.get_base_url()
http://cheat.sh/
```

-   cheat_sh.get_supported_language()
```python
>>> import cheat_sh
>>> # hard coded list
>>> cheat_sh.get_supported_language()
[...]
```
