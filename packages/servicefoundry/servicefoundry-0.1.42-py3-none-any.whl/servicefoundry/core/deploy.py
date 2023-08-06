from servicefoundry.core.notebook.notebook_util import get_default_callback, is_notebook
from servicefoundry.internal.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.internal.deploy.deploy import deploy as __deploy_remote
from servicefoundry.internal.deploy.deploy import deploy_local as __deploy_local
from servicefoundry.internal.package.package import package

process = None


def _deploy_local(packaged_output, callback):
    global process
    if not is_notebook():
        process = __deploy_local(packaged_output, callback)
        process.join()
    else:
        callback.start_panel()
        if process is not None and process.is_alive():
            callback.print_line("Stopping the old process.")
            process.stop()
            process.join()
            callback.print_line("Old process stopped.")
        process = __deploy_local(packaged_output, callback)
        callback.close_panel()


def deploy_local():
    callback = get_default_callback()
    packaged_output = package(callback=callback)
    return _deploy_local(packaged_output, callback)


def _deploy(packaged_output, callback):
    deployment = __deploy_remote(packaged_output)
    callback.print_line('Your service is being deployed. You can track your deployment at ${AUTH_UI}/workspace')
    return deployment


def deploy():
    callback = get_default_callback()
    packaged_output = package(callback=callback)
    _deploy(packaged_output, callback)
