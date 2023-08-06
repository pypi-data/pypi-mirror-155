import datetime as DT 

MAJOR_VERSION = 0
'''Major version number'''

MINOR_VERSION = 3
'''Minor version number'''

REVISION_VERSION = 10
'''Revision version number'''

VERSION = (MAJOR_VERSION,MINOR_VERSION,REVISION_VERSION)
'''DAPI2 library DAPI2 version (3-tuple)'''

__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)
'''DAPI2 library DAPI2 version (str)'''

__ver__ = '{0:d}.{1:d}'.format(*VERSION)
'''DAPI2 library DAPI2 short version (str)'''

DATE = DT.date(2022, 6, 15)
'''Release date'''