from .common import traderrpc, auctioneerrpc, BaseClient
from .errors import handle_rpc_errors
from datetime import datetime
import binascii

class HashmailRPC(BaseClient):
    pass
    # @handle_rpc_errors
    # def import_graph(self, nodes, edges):
    #     """
    #     ImportGraph
    #     """
    #     request = dev.ChannelGraph(
    #         nodes=nodes,
    #         edges=edges
    #     )
    #     response = self._dev_stub.ImportGraph(request)
    #     return response