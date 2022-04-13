import React, {Component} from 'react'
import {Card, List} from 'antd'
import {LeftOutlined} from '@ant-design/icons';

import LinkButton from '../../components/Link_Button/Link_Button'
import memoryUtils from '../../Utils/memoryUtils'
import {reqCategory, reqProduct} from '../../api/API'
import ApiUtil from "../../Utils/ApiUtil";
import FileViewer from 'react-file-viewer';

const Item = List.Item

/* 
NFT详情路由组件
*/
export default class ProductDetail extends Component {
	
	state = {
		categoryName: '',
		product: memoryUtils.product,
		previewTitle: '',
		previewContent: null,
	}
	
	getCategory = async (categoryId) => {
		const result = await reqCategory(categoryId)
		if (result.status === 0) {
			const categoryName = result.data.category_name
			this.setState({categoryName})
		}
	}
	
	renderFile = (product) => {
		console.log(product)
		//文件名
		const filename = product.file_url
		//文件类型
		const filetype = product.file_type
		//文件扩展名
		const ext = filename.substring(filename.lastIndexOf('.') + 1);
		//文件远程地址
		const src = ApiUtil.API_FILE_URL + filename
		if (/^image\/\S+$/.test(filetype)) {
			this.setState({
				previewContent: <img src={src} alt={filename} className='file'/>
			})
		} else if (/^video\/\S+$/.test(filetype)) {
			this.setState({
				previewContent: <video src={src} loop preload controls className='file'/>
			})
		} else if (/^audio\/\S+$/.test(filetype)) {
			this.setState({
				previewContent:
					<audio controls preload className='file'>
						<source src={src}/>
						<embed src={src}/>
					</audio>
			})
		} else if (/^text\/\S+$/.test(filetype)) {
			//	实际是前台存储的docx和pdf格式(前台将其类型规定为text)
			this.setState({
				previewContent:
					<FileViewer
						fileType={ext}
						filePath={src}
					/>
			})
		} else {
			this.setState({
				previewContent:
					<FileViewer
						fileType={ext}
						filePath={src}
					/>
			})
		}
		
	}
	
	async initProduct() {
		let product = this.state.product
		if (product.product_id) { // 如果NFT有数据, 获取对应的分类
			await this.getCategory(product.category_id)
			// console.log(product)
		} else { // 如果当前product状态没有数据, 根据id参数中请求获取NFT并更新
			const id = this.props.match.params.id
			const result = await reqProduct(id)
			// console.log(result)
			if (result.status === 0) {
				// console.log(result)
				product = result.data
				this.setState({
					product
				})
				this.getCategory(product.category_id) // 获取对应的分类
			}
		}
		if (product.file_url) {
			this.renderFile(product)
		}
	}
	
	componentDidMount() {
		this.initProduct()
	}
	
	render() {
		const {categoryName} = this.state
		const product = this.state.product
		
		
		const title = (
			<span>
		        <LinkButton onClick={() => this.props.history.goBack()}>
		          <LeftOutlined/>
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
						<div className="file-content">
							{this.state.previewContent}
						</div>
					</Item>
				</List>
			</Card>
		)
	}
}
