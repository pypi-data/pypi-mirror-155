import { ISessionContext, ReactWidget, showErrorMessage } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { createRemoteIKernelHandler } from './handler';
import * as React from 'react';
import { ClusterStore } from './store';
import { ICluster } from './types';
import ClusterSelectList from './clusterSelect';
import { shouldAutoAttachHandler } from './handler';

interface IProps {
  store: ClusterStore;
  startKernelForCluster: (clusterUUID?: string) => Promise<boolean>;
  getClusterUUIDFromKernel: (kernelName: string) => Promise<any>;
  sessionContext: ISessionContext;
}

interface IState {
  clusters: ICluster[];
  currentClusterUUID: string | null;
  autoAttachState: boolean | null;
}

class ClusterSelect extends React.Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {
      clusters: props.store.clusters,
      currentClusterUUID: null,
      autoAttachState: null,
    };
    this._tryAutoAttach();
  }

  componentDidMount() {
    this.props.store.clusterChaged.connect(this._onClusterUpdate, this);
    this.props.sessionContext.sessionChanged.connect(this._onSessionUpdate, this);
  }

  componentWillUnmount() {
    this.props.store.clusterChaged.disconnect(this._onClusterUpdate, this);
    this.props.sessionContext.sessionChanged.disconnect(this._onSessionUpdate, this);
  }

  _onSessionUpdate(emitter: ISessionContext, newSession: any): void {
    console.log('Detected Session Change.');
    if (newSession.newValue?._kernel?._name) {
      console.debug('Session Change New Kernel Name: ', newSession.newValue._kernel._name);
      this.props.getClusterUUIDFromKernel(newSession.newValue._kernel._name).then(
        (clusterUUID) => {
          console.debug('Found cluster for this kernel: ', clusterUUID);
          this.setState({ currentClusterUUID: clusterUUID });
        },
        (reason: any) => {
          console.error('Error while getting cluster UUID from kernel: ', reason);
          console.error('Setting currentClusterUUID to null.');
          this.setState({ currentClusterUUID: null });
        }
      );
    } else {
      console.debug('Session has no kernel. Setting currentClusterUUID to null.');
      this.setState({ currentClusterUUID: null });
    }
  }

  async _onClusterUpdate(
    emitter: ClusterStore,
    newClusters: IChangedArgs<ICluster[] | undefined>
  ): Promise<void> {
    const { currentClusterUUID } = this.state;

    let newClusterList: ICluster[];
    if (newClusters.newValue) {
      newClusterList = newClusters.newValue;
    } else {
      newClusterList = [];
    }
    let newCurrentClusterUUID = currentClusterUUID;
    if (currentClusterUUID && !newClusterList.map((x) => x.uuid).includes(currentClusterUUID)) {
      newCurrentClusterUUID = null;
      showErrorMessage(
        'Cluster not available anymore!',
        'The cluster was removed or is being modified. Your session will be shutdown.'
      );
      this.props.startKernelForCluster(); // Change to no kernel
    }

    this.setState({
      clusters: newClusterList,
      currentClusterUUID: newCurrentClusterUUID,
    });

    this._tryAutoAttach();
  }

  async _tryAutoAttach(): Promise<void> {
    const { clusters, currentClusterUUID, autoAttachState } = this.state;
    let autoAttach = autoAttachState;
    let newCurrentClusterUUID = currentClusterUUID;

    // If autoAttach hasn't been fetched from the backend yet
    // fetch it. Since the response from the backend won't change
    // only fetch it once.
    if (autoAttachState === null) {
      autoAttach = await shouldAutoAttachHandler();
    }

    // If the notebook isn't attached to a cluster, there is only one cluster available
    // and is configured to have autoAttach enabled then start a kernel on the cluster
    // and set it as the currently attached cluster
    if (!currentClusterUUID && clusters.length === 1 && autoAttach) {
      this.props.startKernelForCluster(clusters[0].uuid).then((success) => {
        if (success) {
          newCurrentClusterUUID = clusters[0].uuid;
        }
      });
    }
    this.setState({ currentClusterUUID: newCurrentClusterUUID, autoAttachState: autoAttach });
  }

  selectClusterCallback(clusterUUID: string) {
    console.debug('[onSelectCluster] clusterUUID: ', clusterUUID);
    const { startKernelForCluster } = this.props;
    if (clusterUUID === '0') {
      startKernelForCluster(); // Change to "No Kernel"
      this.setState({ currentClusterUUID: null });
    } else {
      startKernelForCluster(clusterUUID).then((success) => {
        if (success) {
          this.setState({ currentClusterUUID: clusterUUID });
        } else {
          this.setState({ currentClusterUUID: null });
        }
      });
    }
  }

  render() {
    const { clusters, currentClusterUUID } = this.state;
    return (
      <ClusterSelectList
        myOnChange={this.selectClusterCallback.bind(this)}
        clusters={clusters}
        currentClusterUUID={currentClusterUUID}
      />
    );
  }
}

export class ToolbarExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  private _store: ClusterStore;

  constructor(store: ClusterStore) {
    this._store = store;
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    const startKernelForCluster = async (clusterUUID?: string) => {
      if (!clusterUUID) {
        console.log('No clusterUUID. Shutting session down...');
        await context.sessionContext.shutdown();
        return true;
      }

      console.log('Starting Kernel for clusterUUID: ', clusterUUID);

      console.debug(
        'Contacting Jupyter Server App to start remote kernel for clusterUUID: ',
        clusterUUID
      );
      let remoteKernelName: string;
      try {
        remoteKernelName = await createRemoteIKernelHandler(clusterUUID);
      } catch (e) {
        console.error('Unable to register a remote kernel: ', e);
        showErrorMessage(
          'Bodo Extension Errror: Unable to create a remote kernel on the cluster.',
          e
        );
        return false;
      }
      console.log('Refreshing kernel specs and changing to remote kernel: ', remoteKernelName);

      // Refresh the list of kernels
      await context.sessionContext.specsManager.refreshSpecs();
      // Switch to the remote kernel for this cluster
      await context.sessionContext.changeKernel({ name: remoteKernelName });
      return true;
    };

    const getClusterUUIDFromKernel = async (kernelName: string) => {
      console.debug('[getClusterUUIDFromKernel] kernelName: ', kernelName);
      console.debug(
        '[getClusterUUIDFromKernel] KernelSpecs: ',
        context.sessionContext.specsManager.specs?.kernelspecs
      );
      if (
        context.sessionContext.specsManager.specs &&
        kernelName in context.sessionContext.specsManager.specs.kernelspecs
      ) {
        const kernelspec = context.sessionContext.specsManager.specs.kernelspecs[kernelName];
        if (kernelspec) {
          const metadata = kernelspec.metadata;
          if (metadata) {
            if ('BodoClusterUUID' in metadata) {
              return metadata['BodoClusterUUID'];
            }
          }
        }
      }
      return null;
    };

    const dropdown = ReactWidget.create(
      <ClusterSelect
        store={this._store}
        startKernelForCluster={startKernelForCluster}
        getClusterUUIDFromKernel={getClusterUUIDFromKernel}
        sessionContext={context.sessionContext}
      />
    );

    panel.toolbar.insertItem(0, 'clusterSelect', dropdown);

    return new DisposableDelegate(() => {
      dropdown.dispose();
    });
  }
}
