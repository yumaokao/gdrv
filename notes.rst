gdrv NOTES
==========

PIP
---
* quick package and upload
  ::

    $ python setup.py sdist
    $ python setup.py sdist upload
    $ pip install -U gdrv

  from start could reference hitchhiker_

* check with pep8
  ::

    $ pep8 gdrv/*.py

* update all pip packages
  ::

    import pip
    from subprocess import call

    for dist in pip.get_installed_distributions():
        call("pip install --upgrade " + dist.project_name, shell=True)

  with root

EXECUTE
-------
* execute in place
  ::

    $ cd gdrv
    $ python -m gdrv

* because we have __main__.py in gdrv.
  ::

    import gdrv
    if __name__ == '__main__':
        gdrv.main.main()

TODO
----
* [X] 2013-12-28 command mkdir
* [ ] make list looks good
* [ ] command url
* [ ] command share
* [ ] manual in github README.md

Q&A
---

REF
---
.. _hitchhiker: http://guide.python-distribute.org/creation.html

.. vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
