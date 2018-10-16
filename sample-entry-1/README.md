## Sample submission

This is a sample submission to the VDF contest, which includes source code with a classgroup implementation, and a dependency and program script.

The dependency.sh script is run by the server to install any dependencies that are necessary to complile and run the code. For example, here we are installing the GMP library as a dependency.

The program.sh is what is actually run to execute the VDF. It takes two arguments:
* A discriminant in hex
* The number of iterations, in decimal

The script should output the result of the VDF (but not the proof), encoded as a, b of the final classgroup element.

## Description

This implementation is written in C/C++ and it uses the GMP library for arithmetic and GCD. The algorithm implemented is the same one from the Binary Quadratic Forms paper linked in the main README.

The initial element is (2, 1, c), where c is calculated using the discriminant passed in. A form is represented by (a, b, c) and the discriminant. Here, reduction is performed after every composition/multiplication, and variables are reinitialized every time. Furthermore, this algorithm is not specific to squaring (i.e it does not require both input elements to multiply to be equal), so there are some possible optimizations to do there.

The GCD of three numbers is computed as GCD(c, GCD(a, b)).