import React, { Component } from 'react'
import {
  Switch,
  Route,
  Redirect
} from 'react-router-dom'
import './Product.less'

import ProductHome from './ProudctHome'
import ProductDetail from './ProductDetail'

/**
 * 商品管理
 */
export default class Product extends Component {

  render () {
    return (
      <Switch>
        <Route path="/product" exact component={ProductHome}/>
        <Route path="/product/detail/:id" component={ProductDetail}/>
        <Redirect to="/product" />
      </Switch>
    )
  }
}
