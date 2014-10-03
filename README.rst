gdrv
============
Another google drive command line interface program written in Python.

Author
============
Yu Mao Kao (yumaokao)

Version
=======
0.1.4

Usage
=====

Quick Start
-----------
* Install with pip/pip2
  code:: sh

  $ sudo pip2 install -U gdrv

* Open the oauth link and grant google drive permission for this gdrv.
  code:: sh

  $ gdrv init

* List files and directories in your google drive root directory.
  code:: sh

  $ gdrv list /

* Make a new directory 'uploads' in your google drive root directory.
  code:: sh

  $ gdrv mkdir /uploads

* Push a local file 'LOCALFILE' to your google drive 'uploads' directory.
  code:: sh

  $ gdrv push LOCALFILE /uploads

* Pull files with a printer-liked prompt to $PWD.
  code:: sh

  $ gdrv pull /uploads/

* Throw files to your google drive trash can.
  code:: sh

  $ gdrv trash /uploads/

* Share the file to 'everyone' who has the url link of this file.
  code:: sh

  $ gdrv share /uploads/LOCALFILE
  $ gdrv url /uploads/LOCALFILE

* Online playing a media file.
  code:: sh

  $ gdrv pull /uploads/SOME.mp4 -o - | mplayer -

Reference
============
.. _gdrive: https://github.com/prasmussen/gdrive

.. vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
