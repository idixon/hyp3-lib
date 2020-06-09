from __future__ import print_function, absolute_import, division, unicode_literals

import os
import shutil
import pytest

_HERE = os.path.dirname(__file__)


@pytest.fixture(scope='session')
def safe_data(tmpdir_factory):
    safe_dir = str(tmpdir_factory.mktemp('safe_data').join('test.SAFE'))
    shutil.copytree(os.path.join(_HERE, 'data', 'test.SAFE'), safe_dir)
    return safe_dir