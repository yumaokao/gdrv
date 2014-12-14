gdrv
============
Another google drive command line interface program written in Python.

Author
============
Yu Mao Kao (yumaokao)

Version
=======
0.1.5

Usage
=====

Installation
-----------
* Install with pip/pip2
.. code-block:: sh

  $ sudo pip2 install -U gdrv

Quick Start
-----------
* Open the oauth link and grant google drive permission for this gdrv.
.. code-block:: sh

  $ gdrv init

* List files and directories in your google drive root directory.
.. code-block:: sh

  $ gdrv list /

* Make a new directory 'uploads' in your google drive root directory.
.. code-block:: sh

  $ gdrv mkdir /uploads

* Push a local file 'LOCALFILE' to your google drive 'uploads' directory.
.. code-block:: sh

  $ gdrv push LOCALFILE /uploads

* Pull files with a printer-liked prompt to $PWD.
.. code-block:: sh

  $ gdrv pull /uploads/

* Throw files to your google drive trash can.
.. code-block:: sh

  $ gdrv trash /uploads/

* Share the file to 'everyone' who has the url link of this file.
.. code-block:: sh

  $ gdrv share /uploads/LOCALFILE
  $ gdrv url /uploads/LOCALFILE

* Online playing a media file.
.. code-block:: sh

  $ gdrv pull /uploads/SOME.mp4 -o - | mplayer -

Reference
============
.. _gdrive: https://github.com/prasmussen/gdrive

.. vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
