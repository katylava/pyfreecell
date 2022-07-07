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

![start screen](https://user-images.githubusercontent.com/10575/177864590-cc07f1b6-9df3-4b10-b489-176f44a8ec55.png)
![game play](https://user-images.githubusercontent.com/10575/177864753-e246af7d-9c1f-4aaa-9371-77c576394698.png)
![show command](https://user-images.githubusercontent.com/10575/177864844-fc5ed6db-6450-42ea-b46c-cdbc9a8f3341.png)
