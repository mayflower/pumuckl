import asyncio
import click
import sys

from .module import Module


@click.command()
@click.argument('puppetfile', type=click.File(),
                required=False, default='Puppetfile')
@click.option('-v', '--verbose', is_flag=True,
              help='Enable verbose mode.')
def cli(puppetfile, verbose):
    """This script checks a Puppetfile for modules with an outdated version."""
    loop = asyncio.get_event_loop()
    mods = Module.parse_puppetfile_forge_mods(puppetfile.read())
    f = asyncio.gather(*[mod.fetch_version() for mod in mods])
    loop.run_until_complete(f)

    up_to_date, outdated = get_filtered_result(f.result())
    display_result(up_to_date, outdated, verbose=verbose)

    if outdated:
        sys.exit(1)


def get_filtered_result(mods):
    up_to_date = filter(lambda mod: mod.is_up_to_date, mods)
    outdated = filter(lambda mod: not mod.is_up_to_date, mods)
    return list(up_to_date), list(outdated)


def display_result(up_to_date, outdated, *, verbose):
    if verbose:
        for mod in up_to_date:
            click.secho('{}/{} at {} = {}'.format(mod.user, mod.mod_name, mod.version, mod.forge_version), fg='green')
    for mod in outdated:
        click.secho('{}/{} at {} < {}'.format(mod.user, mod.mod_name, mod.version, mod.forge_version), fg='red')
    click.echo()
    if not outdated:
        click.secho('All {} modules are up-to-date'.format(len(up_to_date)), fg='green')
    else:
        click.secho(str(len(outdated)), nl=False, fg='red')
        click.secho(' module{} outdated, {} module{} up-to-date'.format(
            ' is' if len(outdated) == 1 else 's are',
            len(up_to_date),
            ' is' if len(up_to_date) == 1 else 's are',
        ), fg='green')
