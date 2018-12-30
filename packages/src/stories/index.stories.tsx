import { storiesOf } from '@storybook/react';
import * as React from 'react';

import { PlayerCard } from "../components/PlayerCard"

storiesOf('Player Summary', module)
  .add('player card', () => <PlayerCard playerId="test-player-1"/> );
  