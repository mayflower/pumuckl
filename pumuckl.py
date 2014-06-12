import asyncio
import aiohttp
import click
import json
import sys
from semantic_version import Version
from pyparsing import QuotedString, Suppress


@click.command()
@click.argument('puppetfile', type=click.File(),
                required=False, default='Puppetfile')
@click.option('-v', '--verbose', is_flag=True,
              help='Enable verbose mode.')
def cli(puppetfile, verbose):
    """This script checks a Puppetfile for modules with an outdated version."""
    loop = asyncio.get_event_loop()
    mods = parse_puppetfile_forge_mods(puppetfile.read())
    f = asyncio.gather(*[check_version(*mod) for mod in mods])
    loop.run_until_complete(f)

    up_to_date, outdated = get_filtered_result(f.result())
    display_result(up_to_date, outdated, verbose=verbose)

    if outdated:
        sys.exit(1)


def get_filtered_result(result):
    up_to_date = filter(lambda res: not res[4], result)
    outdated = filter(lambda res: res[4], result)
    return list(up_to_date), list(outdated)


def display_result(up_to_date, outdated, *, verbose):
    if verbose:
        for res in up_to_date:
            click.secho('{}/{} at {} = {}'.format(*res), fg='green')
    for res in outdated:
        click.secho('{}/{} at {} < {}'.format(*res), fg='red')
    if not outdated:
        click.secho('All modules are up-to-date', fg='green')


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


def parse_puppetfile_forge_mods(content):
    mod_grammar = Suppress('mod') + QuotedString('\'') + \
        Suppress(',') + QuotedString('\'')
    mods = mod_grammar.searchString(content)
    for mod, version in mods:
        user, mod_name = mod.split('/')
        yield user, mod_name, version


@asyncio.coroutine
def check_version(*mod):
    url = build_url(*mod)
    forge_version = yield from get_version(url)
    version = mod[2]
    return mod + (forge_version, Version(forge_version) > Version(version))


@asyncio.coroutine
def get_version(url):
    response = yield from request_version(url)
    return json.loads(response.decode('utf-8'))['version']


@asyncio.coroutine
def request_version(url):
    response = yield from aiohttp.request('GET', url)
    return (yield from response.read_and_close(decode=True))


def build_url(*mod):
    return 'http://forge.puppetlabs.com/users/{}/modules/{}/releases/find.json'.format(*mod)
