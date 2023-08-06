"""Strangeworks SDK"""

import importlib.metadata

from .auth import auth
from .client import Client

__version__ = importlib.metadata.version("strangeworks")

client = Client()  # instantiate a client on import by default

# strangeworks.(public method)
authenticate = client.authenticate
login = auth.Login
rest_client = client.rest_client
circuit_runner = client.circuit_runner
backends_service = client.backends_service
