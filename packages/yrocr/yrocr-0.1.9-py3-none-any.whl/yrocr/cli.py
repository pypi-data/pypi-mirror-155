#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: CLI模块


import click


@click.group()
def ocr_cli():
    click.echo('ocr cli')
    pass

# @ocr.command()
# def check():
#     click.echo('ocr check')
#
#
# @ocr.group()
# def to():
#     click.echo('ocr to')
#
#
# @to.command()
# def csv():
#     click.echo('ocr to csv')
