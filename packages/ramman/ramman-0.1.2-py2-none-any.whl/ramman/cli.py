import os
import json
import click
from ramman import Ramman 

config = {
    'url': os.getenv('HEMAN_URL', None),
}

@click.group()
@click.pass_context
def ramman(ctx):
    try:
        ctx.obj['emp'] = Ramman(ctx.obj['config'], debug=False)
    except Exception, e:
        click.echo('Heman service connection failed')

@ramman.command()
@click.pass_context
@click.argument('id', nargs=1)
@click.argument('token', nargs=1)
@click.argument('ot', nargs=1)
@click.argument('period', nargs=1)
def get_results(ctx, id, token, ot, period):
    click.echo(json.dumps(ctx.obj['emp'].get(id, token, ot, period), indent=4))


if __name__ == '__main__':
    ramman(obj={'config': config})
