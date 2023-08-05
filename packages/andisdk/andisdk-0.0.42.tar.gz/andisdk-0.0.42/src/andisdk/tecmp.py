"""
andi.tecmp
============

Helper module for extract TECMP status messages from ethernet messages and return the parsed status.
See documentation for more details :doc:`/Tutorials/TECMP`.	
"""
try:
  import clr
  clr.AddReference('PrimaTestCaseLibrary')
  from PrimaTestCaseLibrary.Utils import TecmpUtils as _TecmpUtils
except ImportError:
  pass    

def get_cm_status(message):
	"""
	Get capture module status from an ethernet message.
    Args:
        message(:py:class:`MessageEthernet`) : The received ethernet message.
    Returns:
        :py:class:`CmStatus` object if message is a valid tecmp capture module status message otherwise 'none'.
    Return Type:
        :py:class:`CmStatus`
	"""
	return _TecmpUtils.TecmpStatusDecoder.GetCmStatus(message)
def get_bus_status(message):
	"""
	Get bus status from an ethernet message.
    Args:
        message(:py:class:`MessageEthernet`) : The received ethernet message.
    Returns:
        :py:class:`BusStatus` object if message is a valid tecmp bus status message otherwise 'none'.
    Return Type:
        :py:class:`BusStatus`
	"""
	return _TecmpUtils.TecmpStatusDecoder.GetBusStatus(message)

__all__ = ['get_cm_status', 'get_bus_status']