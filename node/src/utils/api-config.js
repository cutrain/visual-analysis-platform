// const server = 'http://localhost:8081/';
const server = 'http://web.ngrok.cutrain.top:8081/'
//const server = "https://easy-mock.com/mock/5c7fb3586498b753ed1f9cd0/vap/";
// const server = 'http://10.141.245.36:8081/';

const api = {
  /**
   * project 项目库，存储用户创建的项目及其流程图
   */
  projectView : server + "project/view",
  projectCreate : server + "project/create",
  projectRename : server + "project/change",
  projectDelete : server + "project/delete",
  // test : server + "/fake",

  /**
   * graph
   */
  graphGet : server + "graph/get",
  graphSave : server + "graph/save",
  graphRun : server + "graph/run",
  graphProgress : server + "graph/progress",
  graphStop : server + "graph/stop",
  // 查看运行后节点输出端的数据
  graphSample : server + "graph/sample",
  graphInit : server + "graph/init",

  /**
   * data
   */
  dataUpload : server + "data/upload",
  dataGet : server + "data/get",
  dataMove : server + "data/move",
  dataDelete : server + "data/delete",
  dataView : server + "data/view",

  /**
   * component
   */
  componentListView : server + "component/list",
  componentParameter : server + "component/param",
}

export default api;

