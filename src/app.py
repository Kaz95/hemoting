import base_classes
import CLI
import core

"""Module for handling....handlers....probably...not sure yet. Definitely main entry point though"""

"""Remember: Receiver -> Command -> Invoker -> Client"""

if __name__ == '__main__':
    core = core.CoreEngine()
    cmd_handler = base_classes.CommandSetHandler(CLI.CommandSet(core))
    interface_handler = base_classes.InterfaceHandler(CLI.Interface(cmd_handler))

    app = base_classes.App(interface_handler=interface_handler, cmd_handler=cmd_handler)
    app.run()
    # Initialize Handlers w/ chosen interface and command set
    # run via app -> interface handler -> interface
    # Command set is responsible for handling commands.
    # I can change command sets on the fly via handler
