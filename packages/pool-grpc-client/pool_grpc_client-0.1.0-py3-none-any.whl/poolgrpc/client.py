from .common import BaseClient, traderrpc, auctioneerrpc
from .errors import handle_rpc_errors

from poolgrpc.trader import TraderRPC
from poolgrpc.auctioneer import AuctioneerRPC
from poolgrpc.hashmail import HashmailRPC

class PoolClient(
    TraderRPC,
    AuctioneerRPC,
    HashmailRPC
):
    pass

def cli():
    import os
    import code
    from pathlib import Path
    credential_path = os.getenv("POOL_CRED_PATH", None)
    if credential_path == None:
        credential_path = Path("/home/skorn/.pool/mainnet")
    else:
        credential_path = Path(credential_path)

    pool_ip = os.getenv("POOL_IP")
    pool_port = os.getenv("POOL_PORT")

    mac = str(credential_path.joinpath("pool.macaroon").absolute())
    tls = str(credential_path.joinpath("tls.cert").absolute())

    pool_ip_port = f"{pool_ip}:{pool_port}"


    pool = PoolClient(
        pool_ip_port,
        macaroon_filepath=mac,
        cert_filepath=tls,
        # no_tls=True
    )

    code.interact(local=dict(globals(), **locals()))  