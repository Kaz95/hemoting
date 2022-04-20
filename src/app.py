import base_classes
import CLI

"""Module for handling....handlers....probably...not sure yet. Definitely main entry point though"""

"""Remember: Receiver -> Command -> Invoker -> Client"""

if __name__ == '__main__':
    c_handler = base_classes.CommandSetHandler(CLI.CommandSet())
    i_handler = base_classes.InterfaceHandler(CLI.Interface(c_handler))

    app = base_classes.App(interface_handler=i_handler, cmd_handler=c_handler)
    app.run()
    # Initialize Handlers w/ chosen interface and command set
    # run via app -> interface handler -> interface
    # Command set is responsible for handling commands.
    # I can change command sets on the fly via handler
