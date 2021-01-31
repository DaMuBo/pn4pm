# Welcome to Petrinets 4 Process Mining
### handling Process Lists with a simple small package V0.0.6.2

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
#### It's very easy to use the package. Just import the package
#### create your activity list with an activity, position of the activity, all direct previous activity ranges
#### call the Petrinet function with your list and create your outputs
from pn4pm_nano import petrinets as pn

list = [['Activity1',0,[-1]],['Activity2',1,[0]],['A....']]

petriobject = pn.Petrinet(list)
print(petriobject.out())
print(petriobject.cel_out())
print(petrionject.cel_out("YourActivityTable"))

#### For silencing the activities just give an empty string as name
['',0,[-1]]
In this case a transition is created but not returned in the frontend

# Other Stuff / Last Words

If you have some issues with the package or ideas what functionalities could be added,
feel free to contact me.

## Changes to Last Version
- internal fixes and optimization for gateway calculations [0.0.5.3] -> [0.0.6]
- multiple changes on the calculations - enabled the handling of loops [0.0.5 - 0.0.5.3]
- Added the handling of duplicated activities in the petrinet Input [0.0.4 - 0.0.5]
- Added Handling of 'Silent' Activitys and Bug Fix in the cel_out() function [0.0.3.2 -> 0.0.4]
- Bug Fix in function cel_out() [0.0.3.1 -> 0.0.3.2]
- Bug Fix after calling the class Petrinet the second time [0.0.1 -> 0.0.3]


# License Information
This Project is using the MIT License