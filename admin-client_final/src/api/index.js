/* 
包含应用中所有请求接口的函数: 接口请求函数
函数的返回值都是promise对象
*/
import ajax from './ajax'
import ApiUtil from "../Utils/ApiUtil";
import HttpUtil from "../Utils/HttpUtil";

const BASE = ''

// 请求登陆
export const reqLogin = (e) => {
    return HttpUtil.post(ApiUtil.API_LOGIN, e)
}

// const persons/personList/personArr = [{}, {}]

// 获取分类列表
// export const reqCategorys = () => ajax.get(BASE + '/manage/Category/list')
/* export const reqCategorys = () => ajax({
  // method: 'GET',
  url: BASE + '/manage/Category/list'
}) */
export const reqCategorys = () => ajax(BASE + '/manage/Category/list')

// 添加分类
export const reqAddCategory = (categoryName) => ajax.post(BASE + '/manage/Category/add', {
    categoryName
})

// 修改分类
export const reqUpdateCategory = ({categoryId, categoryName}) => ajax.post(BASE + '/manage/Category/update', {
    categoryId,
    categoryName
})

// 根据分类id获取分类
export const reqCategory = (categoryId) => ajax(BASE + '/manage/Category/info', {
    params: {
        categoryId
    }
})

/* 获取NFT分页列表 */
export const reqProducts = (pageNum, pageSize) => {
    return HttpUtil.get(ApiUtil.API_PRODUCT_LIST + `?pageNum=${pageNum}&pageSize=${pageSize}`)
}


/* 根据Name/desc搜索NFT分页列表 */
export const reqSearchProducts = ({pageNum,pageSize,searchName,searchType})=> {
    return HttpUtil.get(ApiUtil.API_SEARCH_PRODUCT_LIST + `?pageNum=${pageNum}&pageSize=${pageSize}&${searchType}=${searchName}`)
}


/* 根据NFT ID获取NFT */
export const reqProduct = (productId) => ajax(BASE + '/manage/Product/info', {
    params: {
        productId
    }
})

/* 对NFT进行通过/不通过处理 */
export const reqUpdateStatus = (product_id, pass_status) => {
    return HttpUtil.post(ApiUtil.API_PRODUCT_UPDATE_STATUS, {product_id, pass_status})
}


/* 删除图片 */
export const reqDeleteImg = (name) => ajax.post(BASE + '/manage/img/delete', {name})

/* 添加/修改NFT */
export const reqAddUpdateProduct = (product) => ajax.post(
    BASE + '/manage/Product/' + (product._id ? 'update' : 'add'),
    product
)

// 获取所有角色的列表
export const reqRoles = () => ajax(BASE + '/manage/Role/list')
// 添加角色
export const reqAddRole = (roleName) => ajax.post(BASE + '/manage/Role/add', {
    roleName
})
// 更新角色
export const reqUpdateRole = (role) => ajax.post(BASE + '/manage/Role/update', role)

// 获取所有用户的列表
export const reqUsers = () => ajax(BASE + '/manage/User/list')
// 删除指定用户
export const reqDeleteUser = (userId) => ajax.post(BASE + '/manage/User/delete', {
    userId
})
// 添加/更新用户
export const reqAddOrUpdateUser = (user) => ajax.post(BASE + '/manage/User/' + (user._id ? 'update' : 'add'), user)