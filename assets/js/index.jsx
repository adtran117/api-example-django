import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import $ from 'jquery';
import App from './App';
import LandingPageView from './views/LandingPageView'

render((
  <Router history={browserHistory}>
    <Route component={App}>
      <Route path='/' component={LandingPageView} />
    </Route>
  </Router>
), document.getElementById('container'));