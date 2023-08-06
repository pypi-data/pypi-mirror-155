import jsw_nx as nx
import gitlab
import os
import click


@click.command()
@click.option('--project_id', prompt=True, required=True, type=int)
@click.option('--yarn_registry', prompt=True, default=os.getenv('ALO7_YARN_REGISTRY'))
@click.option('--alibabacloud_access_key_id', prompt=True, default=os.getenv('ALIBABACLOUD_ACCESS_KEY_ID'))
@click.option('--alibabacloud_access_key_secret', prompt=True, default=os.getenv('ALIBABACLOUD_ACCESS_KEY_SECRET'))
@click.option('--alibabacloud_region_id', prompt=True, default=os.getenv('ALIBABACLOUD_REGION_ID'))
def cli(**kwargs):
  gl = gitlab.Gitlab(url="https://git.saybot.net/", private_token=os.getenv('GITLAB_TOKEN'))
  prj = gl.projects.get(kwargs['project_id'])

  envs = [
    {'key': 'YARN_REGISTRY', 'value': kwargs['yarn_registry']},
    {'key': 'ALIBABACLOUD_ACCESS_KEY_ID', 'value': kwargs['alibabacloud_access_key_id']},
    {'key': 'ALIBABACLOUD_ACCESS_KEY_SECRET', 'value': kwargs['alibabacloud_access_key_secret']},
    {'key': 'ALIBABACLOUD_REGION_ID', 'value': kwargs['alibabacloud_region_id']},
  ]

  for item in envs:
    prj.variables.create(item)


if __name__ == '__main__':
  cli()
