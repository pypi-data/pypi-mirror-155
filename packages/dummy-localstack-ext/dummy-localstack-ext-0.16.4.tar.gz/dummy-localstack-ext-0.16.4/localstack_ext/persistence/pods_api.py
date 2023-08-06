_A='DELETE'
from localstack.http import route
from werkzeug import Request
from localstack_ext.constants import API_PATH_PODS
from localstack_ext.utils.cloud_pods import handle_get_state_request_in_memory,handle_pod_state_injection,handle_reset_state_request
class PodsApi:
	@route(f"{API_PATH_PODS}",methods=['POST'])
	def pods(self,request):return handle_pod_state_injection(request.get_data())
	@route(f"{API_PATH_PODS}/state",methods=['GET',_A])
	def pods_state(self,request):
		A=request
		if A.method==_A:return handle_reset_state_request(A.path,A.data,A.values,reset_data_dir=False)
		return handle_get_state_request_in_memory()
	@route(f"{API_PATH_PODS}/state/datadir",methods=[_A])
	def pods_state_datadir(self,request):A=request;return handle_reset_state_request(A.path,A.data,A.values,reset_data_dir=True)