"""Tornado handler for bodo cluster management."""

import json
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

from .platform import PlatformClusterManager
from .remote_ikernels_manager import (
    cleanup_kernelspecs,
    get_remote_kernel_name_for_cluster,
)
from .ssh_keys_manager import cleanup_ssh_keys, get_cluster_ssh_key_fname
from .auto_attach import should_auto_attach


class ClusterRemoteIKernelHandler(APIHandler):
    """
    Handler for Remote IKernels on Clusters
    """

    @web.authenticated
    async def post(self, cluster_id: str) -> None:
        """
        Create a remote kernel on one of the hosts and return its name.
        """
        logging_prefix = f"[ClusterRemoteIKernelHandler.post][UUID: {cluster_id}]"
        self.log.info(f"{logging_prefix} Starting...")

        error = None
        try:
            hostlist = PlatformClusterManager.get_cluster_hostlist(
                cluster_id, logger=self.log
            )
            self.log.info(f"{logging_prefix} hostlist: {hostlist}")
            ssh_key_fname: str = get_cluster_ssh_key_fname(
                cluster_id, logger=self.log, hard_refresh=False,
            )
            self.log.info(f"{logging_prefix} ssh_key_fname: {ssh_key_fname}")
            remote_kernel_name: str = get_remote_kernel_name_for_cluster(
                cluster_id, hostlist, ssh_key_fname, logger=self.log,
            )
            self.log.info(f"{logging_prefix} remote_kernel_name: {remote_kernel_name}")
        except Exception as e:
            self.log.error(f"{logging_prefix} Error: {e}")
            remote_kernel_name = None
            error = str(e)

        self.log.info(f"{logging_prefix} Finishing...")
        self.finish(json.dumps({"remote_kernel_name": remote_kernel_name, "e": error}))


class PlatformClusterListHandler(APIHandler):
    @web.authenticated
    async def get(self):
        """
        Get list of clusters from the platform.
        Also do a kernelspec and ssh keys cleanup after.
        """
        logging_prefix = "[PlatformClusterListHandler.get]"
        self.log.info(f"{logging_prefix} Starting...")
        error = None
        try:
            clusters = PlatformClusterManager.get_clusters_list(logger=self.log)
            self.log.info(f"{logging_prefix} clusters: {clusters}")
        except Exception as e:
            self.log.error(f"{logging_prefix} Error: {e}")
            clusters = None
            error = str(e)

        try:
            self.log.info(f"{logging_prefix} Calling KernelSpec cleanup...")
            cleanup_kernelspecs(self.log)
            self.log.info(
                f"{logging_prefix} Successfully finished KernelSpec cleanup..."
            )
        except Exception as e:
            self.log.warning(f"{logging_prefix} Error during KernelSpec cleanup: {e}")

        try:
            self.log.info(f"{logging_prefix} Calling SSH Keys cleanup...")
            cleanup_ssh_keys(self.log)
            self.log.info(f"{logging_prefix} Successfully finished SSH Keys cleanup...")
        except Exception as e:
            self.log.warning(f"{logging_prefix} Error during SSH Keys cleanup: {e}")

        self.log.info(f"{logging_prefix} Finishing...")
        self.finish(json.dumps({"clusters": clusters, "e": error}))


class AutoAttachHandler(APIHandler):
    """
    Determine whether a cluster should be auto attached to a notebook.
    """

    @web.authenticated
    async def get(self):
        logging_prefix = "[AutoAttachHandler.get]"
        self.log.info(f"{logging_prefix} Starting...")
        error = None

        try:
            auto_attach = should_auto_attach()
            self.log.info(f"{logging_prefix} auto_attach: {auto_attach}")

        except Exception as e:
            self.log.error(f"{logging_prefix} Error: {e}")
            auto_attach = None
            error = str(e)

        self.log.info(f"{logging_prefix} Finishing...")
        self.finish(json.dumps({"auto_attach": auto_attach, "e": error}))


def setup_handlers(web_app):
    base_url = web_app.settings["base_url"]
    cluster_id_regex = r"(?P<cluster_id>[\w-]+)"
    remote_ikernel_cluster_path = url_path_join(
        base_url, rf"/cluster-remote-ikernel/{cluster_id_regex}"
    )
    cluster_list_path = url_path_join(base_url, r"/bodo/cluster")
    auto_attach_path = url_path_join(base_url, r"/bodo/autoattach")

    handlers = [
        (remote_ikernel_cluster_path, ClusterRemoteIKernelHandler),
        (cluster_list_path, PlatformClusterListHandler),
        (auto_attach_path, AutoAttachHandler),
    ]
    web_app.add_handlers(".*$", handlers)
