// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/6/max/MaxL.asm

// Symbol-less version of the Max.asm program.
// Designed for testing the basic version of the assembler.

   // D = R0 - R1

   @R0

   D=M

   @R1

   D=D-M

   // If (D > 0) goto ITSR0

   @ITSR0

   D;JGT

   // Its R1

   @R1

   D=M

   @SET_RESULT

   0;JMP

(ITSR0)

   @R0

   D=M

(SET_RESULT)

   @R2

   M=D

(END)

   @END

   0;JMP
