#!/usr/bin/env python

import argparse

import docker


def append_requires(requires, name, ver):
    if ver and ver != 'none':
        requires.append('%s==%s' % (name, ver))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test script for installation')
    parser.add_argument('--base', choices=docker.base_choices, required=True)
    parser.add_argument('--cuda', choices=docker.cuda_choices, required=True)
    parser.add_argument('--cudnn', choices=docker.cudnn_choices, required=True)
    parser.add_argument('--numpy')
    parser.add_argument('--setuptools')
    parser.add_argument('--pip')
    parser.add_argument('--cython')

    parser.add_argument('--http-proxy')
    parser.add_argument('--https-proxy')
    args = parser.parse_args()

    # make sdist
    build_conf = {
        'base': 'ubuntu14_py2',
        'cuda': 'cuda65',
        'cudnn': 'none',
        'requires': ['cython'],
    }
    docker.run_with(build_conf, './build_sdist.sh')

    conf = {
        'base': args.base,
        'cuda': args.cuda,
        'cudnn': args.cudnn,
        'requires': [],
    }

    append_requires(conf['requires'], 'numpy', args.numpy)
    append_requires(conf['requires'], 'setuptools', args.setuptools)
    append_requires(conf['requires'], 'pip', args.pip)
    append_requires(conf['requires'], 'cython', args.cython)

    if args.http_proxy:
        conf['http_proxy'] = args.http_proxy
    if args.https_proxy:
        conf['https_proxy'] = args.https_proxy

    docker.run_with(conf, './test_install.sh')
