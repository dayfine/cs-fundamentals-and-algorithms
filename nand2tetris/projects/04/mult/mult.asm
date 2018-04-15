// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// m = R0
// n = R1
// product = 0

// LOOP:
//   if n == 0 goto STOP
//   product += m
//   n -= 1
//   goto LOOP
// STOP:
//   R2 = product

// declartion variables: m * n = product
@R0
D=M

@m
M=D

@R1
D=M

@n
M=D

@product
M=0

(LOOP)
  @n
  D=M
  @STOP
  D;JEQ // check n == 0

  @product
  D=M
  @m
  D=D+M
  @product
  M=D
  @n
  M=M-1
  @LOOP
  0;JMP

(STOP)
  @product
  D=M
  @R2
  M=D
  @product
  M=0 // clean up afterwards

(END)
  @END
  0;JMP
