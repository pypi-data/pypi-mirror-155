import collections
import argparse
import inspect
import sys
from functools import wraps, partial as ft_partial
from typing import (
    Callable,
    Generator,
    Iterable,
    Optional,
    Union,
    Sequence,
    Tuple,
    Dict,
    cast,
    Any,
    TypeVar,
    FrozenSet,
)
import pprint

from libbiomedit.lib.classify import is_optional, IsTypingType
from libbiomedit.lib.deserialize import optional_type as _libbiomedit_optional_type

# Python 3.7: Protocol is not present in the base typing module for
# python versions <= 3.7, and must be imported from typing_extensions.
# NOTE: mypy does not accept the "try: ... except ImportError:" syntax for
# importing Protocol.
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


class ParserLike(Protocol):
    """Protocol interface to define a generic parser that has both the
    add_argument and add_mutually_exclusive_group methods.
    This allows the ParserLike class to impersonate objects from both the
    argparse.ArgumentParser and argparse._MutuallyExclusiveGroup classes.
    """

    def add_argument(self, *args: Any, **kwargs: Any) -> argparse.Action:
        """Add an argument to the parser. This is the same as the original
        argparse.ArgumentParser.add_argument() method.
        """

    def add_mutually_exclusive_group(self, required: bool = True) -> "ParserLike":
        """Create a new (sub)parser for the current parser, to which a group of
        mutually exclusive arguments can be added.
        """


class SubcommandParserBuilder(Protocol):
    """Protocol interface to define a generic subcommand parser factory object
    that is used to impersonate the argparse._SubParsersAction class.
    """

    def add_parser(self, name: str, **kwargs: Any) -> Any:
        """argparse.ArgumentParser argparse._MutuallyExclusiveGroup"""


class Argument:
    """Command line argument that can be added to a CLI parser."""

    def __init__(self, *args: Any, **kwargs: Any):
        self.args = args
        self.kwargs = kwargs

    def add_to_parser(self, parser: ParserLike) -> None:
        parser.add_argument(*self.args, **self.kwargs)

    @classmethod
    def primitive(
        cls, dest: str, arg_names: Iterable[str], **kwargs: Any
    ) -> Tuple["Argument"]:
        return (cls(*arg_names, dest=dest, **kwargs),)

    @classmethod
    def boolean(
        cls, dest: str, arg_names: Iterable[str], positional: bool, **kwargs: Any
    ) -> Tuple[Union["Argument", "ArgumentMutExGroup"]]:
        if positional:
            return cls.positional_boolean(dest, arg_names, **kwargs)
        return (cls.keyword_boolean(dest, arg_names, **kwargs),)

    @classmethod
    def positional_boolean(
        cls, dest: str, arg_names: Iterable[str], **kwargs: Any
    ) -> Tuple["Argument"]:
        return cls.primitive(dest, arg_names, type=parse_bool, **kwargs)

    @classmethod
    def keyword_boolean(
        cls,
        dest: str,
        arg_names: Iterable[str],
        default: bool = False,
        help: Optional[str] = None,  # pylint: disable=redefined-builtin
        **kwargs: Any,
    ) -> "ArgumentMutExGroup":
        kwargs.pop("required", None)
        long_arg_names = tuple(filter(lambda n: n.startswith("--"), arg_names))
        short_arg_names = tuple(filter(lambda n: n not in long_arg_names, arg_names))
        negation_flags = tuple(a.replace("--", "--no-") for a in long_arg_names)
        default_flags = arg_names if default else negation_flags
        if short_arg_names and default:
            raise ValueError(
                "booleans with short argument name and default=True are not supported."
            )
        if help:
            help += " "
        else:
            help = ""
        help += f"(disable with {', '.join(negation_flags)}, default: {', '.join(default_flags)})"
        return ArgumentMutExGroup(
            cls(
                *arg_names,
                action="store_true",
                dest=dest,
                default=default,
                help=help,
                **kwargs,
            ),
            cls(
                *negation_flags,
                action="store_false",
                default=default,
                dest=dest,
                help=argparse.SUPPRESS,
            ),
        )


class ArgumentMutExGroup:
    """Group of mutually exclusing arguments that can be added to a CLI parser."""

    def __init__(self, *args: Argument):
        self.args = args

    def add_to_parser(self, parser: ParserLike) -> None:
        grp = parser.add_mutually_exclusive_group()
        for arg in self.args:
            arg.add_to_parser(grp)


class SubcommandBase:
    """Abstract definition (interface) for a single subcommand of a CLI.
    Objects derived from this class are accepted as input for the "subcommands"
    property of CliWithSubcommands.
    """

    def __init__(
        self,
        name: str,
        action: Callable[..., Any],
        arguments: Sequence[Union[Argument, ArgumentMutExGroup]],
        help: Optional[str] = None,  # pylint: disable=redefined-builtin
    ):
        self.name = name
        self.help = help
        self.action = action
        self.arguments = arguments

    def add_to_parser(
        self,
        parser_factory: SubcommandParserBuilder,
        actions: Dict[str, Callable[..., Any]],
    ) -> None:
        """Add the subcommand to the main parser via a parser_factory object
        that belongs to the main parser.

        :param parser_factory:
        :param actions:
        """

    def add_arguments(self, parser: ParserLike) -> None:
        """Add arguments of subcommand to the specified argument parser - which
        must be derived from the main (top level) parser of the CLI.
        The argument parser will typically be the parser for the subcommand or
        a parser for a group of arguments.
        """
        for arg in self.arguments:
            arg.add_to_parser(parser)


class Subcommand(SubcommandBase):
    """A single subcommand corresponding to a function f of the main workflow."""

    def __init__(self, f: Callable[..., Any], **kwargs: Any):
        omit = frozenset(getattr(f, "keywords", ()))
        omit_pos = frozenset(range(len(getattr(f, "args", ()))))
        args = arguments_by_signature(
            f, omit_positionals=omit_pos, omit_keywords=omit, **kwargs
        )
        super().__init__(
            name=kebab_case(f.__name__), action=f, arguments=tuple(args), help=f.__doc__
        )

    def add_to_parser(
        self,
        parser_factory: SubcommandParserBuilder,
        actions: Dict[str, Callable[..., Any]],
    ) -> None:
        # Register the name and function (action) of the current subcommand
        # in the "actions" dict of the command line.
        actions[self.name] = self.action

        # Create a new parser for the subcommand and add all of the
        # subcommand's arguments to it.
        subcommand_parser = parser_factory.add_parser(self.name, help=self.help)
        self.add_arguments(parser=subcommand_parser)


class SubcommandGroup(SubcommandBase):
    """A subcommand consisting of multiple subsubcommands corresponding
    to functions without arguments.
    """

    def __init__(
        self,
        name: str,
        *functions: Any,
        help: Optional[str] = None,  # pylint: disable=redefined-builtin
    ):
        def call(f: Callable[[], Any]) -> None:
            f()

        args = (
            Argument("--" + f.__name__, action="store_const", dest="f", const=f)
            for f in functions
        )
        super().__init__(name=name, action=call, arguments=tuple(args), help=help)

    def add_to_parser(
        self,
        parser_factory: SubcommandParserBuilder,
        actions: Dict[str, Callable[..., Any]],
    ) -> None:
        # Register the name and function (action) of the current subcommand
        # in the "actions" dict of the command line.
        actions[self.name] = self.action

        # Create a new argument group parser for the subcommand and add all of
        # the subcommand's arguments to it.
        subcommand_parser = parser_factory.add_parser(self.name, help=self.help)
        arg_group = subcommand_parser.add_mutually_exclusive_group(required=True)
        self.add_arguments(parser=arg_group)


class CliWithSubcommands:
    """Entry point to command line interfaces. This is the class that
    instantiates the main (top level) parser for the CLI, that invokes it, and
    retrieves the values passed by the user on the command line.

    Subcommands can be added by creating a new class derived from this class
    and passing the subcommands as 'Subcommand' objects to the static
    :subcommands: variable.

    Example:

        class Cli(CliWithSubcommands):
            subcommands =

    Tu run the CLI, simply instantiate a new instance of the class: "Cli()".
    """

    description: Optional[str] = None
    required = True
    subcommands: Tuple[SubcommandBase, ...] = ()
    version: Optional[str] = None

    def __init__(self, *args: Any, **kwargs: Any):
        # Create the main parser object for the command line, as well as a
        # dict object "actions" that will be used to store the function
        # associated to each subcommand.
        parser = argparse.ArgumentParser(
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        actions: Dict[str, Callable[..., Any]] = {}

        # Add the --version argument to the command line.
        if self.version is not None:
            parser.add_argument("--version", action="version", version=self.version)

        # Add subcommands to the command line.
        subparser_factory = parser.add_subparsers(
            dest="action", help="Action help", required=self.required
        )
        for cmd in self.subcommands:
            cmd.add_to_parser(parser_factory=subparser_factory, actions=actions)

        # Retrive command line arguments passed by the user.
        cmd_args = vars(parser.parse_args(*args, **kwargs))

        # Run the function corresponding to the subcommand passed by the user.
        action = actions[cmd_args.pop("action")]
        action(**cmd_args)


# Starting with python 3.7, the typing module has a new API.
_origin_attr = "__extra__" if sys.version_info < (3, 7) else "__origin__"


# T is used as generic variable type.
T = TypeVar("T")


def default_args(default: T) -> Dict[str, Union[bool, T]]:
    if default is inspect.Signature.empty:
        return {"required": True}
    return {"default": default}


def arguments_by_signature(
    f: Callable[..., Any],
    overrides: Optional[Dict[str, Any]] = None,
    omit_keywords: FrozenSet[str] = frozenset(),
    omit_positionals: FrozenSet[int] = frozenset(),
) -> Generator[Union[Argument, ArgumentMutExGroup], None, None]:
    """Builds argparser arguments according to the signature of a function f.
    Type hint annotations are used to infer the type for argparse.
    """
    sig = inspect.signature(f)

    if overrides is None:
        overrides = {}
    unknown_parameters = set(overrides) - set(sig.parameters)
    if unknown_parameters:
        raise ValueError(
            f"Function {f.__name__} does not have arguments {', '.join(unknown_parameters)} "
            f"(which have been provided as parameter docs)"
        )
    has_keyword_only = any(
        p.kind is inspect.Parameter.KEYWORD_ONLY for p in sig.parameters.values()
    )
    for pos, (p_name, p) in enumerate(sig.parameters.items()):
        if p_name in omit_keywords or pos in omit_positionals:
            continue
        positional = has_keyword_only and p.kind is not inspect.Parameter.KEYWORD_ONLY
        p_overrides = overrides.get(p_name, {})
        arg_names = make_arg_names(
            p_overrides.get("name", kebab_case(p_name) if not positional else p_name),
            p_overrides.get("alias", ()),
            positional,
        )
        default = p_overrides.get("default", p.default)
        args = dict(help=p_overrides.get("help"))
        t = p_overrides.get("type", p.annotation)
        if t is inspect.Signature.empty:
            raise ValueError(f"Argument {arg_names[0]} has no type hint")
        try:
            t = unwrap_opt(t, default)
        except ValueError as e:
            raise ValueError(f"{f.__name__}: {p_name}: {e}") from None

        if not positional:
            args["dest"] = p_overrides.get("dest", p_name)
            args.update(default_args(default))
        if t is bool:
            yield from Argument.boolean(
                arg_names=arg_names, positional=positional, **args
            )
            continue
        if is_sequence(t):
            t = getattr(t, "__args__", (str,))[0]
            if default is not inspect.Signature.empty:
                args["default"] = default
            if positional:
                args["nargs"] = "+" if default is inspect.Signature.empty else "*"
            else:
                args["action"] = "append"
        yield Argument(*arg_names, type=t, **args)


def make_arg_names(
    name: str, aliases: Iterable[str], positional: bool
) -> Tuple[str, ...]:
    """Combines name and aliases into one tuple of argument names
    including "--".
    """
    n_dashes = min(2, len(name))
    arg_prefix = "-" * n_dashes
    if positional:
        if aliases:
            raise ValueError("Aliases are not allowed for positional arguments.")
        arg_prefix = ""
    arg_names = (arg_prefix + name,)
    if isinstance(aliases, str):
        aliases = (aliases,)
    return arg_names + tuple(aliases)


def parse_bool(s: str) -> bool:
    """Returns True is the evaluated string is considered to represent the
    value True, and False if not.
    """
    bool_true_literals = ("1", "true", "y", "yes")
    bool_false_literals = ("0", "false", "n", "no")
    bool_literal_mapping = dict(
        [(l, True) for l in bool_true_literals]
        + [(l, False) for l in bool_false_literals]
    )
    return bool_literal_mapping[s]


def is_sequence(t: Any) -> bool:
    t_origin = getattr(t, "__origin__", None)
    return isinstance(t_origin, type) and issubclass(t_origin, collections.abc.Sequence)


# R is used as generic type for return values.
R = TypeVar("R")


def decorate(
    f: Callable[..., R], *decorators: Callable[[Callable[..., R]], Callable[..., R]]
) -> Callable[..., R]:
    """Apply one or more decorator functions to the input function f. This
    allows to decorate a function in those cases where the @decorator() syntax
    cannot be used.
    """
    for dec in decorators:
        f = dec(f)
    return f


def partial(
    *args: Any, **kwargs: Any
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Modified version of :functools.partial: which preserves the __name__
    and __doc__ attributes and can be used as a decorator.
    """

    def decorator(f: Callable[..., R]) -> Callable[..., R]:
        keywords = getattr(f, "keywords", {})
        f_new = ft_partial(f, *args, **{**keywords, **kwargs})
        setattr(f_new, "__name__", f.__name__)
        f_new.__doc__ = f.__doc__
        return f_new

    return decorator


def lazy_partial(
    *args: Any, **kwargs: Any
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Similar to :functools.partial: but loads the bound arguments at runtime
    of the wrapped function, by calling the arguments.
    """

    def decorator(f: Callable[..., R]) -> Callable[..., R]:
        @wraps(f)
        def wrapped_f(*_args: Any, **_kwargs: Any) -> R:
            newkeywords = {key: val() for key, val in kwargs.items()}
            newkeywords.update(_kwargs)
            return f(*[f() for f in args], *_args, **newkeywords)

        # NOTE: somehow mypy does not accept creating a new attribute for a
        # function using the syntax "function.new_attribute = value", so
        # "setattr()" is used instead.
        setattr(wrapped_f, "args", getattr(f, "args", ()) + args)
        new_keywords = getattr(f, "keywords", {})
        new_keywords.update(kwargs)
        setattr(wrapped_f, "keywords", new_keywords)

        return wrapped_f

    return decorator


def set_default(
    **defaults: Any,
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Sets or changes default values of the decorated function."""

    def decorator(f: Callable[..., R]) -> Callable[..., R]:
        @wraps(f)
        def wrapped_f(*args: Any, **kwargs: Any) -> R:
            return f(*args, **{**defaults, **kwargs})

        return wrapped_f

    return decorator


def rename(name: str) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Changes the name of the decorated function."""

    def decorator(f: Callable[..., R]) -> Callable[..., R]:
        def wrapped_f(*args: Any, **kwargs: Any) -> R:
            return f(*args, **kwargs)

        wrapped_f.__name__ = name
        return wrapped_f

    return decorator


def block(*arg_names: str) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Hides the arguments of a function from arguments_by_signature."""

    def wrapper(f: Callable[..., R]) -> Callable[..., R]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> R:
            return f(*args, **kwargs)

        keywords = getattr(wrapped, "keywords", {})
        keywords.update({n: object() for n in arg_names})
        setattr(wrapped, "keywords", keywords)
        return wrapped

    return wrapper


def return_to_stdout(f: Callable[..., Any]) -> Callable[..., None]:
    """Converts a function :f: into a function pretty printing the return value
    of :f: and returning None.
    """
    pp = pprint.PrettyPrinter(indent=2)

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        pp.pprint(f(*args, **kwargs))

    return wrapper


def kebab_case(name: str) -> str:
    return name.replace("_", "-")


def unwrap_opt(t: type, default: Any) -> type:
    opt_type = optional_type(t)
    if opt_type is None:
        return t
    if default is inspect.Signature.empty:
        raise ValueError(
            "typing.Optional arguments are allowed only when accompanied by "
            "a default value."
        )
    return opt_type


def optional_type(type_obj: type) -> Optional[type]:
    """For Optional types provided by typing, return the underlying python
    type. If the type_obj is not an optional type, return None.

    Example: the function will return 'int' for 'typing.Optional[int]'.
    """
    if not is_optional(type_obj):
        return None
    return _libbiomedit_optional_type(cast(IsTypingType, type_obj))
