# Stuff in examples/test/
AutoGenerate.py that generates 20 tests of following form  
that are used for example testing.
- **test{n}/test.in**
 two integer numbers, separated by newline (\n)
  > a  
  > b  

  `%d+\n%d+\n`
- **test{n}/test.out**
 results of addition (+), subtraction (-), and multiplication (*), separated by newline (\n)
  > a+b  
  > a-b  
  > a*b  

  `%d+\n%d+\n%d+\n`
