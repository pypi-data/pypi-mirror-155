# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Luckysheet(Component):
    """A Luckysheet component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- data (boolean | number | string | dict | list; optional):
    data shown by the component.

- style (boolean | number | string | dict | list; optional):
    additional style options.

- xlsx (boolean | number | string | dict | list; optional):
    data of an xlsx file."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_luckysheet'
    _type = 'Luckysheet'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, data=Component.UNDEFINED, xlsx=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'style', 'xlsx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'style', 'xlsx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Luckysheet, self).__init__(**args)
