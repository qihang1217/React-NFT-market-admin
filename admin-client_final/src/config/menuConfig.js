const menuList = [
	{
		title: '首页', // 菜单标题名称
		key: '/home', // 对应的path
		icon: 'home', // 图标名称
		public: true, // 公开的
	},
	{
		title: 'NFT',
		key: '/products',
		icon: 'appstore',
		children: [ // 子菜单列表
			{
				title: '种类管理',
				key: '/category',
				icon: 'bars'
			},
			{
				title: '铸造管理',
				key: '/product',
				icon: 'tool'
			},
		]
	},
	
	{
		title: '用户管理',
		key: '/user',
		icon: 'user'
	},
	{
		title: '角色管理',
		key: '/role',
		icon: 'safety',
	},
	
	{
		title: '图形图表',
		key: '/charts',
		icon: 'area-chart',
		children: [
			{
				title: '柱形图',
				key: '/charts/bar',
				icon: 'bar-chart'
			},
			{
				title: '折线图',
				key: '/charts/line',
				icon: 'line-chart'
			},
			{
				title: '饼图',
				key: '/charts/pie',
				icon: 'pie-chart'
			},
		]
	},
]

export default menuList