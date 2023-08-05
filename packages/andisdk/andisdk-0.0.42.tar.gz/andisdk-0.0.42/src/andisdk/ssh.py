"""
andi.ssh
============

Helper module to handle SSH (Secure Shell) implementation.
See documentation for more details :doc:`/Tutorials/ssh`.
"""
try:
    import clr
    clr.AddReference('PrimaTestCaseLibrary')
    from PrimaTestCaseLibrary.Utils.SSH import SshClient as _SC
    
    class SshClient(_SC):
        def __init__(self, **kwargs):
             for (name, value) in list(kwargs.items()):
                if hasattr(self, name):
                    setattr(self, name, value)
                else:
                    raise TypeError("__init__() got an unexpected keyword argument '{}'".format(name))

        def __enter__(self):
            self.connect()
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.disconnect()
                

except ImportError:

    class SshClient:
        def __init__(self, **kwargs):
            """
                specifies an SSH Client socket object
            """
            pass
            
        def connect(self):
            """
            tried to open connection.
            """
            pass

        def disconnect(self):
            """
            tried to disconnect client.
            """
            pass

        def start_command(self, command):
            """
            starts an ssh command.
            Args:
                command : The command to be executed.
            Returns:
                the created command.
            Return Type:
                :py:class:`SshCommand`
            """
            pass
        def execute_command(self, command):
            """
            executed an ssh command adn returns the output.
            Args:
                command : The command to be executed.
            Returns:
                the output of the executed command.
            Return Type:
                :py:class:`str`
            """
            pass
        def __enter__(self):
            self.connect()
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.disconnect()
    
    
__all__ = ['SshClient']
