import React, { Component } from 'react'
import { Redirect, Switch, Route } from 'react-router-dom'
import { Layout } from 'antd';

import LeftNav from '../../components/Left_Nav/Left_Nav'
import Header from '../../components/Header/Header'

import Home from '../Home/Home'
import Category from '../Category/Category'
import Product from '../Product/Product'
import Role from '../Role/Role'
import User from '../User/User'
import Bar from '../charts/bar'
import Line from '../charts/line'
import Pie from '../charts/pie'
import memoryUtils from "../../Utils/memoryUtils";

const { Footer, Sider, Content } = Layout


export default class Admin extends Component {
  render() {
    // 读取保存的user, 如果不存在, 直接跳转到登陆界面
    const token = memoryUtils.token
    if (!token) {
      // 自动跳转到登陆界面
      return <Redirect to="/login"/>
    }

    return (
      <Layout style={{ height: '100%' }}>
        <Sider>
          <LeftNav />
        </Sider>
        <Layout>
          <Header/>
          <Content style={{ background: 'white', margin: '20px'}}>
            <Switch>
              <Route path="/home" component={Home}/>
              <Route path='/category' component={Category} />
              <Route path='/product' component={Product} />
              <Route path='/role' component={Role} />
              <Route path='/user' component={User} />
              <Route path='/charts/bar' component={Bar} />
              <Route path='/charts/line' component={Line} />
              <Route path='/charts/pie' component={Pie} />
              <Redirect to="/home"/>
            </Switch>
          </Content>
          <Footer style={{ textAlign: 'center', color: 'rgba(0, 0, 0, 0.5)'}}>
            NFT marketplace ©2021
          </Footer>
        </Layout>
      </Layout>
    )
  }
}
