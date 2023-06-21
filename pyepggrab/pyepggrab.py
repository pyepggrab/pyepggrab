"""Main entry point of pyepggrab.

Functions and decorators in this module provides an easy-to-use interface for
writing grabbers. Automates of handling arguments, setting up logging,
create the config manager and supply it to your main and configure function.

Every grabber should use at least the `@grabber_main` decorator on the `main`
function and call the `pyepggrab_main()` when the grabber starts.
Highly recommended using the `@grabber_config` decorator on the
configuration function (if missing, the `main` called even if the
`--configure` is supplied).

If you need extra arguments in the grabber you can decorate that callback with
`@grabber_extraargs` and modify the passed `ArgumentParser` instance.

Writing grabber that not using these are possible but not recommended (if you
still want to do, use this as a reference).
"""

import sys
from argparse import Namespace
from json import JSONDecoder, JSONEncoder
from typing import Callable, ClassVar, List, NoReturn, Optional, Type

from pyepggrab import __about__
from pyepggrab.configbase import ConfigEncoder, ConfigRootBase, T
from pyepggrab.log import Log

from .args import ArgParser, ExtraargsType
from .configmanager import ConfigManager

MainType = Callable[[Namespace, ConfigManager], Optional[int]]


class Pyepggrab:
    """Pyepggrab convenience functions and decorators."""

    _grabber_main: ClassVar[Optional[MainType]] = None
    _grabber_config: ClassVar[Optional[MainType]] = None
    _grabber_extraargs: ClassVar[Optional[ExtraargsType]] = None

    @classmethod
    def grabber_main(cls, func: MainType) -> MainType:
        """Decorate the grabber main function with this.

        Called when grabber starts in normal operation.

        Callback signature:
        `def fun(args: Namespace, confman: ConfigManager) -> Optional[int]`
        """
        cls._grabber_main = func
        return func

    @classmethod
    def grabber_config(cls, func: MainType) -> MainType:
        """Decorate the grabber configuration function with this.

        Called when the `--configure` arg is supplied

        Callback signature:
        `def fun(args: Namespace, confman: ConfigManager) -> Optional[int]`
        """
        cls._grabber_config = func
        return func

    @classmethod
    def grabber_extraargs(cls, func: ExtraargsType) -> ExtraargsType:
        """Decorate a grabber function with this to add extra arguments.

        Decorator for callback that adds extra arguments to the argument parser.
        Good fit for adding grabber specific parameters.

        Callback signature: `def fun(argp: ArgumentParser) -> None`
        """
        cls._grabber_extraargs = func
        return func

    @classmethod
    def main(  # noqa: PLR0913
        cls,
        version: str,
        description: str,
        caps: List[str],
        config_root: Type[T] = ConfigRootBase,  # type: ignore # see:python/mypy#3737
        config_encoder: Type[JSONEncoder] = ConfigEncoder,
        config_decoder: Optional[Type[JSONDecoder]] = None,
        args_override: Optional[str] = None,
    ) -> NoReturn:
        """Call to start pyepggrab.

        This is the main entry point of pyepggrab.
        Calling this function can automate most of the task that required to start
        a grabber running. Automates of handling arguments, setting up logging,
        create the config manager and supply it to your main and configure function.

        If the `main` or `config` returns a number, this number is used as an
        exitcode, if return nothing exits with `0`.

        :param version: version of the grabber. Displayed on --version
        :param description: short description of the grabber.
            Used by `tv_find_grabbers`. Displayed on --description
        :param caps: XMLTV capabilities of the grabber. See: `args`
        :param config_root: type of the configuration root, if custom configuration
            used this should be changed. See: `configmanager`
        :param config_encoder: encoder for the config file, the default usually enough
        :param config_decoder: optional decoder for the config file, usually not needed
        :param args_override: override the supplied arguments. Do not use in production
        """
        Log.init_loggers()
        pyepggrablog = Log.get_pyepggrab_logger()
        pyepggrablog.debug("Starting pyepggrab %s", __about__.__version__)

        argparser = ArgParser(version, description, caps, cls._grabber_extraargs)
        args = argparser.parse_args(args_override)

        decor_confman = ConfigManager(
            path=args.config_file,
            root=config_root,
            encoder=config_encoder,
            decoder=config_decoder,
        )

        try:
            conf = decor_confman.read_config()
            if hasattr(conf, "options"):
                argparser.parser.set_defaults(**conf.options)
        except FileNotFoundError as fnf:
            pyepggrablog.warning(
                "Cannot read default options: Config file not found ('%s')",
                fnf.filename,
            )

        # Parse again to apply the contents of the config file
        args = argparser.parse_args(args_override)

        argparser.exec_common()
        Log.finalize_loggers()

        confman = decor_confman
        if args.configure and cls._grabber_config:
            pyepggrablog.debug("Starting configure")
            exitc = cls._grabber_config(args, confman)
        elif cls._grabber_main:
            if args.configure:
                pyepggrablog.debug(
                    "--configure parameter supplied, but config callback is None."
                    "Not calling it",
                )
            pyepggrablog.debug("Starting main")
            exitc = cls._grabber_main(args, confman)
        else:
            msg = "At least @grabber_main is required if you are using pyepggrab_main()"
            raise TypeError(msg)

        if exitc:
            sys.exit(exitc)

        sys.exit(0)
