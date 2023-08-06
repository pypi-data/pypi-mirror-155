from .apis.AzureAPI import AzureAPI
from .apis.GraphAPI import GraphAPI
from .apis.SalesForceAPI import SalesForceAPI
from .fourmatters import virtual_network, virtual_machine
from .logger.Logger import Logger
from .http.HttpListener import HttpListener
from . import gcp

def format(data, table_type):
    formatter_types = {
        'virtual_network_table_std': virtual_network.virtual_network_table_std,
        'virtual_machine_table_comprehensive': virtual_machine.virtual_machine_table_comprehensive 
    }
    return formatter_types.get(table_type).format(data)
    
    
