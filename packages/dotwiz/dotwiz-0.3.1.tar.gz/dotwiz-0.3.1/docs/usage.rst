=====
Usage
=====

To use ``dotwiz`` in a project::

    import dotwiz


:class:`DotWizPlus`
-------------------

Simple usage with :class:`DotWizPlus` to illustrate how keys with invalid characters
are made safe for attribute access:

.. code:: python3

    from dotwiz import DotWizPlus

    dw = DotWizPlus({
        'items': {
            'camelCase': 1,
            'TitleCase': 2,
            'Spinal-Case': 3,
            'To': {'1NFINITY': {'AND': {'Beyond  !! ': True}}},
            '1abc': 4,
            '42': 5,
            'Hello !@#&^+  W0rld   !!!': 'test',
        }
    })

    print(dw)
    # prints the following, on a single line:
    # >  ✪(items_=✪(camel_case=1, title_case=2, spinal_case=3,
    #               to=✪(_1nfinity=✪(and_=✪(beyond=True))),
    #                    _1abc=4, _42=5, hello_w0rld='test'))

    # confirm that we can access keys by dot (.) notation
    assert dw.items_.to._1nfinity.and_.beyond
    assert dw.items_._1abc == 4

    # the original keys can also be accessed like a normal `dict`, if needed
    assert dw['items']['To']['1NFINITY']['AND']['Beyond  !! ']

    print(dw.to_dict())
    # >  {'items': {'camelCase': 1, 'TitleCase': 2, ...}}

    print(dw.to_attr_dict())
    # >  {'items_': {'camel_case': 1, 'title_case': 2, ...}}

Complete Example
~~~~~~~~~~~~~~~~

Example with :func:`make_dot_wiz_plus` to illustrate how :class:`DotWizPlus`
mutates keys with invalid characters to a safe, *snake-cased* format:

.. code:: python3

    from dotwiz import make_dot_wiz_plus

    dw = make_dot_wiz_plus(
        [
            # 1: reserved `keywords`
            ('class', 1), ('for', 1), ('lambda', 1), ('pass', 1),
            # 2: overwriting `dict` or `DotWizPlus` method names
            ('to_dict', 2), ('items', 2), ('keys', 2), ('copy', 2), ('values', 2),
            # 3: invalid identifiers
            ('99', 3), ('1abc', 3), ('x+y', 3),
            ('This  @!@# I!@#$%^&*()[]{};:"\'<,>.?/s    a test.', 3),
            ('Hello !@#&^+  W0rld   !!!', 3),
            # 4: special-cased keys
            ('Title Case', 4), ('SCREAMING_SNAKE_CASE', 4),
            ('camelCase', 4), ('PascalCase', 4), ('spinal-case', 4),
        ],
    )

    print(dw)
    # prints the following, on a single line:
    # >  ✪(class_=1, for_=1, lambda_=1, pass_=1,
    #      to_dict_=2, items_=2, keys_=2, copy_=2, values_=2,
    #      _99=3, _1abc=3, x_y=3, this_i_s_a_test=3, hello_w0rld=3,
    #      title_case=4, screaming_snake_case=4, camel_case=4, pascal_case=4, spinal_case=4)

    print(dw.to_dict())
    # >  {'class': 1, 'for': 1, ...}

    print(dw.to_attr_dict())
    # >  {'class_': 1, 'for_': 1, ...}

    # confirm that retrieving keys from the `DotWizPlus` instance by
    # attribute (dot) access works as expected.
    assert dw.class_ == dw.for_ == dw.lambda_ == dw.pass_ == 1
    assert dw.to_dict_ == dw.items_ == dw.keys_ == dw.copy_ == dw.values_ == 2
    assert dw._99 == dw._1abc == dw.x_y == dw.this_i_s_a_test == dw.hello_w0rld == 3
    assert dw.title_case == dw.screaming_snake_case == \
           dw.camel_case == dw.pascal_case == dw.spinal_case == 4
