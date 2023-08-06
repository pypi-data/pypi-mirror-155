import React from 'react';
import {
  ServerType,
  ServerControllerState,
  ServerControllerProps
} from './types';
import { ServerDetailForm } from './ServerDetailForm';
import { DBController } from './database';
import { editIcon, closeIcon } from '@jupyterlab/ui-components';

export class ServerController extends React.Component<
  ServerControllerProps,
  ServerControllerState
> {
  constructor(props: ServerControllerProps) {
    super(props);

    this.state = {
      renderView: 'default'
    };

    this.setEditingState = this.setEditingState.bind(this);
    this.updateServer = this.updateServer.bind(this);
    this.handleExit = this.handleExit.bind(this);
    this.deleteServer = this.deleteServer.bind(this);
  }

  setEditingState(state: boolean): void {
    if (state) {
      this.setState({ renderView: 'editing' });
    } else {
      this.setState({ renderView: 'default' });
    }
  }

  updateServer(newServer: ServerType): void {
    this.props.updateServer(this.props.id, newServer);
  }

  deleteServer(): void {
    this.props.deleteServer(this.props.id);
  }

  handleExit(): void {
    this.setState({ renderView: 'default' });
  }

  render(): JSX.Element {
    if (this.state.renderView === 'editing') {
      return (
        <fieldset>
          <ServerDetailForm
            serverName={this.props.serverName}
            serverAddress={this.props.serverAddress}
            hostOS={this.props.hostOS}
            restPort={this.props.restPort}
            gsqlPort={this.props.gsqlPort}
            setEditingState={this.setEditingState}
            submitServerDetail={this.updateServer}
          />
        </fieldset>
      );
    } else if (this.state.renderView === 'database') {
      return (
        <fieldset>
          <DBController
            handleExit={this.handleExit}
            serverAddress={this.props.serverAddress}
            restPort={this.props.restPort}
            gsqlPort={this.props.gsqlPort}
            hostOS={this.props.hostOS}
            jupyterApp={this.props.jupyterApp}
          />
        </fieldset>
      );
    } else {
      return (
        <fieldset>
          <legend>{this.props.serverName}</legend>
          <p>
            {this.props.serverAddress}
            <button
              className="btn-invisible"
              onClick={() => this.setState({ renderView: 'editing' })}
            >
              <editIcon.react
                height="14px"
                margin-bottom="-2px"
                margin-left="2px"
                padding="0px"
              />
            </button>
            <button
              className="btn-invisible"
              onClick={() => this.deleteServer()}
            >
              <closeIcon.react
                height="14px"
                margin-bottom="-2px"
                margin-left="2px"
                padding="0px"
              />
            </button>
          </p>
          <button onClick={() => this.setState({ renderView: 'database' })}>
            GraphStudio
          </button>
        </fieldset>
      );
    }
  }
}
