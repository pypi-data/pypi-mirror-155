import { Widget } from '@lumino/widgets';

type tutorialType = {
  [key: string]: {
    [key: string]: string;
  };
};

const tutorialIndex: { [key: string]: tutorialType } = {
  basics: {
    '0_data_ingestion': {
      label: 'Data Ingestion',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/0_data_ingestion.ipynb'
    },
    '1_data_processing': {
      label: 'Data Processing',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/1_data_processing.ipynb'
    },
    '2_feature_engineering': {
      label: 'Feature Engineer',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/2_feature_engineering.ipynb'
    },
    '3_neighbor_loader': {
      label: 'Neighbor Loader',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/3_neighborloader.ipynb'
    },
    '3_graph_loader': {
      label: 'Graph Loader',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/3_graphloader.ipynb'
    },
    '3_edge_loader': {
      label: 'Edge Loader',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/3_edgeloader.ipynb'
    },
    '3_vertex_loader': {
      label: 'Vertex Loader',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/basics/3_vertexloader.ipynb'
    },
    '4_graph_convolutional_network': {
      label: 'GCN (node classification)',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/gnn_pyg/gcn_node_classification.ipynb'
    },
    '4_graphSAGE': {
      label: 'GraphSAGE (node classification)',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/gnn_pyg/graphsage_node_classification.ipynb'
    },
    '4_graph_attention_network': {
      label: 'GAT (node classification)',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/gnn_pyg/gat_node_classification.ipynb'
    },
    '4_hetero_graph_attention_network': {
      label: 'HGAT (node classification)',
      url: 'https://raw.githubusercontent.com/TigerGraph-DevLabs/mlworkbench-docs/1.0/tutorials/gnn_pyg/hgat_node_classification.ipynb'
    }
  }
};

export class MLTutorials extends Widget {
  public constructor() {
    const body = document.createElement('div');
    const label = document.createElement('label');
    label.textContent = 'Tutorials:';

    const tutoSelect = document.createElement('select');
    const basics = tutorialIndex.basics;
    for (const tid of Object.keys(basics)) {
      const option = document.createElement('option');
      option.label = basics[tid].label;
      option.text = basics[tid].label;
      option.value = basics[tid].url;
      tutoSelect.appendChild(option);
    }

    body.appendChild(label);
    body.appendChild(tutoSelect);
    super({ node: body });
  }

  public getValue(): string {
    return this.inputNode.value;
  }

  public get inputNode(): HTMLSelectElement {
    return this.node.getElementsByTagName('select')[0];
  }
}
