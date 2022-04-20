import base_classes
import CLI

"""Module for handling....handlers....probably...not sure yet. Definitely main entry point though"""

"""Remember: Receiver -> Command -> Invoker -> Client"""


class InterfaceHandler:
    pass


class CommandSetHandler:
    def __init__(self, command_set: base_classes.CommandSet):
        self.command_set = command_set
        self.command_set.register_command(self.ls, 1, "Lists all current commands in the current command set.",
                                          ['ls', 'list'])

    @staticmethod
    def _split_input(user_input):
        split_input = user_input.split()
        match split_input:
            case [cmd, *args]:
                return [cmd, args]
            case _:
                print('invalid input')

    def handle_command(self, user_input):
        cmd, args = CommandSetHandler._split_input(user_input)
        receiver_info = self.command_set.get_receiver_info(cmd)
        receiver = receiver_info.receiver
        # Make sure receiver is called without args if needed.
        # I suppose I might have been better off making all receivers accept *args, no matter what.
        if receiver_info.number_of_args == 0 or len(args) == 0:
            receiver()
        else:
            receiver(args)

    def ls(self, option=None):
        if option:
            option = option[0]
            self.ls_option(option)
        else:
            self.command_set.list_commands()

    def ls_option(self, option):
        cmd = self.command_set.command_info_registry[option]
        print(f'Command: {option}')
        print(f'Description: {cmd.description}')
        print(f'Aliases: {cmd.aliases}')


# This could easily be a 'main' function. A class allows for namespacing, holding state(settings), and the coupling
# of logic to the aforementioned state. Consider if this is the best solution later.
class App:
    pass


if __name__ == '__main__':
    cmd_set = CLI.CommandSet()
    cmd_handler = CommandSetHandler(cmd_set)
    interface_handler = CLI.Interface()
    while True:

        u_input = interface_handler.run()
        if u_input == 'q':
            break
        # u_input = 'run 2022-2-2'
        cmd_handler.handle_command(u_input)

    # Initialize Handlers w/ chosen interface and command set
    # run interface via handler
    # Command set is responsible for handling commands.
    # I can change command sets on the fly via handler
    pass
