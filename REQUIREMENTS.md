Copy all existing gaming/gaming related rules to the 
new Parent device group, “Gaming”.

 

1. Criteria for Rules that need to be copied  to the “Gaming” Parent Device Group:
  * Rules that are member of the following Source and/or Destination Zones
    * Any
    * GAMING
    * GAME_CLIENTS

  * AND Have the following target devices
    * Any
    * Data Center

Search/filter criteria:  

((from/member eq 'any') OR (to/member eq 'any') OR (from/member eq 'GAMING') OR (to/member eq 'GAMING') OR (from/member eq 'GAME_CLIENTS') OR (to/member eq 'GAME_CLIENTS'))  and ((target/devices eq 'any') or (target/devices/entry/@name eq '007901003306') )

 

2. During copy to Device Group “Gaming”, strip any targets from what is 
written to the new Device Group “Gaming”.  (Do not alter the source 
Device Group rule in terms of targeting)

3. Firewall Rules need to be copied from the following location to the
Device Group “Gaming” and placed under Pre Rules

* On_Premises / Pre Rules
* Cosmo Data Center / Post Rules – These rules should be placed right
  after the copied Pre-Rules from above.

4. Other Requirements:

* Name for all rules copied to Device Group “Gaming” must be adjusted to 
  include “-G” at the end of the name.
* Any rule Name that is longer than 63 characters much be shorten to 60
  character before adding “-G” to the end of the name (New names should
  not exceed 62 characters total)
* Add tag “Game Legacy” to both the original and copied rules. 
* TCOLV will create the “Game Legacy” Shared Tag prior to the implementation of the script.  (Shared Tag does not need to be created as part of this script)
* Each script run should have a maximum limit of 50 rules

Other recommendations/suggestions:

* Depending on PAN Consultant availability, TCOLV offers the following suggestion for the implementation of this change:

* Option 1 - Completed all the changes at the same time next Wednesday, 04/07/2021
* Option 2 –

§  PAN to build out a script to identify and tag all the rules that meet above Criteria as soon as possible and prior to next Wednesday, 04/07/2021

§  On Wednesday, 04/07/2021 – Move all the identified/tagged rules to the Device Group “Gaming” and complete remaining tasks (Remove Targets, Rename, etc.)

Timeline for the next steps and mentioned below: 

* New Script available for review and approval by Tuesday 04/06/2021
* Deploy Script to move the rules based on the requirement on Wednesday 04/07/2021

