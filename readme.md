
NOVELTIES
=========

* New Operators: % != \
* New Builtins: random randint strlen getchar run \
* New Error System \
* Jumping Backward Works ( -n => ignores n lines backward and starts running n+1 line ) \
* Recursion Works 

DOCUMENTATION
=============

**!!! no comments yet !!!**

Variable Types 
--------------

 INT FLOAT STR BOOL NULL

Available Binary Operators 
--------------------------

 \+ - * / // ** %

Available Comparison Operators
------------------------------

 == < > <= >= !=

Available Builtins Procedures
-----------------------------

write(object: ANY) > void 
  - Prints the **`object`** in the console without a break line.

read() > STR 
  - Returns the user's input.

random() > FLOAT 
  - Returns a FLOAT between 0 and 1.

randint(start: INT, end: INT) > INT 
  - Returns an INT between **`start`** and **`end`**.

strlen(string: STR) > INT 
  - Returns the length of the **`string`**.

getchar(string: STR, index: INT) > STR 
  - Returns the **`index`** th char of the **`string`**.

run(cmd: STR) > void 
  - Runs the **`cmd`** in the console.

Instructions
------------

 load_const     : lc (constant)
  - Pushes the **`constant`** onto the STACK. 
 
 create_var     : cv (variable)
  - Create a variable with the name **`variable`** and set its value to NULL.

 load_var       : lv (variable)
  - Pushes the **`variable`** onto the STACK.

 store_var      : sv (variable)
  - Pops the STACK[-1] object and store it into the **`variable`**.

 binary_op      : bo (operator)
  - Pops the STACK[-1] and STACK[-2] objects and pushes the result
     of the Binary operation (with the **`operator`**) onto the STACK.

 compare_op     : co (operator)
  - Pops the STACK[-1] and STACK[-2] objects and pushes the result
     of the Boolean operation (with the **`operator`**) onto the STACK.

 jump_true      : jt (delta)
  - If STACK[-1] is true, increments the counter by **`delta`**,
     STACK[-1] is popped.

 jump_false     : jf (delta)
  - If STACK[-1] is false, increments the counter by **`delta`**,
     STACK[-1] is popped.

 jump_always    : ja (delta)
  - Increments the counter by **`delta`**.

 call_proc      : cp (proc)
  - Pops the n first argument (n is the number of arguments of the **`proc`**)
     and then uses them as arguments to call the **`proc`**.

 is_instance    : ii (type)
  - Pops STACK[-1] and checks if it's of the same type as **`type`**,
     and then pushes the result.

 transform_into : ti (type)
  - Transforms the STACK[-1] element into **`type`**.

 build_string   : bs (number)
  - Pops the STACK[-1] to STACK\[-**`number`**\] strings, and pushes the
     concatenated result.

 return         : rt (number)
  - Pops the STACK[-1] to STACK\[-**`number`**\] elements, and pushes them
     onto the PARENT_STACK.


Example :
---------

print obj:\
    lv obj\
    cp write\
    lc '\n'\
    cp write\
    rt 0

input string:\
    lv string\
    lc NULL\
    co ==\
    jt 2\
    lv string\
    cp write\
    cp read\
    rt 1

fac n:\
    lv n\
    lc 0\ 
    co ==\        
    jf 2\     
    lc 1\
    rt 1\
    lv n\
    lc 1\
    bo -\        
    cp fac\        
    lv n\        
    bo *\
    rt 1

main:\
    lc 'cls'\
    cp run\
    cv answer\
    lc 0\
    lc 10\
    cp randint\
    cp fac\
    sv answer\
    cv lives\
    lc 3\
    sv lives\
    lc 'You have '\
    lv lives\
    ti STR\
    lc ' lives left'\
    bs 3\
    cp print\
    lc 'Enter a number? '\
    cp input\
    ti INT\
    cp fac\
    lv answer\
    co ==\
    jf 3\
    lc 'Success!'\
    cp print\
    rt 0\
    lv lives\
    lc 1\
    bo -\
    sv lives\
    lv lives\
    lc 0\
    co ==\
    jf 6\
    lc 'You noob, the right answer was '\
    lv answer\
    ti STR\
    bs 2\
    cp print\
    rt 0\
    lc 'cls'\
    cp run\
    lc 'This is not it, you have '\
    lv lives\
    ti STR\
    lc ' lives left'\
    bs 3\
    cp print\
    ja -31\
    rt 0