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

class AddStudioLayoutRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'live', '2016-11-01', 'AddStudioLayout','live')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ScreenInputConfigList(self):
		return self.get_query_params().get('ScreenInputConfigList')

	def set_ScreenInputConfigList(self,ScreenInputConfigList):
		self.add_query_param('ScreenInputConfigList',ScreenInputConfigList)

	def get_LayoutType(self):
		return self.get_query_params().get('LayoutType')

	def set_LayoutType(self,LayoutType):
		self.add_query_param('LayoutType',LayoutType)

	def get_LayoutName(self):
		return self.get_query_params().get('LayoutName')

	def set_LayoutName(self,LayoutName):
		self.add_query_param('LayoutName',LayoutName)

	def get_LayerOrderConfigList(self):
		return self.get_query_params().get('LayerOrderConfigList')

	def set_LayerOrderConfigList(self,LayerOrderConfigList):
		self.add_query_param('LayerOrderConfigList',LayerOrderConfigList)

	def get_MediaInputConfigList(self):
		return self.get_query_params().get('MediaInputConfigList')

	def set_MediaInputConfigList(self,MediaInputConfigList):
		self.add_query_param('MediaInputConfigList',MediaInputConfigList)

	def get_CasterId(self):
		return self.get_query_params().get('CasterId')

	def set_CasterId(self,CasterId):
		self.add_query_param('CasterId',CasterId)

	def get_BgImageConfig(self):
		return self.get_query_params().get('BgImageConfig')

	def set_BgImageConfig(self,BgImageConfig):
		self.add_query_param('BgImageConfig',BgImageConfig)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_CommonConfig(self):
		return self.get_query_params().get('CommonConfig')

	def set_CommonConfig(self,CommonConfig):
		self.add_query_param('CommonConfig',CommonConfig)