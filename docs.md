# Documentation

## How to run

```
python3.11 strict.py [file]
```

## How to use functions

Most functions operate by:
```
FUNCTION value variable
```

REPORT and SAY both print text, but say includes a newline at the end
```
REPORT "Hello world!"
```

PLACE sets a variable as a value
```
PLACE "1" VAR
PLACE VAR OTHER_VAR
PLACE [ARRAY][1] OTHER_OTHER_VAR
```

DOGEAR is a special function. There is no functions in this language, so good luck.
A dogear just keeps a record of the line the dogear is on so that the GOTO command
can loop back to it
```
DOGEAR THIS
GOTO THIS
```

IF compares to variables. If the comparison is true, go to next line
```
IF "hi" "hi"
SAY "TRUE"
IF EQ "hi" "hi"
SAY "TRUE"
IF GR 2 1
SAY "TRUE"
IF LS 1 2
SAY "TRUE"
IF NE "Alice" "Bob"
SAY "TRUE"
```

INC and DEC respectively increase or decrease a variable by 1
```
INC VAR
DEC VAR
```

ADD, SUB, MUL, DIV, MOD, ROUND all do their specific math function 
```
ADD 1 1 VAR_IS_2 # VAR_IS_2 = 1 + 1
SUB 5 1 VAR_IS_4
ROUND VAR
```

INPUT takes in user input and saves it to a variable
```
INPUT VAR
```

WAIT just sleeps for x amount of seconds
```
WAIT 5
```

INCLUDE is a doozy. It essentially adds whatever str file you give it
to the existing content and refreshes dogears
```
INCLUDE "random.str"
```

RETURN is a really cool way to go back to the previous GOTO. It stores previous locations too
```
RETURN
```

READ accepts a file and then turns it into an array by splitting it by newlines
```
READ "meow.txt" VAR
```

MAKE is also a doozy. It has subcommands
```
MAKE ARRAY NEW_ARRAY #makes an array called NEW_ARRAY
MAKE INT VAR #turns var into an int
MAKE VAR #makes a var called VAR and sets it equal to 0
```

ARRAY is another subcommand thing
```
ARRAY NEW_ARRAY ADD "Hello" #adds "Hello" to the array NEW_ARRAY
ARRAY NEW_ARRAY DEL 0 #deletes the first value of the array
ARRAY NEW_ARRAY SET "Hello" 0 #sets NEW_ARRAY[0] = "Hello"
ARRAY STRING_ARRAY LIST "Hello" # STRING_ARRAY = list("Hello")
```

LEN takes the length of a value and sets a var equal to it
```
LEN "JOHN" VAR
LEN VAR OTHER_VAR
```

DEL is a useful command to delete both vars and arrays
```
DEL VAR VAR_2 MEOW [array]
```

END just goes to next dogear or ends program. I'll add something later
```
END #ends program
END PROGRAM #ditto
END DOGEAR
```

## Variables, strings, and arrays
Strings are denoted through double quotes
```
"Howdy" "Howdy \"Bob\""
```
Variables are denoted by having no quotes
```
FOO BAR foo bar foo_bar
```
Arrays are denoted through this syntax:
```
[ARRAY][NUMBER_IN_ARRAY]
```

## Comments
Really almost anything after a command can be treated like a comment.
Which I think is really cool
```
SAY "Hi" /* comment */
SAY "Howdy" #comment
SAY "Whazzup" ;;comment
;;this is even a comment
even this is a comment
```
