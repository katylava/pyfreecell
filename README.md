_Aside from updating this for python 3 in 2022, this repo is a 2012 time
capsule. That said, I still use it._

Requirements:

* Uses sqlite3 to store games played.
* Color terminal that can handle utf-8 and bright backgrounds


        Usage: freecell.py [--test]

        Options:
         -h, --help            show this help message and exit
         -t, --test            Run doctests
         -d DB, --db=DB        Path to game history database
         -w WIDTH, --width=WIDTH
                               Card width
         -o OFFSET, --offset=OFFSET
                                The difference between the --width and the actual card
                                width when the suit symbols take up less room on
                                screen than their actual width. You will most likely
                                have to set this to 2.



In iTerm I run it like `./freecell.py -w 8 -o 2`

Which font you use is very important for lining up the cards and making the
suit symbols look nice. Some fonts that work well for me:

* DejaVu Sans Mono
* Chica Mono
* Menlo
* Monaco
* NotCourierSans
* Onuava
* Phaisarn (standard only)
* TeX Gyre Cursor
* Verily Serif Mono

YMMV

![start screen](https://img.skitch.com/20120302-cm78ycsti1d827ukgrrhhnun9m.jpg)
![game play](https://img.skitch.com/20120302-mkg2srw65jpdt1gnxw1ps6ww24.jpg)
![show command](https://img.skitch.com/20120302-b4pbrj4gt39x926p1ru1h7tryg.jpg)
