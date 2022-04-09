export default class ApiUtil {
    static URL_IP = 'http://127.0.0.1:4999';
    static URL_ROOT = '/api/v1';
    static URL_WEB = '/api';
    static URL_INTERFACE = ApiUtil.URL_IP + ApiUtil.URL_ROOT

    static API_STAFF_UPDATE = ApiUtil.URL_INTERFACE + '/updateStaff';
    static API_STAFF_LIST = ApiUtil.URL_INTERFACE + '/getStaffList/';
    static API_STAFF_DELETE = ApiUtil.URL_INTERFACE + '/deleteStaff/';
    static API_STAFF_SEARCH_3 = ApiUtil.URL_INTERFACE + '/searchStaff_3';  //只搜索3个属性

    static API_LOGIN = ApiUtil.URL_INTERFACE + '/login';
    static API_CHECK_USERNAME = ApiUtil.URL_INTERFACE + '/checkUserName';
    static API_CHECK_PASSWORD = ApiUtil.URL_INTERFACE + '/checkPassword';
    static API_ADMIN = ApiUtil.URL_INTERFACE + '/gotoAdmin'; //进入管理员状态
    static API_EXPORT_TO_FILE = ApiUtil.URL_INTERFACE + '/export_to_file'; //将数据导出到文件

}