# ipython_custom_timeit
```
In [1]: %install_ext https://raw.githubusercontent.com/hh-h/ipython_custom_timeit/master/custom_timeit.py
Installed custom_timeit.py. To use it, type:
  %load_ext custom_timeit

In [2]: %load_ext custom_timeit

In [3]: %timeit2 123
100000000 loops
   AVG of 3: 7.46 ns per loop
  BEST of 3: 7.32 ns per loop
 WORST of 3: 7.6 ns per loop
```
it also has feature to enable garbage collector
```
In [4]: %timeit2 -g 123
100000000 loops
   AVG of 3: 7.2 ns per loop
  BEST of 3: 7.18 ns per loop
 WORST of 3: 7.24 ns per loop
```

# autoload
then in ipython_config.py
```
c.InteractiveShellApp.extensions = [
    'custom_timeit'
]
```
