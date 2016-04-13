# ipython_custom_timeit
```
In [1]: %install_ext https://raw.githubusercontent.com/hh-h/ipython_custom_timeit/master/custom_timeit.py
Installed custom_timeit.py. To use it, type:
  %load_ext custom_timeit

In [2]: %load_ext custom_timeit

In [3]: %timeit2 123
100000000 loops
   AVG of 3: 10.7 ns per loop
  BEST of 3: 10.7 ns per loop
 WORST of 3: 10.7 ns per loop

```

then in ipython_config.py
```
c.InteractiveShellApp.extensions = [
    'custom_timeit'
]
```
