from argparse import ArgumentParser, Namespace


def uvicorn_server_factory(parser: ArgumentParser):
    from fastapi import FastAPI
    argument_group = parser.add_argument_group(title='Uvicorn server arguments')
    argument_group.add_argument('-remote', action='store_true', help='should listen for remote connections')
    argument_group.add_argument('-port', type=int, help='port to listen on', default=8000)
    argument_group.add_argument('-logging_conf', help='path to json file with logging config',
                                default='talisman-tools/default_logging_conf.json')

    def launcher(app: FastAPI, args: Namespace) -> None:
        import logging.config
        import uvicorn
        from talisman_tools.configure.configure import read_json_config

        logging.config.dictConfig(read_json_config(args.logging_conf))
        host = "0.0.0.0" if args.remote else "127.0.0.1"
        uvicorn.run(app, host=host, port=args.port, log_config=None)

    return launcher
