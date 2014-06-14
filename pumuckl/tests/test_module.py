import unittest
from pumuckl.module import Module


class TestModule(unittest.TestCase):
    """docstring for ModuleTest"""

    def setUp(self):
        self.module = Module('mayflower', 'php', '1.0.1')

    def test_init(self):
        self.assertEqual('mayflower', self.module.user)
        self.assertEqual('php', self.module.mod_name)
        self.assertEqual('1.0.1', self.module.version)

    def test_current_version_url(self):
        self.assertEqual(
            'https://forge.puppetlabs.com/users/mayflower/modules/php/releases/find.json',
            self.module.current_version_url
        )

    def test_is_up_to_date(self):
        self.module.forge_version = '1.0.1'
        self.assertTrue(self.module.is_up_to_date)
        self.module.forge_version = '1.0.2'
        self.assertFalse(self.module.is_up_to_date)

    def test_parse_puppetfile_forge_mods(self):
        puppetfile = '''
forge "http://fnordforge"

mod 'mayflower/php',     '1.0.1'
mod 'mayflower/prosody', '0.1.3'
'''
        mods = list(Module.parse_puppetfile_forge_mods(puppetfile))
        expected_mods = [
            Module('mayflower', 'php', '1.0.1', forge_url='http://fnordforge'),
            Module('mayflower', 'prosody', '0.1.3', forge_url='http://fnordforge')
        ]
        self.assertEqual(expected_mods, mods)

