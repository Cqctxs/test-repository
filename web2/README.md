# "Compiler"

**allow a zip of the exec folder to be downloaded by the user, but replace the FLAG env variable in Dockerfile with wxmctf{dummy_flag}, server is needed to host the program**

## Description
Come check out this python compiler I made! Just don't look too far into it...

## Flag
`wxmctf{ok4Y_M4y8e_I_5K1mpED_@_bit}`

## Solution
Upon further inspection, we find that the "compiler" is just an exec statement, and looking at the Dockerfile, we can see that the flag is stored in an environment variable FLAG. As a result, we can just run 
```python
import os
print(os.environ['FLAG'])
```
to retrieve the flag.
