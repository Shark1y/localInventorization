Due to my hobby of game collecting and trading, I ran into a problem of inventorization. 
Paying money for my basic needs is not feasible, so creating my own solution was the choice. 

The system is very basic and allows you to inventory anything based on the inventory references you decide on. 

Each item can be created and has these attributes:
-pid (item ID in the internal system) *Can't be empty*
-invRef (item inventory reference number) *Can't be empty*
-title (name of the item) *Can't be empty*
-price (price you paid or sold it for, depends on your needs) *Can't be empty*
-condition *Can't be empty*
    *New, sealed - best condition you can have, obviously
    *CIB - complete in box, open box 
    *Loose - just the cartridge/disk/whatever type of media or box
-status (can be altered as well) 
    *in stock - you own the item, pretty simple
    *sold - you sold the item, but now you regret it and look at it time-to-time
    *on hold - you don't know what to do with it, so it's on hold
-image (path to the picture that is saved locally and associated with the item) *Can't be empty and default to the basic image if none is provided*
-user_id (the user that is associated with the item created) *Can't be empty, assigned automatically*

An inventory search is present and the system looks up items based on the string provided by the user and checks two fields: invRef and title. 

Item details allow you to see details on a separate page and edit the details if needed. 

More functions are coming, however at the current stage project fully fullfills my needs. Future docker integration and stand-alone deployment will be implemented. 

How to use:
1) Copy the repository and cd into the directory of the application
2) Run commands that are required:
   a) pip install -r ./requirements.txt
   b) flask db init
   c) ./run.py
3) Command line should show you the ip address and system is ready to use
*In the future docker container is coming for the ease of use*
