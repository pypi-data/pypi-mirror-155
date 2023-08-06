# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest
from aliyunsdkedas.endpoint import endpoint_data

class GetAccountMockRuleRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'Edas', '2017-08-01', 'GetAccountMockRule','Edas')
		self.set_uri_pattern('/pop/sp/api/mock/getAccountMockRule')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ProviderAppName(self): # string
		return self.get_query_params().get('ProviderAppName')

	def set_ProviderAppName(self, ProviderAppName):  # string
		self.add_query_param('ProviderAppName', ProviderAppName)
	def get_PageNumber(self): # string
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # string
		self.add_query_param('PageNumber', PageNumber)
	def get_PageSize(self): # string
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # string
		self.add_query_param('PageSize', PageSize)
	def get_Name(self): # string
		return self.get_query_params().get('Name')

	def set_Name(self, Name):  # string
		self.add_query_param('Name', Name)
	def get_Namespace(self): # string
		return self.get_query_params().get('Namespace')

	def set_Namespace(self, Namespace):  # string
		self.add_query_param('Namespace', Namespace)
	def get_MockType(self): # integer
		return self.get_query_params().get('MockType')

	def set_MockType(self, MockType):  # integer
		self.add_query_param('MockType', MockType)
	def get_Region(self): # string
		return self.get_query_params().get('Region')

	def set_Region(self, Region):  # string
		self.add_query_param('Region', Region)
	def get_ConsumerAppName(self): # string
		return self.get_query_params().get('ConsumerAppName')

	def set_ConsumerAppName(self, ConsumerAppName):  # string
		self.add_query_param('ConsumerAppName', ConsumerAppName)
