gdrv NOTES
==========

virtualenv
----------
* install
  code:: sh

  $ yaourt virtualenv

* usage
  code:: sh

  # build
  $ virtualenv .env

  # enter
  $ source .env/bin/activate

  # exit
  $ deactivate


PIP
---
* quick package and upload
  code:: python

    $ python setup.py sdist
    $ python setup.py sdist upload
    $ pip install -U gdrv

  from start could reference hitchhiker_

* check with pep8
  code:: sh

    $ pep8 gdrv/*.py

* update all pip packages
  code:: python

    import pip
    from subprocess import call

    for dist in pip.get_installed_distributions():
        call("pip install --upgrade " + dist.project_name, shell=True)

  with root

* change pypi password
  code:: sh

    vim ~/.pypirc
    [pypi]
    username:Yu.Mao.Kao
    password:XXXXXXXX
    [server-login]
    username:Yu.Mao.Kao
    password:XXXXXXXX

EXECUTE
-------
* execute in place
  code:: sh

    $ cd gdrv
    $ python -m gdrv

* because we have __main__.py in gdrv.
  code:: python

    import gdrv
    if __name__ == '__main__':
        gdrv.main.main()

UTF-8
-----
* make prinf with utf-8 encoding
  code:: python

    # -*- coding: utf-8 -*-

    reload(sys)
    sys.setdefaultencoding('utf-8')

TODO
----
* [$] 2013-12-28 ~ 2014-05-18 command mkdir
* [$] 2014-03-02 ~ 2014-05-18 uft8
* [$] 2014-05-18 ~ 2014-05-18 command url
* [$] 2014-05-18 ~ 2014-05-18 command share
* [$] 2014-05-18 ~ 2014-05-18 refine import in gdrv/main.py
* [%] 2014-05-18 make list looks good
* [%] 2014-05-18 make url looks good
* [ ] 2014-05-18 manual in github README.md

Q&A
---

REF
---
.. _hitchhiker: http://guide.python-distribute.org/creation.html

.. vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
