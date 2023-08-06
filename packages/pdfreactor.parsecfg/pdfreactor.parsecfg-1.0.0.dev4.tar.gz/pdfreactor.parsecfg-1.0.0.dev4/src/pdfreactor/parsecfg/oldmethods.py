"""
oldmethods: Map old API method calls (i.e., their arguments) to config keys of
the new PDFreactor client API.

As far as "symbols" are involved (like CLEANUP_CYBERNEKO and the like), we
have a mapping of the old names to the new values already in ./oldsymbols.py.
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import zip


def negate(val):
    # negate the given value
    return not val

def unsupported(val):
    raise ValueError('The use of this method can\'t be converted '
                     'to some config key in the new PDFreactor API!')


map2 = {
    'setOutputFormat': [{
        'key': 'outputType',
        'subkey': 'type',
        }, {
        'key': 'outputType',
        'subkey': 'width',
        }, {
        'key': 'outputType',
        'subkey': 'height',
        }],
    'setCleanupTool': [{  # _new.Cleanup symbols
        'key': 'cleanupTool',
        }],
    'setEncoding': [{
        'key': 'encoding',
        }],
    'setJavaScriptMode': [{  # _new.JavaScriptMode symbols
        'key': 'javaScriptMode',
        }],
    'setAddBookmarks': [{
        'key': 'addBookmarks',
        }],
    'setAddLinks': [{
        'key': 'disableLinks',
        'convert': negate,
        }],
    'setAppendLog': [{
        'key': 'debugSettings',
        'subkey': 'appendLogs',
        }],
    'setDocumentType': [{
        'key': 'documentType',
        }],
    'setLicenseKey': [{  # replaced by the PDFreactor.apiKey attribute
        'convert': unsupported,
        }],
    # https://www.pdfreactor.com/product/doc_html/#Logging
    'setLogLevel': [{  # _new.logLevel symbols
        'key': 'logLevel',
        }],
    }


def _specs(liz):
    if not liz:
        return
    elif not liz[1:]:
        yield 'val'
        return
    res = []
    for dic in liz:
        yield dic['subkey']


if __name__ == '__main__':
    dictnames = set()
    nodicts = set()

    for name in sorted(map2.keys()):
        args = map2[name]
        specs = list(_specs(args))
        arglist = ', '.join(specs)
        print('%(name)s(%(arglist)s) -->' % locals())
        for spec, dic in zip(specs, args):
            try:
                key = dic['key']
            except KeyError:
                print('    (UNSUPPORTED)')
            else:
                if dic.get('convert'):
                    spec = '(converted) ' + spec
                if 'subkey' in dic:
                    subkey = dic['subkey']
                    assert key not in nodicts
                    dictnames.add(key)
                    print('    config[%(key)r][%(subkey)r] = %(spec)s' % locals())
                else:
                    assert key not in dictnames
                    nodicts.add(key)
                    print('    config[%(key)r] = %(spec)s' % locals())
