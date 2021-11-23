# autoGuestWifi
A python wrapper to create and manage guest wifi networks on asus routers!

## Usage
Flags: -m, --mode: 0 = turn off, 1 = turn on, 2 = toggle, 3 = status
       -w, --wifi: id of the guest network 1-6 (1-3 are the 2.4GHz and 4-6 are the 5.0GHz networks)
Example
```
python main.py -m 2 -w 4 // turn on the 4th wifi network
```
