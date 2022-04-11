import React, {Component} from 'react'
import {Button, Card, Input, message, Select, Table} from 'antd'
import throttle from 'lodash/throttle'

import {reqProducts, reqSearchProducts, reqUpdateStatus} from '../../api/API'
import LinkButton from '../../components/Link_Button/Link_Button'
import {PRODUCT_PAGE_SIZE} from '../../Utils/Constants'
import memoryUtils from '../../Utils/memoryUtils';

const Option = Select.Option
/* 
商品管理的首页组件
*/
export default class ProductHome extends Component {

    state = {
        loading: false,
        products: [], // 商品列表
        total: 0, // 商品的总数量
        searchType: 'productName', // 默认是按商品名称搜索
        searchName: '', // 搜索的关键字
    }

    updateStatus = throttle(async (product_id, pass_status) => {
        // 计算更新后的值
        pass_status = pass_status === false;
        // 请求更新
        const result = await reqUpdateStatus(product_id, pass_status)
        if (result.status === 0) {
            message.success('更新商品状态成功!')
            // 获取当前页显示
            await this.getProducts(this.pageNum)
        }
    }, 2000)

    initColumns = () => {
        this.columns = [
            {
                title: 'NFT名称',
                dataIndex: 'product_name'
            },
            {
                title: '描述',
                dataIndex: 'description'
            },
            {
                title: '价格',
                width: 100,
                dataIndex: 'price',
                render: (price) => price + 'ETH'
            },
            {
                title: '状态',
                width: 100,
                // dataIndex: 'pass_status',
                render: ({product_id, pass_status}) => {
                    let btnText = '通过'
                    let text = '不通过'
                    if (pass_status === true) {
                        btnText = '不通过'
                        text = '通过'
                    }
                    return (
                        <span>
                          <button onClick={() => {
                              this.updateStatus(product_id, pass_status)
                          }}>
                              {btnText}
                          </button>
                            <br/>
                          <span>{text}</span>
                        </span>
                    )
                }
            },

            {
                title: '操作',
                width: 100,
                render: (product) => (
                    <span>
                        <LinkButton
                            onClick={() => {
                                // 在内存中保存product
                                memoryUtils.product = product
                                this.props.history.push('/Product/detail/' + product.product_id)
                            }}
                        >
                          详情
                        </LinkButton>
                    </span>
                )
            },
        ]
    }

    /*
    异步获取指定页码商品分页(可能带搜索)列表显示
    */
    getProducts = async (pageNum) => {
        // 保存当前请求的页码
        this.pageNum = pageNum
        const {searchName, searchType} = this.state
        let result
        // 发请求获取数据
        if (!this.isSearch) {
            result = await reqProducts(pageNum, PRODUCT_PAGE_SIZE)
        } else {
            result = await reqSearchProducts({pageNum, pageSize: PRODUCT_PAGE_SIZE, searchName, searchType})
        }

        if (result.status === 0) {
            // 取出数据
            const {total, list} = result.data
            // 更新状态
            this.setState({
                products: list,
                total
            })
        }
    }

    componentWillMount() {
        this.initColumns()
    }

    componentDidMount() {
        // 获取第一页显示
        this.getProducts(1)
    }

    render() {

        const {loading, products, total, searchType, searchName} = this.state

        const title = (
            <span>
                <Select
                    style={{width: 200}}
                    value={searchType}
                    onChange={(value) => this.setState({searchType: value})}
                >
                    <Option value="productName">按名称搜索</Option>
                    <Option value="productDesc">按描述搜索</Option>
                </Select>
                <Input
                    style={{width: 200, margin: '0 10px'}}
                    placeholder="关键字"
                    value={searchName}
                    onChange={event => this.setState({searchName: event.target.value})}
                />
                <Button type="primary" onClick={() => {
                    this.isSearch = true  // 保存搜索的标记
                    this.getProducts(1)
                }}>
                    搜索
                </Button>
            </span>
        )

        return (
            <Card title={title}>
                <Table
                    bordered={true}
                    rowKey="product_id"
                    loading={loading}
                    columns={this.columns}
                    dataSource={products}
                    pagination={{
                        total,
                        defaultPageSize: PRODUCT_PAGE_SIZE,
                        showQuickJumper: true,
                        onChange: this.getProducts,
                        current: this.pageNum
                    }}
                />
            </Card>
        )
    }
}
