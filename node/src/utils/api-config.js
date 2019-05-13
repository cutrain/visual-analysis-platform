const server = 'http://10.141.2.231:8081/';
//const server = 'http://localhost:8081/';
 //const server = 'http://web.ngrok.cutrain.top:8081/';
//const server = "https://easy-mock.com/mock/5c7fb3586498b753ed1f9cd0/vap/";
//const server = 'http://10.141.2.231:8081/';

const api = {
  server : server,
  /**
   * project
   */
  projectView : server + "project/view",
  projectCreate : server + "project/create",
  projectRename : server + "project/change",
  projectDelete : server + "project/delete",

  /**
   * graph
   */
  graphGet : server + "graph/get",
  graphSave : server + "graph/save",
  graphRun : server + "graph/run",
  graphProgress : server + "graph/progress",
  graphStop : server + "graph/stop",
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
  dataCreateSet : server + "data/createset",
  dataDownload : server + "data/download",

  /**
   * component
   */
  componentListView : server + "component/list",
  componentParameter : server + "component/param",
}

export default api;

