import { IChangedArgs } from '@jupyterlab/coreutils';
import { Poll } from '@lumino/polling';
import { Signal, ISignal } from '@lumino/signaling';
import { CLUSTER_LIST_REFRESH_SECONDS } from './config';
import { ICluster } from './types';
import { getClusterListHandler } from './handler';
import { showErrorMessage } from '@jupyterlab/apputils';

class ClusterStore {
  private _clusters: ICluster[];
  private _poll: Poll<any, any, 'standby'>;
  private _clusterChanged: Signal<ClusterStore, IChangedArgs<ICluster[] | undefined>>;
  // If we've shown the error once, we shouldn't show it again.
  private _clusterListErrorShown = false;

  constructor() {
    this._clusters = [];
    // Initial update
    void this.updateClusters();

    this._clusterChanged = new Signal<this, IChangedArgs<ICluster[] | undefined>>(this);

    this._poll = new Poll({
      factory: async () => {
        await this.updateClusters();
      },
      frequency: {
        interval: CLUSTER_LIST_REFRESH_SECONDS * 1000,
        backoff: true,
        max: 60 * 1000,
      },
      standby: 'when-hidden',
    });

    this._poll.start();
  }

  public get clusters(): ICluster[] {
    return this._clusters;
  }

  public get clusterChaged(): ISignal<ClusterStore, IChangedArgs<ICluster[] | undefined>> {
    return this._clusterChanged;
  }

  private async getClustersList(): Promise<ICluster[]> {
    try {
      return (await getClusterListHandler()) as ICluster[];
    } catch (e) {
      console.error('Error in ClusterStore.getClustersList: ', e);
      if (!this._clusterListErrorShown) {
        showErrorMessage('Bodo Extension Errror: Unable to get cluster list', e);
        this._clusterListErrorShown = true;
      }
      return [];
    }
  }

  private clusterListHasChanged(oldList: ICluster[], newList: ICluster[]): boolean {
    if (oldList.length !== newList.length) {
      return true;
    }
    // Sort the lists by UUID
    oldList.sort((a, b) => (a.uuid < b.uuid ? -1 : 1));
    newList.sort((a, b) => (a.uuid < b.uuid ? -1 : 1));
    // Compare each element
    for (let i = 0; i < oldList.length; i++) {
      if (JSON.stringify(oldList[i]) !== JSON.stringify(newList[i])) {
        return true;
      }
    }
    return false;
  }

  private async updateClusters(): Promise<void> {
    const newClusters: ICluster[] = await this.getClustersList();

    // Only emit a signal if the list has changed or it's the first call
    if (this.clusterListHasChanged(this._clusters, newClusters)) {
      this._clusterChanged.emit({
        name: 'cluster',
        oldValue: this._clusters,
        newValue: newClusters,
      });
      this._clusters = newClusters;
    }
  }
}

export { ClusterStore };
