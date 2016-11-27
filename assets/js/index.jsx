import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, browserHistory, Link } from 'react-router';
import $ from 'jquery';
import App from './App';
import LandingPageView from './views/LandingPageView'
import DashboardView from './views/DashboardView'

function isAuthenticated() {
  $.ajax({
      method: 'GET',
      url: 'api/getUserInfo'
    }).done((data) => {
      if(!JSON.parse(data)) {
        browserHistory.push('/')
      }
  })
}

render((
  <Router history={browserHistory}>
    <Route component={App}>
      <Route onEnter={isAuthenticated} path='/' component={LandingPageView} />
      <Route onEnter={isAuthenticated} path='/dashboard' component={DashboardView} />
    </Route>
  </Router>
), document.getElementById('container'));