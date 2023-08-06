
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from xbim_flex.comms.api.contacts_api import ContactsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from xbim_flex.comms.api.contacts_api import ContactsApi
from xbim_flex.comms.api.conversations_api import ConversationsApi
from xbim_flex.comms.api.files_api import FilesApi
from xbim_flex.comms.api.snapshots_api import SnapshotsApi
