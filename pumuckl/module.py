from pyparsing import QuotedString, Suppress
from semantic_version import Version
import asyncio
import aiohttp
import json


class Module():
    def __init__(self, user, mod_name, version, forge_url='https://forge.puppetlabs.com'):
        self.user = user
        self.mod_name = mod_name
        self.version = version
        self.forge_url = forge_url
        self.forge_version = '0.0.0'

    @property
    def current_version_url(self):
        return '{}/users/{}/modules/{}/releases/find.json'.format(self.forge_url, self.user, self.mod_name)

    @property
    def is_up_to_date(self):
        return not Version(self.version) < Version(self.forge_version)

    @asyncio.coroutine
    def fetch_version(self):
        response = yield from self.request_version()
        self.forge_version = json.loads(response.decode('utf-8'))['version']
        return self

    @asyncio.coroutine
    def request_version(self):
        response = yield from aiohttp.request('GET', self.current_version_url)
        return (yield from response.read_and_close(decode=True))

    @classmethod
    def parse_puppetfile_forge_mods(cls, file_contents):
        mod_kwargs = {}
        quotedString = QuotedString('"') ^ QuotedString('\'')

        forge_url_grammar = Suppress('forge') + quotedString
        for url, in forge_url_grammar.searchString(file_contents):
            mod_kwargs['forge_url'] = url

        mod_grammar = Suppress('mod') + quotedString + Suppress(',') + quotedString
        mods = mod_grammar.searchString(file_contents)
        for mod, version in mods:
            user, mod_name = mod.split('/')
            yield cls(user, mod_name, version, **mod_kwargs)

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False

        return self.user == other.user and self.mod_name == other.mod_name \
            and self.version == other.version \
            and self.forge_url == other.forge_url

