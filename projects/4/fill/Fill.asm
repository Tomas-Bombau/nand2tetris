// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

@8192
D=A
@max
M=D

@0
D=A
@i
M=D

(LOOP)
@KBD
D=M
@CLEAR
D;JEQ

(FILL)
@max
D=M
@i
D=D-M
@LOOP
D;JLE

@i
D=M
@SCREEN
A=A+D
M=-1

@i
D=M
D=D+1
@i
M=D

@LOOP
0;JMP

(CLEAR)
@i
D=M
@SCREEN
A=A+D
M=0

@i
D=M
@LOOP
D;JLE

D=D-1
@i
M=D

@LOOP
0;JMP