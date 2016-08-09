@r=BasicOilProcessing “Basic Oil Processing“
10oil -> 3heavyoil + 3lightoil + 4petroleumgas
rateOil : rateOil=0.2

@r=AdvancedOilProcessing “Advanced Oil Processing“
20oil -> 2heavyoil + 9lightoil + 11petroleumgas
rateOil : rateOil=0.2

@r=LightOilSolidFuelCrafting “Light Oil to Solid Fuel Crafting“
1lightoil -> solidfuel
rateOil : rateOil=0.333333

@r=HeavyOilSolidFuelCrafting “Heavy Oil to Solid Fuel Crafting“
2heavyoil-> solidfuel
rateOil : rateOil=0.333333

@r=PetroleumSolidFuelCrafting “Petroleum Gas to Solid Fuel Crafting“
2petroleumgas-> solidfuel
rateOil : rateOil=0.333333

@r=LubricantCrafting “Lubricant Crafting“
heavyoil-> lubricant
rateOil : rateOil=1

@r=HeavyOilCracking “Heavy Oil Cracking“
4heavyoil + 3water-> 3lightoil
rateOil : rateOil=0.2

@r=LightOilCracking “Light Oil Cracking“
3lightoil + 3water-> 3petroleumgas
rateOil : rateOil=0.2

@r=FirearmMagazineCrafting “Firearm Magazine Crafting“
2ironplate-> firearmmagazine
rateFirearm: rateFirearm=0.5

@r=GunTurretCrafting “Gun Turret Crafting“
20ironplate + 10copperplate + 10irongearwheel -> gunturret
rateTurret: rateTurret=0.1

@r=LaserTurretCrafting “Laser Turret Crafting“
20steelplate + 20electroniccircuit + 12battery -> laserturret
rateLaserTurret: rateLaserTurret=0.05

@r=BasicBeaconCrafting “Basic Beacon Crafting“
20electroniccircuit + 20advancedcircuit + 20steelplate +10coppercable -> basicbeacon
rateBeacon : rateBeacon = 0.06666666666

@r=EmptyBarrelCrafting “Empty Barrel Crafting“
steelplate -> emptybarrel
rateBarrel : rateBarrel = 1

@r=StoneWallCrafting “Stone Wall Crafting”
stonebrick -> stonewall
rateWall : rateWall = 2

@r=StoneBrickCrafting “Stone Brick Crafting”
2stone -> stonebrick
rateStone: rateStone = 0.28571428

@r=TransportBeltCrafting “Transport Belt Crafting”
iron plate + irongearwheel -> fastsplitter
rateBelt : rateBelt = 2

@r=UndergroundBeltCrafting “Underground Belt Crafting”
5transportbelt + 10ironplate -> undergroundbelt
rateWall : rateWall = 0.1

@r=BasicSplitterCrafting “Basic Splitter Crafting”
5electroniccircuit + 5ironplate + 4transportbelt -> basicsplitter
rateBasicSplitter : rateBasicSplitter = 1

@r=FastSplitterCrafting “Fast Splitter Crafting”
splitter + 10irongearwheel + 10electroniccircuit -> fastsplitter
rateFastSplitter : rateFastSplitter = 0.5

@r=ExpressSplitterCrafting “Express Splitter Crafting”
fastsplitter + 10irongearwheel + 10advancedcircuit + 8lubricant -> fastsplitter
rateFastSplitter : rateFastSplitter = 0.5
