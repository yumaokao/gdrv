gdrv
============

Another google drive command line interface program written in Python.

Author
============

Yu Mao Kao (yumaokao)

Quick Start
===========

$ gdrv init
Open the oauth link and grant google drive permission for this gdrv.

$ gdrv list /
List files and directories in your google drive root directory.

$ gdrv mkdir /uploads
Make a new directory 'uploads' in your google drive root directory.

$ gdrv push LOCALFILE /uploads
Push a local file 'LOCALFILE' to your google drive 'uploads' directory.

$ gdrv pull /uploads/
Pull files with a printer-liked prompt to $PWD.

$ gdrv trash /uploads/
Pull files to your google drive trash can.

$ gdrv share /uploads/LOCALFILE
$ gdrv url /uploads/LOCALFILE
Share the file to 'everyone' who has the url link of this file.

$ gdrv pull /uploads/SOME.mp4 -o - | mplayer -
Online playing a media file.

Reference
============
1. [gdrive](https://github.com/prasmussen/gdrive)
