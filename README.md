BT Wifi logs me out for no apparent reason several times a day.. so I wrote a cron script to reconnect me every few minutes!

If it detects a lack of internet connectivity, it runs a virtual browser (phantom JS) and logs you in.

# Running

    python3 check_and_reconnect.py

# Adding to cron

# Prerequisites
* `selenium` (for interaction with BT wifi login page)
* `phantomjs` (see `config.py.example` for more details)