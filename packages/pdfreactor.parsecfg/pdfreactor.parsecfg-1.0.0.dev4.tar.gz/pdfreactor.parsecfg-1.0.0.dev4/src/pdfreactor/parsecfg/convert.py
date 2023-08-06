# -*- coding: utf-8
"""
pdfreactor.parsecfg.convert: convert textual configuration to config dict
"""

# Python compatibility:
from __future__ import absolute_import

__all__ = [
    'parse_configuration',  # (**named options)
    # Toolset for own conversions: 
    'update_config_dict',   # ...(config, statement)
    'resolve_value',        # ...(TokenGroup [,factory])
    ]

# Standard library:
from tokenize import (
    NAME,
    NUMBER,
    OP,
    STRING,
    )

# We might get along without this, but we'd like to have more tests first:
from visaplan.tools.sequences import sequence_slide

# Local imports:
from pdfreactor.parsecfg._args import extract_input_specs
from pdfreactor.parsecfg._configkeys import _factories
from pdfreactor.parsecfg.parse import generate_statements
from pdfreactor.parsecfg.symbols import SYMBOL_STRINGS, SIMPLE_SYMBOLS

# ... for doctests:
from pdfreactor.parsecfg._tokensgroup import TokensGroup
from pdfreactor.parsecfg._tokensgroup import generate_token_groups


def parse_configuration(*args, **kwargs):
    """
    Parse a textual configuration specification and return or modify a config
    dictionary (to be thrown e.g. at the PDFreactor.convert API method).

    >>> txt='config.outputFormat.type = OutputType.JPEG'

    If only one unnamed option is given, it is expected to be text, and the
    resulting config dict is returned:

    >>> config = parse_configuration(txt)
    >>> config
    {'outputFormat': {'type': 'JPEG'}}

    The configuration text can be specified as a named `text` option as well,
    or alternatively (UNTESTED) as a readable file object.

    An empty configuration text yields an empty dict, of course:
    >>> parse_configuration('')
    {}

    You might have a default configuration and want to apply changes to it.
    In this case you'd specify a named option `config` which will then be
    updated:

    >>> parse_configuration('config.outputFormat.width = 640', config=config)
    >>> config                                # doctest: +NORMALIZE_WHITESPACE
    {'outputFormat': {'width': 640,
                      'type': 'JPEG'}}

    >>> parse_configuration('''config.outputFormat = {
    ... width: 123,
    ... type: 'PNG',
    ... }''')
    {'outputFormat': {'width': 123, 'type': 'PNG'}}
    >>> parse_configuration('''outputFormat = {
    ... width: 234,
    ... type: 'JPEG',
    ... }''')
    {'outputFormat': {'width': 234, 'type': 'JPEG'}}
    >>> parse_configuration('''config.someList = (1, 2,3)''')
    {'someList': (1, 2, 3)}

    You might have special commands in your configuration which can't be taken
    as config assignments.  By default, these will cause the conversion to
    fail:
    >>> fancy_config = '''strict on
    ... config.outputFormat.type = OutputType.PNG_TRANSPARENT
    ... '''
    >>> parse_configuration(fancy_config)
    Traceback (most recent call last):
      ...
    ValueError: Found 1 unsupported statement(s) (strict on)

    You may specify an `unused` list to handle this:
    >>> unused = []
    >>> parse_configuration(fancy_config, unused=unused)
    {'outputFormat': {'type': 'PNG_TRANSPARENT'}}
    >>> unused
    [<Statement (strict on)>]

    Alternatively you might specify an own conversion function (named option
    `convert`) which is tried first for each statement and handles those, as
    we call them, "control commands".  If it returns something falsy, the
    standard processing will be tried next:

    >>> parse_configuration('', convert=42)   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    ValueError: 'convert' option must be some function
                  bool <= f(statement, config, control);
                found <type 'int'>!

    Finally, of course, we won't be fooled by illegal options:
    >>> parse_configuration('', no_unused=False)
    Traceback (most recent call last):
      ...
    TypeError: Found unsupported option(s)! ('no_unused')

    """
    input_specs = extract_input_specs(args, kwargs)
    inspect_parse_specs(kwargs)  # all are keyword-only

    config = kwargs['config']
    control = kwargs['control']
    unused = kwargs['unused']
    convert = kwargs['convert']
    dict_style = kwargs['style'] == 'dict'
    statements = generate_statements(**input_specs)
    for stmt in statements:
        if convert is not None and convert(stmt, config, control):
            continue
        elif not stmt.is_assignment:
            unused.append(stmt)
        elif dict_style:
            update_config_dict(config, stmt)
        else:
            amend_config_list(config, stmt)

    if unused and kwargs['no_unused']:
        cnt = len(unused)
        first = unused[0]
        more = cnt > 1 and ' (...)' or ''
        raise ValueError('Found %(cnt)d unsupported statement(s) '
                         '(%(first)s%(more)s)'
                         % locals())
    if kwargs['return_configuration']:
        return config


def inspect_parse_specs(kw):
    """
    Helper: Evaluate named options for the parse_configuration function above

    >>> kw = {}
    >>> inspect_parse_specs(kw)
    >>> sorted(kw.items())                    # doctest: +NORMALIZE_WHITESPACE
    [('config', {}),
     ('control', {}),
     ('convert', None),
     ('no_control', True),
     ('no_unused', True),
     ('return_configuration', True),
     ('style', 'dict'),
     ('unused', [])]

    If a config dict is given, it is not returned but modified in-place:
    >>> config = {'some': 'configuration'}
    >>> kw = {'config': config}
    >>> inspect_parse_specs(kw)
    >>> kw['return_configuration']
    False

    Some day, perhaps, the given configuration may be alternatively a list:
    >>> config = [('some', 'configuration')]
    >>> kw = {'config': config}
    >>> inspect_parse_specs(kw)                               # doctest: +SKIP
    >>> sorted(kw.items())              # doctest: +NORMALIZE_WHITESPACE +SKIP
    [('config', [('some', 'configuration')]),
     ('control', {}),
     ('convert', None),
     ('no_control', True),
     ('no_unused', True),
     ('return_configuration', False),
     ('style', 'list'),
     ('unused', [])]

    This is not implemented (yet), however; so we'll get an error:
    >>> inspect_parse_specs(kw)
    Traceback (most recent call last):
      ...
    ValueError: config structure 'list' style is not (yet?) supported
    """
    pop = kw.pop
    no_config = 'config' not in kw
    upd = {'return_configuration': no_config}
    if no_config:
        fact = pop('config_factory', dict)
        kw['config'] = fact()
    val = kw['config']  # will be used
    if isinstance(val, dict):
        upd['style'] = 'dict'
    elif isinstance(val, list):
        upd['style'] = 'list'
        raise ValueError('config structure %(style)r style is not (yet?)'
                         ' supported' % upd)
    else:
        raise ValueError('config structure must be a list or dict; found %s!'
                         % (type(val),
                            ))

    # control: a namespace for 'strict' (...) specifications
    #          (to be implemented in your own application)
    upd['no_control'] = no_control = 'control' not in kw
    if no_control:
        kw['control'] = {}
    elif not isinstance(kw['control'], dict):
        raise ValueError('control structure must be some dict; found %s!'
                         % (type(kw['control']),
                            ))

    # unused: a list of unused statements.
    #
    # You might have statements which don't result in some config assignment,
    # and which are meant to be used by your application code (typically before
    # requesting the PDF conversion).
    # Specify a list to handle them yourself after parsing;
    # if you don't, we'll consider such statements an error.
    upd['no_unused'] = no_unused = 'unused' not in kw
    if no_unused:
        kw['unused'] = []
    elif not isinstance(kw['unused'], list):
        raise ValueError("'unused' option must be some list; found %s!"
                         % (type(kw['unused']),
                            ))

    # convert: a function for alternate conversions
    #
    # This is the plugin facility for custom conversions.
    # You might specify a function with the following signature:
    #
    #   bool <= f(stmt, config, control)
    #
    # The function should inspect the statement <stmt> (just a list of groups
    # of tokens; see our Statement class) and apply changes to the config
    # structure and / or control dict.
    # If it returns True, the statement is considered dealt with;
    # otherwise we'll check whether we recognize it as an assignment.
    # If we don't, it is put to the 'unused' list.
    val = kw.setdefault('convert', None)
    assert 'convert' in kw
    if val is None:
        pass
    elif not callable(val):
        raise ValueError("'convert' option must be some function"
                         ' bool <= f(statement, config, control);'
                         ' found %s!'
                         % (type(kw['convert']),
                            ))
    valid_options = set(['config', 'control',
                         'convert',
                         'unused'])
    invalid = set(kw) - valid_options
    if invalid:
        raise TypeError('Found unsupported option(s)! (%r)'
                        % (sorted(invalid)[0],
                           ))
    kw.update(upd)


def checked_reactor_dest(tg):
    """
    Take a TokenGroup and return a dict to tell how to deal with it.

    We'll use a handy little test helper here:

    >>> def f(txt):
    ...     groups = list(generate_token_groups(txt))
    ...     dest = groups[0]
    ...     return sorted(checked_reactor_dest(dest).items())

    >>> f('config.disableLinks')              # doctest: +NORMALIZE_WHITESPACE
    [('key', 'disableLinks'),
     ('key_factory', <type 'bool'>),
     ('subkey', None),
     ('tip_factory', <type 'bool'>),
     ('tip_keys', ['disableLinks'])]

    In fact the leading 'config.' is optional:
    >>> f('disableLinks')                     # doctest: +NORMALIZE_WHITESPACE
    [('key', 'disableLinks'),
     ('key_factory', <type 'bool'>),
     ('subkey', None),
     ('tip_factory', <type 'bool'>),
     ('tip_keys', ['disableLinks'])]

    The most interesting case are dotted assignment targets:
    >>> f('outputFormat.type')                # doctest: +NORMALIZE_WHITESPACE
    [('key',            'outputFormat'),
     ('key_factory',    <type 'dict'>),
     ('subkey',         'type'),
     ('subkey_factory', <type 'str'>),
     ('tip_factory', <type 'str'>),
     ('tip_keys', ['outputFormat', 'type'])]

    A bare 'config' won't be enough, though:
    >>> f('config')                           # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    ValueError: Invalid assigment destination <NAME config>:
        no names left behind 'config'!
    """
    names = list(tg.names_list)
    if names[0] == 'config':
        # currently we don't have a complete list of possible names and their types yet ...
        # so we just check that there is more:
        head = names.pop(0)
        if not names:
            raise ValueError('Invalid assigment destination %(tg)r: '
                    'no names left behind %(head)r!'
                    % locals())
    key = names.pop(0)
    tip_keys = [key]
    res = {
        'key': key,
        }
    key_factory = _factories.get((key,), None)

    if names:
        subkey = names.pop(0)
        if names:
            raise ValueError('Invalid assigment destination %(tg)r: '
                    'too many levels!'
                    % locals())
        tip_keys.append(subkey)
        subkey_factory = _factories.get((key, subkey), None)
        if key_factory is None:
            # we have subkeys, so this should be a dict:
            key_factory = dict
        else:
            assert key_factory is dict
        res.update({
            'subkey': subkey,
            'subkey_factory': subkey_factory,
            'tip_factory': subkey_factory,
            })
    else:
        res.update({
            'tip_factory': key_factory,
            'subkey': None,
            })
    res.update({
        'key_factory': key_factory,
        'tip_keys': tip_keys,
        })
    return res


_more_factories = {}
def make_af():
    from os.path import dirname, join, sep
    mydir = dirname(__file__)
    devmode = 'src' in mydir.split(sep)
    modfile = join(mydir, '_configkeys.py')

    def add_new_factory(fact, *keys):
        if isinstance(keys, list):
            keys = tuple(keys)
        if keys in _more_factories:
            oldfact = _more_factories[keys]
            if oldfact is fact:
                return 0
            raise ValueError('Factories conflict for %(keys)r: '
                    '%(fact)r mismatches %(oldfact)r!'
                    % locals())
        else:
            assert callable(fact), ('Something callable expected;'
                    ' %(fact)r found!'
                    ) % locals()
            _more_factories[keys] = fact
            return 1

    def amend_module(fact, *keys):
        if add_new_factory(fact, *keys):
            if isinstance(keys, list):
                keys = tuple(keys)
            with open(modfile, 'a') as mf:
                txt = '_factories[%(keys)s] = %(fact)s\n' % locals()
                mf.write(txt)

    if devmode and 0:
        return amend_module
    return add_new_factory
another_factory = make_af()


def set_value(dic, key, tg, fact=None):
    """
    Helper function for update_config_dict
    """
    assert isinstance(dic, dict)
    assert isinstance(key, basestring)
    assert isinstance(tg, TokensGroup)
    dic[key] = resolve_value(tg, fact)


def resolve_value(tg, fact=None):
    """
    Resolve the value of a TokenGroup to some Python value.

    Let's use a little test helper:

    >>> def f(txt, factory=None):
    ...     groups = list(generate_token_groups(txt))
    ...     group = groups[0]
    ...     return resolve_value(group, factory)

    We support PDFreactor symbols:

    >>> f('OutputType.JPEG')
    'JPEG'

    ... unless mistyped:
    >>> f('outputType.JPEG')
    Traceback (most recent call last):
      ...
    ValueError: <NAME outputType.JPEG>: No known symbol!

    We support simple (case insensitive) aliases for boolean and None values:

    >>> f('OFF')
    False
    >>> f('Yes')
    True
    >>> f('NIL') is None
    True
    >>> f('nothing') is None
    True

    We support strings:
    >>> f('"Some string"')
    'Some string'

    We support numbers:
    >>> f('42')
    42
    >>> f('3.141')
    3.141

    You may specify a custom factory function:
    >>> def foolme(s):
    ...     return 3.141 if '.' in s else 42    
    >>> f('1.2', foolme)
    3.141
    >>> f('1', foolme)
    42

    """
    if fact is not None:
        assert callable(fact)
    if tg.is_dotted_name:
        txt = tg.text
        if txt in SYMBOL_STRINGS:
            val = SYMBOL_STRINGS[txt]
        else:
            ltxt = txt.lower()
            if ltxt in SIMPLE_SYMBOLS:
                val = SIMPLE_SYMBOLS[ltxt]
            else:
                raise ValueError('%(tg)s: No known symbol!'
                        % locals())
    elif tg.ttype == NUMBER:
        txt = tg.text
        if fact is not None:
            val = fact(txt)
        elif '.' in txt:
            val = float(txt)
        else:
            val = int(txt)
    elif tg.ttype == STRING:
        val = eval(tg.text)
    else:
        raise ValueError('Don\'t know how to use the value %(tg)s!'
                         % locals())
    return val


def update_config_dict(config, statement):
    """
    Use the given statement to apply changes to the given config dict
    """
    if not statement.is_assignment:
        return False
    strict = True  # (no option yet)
    try:
        dest, op = statement[:2]
        dest_dic = checked_reactor_dest(dest)
    except ValueError as e:
        if strict:
            raise
        print(e)
        return False
    else:
        rest = list(statement[2:])
        if not rest:
            raise ValueError('Incomplete assigment: %(statement)s'
                             % locals())
        key = dest_dic['key']
        subkey = dest_dic['subkey']
        key_factory = dest_dic['key_factory']
        tip_factory = dest_dic['tip_factory']
        tip_keys = tuple(dest_dic['tip_keys'])
        if rest[0].ttype != OP:
            valgrp = rest.pop(0)
            if rest and not rest[0].is_terminator:
                surplus = len(rest)
                raise ValueError('%(statement)r: nothing expected after '
                        '%(valgrp)r; %(surplus)d surplus token( group)s found!'
                        % locals())
            if subkey is None:
                if key_factory is dict:
                    raise ValueError('%(statement)r: missing subkey '
                            'for %(key)r; can\'t assign %(valgrp)r!'
                            % locals())
                set_value(config, key, valgrp, key_factory)
            else:
                if key_factory is None:
                    another_factory(dict, key)
                elif key_factory is not dict:
                    raise ValueError('%(statement)r: key_factory for (%(key)r,) '
                            'expected to be <dict>; found %(key_factory)r!'
                            % locals())
                subdict = config.setdefault(key, {})
                set_value(subdict, subkey, valgrp, tip_factory)
            return True

        if key_factory is dict:
            target_dict = config.setdefault(key, {})
        else:
            target_dict = config
            use_key = key
        pa1 = rest.pop(0)
        pa1tex = pa1.text
        if not pa1.opens_brace:
            raise ValueError('%(statement)r: opening brace expected; '
                             '%(pa1)r found!'
                             % locals())
        expected = pa1.expects_brace
        opens_dict = pa1tex == '{'
        if opens_dict:
            if subkey is not None:
                raise ValueError('%(statement)r: subkey %(subkey)r *and* '
                                 '%(pa1)r?!'
                                 % locals())
            elif tip_factory is None:
                another_factory(dict, *tip_keys)
                tip_factory = dict
            elif tip_factory is not dict:
                raise ValueError('%(statement)r: factory for %(tip_keys)s '
                        'expected to be <dict>; found %(tip_factory)r!'
                        % locals())
            more_names = 1
        else:
            # FINDOUT: do we need to distinguish lists and tuples?
            if pa1tex == '(':
                if tip_factory is None:
                    another_factory(tuple, *tip_keys)
                    tip_factory = tuple
                elif tip_factory is list:
                    pass
                elif tip_factory is not tuple:
                    raise ValueError('%(statement)r: factory for %(tip_keys)r '
                            'expected to be <tuple> (or list); '
                            'found %(tip_factory)r!'
                            % locals())
            else:
                assert pa1tex == '['
                if tip_factory is None:
                    another_factory(list, *tip_keys)
                    tip_factory = list
                elif tip_factory is tuple:
                    pass
                elif tip_factory is not list:
                    raise ValueError('%(statement)r: factory for %(tip_keys)r '
                            'expected to be <list> (or tuple); '
                            'found %(tip_factory)r!'
                            % locals())
            more_names = 0
        if more_names:
            name = None
            val = None
            for prev_tg, tg, next_tg in sequence_slide(rest):
                assert isinstance(tg, TokensGroup)
                ttype = tg.ttype
                text = tg.text
                if ttype == OP:
                    if text == ':':
                        if name is None:
                            raise ValueError('%(tg)r: expected to have a '
                                    'name here to assign to!'
                                    % locals())
                    elif tg.is_terminator:
                        assert next_tg is None
                        break
                    elif text == ',':
                        if name is None or val is None:
                            raise ValueError('%(tg)r: expected to have '
                                    'both a name and a value here; '
                                    'found %(name)r, %(val)r!'
                                    % locals())
                        name = None
                        val = None
                    elif text == expected:
                        if next_tg is None or next_tg.is_terminator:
                            pass
                        else:
                            raise ValueError('Unexpected %(next_tg)r '
                                    'following %(tg)r!'
                                    % locals())
                    else:
                        raise ValueError('Unexpected operator %(tg)r!'
                                % locals())
                elif name is None:
                    if ttype != NAME:
                        raise ValueError('%(tg)r: expected a name!'
                                % locals())
                    name = tg
                elif val is None:
                    val = tg
                    set_value(target_dict, name.text, val)
                else:
                    raise ValueError('%(tg)r: surplus value; '
                            'expected a comma or closing brace! '
                            '(name=%(name)r, val=%(val)r)'
                            % locals())
        else:
            val = None
            vals = []
            for prev_tg, tg, next_tg in sequence_slide(rest):
                assert isinstance(tg, TokensGroup)
                ttype = tg.ttype
                text = tg.text
                if ttype == OP:
                    if tg.is_terminator:
                        assert next_tg is None
                        break
                    elif text in (',', expected):
                        if val is None:
                            raise ValueError('%(tg)r: expected to have '
                                    'a value here; '
                                    'found %(val)r!'
                                    % locals())
                        val = None
                    else:
                        raise ValueError('Unexpected operator %(tg)r!'
                                % locals())
                elif val is None:
                    val = tg
                    vals.append(resolve_value(val))
                else:
                    raise ValueError('%(tg)r: surplus value; '
                            'expected a comma or closing brace! '
                            '(name=%(name)r, val=%(val)r)'
                            % locals())
            target_dict[use_key] = tip_factory(vals)


def amend_config_list(config, statement):
    """
    Use the given statement to append changes to the given config list
    """
    raise NotImplemented


if __name__ == '__main__':
    # if 0: (removed)
    # Standard library:
    import doctest
    doctest.testmod()
