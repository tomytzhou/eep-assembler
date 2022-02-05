# eep-assembler
Assembler for EEP1 and EEP0 CPUs

## Overview
These python scripts can convert assembly mneumonics into machine code in a .ram file, which can be easily loaded into [ISSIE](https://github.com/tomcl/issie), removing the need to enter values into the ROM manually.

## How to use
1. Run the .py file. It will read from 'assembly.txt' and generate 'assembly.ram'
2. Place the .ram file into the same folder as the ISSIE project
3. In ISSIE create a new ROM, hover over 'Enter data later' and select 'assembly.ram'
4. Delete the old ROM and connect the new ROM.

## Notes
The EEP1 assembler currently only supports the EEP0 instruction set. 
