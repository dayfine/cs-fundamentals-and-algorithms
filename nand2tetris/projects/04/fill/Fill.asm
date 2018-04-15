// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)
@SCREEN
D=A
@addr
M=D // addr = 16384
@i
M=0 // counter
@color
M=0 // default to clear

@KBD
D=M
@FILL
D;JEQ // jump if D==0, i.e. no key pressed
@color
M=-1

(FILL)
  @i
  D=M
  @256
  D=A-D // check row num
  @START
  D;JEQ

  @j
  M=0 //inner counter
  (LOOP)
    @j
    D=M
    @32
    D=A-D // cols compared to 32
    @ENDLOOP
    D;JEQ

    @color
    D=M
    @addr
    A=M
    M=D // fill!

    @j
    M=M+1
    @addr
    M=M+1
    @LOOP
    0;JMP
  (ENDLOOP)
    @i
    M=M+1
    @FILL
    0;JMP
