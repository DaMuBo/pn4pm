# Welcome to Petrinets 4 Process Mining
### handling Process Lists with a simple small package V0.0.3

# Content:
- Author Information
- Description
- Classes
- Usage / Examples
- Other Stuff / Last Words
- License Information

# Author Information
- Name: Daniel Muller
- Website: http://damu-analytics.de

# Description
The purpose of this package is it to offer an easy way
to create a petrinet, you can use for process mining, without having a full PNML file.
All you need is a simple list of your process steps, the number of your step and the number 
of all Previous Steps.

### This is just the first Version of the Package. I will try to develop more possible outputs when i got time.

# Classes
The package offers the following classes:
- Petrinet(labels,[places, transitions, edges, inc_gateways, exc_gateways, parall_gateways])
  - output([tablename])
  - cel_out([tablename])
  
# Usage / Examples  


# Other Stuff / Last Words

If you have some issues with the package or ideas what functionalities could be added,
feel free to contact me.

## Changes to Last Version
- Bug Fix in function cel_out() [0.0.3.1 -> 0.0.3.2]
- Bug Fix after calling the class Petrinet the second time [0.0.1 -> 0.0.3]


# License Information
This Project is using the MIT License