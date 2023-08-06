
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from xbim_flex.aim.api.admin_api import AdminApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from xbim_flex.aim.api.admin_api import AdminApi
from xbim_flex.aim.api.applications_api import ApplicationsApi
from xbim_flex.aim.api.assemblies_api import AssembliesApi
from xbim_flex.aim.api.assets_api import AssetsApi
from xbim_flex.aim.api.attributes_api import AttributesApi
from xbim_flex.aim.api.component_types_api import ComponentTypesApi
from xbim_flex.aim.api.components_api import ComponentsApi
from xbim_flex.aim.api.contacts_api import ContactsApi
from xbim_flex.aim.api.diagnostics_api import DiagnosticsApi
from xbim_flex.aim.api.document_files_api import DocumentFilesApi
from xbim_flex.aim.api.documents_api import DocumentsApi
from xbim_flex.aim.api.entities_api import EntitiesApi
from xbim_flex.aim.api.facilities_api import FacilitiesApi
from xbim_flex.aim.api.floorplans_api import FloorplansApi
from xbim_flex.aim.api.issues_api import IssuesApi
from xbim_flex.aim.api.jobs_api import JobsApi
from xbim_flex.aim.api.levels_api import LevelsApi
from xbim_flex.aim.api.logs_api import LogsApi
from xbim_flex.aim.api.model_files_api import ModelFilesApi
from xbim_flex.aim.api.model_mapping_api import ModelMappingApi
from xbim_flex.aim.api.models_api import ModelsApi
from xbim_flex.aim.api.resources_api import ResourcesApi
from xbim_flex.aim.api.schedules_api import SchedulesApi
from xbim_flex.aim.api.sites_api import SitesApi
from xbim_flex.aim.api.spaces_api import SpacesApi
from xbim_flex.aim.api.spares_api import SparesApi
from xbim_flex.aim.api.stats_api import StatsApi
from xbim_flex.aim.api.systems_api import SystemsApi
from xbim_flex.aim.api.thumbnails_api import ThumbnailsApi
from xbim_flex.aim.api.wexbim_api import WexbimApi
from xbim_flex.aim.api.zones_api import ZonesApi
