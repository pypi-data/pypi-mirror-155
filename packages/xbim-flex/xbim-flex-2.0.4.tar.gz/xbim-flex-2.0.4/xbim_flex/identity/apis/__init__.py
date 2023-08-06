
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from xbim_flex.identity.api.authentication_api import AuthenticationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from xbim_flex.identity.api.authentication_api import AuthenticationApi
from xbim_flex.identity.api.client_applications_api import ClientApplicationsApi
from xbim_flex.identity.api.invitations_api import InvitationsApi
from xbim_flex.identity.api.masters_api import MastersApi
from xbim_flex.identity.api.me_api import MeApi
from xbim_flex.identity.api.members_api import MembersApi
from xbim_flex.identity.api.registration_api import RegistrationApi
from xbim_flex.identity.api.tenants_api import TenantsApi
from xbim_flex.identity.api.users_api import UsersApi
