# manual
Python interfaces to system calls

To install:	```pip install manual```


# Examples

Write some "instructions" for someone with some placeholders like so:

```python
template = """
git checkout {main_branch}
git pull
git checkout {to_merge_branch}
git merge {main_branch}
git push
"""
```

Then just make a function like this:

```python
ri = mk_command_runner(template)
```

Then `ri` is a function with a nice signature with arguments to control the 
placeholders. 

```python
from inspect import signature
assert str(signature(ri)) == '(main_branch, to_merge_branch, *, _dry_run=False)'
```

If you call the function, it will run the commands one by one, printing 
the command it's about the run and then the output of the run.
The `_dry_run` allows one to just do the command prints without actually running 
the commands:

```python
print(ri('master', 'fixing_something', _dry_run=True))
```

```
(1/5)$ git checkout master

(2/5)$ git pull

(3/5)$ git checkout fixing_something

(4/5)$ git merge master

(5/5)$ git push
```

Note that you can also specify your commands as a list, 
and also ask that the commands be run one by one, asking the user to 
type any key to continue at every step:

```python
pwd_and_ls = mk_command_runner(["pwd", "ls -l"], step_by_step=True)
pwd_and_ls()
```

```
(1/2)$ pwd
/Users/Thor.Whalen/Dropbox/dev/p3/proj/t/manual

TYPE ANY KEY TO CONTINUE

(2/2)$ ls -l
total 48
-rw-r--r--@ 1 Thor.Whalen  staff  11357 Jun 15 21:00 LICENSE
-rw-r--r--@ 1 Thor.Whalen  staff   1040 Jun 15 21:13 README.md
drwxr-xr-x@ 9 Thor.Whalen  staff    288 Jun 15 21:00 docsrc
drwxr-xr-x@ 5 Thor.Whalen  staff    160 Jun 15 21:04 manual
-rw-r--r--@ 1 Thor.Whalen  staff    422 Jun 15 21:04 setup.cfg
-rw-r--r--@ 1 Thor.Whalen  staff     91 Jun 15 21:00 setup.py
```

# Where this is going

How many times do we write instructions for others, or ask others for us.
Or perhaps we're even organized enough to have a little file where 
we put our little how-to recipes, commenting them with natural language
so we can understand what the steps are, and simply be able to 
find those instructions when the time comes.

And then we go through those commands one by one, making sure we replace the 
right part of the instructions with the right values for our context,
maybe trying to read the comments, so we know what we're doing. 

Really though, we no extra effort but following some convention to 
make our instructions parsable, 
we can make our instructions, well, executable.

So instead of this:

```
git checkout {your_main_branch}
git pull
git checkout {your_branch}
git merge {your_main_branch}
# Now resolve conflics and press any key when ready for the next step
git commit -m {your_commit_message}
git push
```

just being that, we can take it as a DSL that will also give us:
- A function that does it all
- A function that will actually guide the user through the steps, 
explaining what's happening etc. (so also educational)

This means that we can then REUSE something like a markdown document 
that explains recipes, installation instructions, etc. 
also as boilerplate-less utils.

