## Sample submission

This is a sample submission to the VDF contest for track 1, which includes source code with a classgroup implementation, and install and run scripts.

The install.sh script is run by the server to install any dependencies, and/or compile the code. For example, here we are installing the GMP library as a dependency.

The run.sh file is what executed to run the VDF. It takes two arguments:
* A discriminant in hex
* The number of iterations, in decimal

```
sh ./dependencies.sh
sh ./program.sh -0xdc2a335cd2b355c99d3d8d92850122b3d8fe20d0f5360e7aaaecb448960d57bcddfee12a229bbd8d370feda5a17466fc725158ebb78a2a7d37d0a226d89b54434db9c3be9a9bb6ba2c2cd079221d873a17933ceb81a37b0665b9b7e247e8df66bdd45eb15ada12326db01e26c861adf0233666c01dec92bbb547df7369aed3b1fbdff867cfc670511cc270964fbd98e5c55fbe0947ac2b9803acbfd935f3abb8d9be6f938aa4b4cc6203f53c928a979a2f18a1ff501b2587a93e95a428a107545e451f0ac6c7f520a7e99bf77336b1659a2cb3dd1b60e0c6fcfffc05f74cfa763a1d0af7de9994b6e35a9682c4543ae991b3a39839230ef84dae63e88d90f457 10000
```

The script should output the result of the VDF (but not the proof), encoded as a, b of the final classgroup element.

## Description

This implementation is written in C/C++ and it uses the GMP library for arithmetic and GCD. The algorithm implemented is the same one from the Binary Quadratic Forms paper linked in the main README.

The initial element is (2, 1, c), where c is calculated using the discriminant passed in. A form is represented by (a, b, c) and the discriminant. Here, reduction is performed after every composition/multiplication.
