import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import { Modal } from 'antd'

import LinkButton from '../Link_Button/Link_Button'
import {reqWeather} from '../../api'
import { formateDate } from '../../Utils/dateUtils'
import menuList from '../../config/menuConfig'
import memoryUtils from '../../Utils/memoryUtils'
import storageUtils from '../../Utils/storageUtils'

import './Header.less'

class Header extends Component {
  state = {
    currentTime: formateDate(Date.now()),
  }

  /* 
    退出登陆
  */
  logout = () => {
    // 显示确认提示
    Modal.confirm({
      title: '确认退出登陆吗?',
      okText:'确认',
      cancelText: '取消',
      onOk: () => {
        // console.log('OK');
        // 确定后, 删除存储的用户信息
        // local中的
        storageUtils.removeUser()
        storageUtils.removeToken()
        // 内存中的
        memoryUtils.user = {}
        memoryUtils.token = ''
        // 跳转到登陆界面
        this.props.history.replace('/Login')
      },
      onCancel() {
        // console.log('Cancel');
      },
    })
    
  }

  /* 
  根据当前请求的path得到对应的title
  */
  getTitle = () => {
    let title = ''
    const path = this.props.location.pathname
    menuList.forEach(item => {
      if (item.key===path) {
        title = item.title
      } else if (item.children) {
        const cItem = item.children.find(cItem => path.indexOf(cItem.key)===0)
        if (cItem) {
          title = cItem.title
        }
      }
      
    })

    return title
  }

  componentDidMount () {
    // 启动循环定时器
    this.intervalId = setInterval(() => {
      // 将currentTime更新为当前时间值
      this.setState({
        currentTime: formateDate(Date.now())
      })
    }, 1000);
  }

  componentWillUnmount () {
    // 清除定时器
    clearInterval(this.intervalId)
  }


  render() {

    const { currentTime,weather } = this.state

    const user = memoryUtils.user
    // 得到当前需要显示的title
    const title = this.getTitle()

    return (
      <div className="header">
        <div className="header-top">
          欢迎, {user.admin_name} &nbsp;&nbsp;

          {/* 组件的标签体作为标签的children属性传入 */}
          <LinkButton onClick={this.logout}>退出</LinkButton>
        </div>
        <div className="header-bottom">
          <div className="header-bottom-left">{title}</div>
          <div className="header-bottom-right">
            <span>{ currentTime }</span>
          </div>
        </div>
      </div>
    )
  }
}

export default withRouter(Header)
