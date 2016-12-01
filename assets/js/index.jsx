import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, browserHistory, Link } from 'react-router';
import $ from 'jquery';
import App from './App';
import LandingPageView from './views/LandingPageView'
import DashboardView from './views/DashboardView'
import CheckInView from './views/CheckInView'

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
      <Route onEnter={isAuthenticated} path='/checkin' component={CheckInView} />
    </Route>
  </Router>
), document.getElementById('container'));