from .common import BaseClient, looprpc
from .errors import handle_rpc_errors


class DebugRPC(BaseClient):
    @handle_rpc_errors
    def force_autoloop(self):
        """ForceAutoLoop"""
        pass
        # request = looprpc.GetLiquidityParamsRequest()
        # response = self._client_stub.GetLiquidityParams(request)
        # return response