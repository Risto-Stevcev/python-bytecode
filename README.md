# Python Byte-code Compiler

This app provides the ability to convert Python files into their **.pyc** files. Python **.pyc** files are *compiled* Python files, compiled into byte-code. If you ever wondered why sometimes Python generates these and the ``__pycache__`` folder, it's for performance reasons.  

The purpose of this exercise is to expose the internals of Python so that some people might experiment with writing their own language that runs on the Python virtual machine. A lot of the more recent languages such as Scala and Clojure run on the JVM. They've become popular because they immediately come with *batteries included* so-to-speak, because they're capable of importing all existing Java libraries. Python is arguably a cleaner language than Java, and so it would be advantageous to have a functional language, for example, that integrates well with Python--a language that follows Pythonic principles (see ``import this``). I plan on working on such a language, but I'd like to open the flood gates for everyone else as well.  


## Generating byte-code (*.pyc files*)  

The structure of **.pyc** files is as follows:  

1. *4 bytes*: **Magic number**  
2. *4 bytes*: **Timestamp**  
3. *4 bytes*: **Padding**  
4. *N bytes*: **Marshalled code object**  

You can get each segment to create a **.pyc** file in the following ways:  

1. The **magic number** corresponds to the required Python version. You can get this number through the **imp** module:  
``import imp``  
``magic_number = imp.get_magic()``  
2. The **timestamp** corresponds to the time it was created. If there's a corresponding **.py** file, it checks this timestamp with that file to see if they match. Otherwise it's irrelevant if the .pyc file is on its own. You can get this number by using the **time** and **struct** modules:  
``import struct, time``  
``timestamp = struct.pack('i', int(time.time()))``  
3. The **padding** is just padding before the code object, basically 4-byte sequence of 0's. This padding seems to only be in Python 3, so **omit it for Python 2**. Sometimes the first byte has some value, but it doesn't seem relevant. You can just use this bytestring:  
``b'A\x00\x00\x00'``  
4. The **code object** is a marshalled python code object. You can use the ``compile`` command to compile a segment of python code into a code object to test this out initially. The command signature is ``compile(code_segment, 'file_name', 'exec')``. You need to make sure that ``file_name`` corresponds to the filename you are writing the **.pyc** file into. Here's a simple example:    
``import marshal``  
``filename = 'addnum.py'``  
``code_segment = 'a = 123 + 321\nprint(a)'``  
``code = compile(code_segment, filename, 'exec')``    
``marshalled_code_object = marshal.dumps(code)``  


You can put it all together like this:  

    # write to addnum.pyc  
    with open(filename + 'c', 'wb') as f:  
        f.write(magic_number)  
        f.write(timestamp)  
        f.write(padding)  
        f.write(marshalled_code_object)  
        
And then you can test it out like a regular python file, it should work!  

    $ python addnum.pyc  
    444  

You can test out the bytecode compiler by running ``python bytecode.py [.py file]`` or ``pybytecode [.py file]`` from the command-line.  


## Writing code objects

You can write Python objects by importing the CodeType type like this: ``from type import CodeType``. You can view the help for the required parameters (``help(CodeType)``), and there's quite a bit of documentation online about the different portions of the python code object. [Alberto's StackOverflow post](http://stackoverflow.com/questions/16064409/how-to-create-a-code-object-in-python) provides a fairly decent overview of each one. I've included his code as part of ``codegen.py``. See this README's Resources section for opcodes so you can start writing a byte-code compiler for your own language that can be read using the Python virtual machine!  

You can test out the code generator by running ``python codegen.py`` or ``pycodegen`` from the command-line.


## Resources

* Python bytecode instructions and their descriptions can be found in the **dis** module [documentation](https://docs.python.org/2/library/dis.html#python-bytecode-instructions).  

* You can view all of the python opcodes from Python's source code in the [Include/opcode.h](https://github.com/python/cpython/blob/master/Include/opcode.h).  

* If in doubt, create a code object of the type of segment you need using ``code = compile(code_segment, my_file_name, 'exec')`` and then disassembling it using ``dis.dis(code)`` and then creating the bytecode by translating to the opcodes and the params that go with it (see codegen.py and opcode.h).  

* Though both of these aren't being maintained anymore, you might want to check out [PEAK](http://peak.telecommunity.com/DevCenter/BytecodeAssembler) and [Byteplay](http://code.google.com/p/byteplay/) for bytecode assembly.
