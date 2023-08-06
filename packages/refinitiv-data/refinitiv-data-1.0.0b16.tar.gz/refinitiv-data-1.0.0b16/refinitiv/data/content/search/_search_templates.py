"""Module to create and use templated search presets for the discovery search

Use templated search from the "Equity" template that was defined in the config:
>>> import refinitiv.data as rd
>>> rd.content.search._templates["Equity"].search()
"""
__all__ = ["templates"]

import operator
import string
import inspect
from functools import reduce
from typing import Iterable, Optional, Dict, Set, List, Any

from humps import depascalize

from refinitiv.data import get_config
from refinitiv.data.errors import ConfigurationError
from refinitiv.data.content.search._definition import Definition
from refinitiv.data.content.search._search_view_type import SearchViews

CONFIG_PREFIX = "search.templates"


def join_sets(sets: Iterable[set]) -> set:
    """Join multiple sets into one"""
    iterator = iter(sets)
    try:
        # Can't pass an empty iterator to `reduce`, that's the way to handle it
        default = next(iterator)
    except StopIteration:
        return set()
    else:
        return reduce(operator.or_, iterator, default)


def get_placeholders_names(template_string: str) -> Set[str]:
    """Get list of placeholder names in format-style string

    >>> get_placeholders_names("{a}, {b}, {a}")
    {'b', 'a'}
    """
    return set(x[1] for x in string.Formatter().parse(template_string) if x[1])


class SearchTemplate:
    """Discovery search preset

    Initialized with default values for content.search.Definition.
    Any string value acts as template string. You can use placeholder variables
    like for `str.format` method, and that variables will be required to prepare
    search parameters through `._search_kwargs()` or to launch search through `.search()`.

    Attributes
    ----------

    name: str
        name of the template

    Examples
    --------

    >>> SearchTemplate(filter="ExchangeName xeq '{name}'")._search_kwargs(name="<name>")
    {'filter': "ExchangeName xeq '<name>'"}
    >>> SearchTemplate(filter="ExchangeName xeq '{name}'")._search_kwargs()
    Traceback (most recent call last):
        ...
    KeyError: 'Those keyword arguments must be defined, but they are not: name'
    >>> SearchTemplate(filter="ExchangeName xeq '{name}'", placeholders_defaults={"name": "<name>"})._search_kwargs()
    {'filter': "ExchangeName xeq '<name>'"}
    """

    def __init__(
        self,
        name=None,
        placeholders_defaults: Optional[Dict[str, Any]] = None,
        **search_defaults,
    ):
        """
        Parameters
        ----------
        name : str, optional
            name of the template
        placeholders_defaults: dict, optional
            <placeholder_name> : <placeholder_default_value>
        search_defaults
            default values for discovery search Definition
        """
        # List search keyword arguments we can use in this template
        self._available_search_kwargs = inspect.signature(Definition).parameters.keys()
        # Default template variables values for a templated defaults
        self._placeholders_defaults = (
            {} if placeholders_defaults is None else placeholders_defaults
        )
        self.name = name

        unknown_defaults = set(search_defaults) - set(self._available_search_kwargs)
        if unknown_defaults:
            raise ValueError(
                "This arguments are defined in template, but not in search Definition: "
                + ", ".join(unknown_defaults)
            )

        # Set of placeholders names for each templated default
        self._placeholders_vars: Dict[str, Set[str]] = {
            name: get_placeholders_names(value)
            for name, value in search_defaults.items()
            if isinstance(value, str)
        }

        self._templated_defaults = {
            name: value
            for name, value in search_defaults.items()
            if self._placeholders_vars.get(name)
        }
        self._other_defaults = {
            name: value
            for name, value in search_defaults.items()
            if name not in self._templated_defaults
        }

        bad_tpl_var_names = (
            join_sets(self._placeholders_vars.values()) & self._available_search_kwargs
        )
        if bad_tpl_var_names:
            raise ValueError(
                "You can't use template arguments with the same name"
                " as search arguments. You are used: " + ", ".join(bad_tpl_var_names)
            )

    def __repr__(self):
        return f"<SearchTemplate '{self.name}'>"

    def _search_kwargs(self, **kwargs) -> dict:
        """Get dictionary of arguments for content.search.Definition"""

        non_redefined_templated_defaults = set(self._templated_defaults) - set(kwargs)
        current_templates = [
            name
            for name, value in self._templated_defaults.items()
            if name in non_redefined_templated_defaults and isinstance(value, str)
        ]

        template_vars_names = join_sets(
            var_names
            for template_name, var_names in self._placeholders_vars.items()
            if template_name in current_templates
        )

        undefined_placeholders = (
            template_vars_names - set(kwargs) - set(self._placeholders_defaults)
        )

        if undefined_placeholders:
            raise KeyError(
                "Those keyword arguments must be defined, but they are not: "
                + ", ".join(undefined_placeholders)
            )

        unexpected_arguments = (
            set(kwargs) - template_vars_names - self._available_search_kwargs
        )

        if unexpected_arguments:
            raise KeyError(f"Unexpected arguments: {', '.join(unexpected_arguments)}")

        kwargs = kwargs.copy()
        # Applying template variables defaults
        for name, value in self._placeholders_defaults.items():
            if name not in kwargs:
                kwargs[name] = value

        result = self._other_defaults.copy()

        # Apply variables to templated defaults
        for name in current_templates:
            result[name] = self._templated_defaults[name].format(**kwargs)

        # Apply other variables from kwargs
        for name, value in kwargs.items():
            if name not in template_vars_names:
                result[name] = value

        return result

    def search(self, **kwargs):
        return Definition(**self._search_kwargs(**kwargs)).get_data().data.df


class Templates:
    """Easy access to search templates from the library config

    Check if search template with the name "Equity" is defined in the config:
    >>> templates = Templates()
    >>> "Equity" in templates
    True
    Get "Equity" search template:
    >>> templates["Equity"]
    Get list of available search template names:
    >>> templates.keys()
    ["Equity"]
    """

    def __iter__(self):
        config = get_config()
        return config.get(CONFIG_PREFIX, {}).keys().__iter__()

    def __getitem__(self, name: str) -> SearchTemplate:
        config = get_config()
        key = f"{CONFIG_PREFIX}.{name}"
        if key not in config:
            raise KeyError(f"Template '{name}' is not found in the config")
        data = config[key].as_attrdict() if config[key] is not None else {}

        # <param_name>: {"default": <default>, "description": <doc>}
        tpl_strs_defaults = {
            name: attrs["default"]
            for name, attrs in data.get("parameters", {}).items()
            if "default" in attrs
        }
        params = depascalize(data.get("request_body", {}))

        if "view" in params:
            # Convert string value to enum for the view argument
            view = params["view"]
            try:
                params["view"] = getattr(SearchViews, depascalize(view).upper())
            except AttributeError:
                raise ConfigurationError(
                    -1,
                    f"Wrong search template value: View={view}. "
                    "It must be one of the following: "
                    f"{', '.join(SearchViews.possible_values())}",
                )
        return SearchTemplate(name, placeholders_defaults=tpl_strs_defaults, **params)

    def keys(self) -> List[str]:
        """Get list of available search template names"""
        return list(self)


templates = Templates()
