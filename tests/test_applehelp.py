"""
    test_applehelp
    ~~~~~~~~~~~~~~

    Test for applehelp extension.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pathlib import Path
import plistlib

import pytest


def check_structure(outdir):
    contentsdir = outdir / 'Contents'
    assert contentsdir.isdir()
    assert (contentsdir / 'Info.plist').isfile()

    with open(contentsdir / 'Info.plist', 'rb') as f:
        plist = plistlib.load(f)
    assert plist
    assert len(plist)
    assert plist.get('CFBundleIdentifier', None) == 'org.sphinx-doc.Sphinx.help'

    assert (contentsdir / 'Resources').isdir()
    assert (contentsdir / 'Resources' / 'en.lproj').isdir()


def check_localization(outdir):
    lprojdir = outdir / 'Contents' / 'Resources' / 'en.lproj'
    assert (lprojdir / 'localized.txt').isfile()


@pytest.mark.sphinx(
    'applehelp', testroot='basic', srcdir='applehelp_output',
    confoverrides={'applehelp_bundle_id': 'org.sphinx-doc.Sphinx.help',
                   'applehelp_disable_external_tools': True})
def test_applehelp_output(app, status, warning):
    (app.srcdir / 'en.lproj').mkdir(parents=True, exist_ok=True)
    (app.srcdir / 'en.lproj' / 'localized.txt').touch()
    app.builder.build_all()

    # Have to use bundle_path, not outdir, because we alter the latter
    # to point to the lproj directory so that the HTML arrives in the
    # correct location.
    bundle_path = Path(app.builder.bundle_path)
    check_structure(bundle_path)
    check_localization(bundle_path)
