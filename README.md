wallboard
=========

GFI Wallboard monitor


At work we use GFI as our remote monitoring application. This service comes with a wallboard monitor to display alerts across our customer base.


We have this up on a big TV on the wall, but in order to check it we need to look up and visually investigate what alerts are showing, or if a server is offline.

This python program (running on a Raspberry Pi) takes a screenshot of a section of the wallboard screen. It then analyses it for any occurances of a pure red pixel (#FF0000). If this is found, then this server is offline.

The program then loops around the next 19 lines checking for more offline servers, stopping when it finds one that is not offline (ie does not have any pure-red pixels).

Then, using the espeak utility, it screams to everyone in the office just how many offline servers there are.

It then continues to alert us of the offline servers every ten minutes (by default).

See comments in the code for any changes. Different resolutions will result in different co-ordinates (this resolution is 1920x1080).

Requirements
------------

Required modules:
- wx
- Image
- espeak
 

Usage
-----

I have this running in an init.d script to start when the Pi starts. If you want to run it manually, use

*python /path/to/file/gfimon.py*

**NOTE:** If you have more than one screen, change line X in *gfimon.py* to be the relevant screen you want (program is currently set to use main screen)
