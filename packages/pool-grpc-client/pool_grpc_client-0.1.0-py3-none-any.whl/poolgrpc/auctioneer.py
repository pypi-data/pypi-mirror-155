from .common import traderrpc, auctioneerrpc, BaseClient
from .errors import handle_rpc_errors
from datetime import datetime
import binascii

class AuctioneerRPC(BaseClient):
    @handle_rpc_errors
    def batch_snapshots(self, start_batch_id, num_batches_back):
        """Get list of previously filled batches"""
        request = auctioneerrpc.BatchSnapshotsRequest(
            start_batch_id=start_batch_id,
            num_batches_back=num_batches_back
        )
        response = self._trader_stub.BatchSnapshots(request)
        return response
