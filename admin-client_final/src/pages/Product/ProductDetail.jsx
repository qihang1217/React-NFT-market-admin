import React, {Component} from 'react'
import {Card, Icon, List} from 'antd'

import LinkButton from '../../components/Link_Button/Link_Button'
import memoryUtils from '../../Utils/memoryUtils'
import {reqCategory, reqProduct} from '../../api/API'

const Item = List.Item

/* 
NFT详情路由组件
*/
export default class ProductDetail extends Component {

  state = {
    categoryName: '',
    product: memoryUtils.product
  }

  getCategory = async (categoryId) => {
    const result = await reqCategory(categoryId)
    if (result.status === 0) {
      const categoryName = result.data.category_name
      this.setState({categoryName})
    }
  }

  async componentDidMount() {
    let product = this.state.product
    if (product.product_id) { // 如果NFT有数据, 获取对应的分类
      await this.getCategory(product.category_id)
    } else { // 如果当前product状态没有数据, 根据id参数中请求获取NFT并更新
      const id = this.props.match.params.id
      const result = await reqProduct(id)
      if (result.status === 0) {
        product = result.data
        this.setState({
          product
        })
        await this.getCategory(product.category_id) // 获取对应的分类
      }
    }
  }

  render() {
    const {categoryName} = this.state
    const product = this.state.product

    const title = (
        <span>
        <LinkButton onClick={() => this.props.history.goBack()}>
          <Icon type="arrow-left"/>
        </LinkButton>
        <span>NFT详情</span>
      </span>
    )
    return (
        <Card title={title} className="detail">
          <List>
            <Item>
              <span className="detail-left">NFT名称:</span>
              <span>{product.product_name}</span>
            </Item>
            <Item>
              <span className="detail-left">NFT描述:</span>
              <span>{product.description}</span>
            </Item>
            <Item>
              <span className="detail-left">NFT价格:</span>
              <span>{product.price}元</span>
            </Item>
            <Item>
              <span className="detail-left">所属分类:</span>
              <span>{categoryName}</span>
            </Item>
            <Item>
              <span className="detail-left">NFT:</span>
            </Item>
            <Item>

            </Item>
          </List>
        </Card>
    )
  }
}
