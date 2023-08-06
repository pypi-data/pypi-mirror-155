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

from aliyunsdkcore.request import RpcRequest
from aliyunsdklive.endpoint import endpoint_data

class AddMultiRateConfigRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'live', '2016-11-01', 'AddMultiRateConfig','live')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_App(self):
		return self.get_query_params().get('App')

	def set_App(self,App):
		self.add_query_param('App',App)

	def get_GroupId(self):
		return self.get_query_params().get('GroupId')

	def set_GroupId(self,GroupId):
		self.add_query_param('GroupId',GroupId)

	def get_Templates(self):
		return self.get_query_params().get('Templates')

	def set_Templates(self,Templates):
		self.add_query_param('Templates',Templates)

	def get_DomainName(self):
		return self.get_query_params().get('DomainName')

	def set_DomainName(self,DomainName):
		self.add_query_param('DomainName',DomainName)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_IsLazy(self):
		return self.get_query_params().get('IsLazy')

	def set_IsLazy(self,IsLazy):
		self.add_query_param('IsLazy',IsLazy)

	def get_AvFormat(self):
		return self.get_query_params().get('AvFormat')

	def set_AvFormat(self,AvFormat):
		self.add_query_param('AvFormat',AvFormat)

	def get_IsTimeAlign(self):
		return self.get_query_params().get('IsTimeAlign')

	def set_IsTimeAlign(self,IsTimeAlign):
		self.add_query_param('IsTimeAlign',IsTimeAlign)