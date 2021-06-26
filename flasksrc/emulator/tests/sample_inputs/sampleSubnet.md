# Allocating Subnets

## CIDR Block

Given: `172.16.*.*/16: 10101100 00010000 ******** ********`

Helpful Numbers:

```
128: 10000000
192: 11000000
224: 11100000
240: 11110000
```

# First Subnet
```X..X X..X`|`00000000 11111110```
`172.16.0.254/16` will be `r1`'s IP, `r1-eth0`

Subnet to 2 subsequent bits:
```
X..X X..X |00|****** ********
X..X X..X |01|****** ********
X..X X..X |10|0***** 00000001 
X..X X..X |11|0***** 00000001 
```
* `172.16.128.1/18` will be an interface `r1-eth1`
* `172.16.192.1/18` will be an interface `r1-eth2`

* We decide to use CIDR blocks `172.16.128.0/18` and `172.16.192.0/18`.

# Second Subnet off First
```X..X X..X 10/000000 11111110```
* We want two subnets in the block `172.16.128.0/18`.
* `172.16.128.254/18` will be `r2`'s IP, `r2-eth0`

Subnet 2 more bits:
```
X..X X..X 10|00|**** ********
X..X X..X 10|01|**** ********
X..X X..X 10|10|0*** 00000001 
X..X X..X 10|11|0*** 00000001
```
* `172.16.160.1/18` will be an interface `r2-eth1`
* `172.16.176.2/18` will be an interface `r2-eth2`

# Third Subnet off First
```X..X X..X 11`|`000000 11111110```
* We want two subnets in the block `172.16.192.0/18`.
* `172.16.192.254/18` will be `r3`'s IP, `r3-eth0`

Subnet 2 more bits:
```
X..X X..X 11|00|**** ********
X..X X..X 11|01|**** ********
X..X X..X 11|10|0*** 00000001 
X..X X..X 11|11|0*** 00000001
```
* `172.16.224.1/20` will be an interface `r3-eth1`
* `172.16.240.1/20` will be an interface `r3-eth2`