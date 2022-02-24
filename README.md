# eep-assembler
Assembler for EEP1 and EEP0 CPUs

## Overview
These python scripts can convert assembly mneumonics into machine code in a .ram file, which can be easily loaded into [ISSIE](https://github.com/tomcl/issie), removing the need to enter values into the ROM manually.

## How to use
1. Run the .py file. It will read from 'assembly.txt' and generate 'assembly.ram'
2. Place the .ram file into the same folder as the ISSIE project
3. In ISSIE create a new ROM, hover over 'Enter data later' and select 'assembly.ram'
4. Delete the old ROM and connect the new ROM.

## Version History

### v1.2
* Added support for symbolic addresses for jumps (same syntax as the ones in class 5)
#### Example:
| Address | Assembly       | Code   |
| ------- | -------------- | ------ |
| 0x0     | Start: JMP END | 0xc007 |
| ...     | ...            |  ...   |
| 0x7     | END: JNE Start | 0xc200 |
* Minor bug fixes


### v1.1
* Now supports the entire EEP1 instruction set
* Added some basic error detection
* Support for bracketed addresses and 0 as an unused line
### v1.0
* The EEP1 assembler currently only supports the EEP0 instruction set
