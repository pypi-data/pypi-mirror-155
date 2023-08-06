from .common import BaseClient, looprpc
from .errors import handle_rpc_errors


class SwapClientRPC(BaseClient):
    @handle_rpc_errors
    def get_liquidity_params(self):
        """GetLiquidityParams"""
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response


    @handle_rpc_errors
    def get_loop_in_quote(self, amt, conf_target, external_htlc=False):
        """GetLoopInQuote"""
        request = looprpc.QuoteRequest(
            amt=amt,
            conf_target=conf_target,
            external_htlc=external_htlc
        )
        response = self._client_stub.GetLoopInQuote(request)
        return response

    @handle_rpc_errors
    def get_loop_in_terms(self):
        """GetLoopInTerms"""
        request = looprpc.TermsRequest()
        response = self._client_stub.GetLoopInTerms(request)
        return response

    @handle_rpc_errors
    def get_lsat_tokens(self):
        """GetLsatTokens"""
        request = looprpc.TokensRequest()
        response = self._client_stub.GetLsatTokens(request)
        return response

    @handle_rpc_errors
    def list_swaps(self):
        """ListSwaps"""
        request = looprpc.ListSwapsRequest()
        response = self._client_stub.ListSwaps(request)
        return response

    @handle_rpc_errors
    def loop_in(self):
        """LoopIn"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def loop_out(self):
        """LoopOut"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def loop_out_quote(self):
        """LoopOutQuote"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def loop_out_terms(self):
        """LoopOutTerms"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def monitor(self):
        """Monitor"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def probe(self):
        """Probe"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def set_liquidity_params(self):
        """SetLiquidityParams"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response

    @handle_rpc_errors
    def suggest_swaps(self):
        """SuggestSwaps"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response


    @handle_rpc_errors
    def swap_info(self):
        """Unlock encrypted wallet at lnd startup"""
        return "not implemented"
        request = looprpc.GetLiquidityParamsRequest()
        response = self._client_stub.GetLiquidityParams(request)
        return response
