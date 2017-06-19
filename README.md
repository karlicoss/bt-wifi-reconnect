BT Wifi logs me out for no apparent reason several times a day.. so I wrote a cron script to reconnect me every few minutes!

If it detects a lack of internet connectivity, it runs a virtual browser (phantom JS) and logs you in.

# Setup
Recursive clone is important since I am using submodule!

    git clone --recursive git@github.com:karlicoss/bt-wifi-reconnect.git

# Running

    cp config.py.example config.py
    vim config.py # type in path to phantomjs, and your credentials
    python3 check_and_reconnect.py

# Adding to cron

1. `crontab -e`
2. add an entry like this `*/2 * * * * /usr/bin/python3 /full/path/to/script/bt_check_and_reconnect.py`, this runs the script every two minutes

Easy peasy!

# Prerequisites
* `pip3 install -r requirements.txt`
* `phantomjs` (see `config.py.example` for more details)
