import asyncio
import unittest
from unittest.mock import patch
import sys
import types

# Provide a dummy discord module so nuke_server can be imported without the
# real dependency installed.
discord_stub = types.ModuleType('discord')

class DummyIntents:
    @classmethod
    def default(cls):
        return cls()

discord_stub.Intents = DummyIntents

class DummyClient:
    def __init__(self, *args, **kwargs):
        pass

    def event(self, func):
        return func

discord_stub.Client = DummyClient
discord_stub.utils = types.SimpleNamespace(get=lambda *args, **kwargs: None)
discord_stub.PermissionOverwrite = type('PermissionOverwrite', (), {})

sys.modules.setdefault('discord', discord_stub)

tqdm_stub = types.ModuleType('tqdm')
tqdm_stub.tqdm = lambda *args, **kwargs: None
sys.modules.setdefault('tqdm', tqdm_stub)

from nuke_server import async_input

class TestAsyncInput(unittest.IsolatedAsyncioTestCase):
    @patch('builtins.input', return_value='5')
    async def test_async_input_returns_value(self, mock_input):
        result = await asyncio.wait_for(async_input('Enter:'), timeout=1)
        self.assertEqual(result, '5')

if __name__ == '__main__':
    unittest.main()
