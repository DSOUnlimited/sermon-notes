"""Generated client library for apigateway version v1alpha1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.generated_clients.apis.apigateway.v1alpha1 import apigateway_v1alpha1_messages as messages


class ApigatewayV1alpha1(base_api.BaseApiClient):
  """Generated client library for service apigateway version v1alpha1."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://apigateway.googleapis.com/'
  MTLS_BASE_URL = 'https://apigateway.mtls.googleapis.com/'

  _PACKAGE = 'apigateway'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
  _VERSION = 'v1alpha1'
  _CLIENT_ID = 'CLIENT_ID'
  _CLIENT_SECRET = 'CLIENT_SECRET'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'ApigatewayV1alpha1'
  _URL_VERSION = 'v1alpha1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new apigateway handle."""
    url = url or self.BASE_URL
    super(ApigatewayV1alpha1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.projects_locations_apis_configs = self.ProjectsLocationsApisConfigsService(self)
    self.projects_locations_apis = self.ProjectsLocationsApisService(self)
    self.projects_locations_gateways = self.ProjectsLocationsGatewaysService(self)
    self.projects_locations_operations = self.ProjectsLocationsOperationsService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsLocationsApisConfigsService(base_api.BaseApiService):
    """Service class for the projects_locations_apis_configs resource."""

    _NAME = 'projects_locations_apis_configs'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsLocationsApisConfigsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new ApiConfig in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.configs.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['apiConfigId'],
        relative_path='v1alpha1/{+parent}/configs',
        request_field='apigatewayApiConfig',
        request_type_name='ApigatewayProjectsLocationsApisConfigsCreateRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a single ApiConfig.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}',
        http_method='DELETE',
        method_id='apigateway.projects.locations.apis.configs.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisConfigsDeleteRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details of a single ApiConfig.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayApiConfig) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.configs.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['view'],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisConfigsGetRequest',
        response_type_name='ApigatewayApiConfig',
        supports_download=False,
    )

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}:getIamPolicy',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.configs.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisConfigsGetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists ApiConfigs in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayListApiConfigsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.configs.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+parent}/configs',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisConfigsListRequest',
        response_type_name='ApigatewayListApiConfigsResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates the parameters of a single ApiConfig.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}',
        http_method='PATCH',
        method_id='apigateway.projects.locations.apis.configs.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['updateMask'],
        relative_path='v1alpha1/{+name}',
        request_field='apigatewayApiConfig',
        request_type_name='ApigatewayProjectsLocationsApisConfigsPatchRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}:setIamPolicy',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.configs.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='apigatewaySetIamPolicyRequest',
        request_type_name='ApigatewayProjectsLocationsApisConfigsSetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (ApigatewayProjectsLocationsApisConfigsTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayTestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}/configs/{configsId}:testIamPermissions',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.configs.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='apigatewayTestIamPermissionsRequest',
        request_type_name='ApigatewayProjectsLocationsApisConfigsTestIamPermissionsRequest',
        response_type_name='ApigatewayTestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsApisService(base_api.BaseApiService):
    """Service class for the projects_locations_apis resource."""

    _NAME = 'projects_locations_apis'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsLocationsApisService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new Api in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsApisCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['apiId'],
        relative_path='v1alpha1/{+parent}/apis',
        request_field='apigatewayApi',
        request_type_name='ApigatewayProjectsLocationsApisCreateRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a single Api.

      Args:
        request: (ApigatewayProjectsLocationsApisDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}',
        http_method='DELETE',
        method_id='apigateway.projects.locations.apis.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisDeleteRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details of a single Api.

      Args:
        request: (ApigatewayProjectsLocationsApisGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayApi) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisGetRequest',
        response_type_name='ApigatewayApi',
        supports_download=False,
    )

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (ApigatewayProjectsLocationsApisGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}:getIamPolicy',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisGetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists Apis in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsApisListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayListApisResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis',
        http_method='GET',
        method_id='apigateway.projects.locations.apis.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+parent}/apis',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsApisListRequest',
        response_type_name='ApigatewayListApisResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates the parameters of a single Api.

      Args:
        request: (ApigatewayProjectsLocationsApisPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}',
        http_method='PATCH',
        method_id='apigateway.projects.locations.apis.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['updateMask'],
        relative_path='v1alpha1/{+name}',
        request_field='apigatewayApi',
        request_type_name='ApigatewayProjectsLocationsApisPatchRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (ApigatewayProjectsLocationsApisSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}:setIamPolicy',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='apigatewaySetIamPolicyRequest',
        request_type_name='ApigatewayProjectsLocationsApisSetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (ApigatewayProjectsLocationsApisTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayTestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/apis/{apisId}:testIamPermissions',
        http_method='POST',
        method_id='apigateway.projects.locations.apis.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='apigatewayTestIamPermissionsRequest',
        request_type_name='ApigatewayProjectsLocationsApisTestIamPermissionsRequest',
        response_type_name='ApigatewayTestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsGatewaysService(base_api.BaseApiService):
    """Service class for the projects_locations_gateways resource."""

    _NAME = 'projects_locations_gateways'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsLocationsGatewaysService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new Gateway in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways',
        http_method='POST',
        method_id='apigateway.projects.locations.gateways.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['gatewayId'],
        relative_path='v1alpha1/{+parent}/gateways',
        request_field='apigatewayGateway',
        request_type_name='ApigatewayProjectsLocationsGatewaysCreateRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a single Gateway.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}',
        http_method='DELETE',
        method_id='apigateway.projects.locations.gateways.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsGatewaysDeleteRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details of a single Gateway.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayGateway) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}',
        http_method='GET',
        method_id='apigateway.projects.locations.gateways.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsGatewaysGetRequest',
        response_type_name='ApigatewayGateway',
        supports_download=False,
    )

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}:getIamPolicy',
        http_method='GET',
        method_id='apigateway.projects.locations.gateways.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsGatewaysGetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists Gateways in a given project and location.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayListGatewaysResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways',
        http_method='GET',
        method_id='apigateway.projects.locations.gateways.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+parent}/gateways',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsGatewaysListRequest',
        response_type_name='ApigatewayListGatewaysResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates the parameters of a single Gateway.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}',
        http_method='PATCH',
        method_id='apigateway.projects.locations.gateways.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['updateMask'],
        relative_path='v1alpha1/{+name}',
        request_field='apigatewayGateway',
        request_type_name='ApigatewayProjectsLocationsGatewaysPatchRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayPolicy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}:setIamPolicy',
        http_method='POST',
        method_id='apigateway.projects.locations.gateways.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='apigatewaySetIamPolicyRequest',
        request_type_name='ApigatewayProjectsLocationsGatewaysSetIamPolicyRequest',
        response_type_name='ApigatewayPolicy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (ApigatewayProjectsLocationsGatewaysTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayTestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/gateways/{gatewaysId}:testIamPermissions',
        http_method='POST',
        method_id='apigateway.projects.locations.gateways.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='apigatewayTestIamPermissionsRequest',
        request_type_name='ApigatewayProjectsLocationsGatewaysTestIamPermissionsRequest',
        response_type_name='ApigatewayTestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the projects_locations_operations resource."""

    _NAME = 'projects_locations_operations'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation. On successful cancellation, the operation is not deleted; instead, it becomes an operation with an Operation.error value with a google.rpc.Status.code of `1`, corresponding to `Code.CANCELLED`.

      Args:
        request: (ApigatewayProjectsLocationsOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}:cancel',
        http_method='POST',
        method_id='apigateway.projects.locations.operations.cancel',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}:cancel',
        request_field='apigatewayCancelOperationRequest',
        request_type_name='ApigatewayProjectsLocationsOperationsCancelRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.

      Args:
        request: (ApigatewayProjectsLocationsOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='DELETE',
        method_id='apigateway.projects.locations.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (ApigatewayProjectsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayOperation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='GET',
        method_id='apigateway.projects.locations.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsOperationsGetRequest',
        response_type_name='ApigatewayOperation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`.

      Args:
        request: (ApigatewayProjectsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations',
        http_method='GET',
        method_id='apigateway.projects.locations.operations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+name}/operations',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsOperationsListRequest',
        response_type_name='ApigatewayListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets information about a location.

      Args:
        request: (ApigatewayProjectsLocationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayLocation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}',
        http_method='GET',
        method_id='apigateway.projects.locations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsGetRequest',
        response_type_name='ApigatewayLocation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists information about the supported locations for this service.

      Args:
        request: (ApigatewayProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApigatewayListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations',
        http_method='GET',
        method_id='apigateway.projects.locations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['extraLocationTypes', 'filter', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+name}/locations',
        request_field='',
        request_type_name='ApigatewayProjectsLocationsListRequest',
        response_type_name='ApigatewayListLocationsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(ApigatewayV1alpha1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }
