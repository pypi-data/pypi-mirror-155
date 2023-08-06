import * as React from 'react';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { ClusterStore } from './store';
import { ICluster } from './types';
import { ReactWidget } from '@jupyterlab/apputils';

interface IClusterListingItemProps {
  cluster: ICluster;
}

function ClusterListItem(props: IClusterListingItemProps) {
  const { cluster } = props;
  const itemClass = 'bodo-ClusterListingItem';

  return (
    <li className={itemClass} data-cluster-id={cluster.uuid} key={cluster.uuid}>
      <div className="bodo-ClusterListingItem-title">{cluster.name}</div>
      <div className="bodo-ClusterListingItem-stats">State: {cluster.status}</div>
      <div className="bodo-ClusterListingItem-stats">
        Number of instances: {cluster.workersQuantity}
      </div>
      <div className="bodo-ClusterListingItem-stats">Instance Type: {cluster.instanceType}</div>
      <div className="bodo-ClusterListingItem-stats">Bodo Version: {cluster.bodoVersion}</div>
      <div className="bodo-ClusterListingItem-stats">Cluster ID: {cluster.uuid}</div>
    </li>
  );
}

function EmptyClustersList(props: any) {
  const itemClass = 'bodo-ClusterListingItem';

  return (
    <li className={itemClass}>
      <div className="bodo-ClusterListingItem-title">No Clusters</div>
    </li>
  );
}

interface IClusterListProps {
  store: ClusterStore;
}
interface IClusterListState {
  clusters: ICluster[];
}

export class ClusterList extends React.Component<IClusterListProps, IClusterListState> {
  constructor(props: IClusterListProps) {
    super(props);
    this.state = { clusters: props.store.clusters };
  }

  componentDidMount() {
    this.props.store.clusterChaged.connect(this._onClusterUpdate, this);
  }

  componentWillUnmount() {
    this.props.store.clusterChaged.disconnect(this._onClusterUpdate, this);
  }

  _onClusterUpdate(emitter: ClusterStore, newClusters: IChangedArgs<ICluster[] | undefined>): void {
    let newClusterList: ICluster[];
    if (newClusters.newValue) {
      newClusterList = newClusters.newValue;
    } else {
      newClusterList = [];
    }
    this.setState({ clusters: newClusterList });
  }

  render() {
    const { clusters } = this.state;
    let listing;
    if (clusters.length > 0) {
      listing = clusters.map((cluster) => {
        return <ClusterListItem cluster={cluster} />;
      });
    } else {
      listing = <EmptyClustersList />;
    }

    // Return the JSX component.
    return (
      <div className="bodo-ClusterManager">
        <div className="bodo-ClusterListing">
          <h2>Bodo Clusters</h2>
          <ul className="bodo-ClusterListing-list">{listing}</ul>
        </div>
      </div>
    );
  }
}

export class BodoClusterListSidebar extends ReactWidget {
  private _store: ClusterStore;

  constructor(store: ClusterStore) {
    super();
    this.addClass('bodo-Sidebar');
    this._store = store;
  }

  render() {
    return (
      <div>
        <ClusterList store={this._store} />
      </div>
    );
  }
}
