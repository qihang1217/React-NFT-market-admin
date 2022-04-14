import React, {Component} from 'react'
import {BrowserRouter, Route, Switch} from "react-router-dom"

import Login from './pages/Login/Login'
import Admin from './pages/Admin/Admin'
import zhCN from 'antd/es/locale/zh_CN';
import {ConfigProvider} from "antd";

/*
应用根组件
 */
class App extends Component {
	render() {
		return (
			<ConfigProvider locale={zhCN}>
				<BrowserRouter>
					<Switch>
						{/* /Login */}
						<Route path="/login" component={Login}/>
						<Route path="/" component={Admin}/>
					</Switch>
				</BrowserRouter>
			</ConfigProvider>
		)
	}
}

export default App
