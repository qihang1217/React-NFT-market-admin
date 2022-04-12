import storageUtils from "./storageUtils"

// 初始时取一次并保存为user
const user = storageUtils.getUser()
const token = storageUtils.getToken()
export default {
	user, // 用来存储登陆用户的信息, 初始值为local中读取的user
	token, //
	product: {}, // 需要查看的NFT对象
}