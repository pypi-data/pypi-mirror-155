# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from xbim_flex.identity.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from xbim_flex.identity.model.application_type import ApplicationType
from xbim_flex.identity.model.client_app import ClientApp
from xbim_flex.identity.model.client_app_endpoint import ClientAppEndpoint
from xbim_flex.identity.model.draft_invitation import DraftInvitation
from xbim_flex.identity.model.invitation import Invitation
from xbim_flex.identity.model.invitation_create import InvitationCreate
from xbim_flex.identity.model.invitation_edit import InvitationEdit
from xbim_flex.identity.model.invite_status import InviteStatus
from xbim_flex.identity.model.master import Master
from xbim_flex.identity.model.master_base import MasterBase
from xbim_flex.identity.model.master_subscription import MasterSubscription
from xbim_flex.identity.model.o_data_boolean import ODataBoolean
from xbim_flex.identity.model.o_data_client_app_endpoint_list import ODataClientAppEndpointList
from xbim_flex.identity.model.o_data_client_app_list import ODataClientAppList
from xbim_flex.identity.model.o_data_invitation_list import ODataInvitationList
from xbim_flex.identity.model.o_data_master_list import ODataMasterList
from xbim_flex.identity.model.o_data_region_info_list import ODataRegionInfoList
from xbim_flex.identity.model.o_data_string import ODataString
from xbim_flex.identity.model.o_data_tenant_list import ODataTenantList
from xbim_flex.identity.model.o_data_tenant_user_list import ODataTenantUserList
from xbim_flex.identity.model.o_data_user_list import ODataUserList
from xbim_flex.identity.model.problem_details import ProblemDetails
from xbim_flex.identity.model.region_info import RegionInfo
from xbim_flex.identity.model.subscription import Subscription
from xbim_flex.identity.model.team_member_create import TeamMemberCreate
from xbim_flex.identity.model.team_member_edit import TeamMemberEdit
from xbim_flex.identity.model.tenancy_type import TenancyType
from xbim_flex.identity.model.tenant import Tenant
from xbim_flex.identity.model.tenant_create import TenantCreate
from xbim_flex.identity.model.tenant_edit import TenantEdit
from xbim_flex.identity.model.tenant_role import TenantRole
from xbim_flex.identity.model.tenant_user import TenantUser
from xbim_flex.identity.model.token_err_response import TokenErrResponse
from xbim_flex.identity.model.token_response import TokenResponse
from xbim_flex.identity.model.user import User
from xbim_flex.identity.model.user_create import UserCreate
from xbim_flex.identity.model.user_tenant import UserTenant
