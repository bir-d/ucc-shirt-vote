# A website for members of [UCC](https://www.ucc.asn.au) to vote on T-shirt designs for our 50th Anniversary.

## Usage
* Collect your shirt designs into one folder.
* Open `./readshirts.sh`, add the correct paths at the top.
* Run it to get the correct DB initialisation script. 
* Insert into and run `init.py` to generate the DB. (Make sure to place it in `cgi-bin!`)
* Host with cgi support: `python -m http.server --cgi 8000`
* Visit at `localhost:8000`

## Stack:
* HTMX
* AlpineJS
* Python (cgi)
* SQLite
