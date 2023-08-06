import click

from glab_preset.presets.react_oss import react_oss


@click.command()
@click.option('--type', prompt=True, type=click.Choice(['react_oss']), default='react_oss')
def cli(**kwargs):
  if 'react_oss' == kwargs.get('type'):
    react_oss()
  else:
    click.echo('Not support.')


if __name__ == '__main__':
  cli()
