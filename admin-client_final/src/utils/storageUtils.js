import store from 'store'

const USER_KEY = 'user_key'
const TOKEN_KEY = 'token_key'

export default {
  /*
  保存user
  */
  saveUser (user) {
    // localStorage.setItem(USER_KEY, JSON.stringify(User))
    store.set(USER_KEY, user)
  },

  /*
  返回一个user对象, 如果没有返回一个{}
  */
  getUser () {
    // return JSON.parse(localStorage.getItem(USER_KEY) || '{}')
    return store.get(USER_KEY) || {}
  },

  /*
  删除保存的token
  */
  removeUser () {
    // localStorage.removeItem(USER_KEY)
    store.remove(USER_KEY)
  },

  /*
  保存token
  */
  saveToken (token) {
    // localStorage.setItem(USER_KEY, JSON.stringify(User))
    store.set(TOKEN_KEY, token)
  },

  /*
  返回一个token对象, 如果没有返回一个{}
  */
  getToken () {
    // return JSON.parse(localStorage.getItem(USER_KEY) || '{}')
    return store.get(TOKEN_KEY) || null
  },

  /*
  删除保存的user
  */
  removeToken () {
    // localStorage.removeItem(USER_KEY)
    store.remove(TOKEN_KEY)
  },
}