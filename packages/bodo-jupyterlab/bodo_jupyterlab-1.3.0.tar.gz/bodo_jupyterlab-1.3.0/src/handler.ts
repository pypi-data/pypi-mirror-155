import { URLExt } from '@jupyterlab/coreutils';

import { ServerConnection } from '@jupyterlab/services';

/**
 * Call the API extension
 *
 * @param path The API endpoint
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI<T>(path = '', init: RequestInit = {}): Promise<T> {
  // Make request to Jupyter API
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, path);
  console.debug('handler.ts:requestAPI:requestUrl: ', requestUrl);

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(requestUrl, init, settings);
  } catch (error: any) {
    console.error('handler.ts:requestAPI:error: ', error);
    throw new ServerConnection.NetworkError(error);
  }

  const data = await response.json();
  console.debug('handler.ts:requestAPI:data: ', data);

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message);
  }

  return data;
}

export async function createRemoteIKernelHandler(clusterUUID: string) {
  const data: { remote_kernel_name: string; e: any } = await requestAPI<any>(
    `cluster-remote-ikernel/${clusterUUID}`,
    { method: 'POST' }
  );
  if (data.e) {
    throw new Error(data.e);
  }
  return data.remote_kernel_name;
}

export async function getClusterListHandler() {
  const data: { clusters: any[]; e: any } = await requestAPI<any>(`bodo/cluster`, {
    method: 'GET',
  });
  if (data.e) {
    throw new Error(data.e);
  }
  return data.clusters;
}

export async function shouldAutoAttachHandler() {
  const data: { auto_attach: boolean; e: any } = await requestAPI<any>(`bodo/autoattach`, {
    method: 'Get',
  });
  if (data.e) {
    throw new Error(data.e);
  }
  return data.auto_attach;
}
