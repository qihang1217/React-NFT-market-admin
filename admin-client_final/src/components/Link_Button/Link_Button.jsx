import React from 'react'
import {Button} from 'antd';

import './Link_Button.less'

export default function LinkButton(props) {
	return <Button type="link" {...props}/>
}