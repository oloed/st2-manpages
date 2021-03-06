st2-manpages
============

![st2-manpages screenshot](https://raw.github.com/nilium/st2-manpages/master/screenshot.png)

st2-manpages is a Sublime Text 2 plugin to search man pages. You can
install it by cloning it into your Sublime Text 2 Packages directory
(to find that, use the 'Browse Packages...' menu item, found under
'Preferences' on Mac OS -- probably under 'File' or something on other
operating systems).

Basically, you want to do this:

    $ cd /path/to/Sublime/Packages
    $ git clone git://github.com/nilium/st2-manpages.git

And you should be good to go.

The command, should you want to add key bindings, is invoked with
`open_man_page` and the argument `source`, which takes a string, either
`'view'` or `'input'`.  `'view'` will search through all words and
selections in the active view for man pages and present those options
to you. `'input'` will open an input panel taking a single keyword to
search for, again offering all possible results (sorted by how closely
they match the keyword).

If you prefer the Command Palette, your have "Manpages: Search for
Text" and "Manpages: Search for Input," which map to the sources above.


Settings
--------

There are two options available for user settings:

* `manpage_use_apropos` → Defaults to `false`

    If set to `true`, this will tell the plugin to use the `apropos`
    command instead of `whatis`. This allows it to match a wider
    variety of man pages, but it can also lead to a great deal of
    incorrect matches. Incidentally, the best way to understand the
    difference between `apropos` and `whatis` is to check their
    respective man pages.

* `manpage_sections` → Defaults to `['2', '3']`

    This specifies which man sections will actually be matched. If it's
    not in here, it doesn't show up in the quick panel. This includes
    subsections such as 3G.  In general, you'll only reference sections
    2 and 3, but if you need more, you can add them.


License
-------

This is licensed under the Do What The Fuck You Want Public License:

```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2012 Noel Cower <me@spifftastic.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

If you have any further questions regarding the license, look at it
again and they should be answered.
