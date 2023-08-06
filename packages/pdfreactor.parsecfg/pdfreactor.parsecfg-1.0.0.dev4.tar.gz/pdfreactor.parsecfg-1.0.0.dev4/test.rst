.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===================
pdfreactor.parsecfg
===================

This package provides a parsing facility for the `PDFreactor` client API,
as provided by the pdfreactor-api_ package.

To effectively make use of it, you'll need

- a license key (from `RealObjects`_; see https://www.pdfreactor.com/buy/)
- a running PDFreactor_ server
- some *PDFreactor* integration for your framework
  *(or have a look at the example scripts to do it yourself);*
  when using Plone, you may use the pdfreactor.plone_ package.


Features
========

1. A `parse_configuration` function
2. In a Plone context, a `pdfreactor-config` browser view
   to make basic use of it,
   i.e. producing a `config` dictionary from:
3. a site-global textual conversion configuration
   which is stored in the Plone registry.


Examples
========

The textual configuration could for example look like::

    # line comments are possible
    outputFormat = {
        width: 640,  # and so are eon-of-line comments
        type: OutputType.PNG_TRANSPARENT,
    }

The symbols defined by the *PDFreactor* API class are recognized, so this would
be converted to the following `config` dictionary::

    {'outputFormat': {
        'width': 640,
        'type': 'PNG_TRANSPARENT',
        }
     }

This doesn't look very magic, but it saves you from finding a way to save
settings for each possible key; you just need one configuration string.

On the values side, we'll accept valid configuration symbols only
(case sensitively, so ``OutputType.png_transparent`` would cause an error)
or valid Python_ string or number tokens;  for conveniense, several common names
for `true`, `false` and `nothing` are accepted (case-insensitively).


Documentation
=============

Installation
------------

Simply install the configuration parser by using pip::

    pip install pdfreactor.parsecfg

or, for projects using `buildout`_,
add to your ``buildout.cfg`` script::

    [buildout]
    ...
    eggs =
        pdfreactor.parsecfg

and then run ``bin/buildout``.


Plone integration
~~~~~~~~~~~~~~~~~

After restarting your Zope instance with pdfreactor.parsecfg_
(and, likely, *pdfreactor.plone*) added to your eggs,
simply use the Plone Add-Ons view or the Quick-Installer to activate it.

Then you may use the configuration registry and use the
``IPdfReactorConversionSettings`` prefix to adjust your conversion preferences.


Possible values
---------------

For the values which will be recognized by the *PDFreactor* backend, please refer
to the documentation by *RealObjects GmbH*:

- `PDFreactor Web service documentation`_


If, for example, the `documentation for the debugSettings model`_ tells you
about the boolean properties 
``appendLogs``,
``attachConfiguration``,
``attachDocuments``,
``attachResources``,
``forceResult`` and
``all``, this means that you may configure e.g.::

    debugSettings.all = on

or::

    debugSettings = {
        appendLogs: yes,
        forceResult: true,
    }


Support
=======

If you are having issues *concerning this configuration parser*,
please let us know;
please use the `issue tracker`_ mentioned above.

For issues regarding the *PDFreactor* itself, please refer to *RealObjects GmbH*:

- `PDFreactor Support Center`_

Contribute
==========

(To this configuration parser package:)

- Issue Tracker: https://github.com/visaplan/pdfreactor.plone/issues
- Source Code: https://github.com/visaplan/pdfreactor.plone


License
=======

The project is licensed under the MIT License.


.. _buildout: https://pypi.org/project/zc.buildout
.. _`documentation for the debugSettings model`: https://www.pdfreactor.com/product/doc/webservice/python.html#Configuration-debugSettings
.. _`issue tracker`: https://github.com/visaplan/pdfreactor.parsecfg/issues
.. _pdfreactor-api: https://pypi.org/project/pdfreactor-api
.. _PDFreactor: https://www.pdfreactor.com
.. _pdfreactor.parsecfg: https://pypi.org/project/pdfreactor.parsecfg
.. _pdfreactor.plone: https://pypi.org/project/pdfreactor.plone
.. _PDFreactor Support Center: https://www.pdfreactor.com/support/
.. _PDFreactor Web service documentation: https://www.pdfreactor.com/product/doc/webservice/
.. _Python: https://www.python.org
.. _`RealObjects GmbH`: https://www.realobjects.com/
.. _RealObjects: https://www.realobjects.com/

.. vim: tw=79 cc=+1 sw=4 sts=4 si et


Author
======

- Tobias Herp, tobias.herp@visaplan.com


Changelog
=========


1.0.0 (unreleased)
------------------

- Initial release.
  [tobiasherp]

