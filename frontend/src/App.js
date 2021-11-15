import React from 'react'
import Home from './Home'
import {BrowserRouter as Router,Switch,Route} from 'react-router-dom'

const App =()=>(
  <Router>
    <Switch>
      <Route exact path = '/' component={Home} />
    </Switch>
  </Router>
)
export default App;