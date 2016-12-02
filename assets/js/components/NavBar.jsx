import React from 'react';
import $ from 'jquery';
import LogoutBtn from './LogoutBtn'
import DashboardBtn from './DashboardBtn'
import CheckInBtn from './CheckInBtn'


let NavBar = ({username}) => (
  <nav className="light-green darken-1" role="navigation">
    <div className="nav-wrapper container"><a id="logo-container" href="#" className="brand-logo">drchrono</a>
      <ul className="right hide-on-med-and-down">
        {username !== null ? <LogoutBtn /> : <a></a>}
      </ul>
      <ul className="right hide-on-med-and-down">
        {username !== null ? <DashboardBtn /> : <a></a>}
      </ul>

      <ul className="right hide-on-med-and-down">
        {username !== null ? <CheckInBtn /> : <a></a>}
      </ul>

      <ul id="nav-mobile" className="side-nav">
        {username !== null ? <LogoutBtn /> : <a></a>}
      </ul>
      <ul id="nav-mobile" className="side-nav">
        {username !== null ? <DashboardBtn /> : <a></a>}
      </ul>

      <a href="#" data-activates="nav-mobile" className="button-collapse"><i className="material-icons">menu</i></a>
    </div>
  </nav>

);

export default NavBar;

 // <li><a href="#">Navbar Link</a></li>