import * as React from 'react';

export namespace PlayerCard {
    export interface Props {
        playerId: string;
    }
}

export class PlayerCard extends React.PureComponent<PlayerCard.Props> {
    public render() {
        return (
            <div className="blp-player-card">
                Hello, World! Displaying information for player with id: {this.props.playerId}.
            </div>
        );
    }
}
