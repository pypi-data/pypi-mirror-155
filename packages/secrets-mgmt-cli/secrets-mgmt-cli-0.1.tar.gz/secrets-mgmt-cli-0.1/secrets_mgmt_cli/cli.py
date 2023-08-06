import json
import datetime

import click

from .aws import aws


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


@click.group()
@click.version_option()
def cli():
    "A simple CLI for managing secrets in AWS Secrets Manager"
    pass


@cli.command(name="command")
@click.argument("example")
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")


@cli.command()
def ls():
    resp = aws.get_secrets_list()
    for secret in resp.get("SecretList"):
        click.echo(f"\n-- {secret.get('Name')} --")
        for key, val in secret.items():
            click.echo(f"{key[:18]+'..' if len(key)>17 else key}{(20-int(len(key)))*'.'}{val}")


# create
@cli.command()
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
@click.option("-d", "--description", "description", required=False, default="string description")
def create(secret_string, secret_name, description):
    # create_secret(self, secret_string, secret_name, description="string description")
    click.echo("create secret method --> needs to be implemented")


# read
@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def read(description):
    click.echo("read secret method --> needs to be implemented")


# update
@cli.command()
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
@click.option("-d", "--description", "description", required=False, default="string description")
def update(secret_string, secret_name, description):
    click.echo("update secret method --> needs to be implemented")


# delete
@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def delete(description):
    click.echo("delete secret method --> needs to be implemented")


cli.add_command(first_command)
cli.add_command(ls)
cli.add_command(create)
cli.add_command(read)
cli.add_command(update)
cli.add_command(delete)
# cli.add_command(search)
