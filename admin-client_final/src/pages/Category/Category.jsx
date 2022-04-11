import React, {Component} from 'react'
import {Button, Card, Form, Icon, Input, message, Modal, Table} from 'antd'

import {reqAddCategory, reqCategories, reqUpdateCategory} from '../../api'
import LinkButton from '../../components/Link_Button/Link_Button'
import {CATEGORY_PAGE_SIZE} from "../../Utils/Constants";


/**
 * 分类管理
 */
export default class Category extends Component {

    formRef = React.createRef();
    state = {
        categorys: [], // 所有分类的数组
        loading: false, // 是否正在请求加载中
        showStatus: 0, // 0: 不显示, 1: 显示添加, 2: 显示修改
    }

    /*
    初始化table的所有列信息的数组
    */
    initColumns = () => {
        this.columns = [
            {
                title: '分类名称',
                dataIndex: 'category_name',
            },
            {
                title: '操作',
                width: 300,
                render: (category) =>
                    <LinkButton onClick={() => {
                        console.log(category)
                        this.category = category // 保存当前分类, 其它地方都可以读取到
                        this.setState({showStatus: 2})
                    }}>修改分类名称</LinkButton>
            },
        ]
    }

    /*
      异步获取分类列表显示
    */
    getCategorys = async () => {
        // 显示loading
        this.setState({loading: true})
        // 发异步ajax请求
        const result = await reqCategories()
        // 隐藏loading
        this.setState({loading: false})
        if (result.status === 0) {
            // 成功
            // 取出分类列表
            const categorys = result.data
            // 更新状态categorys数据
            this.setState({
                categorys
            })
        } else {
            message.error('获取分类列表失败')
        }
    }

    /*
      点击确定的回调: 去添加/修改分类
    */
    handleOk = () => {

        // 进行表单验证
        this.formRef.current.validateFields().then(async values => {
            // 验证通过后, 得到输入数据
            const {categoryName} = values
            const {showStatus} = this.state
            let result
            if (showStatus === 1) { // 添加
                // 添加分类
                result = await reqAddCategory(categoryName)
            } else {
                // 修改分类
                const categoryId = this.category.category_id
                result = await reqUpdateCategory({categoryId, categoryName})
            }

            this.setState({showStatus: 0})

            const action = showStatus === 1 ? '添加' : '修改'
            // 根据响应结果, 做不同处理
            if (result.status === 0) {
                // 重新获取分类列表显示
                await this.getCategorys()
                message.success(action + '更新分类成功')
            } else {
                message.error(action + '更新分类失败')
            }
        })
    }

    /*
      点击取消的回调
    */
    handleCancel = () => {
        this.setState({
            showStatus: 0
        })
    }


    componentWillMount() {

        this.initColumns()
    }

    componentDidMount() {
        this.getCategorys()

    }

    render() {

        // 取出状态数据
        const {categorys, loading, showStatus} = this.state

        // 读取更新的分类名称
        const category = this.category || {}

        // Card右上角的结构
        const extra = (
            <Button type="primary" onClick={() => {
                this.category = null
                this.setState({showStatus: 1})
            }}>
                <Icon type="plus"/>
                添加
            </Button>
        )

        return (
            <Card extra={extra}>
                <Table
                    bordered={true}
                    rowKey="category_id"
                    loading={loading}
                    columns={this.columns}
                    dataSource={categorys}
                    pagination={{defaultPageSize: CATEGORY_PAGE_SIZE, showQuickJumper: true}}
                />

                <Modal
                    //关闭后自动清空
                    destroyOnClose
                    title={showStatus === 1 ? "添加分类" : "修改分类名称"}
                    visible={showStatus !== 0}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                >
                    <Form ref={this.formRef}>
                        <Form.Item
                            name="categoryName"
                            initialValue={category.category_name || ''}
                            rules={[
                                {required: true, message: '分类名称必须输入'},
                            ]}
                        >
                            <Input type="text" placeholder="请输入分类名称"/>
                        </Form.Item>
                    </Form>
                </Modal>
            </Card>
        )
    }
}

