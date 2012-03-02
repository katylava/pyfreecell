**WARNING - WORK IN PROGRESS**

Requirements:
* Uses sqlite3 to store games played.
* Color terminal that can handle utf-8

    Usage: freecell.py [--test]

    Options:
     -h, --help            show this help message and exit
     -t, --test            Run doctests
     -d DB, --db=DB        Path to game history database
     -w WIDTH, --width=WIDTH
                           Card width
     -o OFFSET, --offset=OFFSET
                           If the 10s make the cards different widths then try
                           some different numbers here


In iTerm I run it like `./freecell.py -w 8 -o 2`

This is just an experiment. My intention is to refactor and create a new
project for more card games.

![start screen](https://img.skitch.com/20120302-cm78ycsti1d827ukgrrhhnun9m.jpg)
![game play](https://img.skitch.com/20120302-mkg2srw65jpdt1gnxw1ps6ww24.jpg)
![show command](https://img.skitch.com/20120302-b4pbrj4gt39x926p1ru1h7tryg.jpg)
