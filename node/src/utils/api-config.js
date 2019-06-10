const site = window.location.origin;
const server = site.substr(0, site.length-4)+ '8081/';
console.log(server);

const api = {
  server:server,
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
  dataDownload: server + "data/download",

  /**
   * component
   */
  componentListView : server + "component/list",
  componentParameter : server + "component/param",
}

export default api;

