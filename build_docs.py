import argparse
import errno
import logging
import os
import sys
import subprocess

if sys.version_info < (3, 6):
    logging.basicConfig(level=logging.INFO)
    main_logger = logging.getLogger('init')
    main_logger.error('only Python Versions from 3.6 are supported')
    sys.exit(1)
else:
    # Project Imports
    from rst_include import *
    from rst_include.libs import lib_log


# CONSTANTS & PROJECT SPECIFIC FUNCTIONS
codeclimate_link_hash = "eafdc923e24d12513284"


def project_specific(repository_slug, repository, repository_dashed):
    # PROJECT SPECIFIC
    pass


def parse_args(cmd_args=sys.argv[1:]):
    # type: ([]) -> []
    parser = argparse.ArgumentParser(
        description='Create Readme.rst',
        epilog='check the documentation on github',
        add_help=True)

    parser.add_argument('travis_repo_slug', metavar='TRAVIS_REPO_SLUG in the form "<github_account>/<repository>"')
    args = parser.parse_args(cmd_args)
    return args, parser


def main(args):
    logger = logging.getLogger('build_docs')
    logger.info('create the README.rst')
    travis_repo_slug = args.travis_repo_slug
    repository = travis_repo_slug.split('/')[1]
    repository_dashed = repository.replace('_', '-')

    project_specific(travis_repo_slug, repository, repository_dashed)

    """
    paths absolute, or relative to the location of the config file
    the notation for relative files is like on windows or linux - not like in python.
    so You might use ../../some/directory/some_document.rst to go two levels back.
    avoid absolute paths since You never know where the program will run.
    """

    logger.info('include the include blocks')
    rst_inc(source='./docs/README_template.rst',
            target='./README.rst')

    # please note that the replace syntax is not shown correctly in the README.rst,
    # because it gets replaced itself by the build_docs.py
    # we could overcome this by first replacing, and afterwards including -
    # check out the build_docs.py for the correct syntax !
    logger.info('replace repository related strings')
    rst_str_replace(source='./README.rst',
                    target='',
                    old='{repository_slug}',
                    new=travis_repo_slug,
                    inplace=True)
    rst_str_replace(source='./README.rst',
                    target='',
                    old='{repository}',
                    new=repository,
                    inplace=True)
    rst_str_replace(source='./README.rst',
                    target='',
                    old='{repository_dashed}',
                    new=repository_dashed,
                    inplace=True)

    rst_str_replace(source='./README.rst',
                    target='',
                    old='{codeclimate_link_hash}',
                    new=codeclimate_link_hash,
                    inplace=True)

    logger.info('done')
    sys.exit(0)


if __name__ == '__main__':
    lib_log.setup_logger()
    main_logger = logging.getLogger('main')
    try:
        _args, _parser = parse_args()

        main(_args)
    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        sys.exit(errno.ENOENT)      # No such file or directory
    except FileExistsError:
        sys.exit(errno.EEXIST)      # File exists
    except TypeError:
        sys.exit(errno.EINVAL)      # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # Invalid Argument
