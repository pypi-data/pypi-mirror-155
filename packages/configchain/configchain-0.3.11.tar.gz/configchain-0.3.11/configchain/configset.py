from functools import singledispatch
from itertools import chain
from typing import List, Optional
from collections import OrderedDict, abc
from operator import add
import re

from .config import Config
from .loader import ConfigLoader
from .snippet import ConfigSnippet
from .types import ConfigFile, WILDCARD, ConfigName, ConfigChainOptions
from .utils import dict_merge_with_wildcard, merge_profile_with_wildcard


class ConfigSet(OrderedDict):
    @classmethod
    def load(cls, *args: ConfigFile, **kwargs: ConfigChainOptions) -> "ConfigSet":
        loader = ConfigLoader(*args, **kwargs)
        loader.load()

        named_snippets = OrderedDict()
        for snippet in chain(*loader.values()):
            named_snippets.setdefault(
                get_config_name(kwargs.get("name", WILDCARD), snippet), [],
            ).append(snippet)

        named_configs = {
            name: Config.from_snippets(snippets, **kwargs)
            for name, snippets in named_snippets.items()
        }

        merge_profile_with_wildcard(named_configs)
        return cls(named_configs)

    def __add__(self, other: "ConfigSet") -> "ConfigSet":
        return dict_merge_with_wildcard(self, other, add)

    def config_names(self) -> List[ConfigName]:
        return self.keys()


@singledispatch
def get_config_name(_getter, _snippet: ConfigSnippet) -> ConfigName:
    return WILDCARD


@get_config_name.register
def _(config_name_getter: abc.Callable, snippet: ConfigSnippet) -> ConfigName:
    return config_name_getter(snippet)


@get_config_name.register
def _(config_name_statement: str, snippet: ConfigSnippet) -> ConfigName:
    reg = r"\${(\w+)}"
    matches = re.findall(reg, config_name_statement)
    vars = {v: snippet.find(v) for v in matches}
    if (
        len(matches) > 0
        and len(
            [
                exist
                for exist in [vars.get(m, None) for m in matches]
                if exist is not None
            ]
        )
        == 0
    ):
        return WILDCARD

    def sub(var):
        (key,) = var.groups()
        return str(vars.get(key, None))

    return re.sub(reg, sub, config_name_statement)


@get_config_name.register
def _(config_name_keys: abc.MutableSequence, snippet: ConfigSnippet) -> ConfigName:
    ids = [
        str(n) for n in [snippet.find(key) for key in config_name_keys] if n is not None
    ]
    if ids:
        return "-".join(ids)
    else:
        return WILDCARD
