export default class ApiUtil {
    static URL_IP = 'http://127.0.0.1:4999';
    static FRONT_IP = 'http://127.0.0.1:5000';
    static UPLOAD_FOLDER = '/upload_folder/';
    
    static URL_ROOT = '/api/admin';
    static URL_INTERFACE = ApiUtil.URL_IP + ApiUtil.URL_ROOT;
    
    static API_LOGIN = ApiUtil.URL_INTERFACE + '/login';
    static API_PRODUCT_LIST = ApiUtil.URL_INTERFACE + '/manage/product/list';
    static API_PRODUCT_UPDATE_STATUS = ApiUtil.URL_INTERFACE + '/manage/product/updateStatus';
    static API_SEARCH_PRODUCT_LIST = ApiUtil.URL_INTERFACE + '/manage/product/search';
    static API_CATEGORY_LIST = ApiUtil.URL_INTERFACE + '/manage/category/list';
    static API_ADD_CATEGORY = ApiUtil.URL_INTERFACE + '/manage/category/add';
    static API_UPDATE_CATEGORY = ApiUtil.URL_INTERFACE + '/manage/category/update';
    static API_CATEGORY_BY_ID = ApiUtil.URL_INTERFACE + '/manage/category/id';
    static API_PRODUCT_BY_ID = ApiUtil.URL_INTERFACE + '/manage/product/id';
    static API_FILE_URL = ApiUtil.FRONT_IP + ApiUtil.UPLOAD_FOLDER;
}