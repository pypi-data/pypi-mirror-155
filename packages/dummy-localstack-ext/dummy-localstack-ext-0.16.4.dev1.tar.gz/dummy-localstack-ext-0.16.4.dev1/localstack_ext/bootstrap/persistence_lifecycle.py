_C='kinesis'
_B='moto'
_A='localstack'
import inspect,logging,os
from typing import Any,Dict,Type,Union
import localstack.config as localstack_config,moto.core
from localstack.constants import TEST_AWS_ACCOUNT_ID
from localstack.services.generic_proxy import RegionBackend
from localstack.services.plugins import BackendStateLifecycle
from localstack.utils.files import cp_r,rm_rf
from localstack.utils.testutil import create_zip_file
from moto.applicationautoscaling.models import ApplicationAutoscalingBackend
from moto.autoscaling.models import AutoScalingBackend
from moto.core.utils import BackendDict
from moto.redshift.models import RedshiftBackend
from localstack_ext.bootstrap.pods.service_state import BackendState,ServiceKey,ServiceState
from localstack_ext.utils.cloud_pods import SINGLE_GLOBAL_REGION_NAME
from localstack_ext.utils.lookup_utils import get_backend_state
from localstack_ext.utils.persistence import marshal_backend
SERVICES_WITHOUT_STATE=['apigatewaymanagementapi','azure','azure','cloudsearch','cloudwatch','configservice','docdb','elasticsearch','iot-data','iot-jobs-data','iotanalytics','iotevents','iotevents-data','iotwireless','mediaconvert','mediastore-data','neptune','qldb-session','rds-data','redshift-data','resource-groups','resourcegroupstaggingapi','route53resolver','s3control','sagemaker-runtime','ssm','swf','timestream-query','timestream-write']
EXTERNAL_SERVICES=['dynamodb',_C,'stepfunctions']
NON_SERVICE_APIS=['edge','support','logs']
LOG=logging.getLogger(__name__)
def _service_state_from_region_backend(service_backend,api):
	A=service_backend;from localstack_ext.constants import REGION_STATE_FILE as C
	def D():
		if not hasattr(A,'REGIONS'):return True
	if D():return ServiceState()
	B=ServiceState()
	for (E,F) in A.regions().items():G=ServiceKey(account_id=TEST_AWS_ACCOUNT_ID,region=E,service=api);H=BackendState(G,{C:marshal_backend(F)});B.add(state_to_add=H)
	return B
def _service_state_from_backend_state(service_backend,api):
	A=service_backend;from localstack.constants import TEST_AWS_ACCOUNT_ID as C;from localstack_ext.constants import MOTO_BACKEND_STATE_FILE as D;B=ServiceState()
	if not isinstance(A,dict):A={SINGLE_GLOBAL_REGION_NAME:A}
	for (E,F) in A.items():G=ServiceKey(account_id=C,region=E,service=api);H=BackendState(G,{D:marshal_backend(F)});B.add(state_to_add=H)
	return B
def _service_state_from_backend(backend,api,memory_management):
	B=memory_management;A=backend
	if B==_A:return _service_state_from_region_backend(service_backend=A,api=api)
	if B==_B:return _service_state_from_backend_state(service_backend=A,api=api)
class BackendStateLifecycleBase(BackendStateLifecycle):
	def get_backends(D):
		A={}
		for B in [_B,_A]:
			C=get_backend_state(api=D.service,memory_manager=B)
			if C:A[B]=C
		return A
	def retrieve_state(A,**F):
		B=ServiceState();E=A.service;C=A.get_backends()
		for D in C.keys():B.add(_service_state_from_backend(backend=C[D],api=E,memory_management=D))
		return B
	def inject_state(A,**B):0
	def reset_state(B):
		D=get_backend_state(B.service,_B);E=get_backend_state(B.service,_A);C=[];D and C.append(D);E and C.append(E)
		if not C:
			if B.service not in SERVICES_WITHOUT_STATE+EXTERNAL_SERVICES+NON_SERVICE_APIS:LOG.debug("Unable to determine state container for service '%s'",B.service)
			return
		for A in C:
			if inspect.isclass(A)and issubclass(A,RegionBackend):A.reset();continue
			if isinstance(A,dict):
				for G in A.keys():reset_moto_backend_state(A,G)
				if isinstance(A,moto.core.utils.BackendDict):A.clear()
				continue
			if isinstance(A,moto.core.BaseBackend):F=getattr(A,'region_name',getattr(A,'region',None));A.__dict__={};A.__init__(*([F]if F else[]));continue
			LOG.warning("Unable to reset state for service '%s', state container: %s",B.service,A)
		B.on_after_reset()
	def on_after_reset(A):0
class BackendStateAssetsLifecycle(BackendStateLifecycleBase):
	def assets_root(A):return A.service
	def get_assets_location(A):B=localstack_config.dirs.data if localstack_config.DATA_DIR else localstack_config.dirs.tmp;return os.path.join(B,A.assets_root())
	def retrieve_assets(A):B=A.get_assets_location();return create_zip_file(B,get_content=True)
	def inject_assets(A,pod_assets_dir):B=A.get_assets_location();C=os.path.join(pod_assets_dir,A.assets_root());cp_r(src=C,dst=B)
	def retrieve_state(B,**C):
		A=super().retrieve_state(**C)
		if not A.state and B.service!=_C:return A
		D=B.retrieve_assets();A.add_asset(B.service,D);return A
	def inject_state(B,**A):super().inject_state(**A)
	def reset_state(A):B=A.get_assets_location();rm_rf(B);super().reset_state()
def reset_moto_backend_state(state_container,region_key):
	D=state_container;B=region_key;A=D.get(B);E=getattr(A,'reset',None)
	if E and callable(E):E();return A
	F=type(A);C=[B]if len(inspect.signature(F.__init__).parameters)>1 else[]
	if isinstance(A,ApplicationAutoscalingBackend):C.append(A.ecs_backend)
	elif isinstance(A,RedshiftBackend):C.insert(0,A.ec2_backend)
	elif isinstance(A,AutoScalingBackend):C=[A.ec2_backend,A.elb_backend,A.elbv2_backend]
	D[B]=F(*(C));return D[B]
class DummyProvider(BackendStateLifecycleBase):
	def __init__(A,service):A.service=service