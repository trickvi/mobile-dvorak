# Mobile DVORAK

## Backstory

Keyboards on smart phones (the touch screen ones) are weird. Well most default keyboards are weird.

We all know the [QWERTY keyboard](https://en.wikipedia.org/wiki/QWERTY) was designed to be slow and some guy called Dr. August Dvorak didn't like it so he designed [his own keyboard](https://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard) to improve speed.

QWERTY still remained **the** keyboard except for some typist nerds.

Then we got smart phones (not the old mobile phones which had ABC mapped to key 1 etc. but the touch one)... Woosh. Out the window goes the finger position used for larger keyboards. In goes two thumbs. A totally different way to type text. But QWERTY remains. That's the weirdest thing ever.

We had a good opportunity to improve our keyboard when users changed from 10 fingers to 2. Then we went ahead and didn't.

## What is this?

So this is an attempt to see how we could have made a better keyboard a **mobile dvorak**... except that it's not. It's current incarnation is not a thoroughly researched way of putting keys on the board but just a small script to run against a bunch of text files who list characters in frequency order and given a keyboard file will arrange them accordingly.

It will **not** take frequent letter combinations into account or put wovels on one side and consonants on the right. It most certainly isn't designed to have the right hand do most of the typing because I'm left handed and I hate it when things are designed for the other hand.

You provide a keyboard layout so you can just play around with different layouts on your own. 

## How to use

First install the requirements. Don't let my software requirements screw up your system so please run it in a virtual environment like [``virtualenv``](http://virtualenv.readthedocs.org/en/latest/):

    > virtualenv venv
    > . venv/bin/activate
    > pip install -r requirements.txt 

Now you can run it:

    > python keyboarder.py --keyboard <LAYOUT FILE> --alternatives <KEY ALTERNATIVES> TEXTFILES...

A layout file is just a file with numbers in it which will be stupidly parsed (and fail if it can't be cast into a number. After running the script, the numbers will be replaced by letters (characters) based on how frequent they are. So the most common character will go into slot 0, second most common character in slot 1 and so on.

Smart phone keyboards have this nice feature where you can press and hold a button to get alternatives to that button. You can provide a ``json`` which maps the main character to the alternatives that should be associated with it.

That's about it. The code shouldn't be too hard to follow if you still don't understand what it's doing.

## Example

Members of Parliament (or congress or whatever) have to be quick if they don't want to [get busted for playing with their phones](http://www.dailymail.co.uk/news/article-2864911/Something-better-doing-MP-caught-playing-Candy-Crush-game-iPad-pensions-experts-gave-evidence-Parliament-hearing.html). So let's help them type text messages faster and because I'm Icelandic, let's do it for Icelandic.

Language Resource for Icelandic on [malfong.is](http://www.malfong.is/index.php?lang=en) have all [discussions from the Icelandic parliament](http://www.malfong.is/index.php?pg=althingi&lang=en) (the Parliament Speech Corpus is distributed und Creative Commons Attribution). We can just use that... and I've already extracted it and put the transcripts into the ``example`` directory.

### Alternatives

Icelandic has more characters in the alphabet than English and but some of them can be mapped as alternatives to more common characters, e.g. **ó** could be an alternative to *o*. **ö** might also (and is on today's keyboards) but I have *ö* in my surname so I don't care and won't have that as an alternative to anything. Iceland is also pretty close to other Nordic countries so I want to include those characters which means I can put in **ø** as an alternative to *ö*.

Also why do current Icelandic keyboards take precious space for characters we hardly use like **z** and **c** or **w** and **q**... oh yeah QWERTY and Icelandic characters are an afterthought. Screw that. We'll pack those four keys into two. So the alternatives' map we'll use (in the ``example`` directory) is:

```json
{
  "a": ["á", "ä", "å"],
  "e": ["é"],
  "i": ["í"],
  "o": ["ó"],
  "u": ["ú"],
  "y": ["ý"],
  "ö": ["ø"],
  "w": ["q"],
  "z": ["c"]
}
```

### Layout

On smart phones most people use their thumbs and hover somewhere over the middle of the keyboard by default (relaxed thumbs). In a highly scientific experimenting involving me drinking a pale ale while holding a phone and seeing where I thought it was best to reach keys I drew up this keyboard (you guessed it, also in the ``example`` directory):

    27 21 3 9 13 12 8 2 20 26
    25 19 11 1 7 6 0 10 18 24
    23 17 5 15 14 4 16 22
 
### Icelandic parliamentary mobile keyboard

And running the keyboarder.py:

    > python keyboarder.py --keyboard example/mobile.keyboard --alternatives example/alternatives_map.json example/transcripts/*

I get this awesome output:

    [   w/q   ][   y/ý   ][   e/é   ][    g    ][    f    ][    k    ][    s    ][   i/í   ][    æ    ][   z/c   ]
    [    x    ][    d    ][    l    ][    r    ][    t    ][   u/ú   ][ a/á/ä/å ][    m    ][    j    ][    p    ]
    [    b    ][    h    ][    ð    ][   o/ó   ][    v    ][    n    ][    þ    ][   ö/ø   ]

## License

This is free software and everything is licensed under the GNU GPL version 3 or later except the transcripts which are as stated previously released under Creative Commons Attributions by *Stofnun Árna Magnússonar í íslenskum fræðum*.
