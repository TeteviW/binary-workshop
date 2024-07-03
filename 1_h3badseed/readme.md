
# Why are bad seed bad


1. **Introduction** Bad seed vulnerabilities are poorly generated random seeds in pseudo random
number generators. They make it easier for adversary to exploit because of how predicatble
they are. A good example is the attack on Android _Bitcoin_ usage of SecureRandom in which
there was an implementation flaw in the pseudorandom bits that led to predictable private
keys in _Bitcoin_ wallets allowing attackes to steal _Bitcoin_.


2. **Approach** The time program returns the time as the number of seconds since the _Epoch_.
This program helps to mitigate vulnerabilities by using time sensetive systems in which
they rely on synchronized clocks in order to make secure transactions. So creating a _seed_
that is time based would be a good soultion because it would create a harder and better
pseudo number _generator_. 
