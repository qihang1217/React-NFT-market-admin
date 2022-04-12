import React, {Component} from 'react'
import {BrowserRouter, Route, Switch} from "react-router-dom"

import Login from './pages/Login/Login'
import Admin from './pages/Admin/Admin'

/*
应用根组件
 */
class App extends Component {
	render() {
		return (
			<BrowserRouter>
				<Switch>
					{/* /Login */}
					<Route path="/login" component={Login}/>
					<Route path="/" component={Admin}/>
				</Switch>
			</BrowserRouter>
		)
	}
}

export default App
