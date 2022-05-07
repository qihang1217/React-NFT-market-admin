import React, {Component} from 'react'
import {Button, Card, Input, message, Select, Table} from 'antd'
import throttle from 'lodash/throttle'

import {reqProducts, reqSearchProducts, reqUpdateStatus} from '../../api/API'
import LinkButton from '../../components/Link_Button/Link_Button'
import {PRODUCT_PAGE_SIZE} from '../../Utils/Constants'
import memoryUtils from '../../Utils/memoryUtils';

const Option = Select.Option
/* 
NFT管理的首页组件
*/
export default class ProductHome extends Component {
	
	state = {
		loading: false,
		products: [], // NFT列表
		total: 0, // NFT的总数量
		searchType: 'examineStatus', // 默认按状态
		searchName: '', // 搜索的关键字
		isClickable: true,
	}
	
	updatePassStatus = throttle(async (product_id, pass_status) => {
		// 请求更新
		const result = await reqUpdateStatus(product_id, true)
		if (result.status === 0) {
			message.success('更新NFT状态成功!')
			// 获取当前页显示
			await this.getProducts(this.pageNum)
		}
	}, 2000)
	
	updateDenyStatus = throttle(async (product_id, pass_status) => {
		// 请求更新
		const result = await reqUpdateStatus(product_id, false)
		if (result.status === 0) {
			message.success('更新NFT状态成功!')
			// 获取当前页显示
			await this.getProducts(this.pageNum)
		}
	}, 2000)
	
	/*
	异步获取指定页码NFT分页(可能带搜索)列表显示
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
	
	setStateAsync(state) {
		return new Promise((resolve) => {
			this.setState(state, resolve)
		});
	}
	
	initColumns = () => {
		this.columns = [
			{
				title: 'NFT名称',
				dataIndex: 'product_name',
				sorter: (a, b) => a.product_name.length - b.product_name.length,
				defaultSortOrder: 'descend',
				align: 'center',
			},
			{
				title: '描述',
				dataIndex: 'description',
				align: 'center',
			},
			{
				title: '价格',
				width: 100,
				dataIndex: 'price',
				defaultSortOrder: 'descend',
				align: 'center',
				sorter: (a, b) => a.price - b.price,
				render: (price) => price + 'ETH',
			},
			{
				title: '通过状态',
				width: 120,
				align: 'center',
				sorter: (a, b) => a.pass_status.length - b.pass_status.length,
				// dataIndex: 'pass_status',
				render: ({pass_status}) => {
					let text = '不通过'
					if (pass_status === true) {
						text = '通过'
					}
					return (
						<span>
                            <span style={{marginRight: 10}}>{text}</span>
                        </span>
					)
				}
			},
			{
				title: '审核状态',
				width: 120,
				align: 'center',
				sorter: (a, b) => a.examine_status.length - b.examine_status.length,
				render: ({examine_status}) => {
					let text = '未审核'
					if (examine_status === true) {
						text = '已审核'
					}
					return (
						<span>
                            <span style={{marginRight: 10}}>{text}</span>
                        </span>
					)
				}
			},
			{
				title: '操作',
				width: 190,
				align: 'center',
				// dataIndex: 'pass_status',
				render: ({product_id, pass_status, examine_status}) => {
					//已审核则无法再次审核
					return (
						<>
							<Button
								type="primary"
								style={{marginRight: 15}}
								disabled={!this.state.isClickable || examine_status}
								onClick={() => {
									this.setState({isClickable: false})
									this.updatePassStatus(product_id, pass_status)
								}}
							>
								通过
							</Button>
							<Button
								type="primary"
								disabled={!this.state.isClickable || examine_status}
								onClick={() => {
									this.setState({isClickable: false})
									this.updateDenyStatus(product_id, pass_status)
								}}
							>
								不通过
							</Button>
						</>
					)
				}
			},
			{
				title: '详情',
				width: 100,
				align: 'center',
				render: (product) => (
					<span>
                        <LinkButton
	                        onClick={() => {
		                        // 在内存中保存product
		                        memoryUtils.product = product
		                        this.props.history.push('/product/detail/' + product.product_id)
	                        }}
                        >
                          详情
                        </LinkButton>
                    </span>
				)
			},
		]
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
	                <Option value="examineStatus">按审核状态搜索</Option>
	                <Option value="productStatus">按通过状态搜索</Option>
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
