from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory


def configure_train_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    reader_factory = get_reader_factory(parser, include_dev=True)

    parser.add_argument('config_path', type=str, metavar='<config.json>', help='Path to training configuration file')
    parser.add_argument('out_model_path', type=str, metavar='<out model path>', help='Path to save trained model to')

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            from .action import train
            extra_actions(args)
            train_reader, dev_reader = reader_factory(args)
            train(train_reader, dev_reader, args)

        return action

    parser.set_defaults(action=get_action)
