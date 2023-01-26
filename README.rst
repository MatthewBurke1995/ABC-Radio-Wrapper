=================
ABC Radio Wrapper
=================


.. image:: https://img.shields.io/pypi/v/abc_radio_wrapper.svg
        :target: https://pypi.python.org/pypi/abc_radio_wrapper

.. image:: https://img.shields.io/travis/matthewburke1995/abc_radio_wrapper.svg
        :target: https://travis-ci.com/matthewburke1995/abc_radio_wrapper

.. image:: https://readthedocs.org/projects/abc-radio-wrapper/badge/?version=latest
        :target: https://abc-radio-wrapper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/MatthewBurke1995/ABC-Radio-Wrapper/main/docs/coverage.svg



API wrapper library for the song history of abc radio channels


* Free software: MIT license
* Documentation: https://abc-radio-wrapper.readthedocs.io.


Quick Start
-----------

.. code-block:: python

    import abc_radio_wrapper

    ABC = abc_radio_wrapper.ABCRadio()

    search_result = ABC.search(station="triplej")

    for radio_play in search_result.radio_songs:
        print(radio_play.song.title)
        for artist in radio_play.song.artists:
            print(artist.name)


Features
--------

- Use python to search through the radio catalogue of triplej, ABC jazz, doublej and more!
- full type coverage for fast type hints on modern IDE's
- >90% test coverage


TODO
----

- Pull out dataclasses into seperate class files
- Pull out unittests into seperate files
- Add async queries 


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
