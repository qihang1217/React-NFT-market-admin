import React, {Component} from 'react'
import {Redirect, withRouter} from 'react-router-dom'
import {Button, Checkbox, Form, Input, message} from 'antd'
import {LockOutlined, UserOutlined} from '@ant-design/icons';

import logo from '../../assets/images/logo.png'
import './Login.less'
import storageUtils from '../../Utils/storageUtils'
import HttpUtil from "../../Utils/HttpUtil";
import ApiUtil from "../../Utils/ApiUtil";
import memoryUtils from "../../Utils/memoryUtils";

class Login extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    async handleSubmit(e) {
        let md5 = require("../../Utils/md5.js"); //引入md5加密模块
        e.password = md5(e.password);
        e['token'] = storageUtils.getToken()
        console.log(e)
        HttpUtil.post(ApiUtil.API_LOGIN, e).then(function (response) {
            console.log(response);
            if (response.responseCode === 200 && response.message === '验证成功') {
                message.success('登陆成功~');
                if (response.token_message !== 'success') {
                    storageUtils.saveToken(response.token)
                }
                // 将user信息保存到local
                const user = response.data[0]
                console.log(user)
                // localStorage.setItem('user_key', JSON.stringify(User))
                storageUtils.saveUser(user)
                //页面跳转
                window.location.href='/'
            } else if (response.responseCode === 200 && response.message === '用户不存在') {
                message.error('账号或密码错误,请稍后重试~');
            } else if (response.responseCode === 200 && response.message === '验证失败') {
                message.error('账号或密码错误,请稍后重试~');
            } else {
                message.error('登陆错误,请稍后重试~');
            }
        }).catch(function (error) {
            // console.log(error);
        });
    }

    render() {

        // 读取保存的user, 如果存在, 直接跳转到管理界面
        const token = memoryUtils.token
        if (token) {
            return <Redirect to="/"/> // 自动跳转到指定的路由路径
        }

        return (
            <div className="login">
                <div className="login-header">
                    <img src={logo} alt="logo"/>
                    <h1>NFT市场后台管理系统</h1>
                </div>
                <div className="login-content">
                    <div className="content-left">
                        <h1>用户登陆</h1>
                        <Form
                            name="normal_login" className="login-form"
                            initialValues={{
                                remember: true,
                            }}
                            onFinish={this.handleSubmit}
                        >
                            <Form.Item
                                name="user_name"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input your Username!',
                                    },
                                ]}
                            >
                                <Input
                                    prefix={<UserOutlined className="site-form-item-icon"
                                                          style={{color: 'rgba(0,0,0,.25)'}}/>}
                                    placeholder="用户名"
                                />
                            </Form.Item>
                            <Form.Item
                                name="password"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input your Password!',
                                    },
                                ]}
                            >
                                <Input
                                    prefix={<LockOutlined className="site-form-item-icon"
                                                          style={{color: 'rgba(0,0,0,.25)'}}/>}
                                    type="password"
                                    placeholder="密码"
                                />
                            </Form.Item>
                            <Form.Item>
                                <Form.Item name="remember" valuePropName="checked" noStyle>
                                    <Checkbox>Remember me</Checkbox><a className="login-form-forgot" href="">
                                    Forgot password
                                </a>
                                </Form.Item>
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit" className="login-form-button">登 陆</Button>
                            </Form.Item>
                        </Form>
                    </div>
                    <div className="content-right">

                    </div>
                </div>
            </div>
        )
    }
}

export default withRouter(Login);