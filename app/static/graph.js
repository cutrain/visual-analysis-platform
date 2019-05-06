'use strict';

// ====================================================== global setting ===========================================
const server = '';
const routes = {
  'component_list' : server + '/component/list',
  'component_param' : server + '/component/param',
  'graph_run' : server + '/graph/run',
  'graph_progress' : server + '/graph/progress',
  'graph_sample' : server + '/graph/sample',
  'graph_stop' : server + '/graph/stop',
  'graph_save' : server + '/graph/save',
  'graph_load' : server + '/graph/get',
  'graph_clean' : server + '/graph/init',
};
const LINE_CIRCLE_X_BIAS = 8;
const LINE_CIRCLE_Y_BIAS = 8;
const CIRCLE_X_BIAS = -6;
const CIRCLE_Y_BIAS = -6;
const CIRCLE_Y_AWAY = 3;


const type_detail = new Map(); // {param_name: {"name":"", "display":"", "in_port":[], "out_port":[], "params":[{"name","display","type","default","list","note"} ]}}
const drag_data = new Map(); // replace default event dataTransfer
var curr_id = null; // selected node id
var G = null;
var finished = true; // check running state

// ====================================================== Renderer class ============================================
class Renderer{
  constructor(container_selector = '.canvas') {
    this.container = $(container_selector);
    // TODO : change svg id
    this.svg_selector = '#svg';
    this.nodes = [];
    this.lines = [];
  }

  addNode(node_id, posiX, posiY){
    let node_type = node_id.split('-')[0];
    let itype = type_detail.get(node_type);
    let node_name = itype.display;
    let in_port_num = itype.in_port.length;
    let out_port_num = itype.out_port.length;
    
    // TODO : spec canvas id
    let $node = $('<div></div>');
    $node.attr("class", "node noselect");
    $node.attr("id", node_id);
    bind_node($node);
    $node.css({"top":posiY, "left":posiX});
    $node.text(node_name);
    $node.click(node_click);

    this.container.append($node);
    let $circle = $('<div></div>');
    $circle.attr('class', 'circle noselect');
    bind_circle($circle);

    function get_full_width(obj) {
      return obj.width() + parseInt(obj.css('padding-left')) + parseInt(obj.css('padding-right'));
    }
    function get_full_height(obj) {
      return obj.height() + parseInt(obj.css('padding-top')) + parseInt(obj.css('padding-bottom'));

    }
    let circle_width = get_full_width($node);
    let circle_height = get_full_height($node);

    // TODO: change x/y bias & check div relation
    for (let i = 0;i < in_port_num; ++ i) {
      let in_circle = $circle.clone();
      in_circle.attr("id", node_id + "-in-" + i);
      in_circle.css("top", CIRCLE_Y_BIAS - CIRCLE_Y_AWAY + 'px');
      in_circle.css("left", Math.floor(circle_width/(1+in_port_num) * (i + 1) + CIRCLE_X_BIAS) + 'px');
      $node.append(in_circle);
    }

    // TODO: change x/y bias & check div relation
    for (let i = 0;i < out_port_num; ++ i) {
      let out_circle = $circle.clone();
      out_circle.attr("id", node_id + "-out-" + i);
      out_circle.css("top", Math.floor(circle_height + CIRCLE_Y_BIAS + CIRCLE_Y_AWAY) + 'px');
      out_circle.css("left", Math.floor(circle_width/(1+out_port_num) * (i + 1) + CIRCLE_X_BIAS) + 'px');
      $node.append(out_circle);
    }

    this.nodes.push(node_id);
  }

  addEdge(node_from, port_from, node_to, port_to) {
    // TODO: check parseInt & x/y bias
    let node_out = node_from + '-out-' + port_from;
    let node_in = node_to + '-in-' + port_to;

    let from = $("#" + node_out);
    let to = $("#" + node_in);
    let x1 = parseInt(from.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(from.parent().css('left'));
    let y1 = parseInt(from.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(from.parent().css('top'));
    let x2 = parseInt(to.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(to.parent().css('left'));
    let y2 = parseInt(to.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(to.parent().css('top'));

    let $line = $('<line/>');
    $line.attr('class', 'line');
    let id = node_out + "-" + node_in;
    $line.attr("id", id);
    $line.attr("x1", x1);
    $line.attr("y1", y1);
    $line.attr("x2", x2);
    $line.attr("y2", y2);
    let svg = $(this.svg_selector);
    svg.append($line);
    svg.html(svg.html());

    this.lines.push(id);
  }

  delNode(node_id) {
    let node = $("#"+node_id);
    node.remove();
    
    // delete lines
    let last_lines = [];
    for (let i in this.lines) {
      let line_id = this.lines[i];
      if (line_id.indexOf(node_id+'-') != -1) {
        $("#"+line_id).remove();
      }
      else {
        last_lines.push(line_id);
      }
    }
    this.lines = last_lines;

    let last_nodes = [];
    for (let i in this.nodes) {
      let inode = this.nodes[i];
      if (inode != node_id)
        last_nodes.push(inode);
    }
    this.nodes = last_nodes;
  }

  delEdge(node_from, port_from, node_to, port_to) {
    let node_out = node_from + '-out-' + port_from;
    let node_in = node_to + '-in-' + port_to;
    let line_id = node_out + '-' + node_in;
    let last_lines = []
    for (let i in this.lines) {
      if (i == line_id) {
        $('#'+line_id).remove();
      }
      else {
        last_lines.push(i);
      }
    }
    this.lines = last_lines;
  }


  setPosition(node_id, posiX, posiY) {
    // TODO check paseInt
    let node = $("#" + node_id);
    node.css("top", posiY);
    node.css("left", posiX);

    this.lines.forEach((line_id) => {
      if (line_id.indexOf(node_id+'-') != -1) {
        let sp = line_id.split('-');
        if (sp[0] + '-' + sp[1] == node_id) {
          let line = $('#' + line_id);
          let circle = $('#' + sp[0] + '-' + sp[1] + '-' + sp[2] + '-' + sp[3]);
          line.attr('x1', parseInt(circle.css('left')) + LINE_CIRCLE_X_BIAS + posiX);
          line.attr('y1', parseInt(circle.css('top')) + LINE_CIRCLE_Y_BIAS + posiY);
        }
        else if (sp[4] + '-' + sp[5] == node_id) {
          let line = $('#' + line_id);
          let circle = $('#' + sp[4] + '-' + sp[5] + '-' + sp[6] + '-' + sp[7]);
          line.attr('x2', parseInt(circle.css('left')) + LINE_CIRCLE_X_BIAS + posiX);
          line.attr('y2', parseInt(circle.css('top')) + LINE_CIRCLE_Y_BIAS + posiY); 
        }
        else {
          alert('bug : Class Renderer : setPosition, node_id wrong');
        }
      }
    });
    let svg = $("#svg");
    svg.html(svg.html());
  }

  clear() {
    let node_list = [];
    for (let i in this.nodes)
      node_list.push(this.nodes[i]);
    for (let i in node_list) {
      let inode = node_list[i];
      this.delNode(inode);
    }
  }
}

// ======================================================= Graph class ===================================================
class Graph {
  constructor() {
    console.log('Graph init');
    this.node = new Map(); // {node_id: {'id':id, 'type':type, 'position':[1,1], 'param':{param_key:param_value} }}
    this.edge = new Map(); // {(node_id-in|out-1):Set() }
    this.type_count = new Map(); // {node_type:counter}
    for (let key of type_detail.keys()) {
      this.type_count.set(key, 0)
    }
    // TODO
    this.isrender = false;
    this.renderer = null;
  }

  addNode(node_type, posiX=0, posiY=0, load_id=null) {
    console.log('Graph call : addNode');
    // check node type
    if (!type_detail.has(node_type)) {
      alert(node_type + " not in component list");
      return -1;
    }

    // create node
    let itype = type_detail.get(node_type);
    let node_param = itype.params;
    let param = {};
    for (let key in node_param) {
      let x = node_param[key];
      param[x.name] = x.default;
    }
    let type_number = this.type_count.get(node_type);
    let node_id = node_type + '-' + type_number;
    if (load_id != null)
      node_id = load_id;
    let new_node = {
      "id" : node_id,
      "type" : node_type,
      "position" : [posiX, posiY],
      "param" : param,
    };
    if (load_id == null)
      this.type_count.set(node_type, type_number+1);
    this.node.set(new_node.id, new_node);

    // initialize edge
    let in_port = itype.in_port;
    for (let i = 0;i < in_port.length;++ i) {
      this.edge.set(node_id + '-in-' + i, new Set());
    }
    let out_port = itype.out_port;
    for (let i = 0;i < out_port.length;++ i) {
      this.edge.set(node_id + '-out-' + i, new Set());
    }

    if (this.isrender)
      this.renderer.addNode(node_id, posiX, posiY);
    return node_id;
  }

  testEdge(node_from, port_from, node_to=null, port_to=null) {
    console.log('Graph call : testEdge');
    // check node exists
    let node_out = '';
    let node_in = '';
    if (node_to == null && port_to == null) {
      node_out = node_from;
      node_in = port_from;
      node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
      port_from = node_out.split('-')[3];
      node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
      port_to = node_in.split('-')[3];
    }
    else {
      node_out = node_from + '-out-' + port_from;
      node_in = node_to + '-in-' + port_to;
    }
    if (!this.edge.has(node_out)) {
      return node_out + " not in node list, please check code";
    }
    if (!this.edge.has(node_in)) {
      return node_in + " not in node list, please check code";
    }

    // check there is no duplicate edge
    let node_out_set = this.edge.get(node_out);
    let node_in_set = this.edge.get(node_in);
    if (node_out_set.has(node_in)) {
      return node_in + " already in " + node_out;
    }
    if (node_in_set.has(node_out)) {
      return node_out + " already in " + node_in;
    }

    // check in port is unique
    if (node_in_set.size >= 1) {
      return node_in + " already has input";
    }

    // check port data type match
    let out_data_type = type_detail.get(this.node.get(node_from).type).out_port[parseInt(port_from)];
    let in_data_type = type_detail.get(this.node.get(node_to).type).in_port[parseInt(port_to)];
    if (out_data_type != in_data_type) {
      return 'type not match : ' + out_data_type + ' & ' + in_data_type;
    }
    return 0;
  }

  addEdge(node_from, port_from, node_to=null, port_to=null) {
    console.log('Graph call : addEdge');
    let node_out = '';
    let node_in = '';
    if (node_to == null && port_to == null) {
      node_out = node_from;
      node_in = port_from;
      node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
      port_from = node_out.split('-')[3];
      node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
      port_to = node_in.split('-')[3];
    }
    else {
      node_out = node_from + '-out-' + port_from;
      node_in = node_to + '-in-' + port_to;
    }
    let test_ret = this.testEdge(node_from, port_from, node_to, port_to);
    if (test_ret != 0) {
      alert(test_ret);
      return -1;
    }

    // add edge
    let node_out_set = this.edge.get(node_out);
    let node_in_set = this.edge.get(node_in);
    node_out_set.add(node_in);
    node_in_set.add(node_out);


    if (this.isrender)
      this.renderer.addEdge(node_from, port_from, node_to, port_to);
    return 0;
  }

  delNode(node_id) {
    console.log('Graph call : delNode');
    // check node id
    if (!this.node.has(node_id)) {
      alert(node_id + ' node exist, please check');
      return -1;
    }

    // delete edge
    let node_type = this.node.get(node_id).type;
    let node_detail = type_detail.get(node_type);
    // delete in edge
    for (let i = 0;i < node_detail.in_port.length; ++ i) {
      let this_in_port = node_id + '-in-' + i;
      let in_edge_set = this.edge.get(this_in_port);
      for (let x of in_edge_set) {
        this.edge.get(x).delete(this_in_port);
      }
      this.edge.delete(this_in_port);
    }
    // delete out edge
    for (let i = 0;i < node_detail.out_port.length; ++ i) {
      let this_out_port = node_id + '-out-' + i;
      let out_edge_set = this.edge.get(this_out_port);
      for (let x of out_edge_set) {
        this.edge.get(x).delete(this_out_port);
      }
      this.edge.delete(this_out_port);
    }

    // delete node
    this.node.delete(node_id);

    if (this.isrender)
      this.renderer.delNode(node_id);
    return 0;
  }

  delEdge(node_from, port_from=null, node_to=null, port_to=null) {
    console.log('Graph call : delEdge');
    let node_out = '';
    let node_in = '';
    if (node_to == null && port_to == null && port_from == null) {
      let sp = node_from.split('-');
      node_from = sp[0] + '-' + sp[1];
      port_from = sp[3];
      node_to = sp[4] + '-' + sp[5];
      port_to = sp[7];
      node_out = sp[0] + '-' + sp[1] + '-' + sp[2] + '-' + sp[3];
      node_in = sp[4] + '-' + sp[5] + '-' + sp[6] + '-' + sp[7];
    }
    else if (node_to == null && port_to == null) {
      node_out = node_from;
      node_in = port_from;
      node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
      port_from = node_out.split('-')[3];
      node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
      port_to = node_in.split('-')[3];
    }
    else {
      node_out = node_from + '-out-' + port_from;
      node_in = node_to + '-in-' + port_to;
    }
    // check node exists
    if (!this.edge.has(node_out)) {
      alert(node_out + " not in node list, please check code");
      return -1;
    }
    if (!this.edge.has(node_in)) {
      alert(node_in + " not in node list, please check code");
      return -1;
    }

    // check edge exist
    let node_out_set = this.edge.get(node_out);
    let node_in_set = this.edge.get(node_in);
    let find = -1;
    if (!node_in_set.has(node_out)) {
      alert('delete edge not match : ' + node_out + ' & ' + node_in);
      return -1;
    }
    if (!node_out_set.has(node_in)) {
      alert("!!ERROR!! there is a bug in Graph class, edge not match");
      return -1;
    }

    // delete edge
    node_in_set.delete(node_out);
    node_out_set.delete(node_in);

    if (this.isrender)
      this.renderer.delEdge(node_from, port_from, node_to, port_to);
    return 0;
  }

  setParam(node_id, param) {
    console.log('Graph call : setParam');
    // check node exist
    if (!this.node.has(node_id)) {
      alert(node_id + ' not exist, please check');
      return -1;
    }
    let node_param = this.node.get(node_id).param;
    for (let key in param) {
      node_param[key] = param[key];
    }

    return 0;
  }

  getParam(node_id) {
    console.log('Graph call : getParam');
    // check node exist
    if (!this.node.has(node_id)) {
      alert(node_id + ' not exist, please check');
      return {};
    }
    let node_param = this.node.get(node_id).param;
    return node_param;
  }

  setPosition(node_id, posiX, posiY) {
    console.log('Graph call : setPosition');
    // check node exist
    if (!this.node.has(node_id)) {
      alert(node_id + ' not exist, please check');
      return -1;
    }
    let node_position = this.node.get(node_id).position;
    node_position = [posiX, posiY];

    if (this.isrender)
      this.renderer.setPosition(node_id, posiX, posiY);
    return 0;
  }

  clear() {
    console.log('Graph call : clear');
    this.node.clear();
    this.edge.clear();
    for (let key in this.type_count.keys()) {
      this.type_count.set(key, 0);
    }

    if (this.isrender)
      this.renderer.clear();
    return 0;
  }

  toJson() {
    console.log('Graph call : toJson');
    // nodes
    let all_nodes = [];
    for (let [key, value] of this.node) {
      let detail = {
        'node_name' : key,
        'node_type' : value.type,
        'node_position' : value.position,
        'details' : value.param,
      };
      all_nodes.push(detail);
    }

    // lines
    let all_lines = [];
    for (let [key, value] of this.edge) {
      if (key.indexOf('-out-') != -1) {
        for (let item of value) {
          let detail = {
            'line_from' : key.split('-')[0] + '-' + key.split('-')[1],
            'line_from_port' : parseInt(key.split('-')[3]),
            'line_to' : item.split('-')[0] + '-' + item.split('-')[1],
            'line_to_port' : parseInt(item.split('-')[3]),
          };
          all_lines.push(detail);
        }
      }
    }
    let ret = {
      all_nodes,
      all_lines,
    }
    return ret;
  }

  loadJson(string_or_obj) {
    console.log('Graph call : loadJson');
    this.clear();
    let obj = string_or_obj;
    if (typeof(string_or_obj) == 'string')
      obj = JSON.parse(string_or_obj);

    // solve nodes
    let nodes = obj.all_nodes;
    for (let key in nodes) {
      let x = nodes[key];
      let name = x.node_name;
      let node_id = this.addNode(x.node_type, x.node_position[0], x.node_position[1], name);
      if (node_id == -1) {
        alert('bug in loadJson');
        return -1;
      }
      if (this.type_count.get(x.node_type) <= parseInt(node_id.split('-')[1])) {
        this.type_count.set(x.node_type, parseInt(node_id.split('-')[1]) + 1);
      }
      this.setParam(node_id, x.details);
    }

    // solve lines
    let lines = obj.all_lines;
    lines.forEach((x) => {
      this.addEdge(x.line_from, x.line_from_port, x.line_to, x.line_to_port);
    });
    return 0;
  }

  startRender(canvas_selector='.canvas') {
    console.log('Graph call : startRender');
    this.renderer = new Renderer(canvas_selector);
    this.isrender = true;
    // TODO
    return -1;
  }

  endRender() {
    console.log('Graph call : endRender');
    this.renderer.clear();
    this.renderer = null;
    this.isrender = false;
    return 0;
  }

}

// ====================================================== common functions =========================================
function getX(obj) {
  let parObj = obj;
  let left = obj.offsetLeft;
  while (parObj = parObj.offsetParent) {
    left += parObj.offsetLeft;
  }
  return left;
}

function getY(obj) {
  let parObj = obj;
  let top = obj.offsetTop;
  while (parObj = parObj.offsetParent) {
    top += parObj.offsetTop;
  }
  return top;
}

function save_detail() {
  if (curr_id == null)
    return;

  let node_params = {};
  $(".param-value").each(function() {
    let tnode = $(this);
    let key = tnode.attr("name");
    let type = tnode.attr("data-type");

    if (!(['text', 'file', 'model', 'password', 'int', 'float', 'list', 'richtext'].includes(type))) {
      alert("<function 'save_detail'>there is something wrong, unknown type found : " + type);
      return false;
    }
    node_params[key] = tnode.val();
  });
  G.setParam(curr_id, node_params);
}

function render_nodes(data) {
  $('.canvas>.node').css('background-color', '#ffffff');
  for (let i in data) {
    let node = data[i];
    let key = node.node_name;
    let status = node.node_status;
    let inode = $('#'+key);
    let color;
    if (status == '0') {
      // finish
      color = '#D5F5E3';
    }
    else if (status == '1') {
      // wait
      color = 'rgba(128,128,128,0)';
    }
    else if (status == '2') {
      // running
      color = '#FCF3CF';
    }
    else if (status == '-1') {
      // fail
      color = '#FADBD8';
    }
    else {
      alert('unknown node status' + status);
    }
    inode.css('background-color', color);
  }
}

function check_progress() {
  if (finished) {
    return;
  }

  // NOTE : temp
  let req = {
    'project_id':'temp'
  };

  $.post(
    routes['graph_progress'],
    JSON.stringify(req),
    (ret) => {
      ret = JSON.parse(ret);
      console.log(ret);
      if (ret.status == 0) {
        finished = true;
        $('#button_stop').css('display', 'none');
        $('#button_run').css('display', 'inline');
        if (curr_id != null)
          $('#button_single_run').css('display', 'inline');
      }
      else {
        finished = false;
        setTimeout('check_progress()', 1000);
      }
      render_nodes(ret.progress);
    }
  );
}

// ============================ button ==================================
function save_button() {
  save_detail();
  let req = G.toJson();
  // NOTE : temp
  req['project_id'] = 'temp';
  $.post(
    routes['graph_save'],
    JSON.stringify(req),
    (ret) => {
      ret = JSON.parse(ret);
      if (ret.succeed == 0) {
        alert('save succeed');
      }
      else {
        alert('save fail : ' + ret.message);
      }
    }
  );
}

function load_button() {
  G.clear();
  // NOTE : temp
  let req = {
    'project_id' : 'temp',
  };
  $.post(
    routes['graph_load'],
    JSON.stringify(req),
    (ret) => {
      ret = JSON.parse(ret);
      if (ret.succeed == 0) {
        let succeed = G.loadJson(ret);
        if (succeed == 1) {
          alert('load failed at creating graph');
          console.log('load failed:');
          console.log(ret);
        }
        curr_id = null;
        delete_button(); // clean param and data table
      }
      else {
        alert('load failed at getting graph');
      }
    }
  );
}

function clean_button() {
  // NOTE : temp
  let req = {
    'project_id' : 'temp',
  };
  $.post(
    routes['graph_clean'],
    JSON.stringify(req),
    (ret) => {
      ret = JSON.parse(ret);
      if (ret.succeed == 0) {
        render_nodes({}); // clean nodes' state color
      }
      else {
        alert('clean cache failed : ' +  ret.message);
      }
    }
  );
}

function stop_button() {
  if (finished) {
    alert('already stoped');
    return;
  }
  // NOTE : temp
  let req = {
    'project_id':'temp',
  };
  $.post(
    routes['graph_stop'],
    JSON.stringify(req),
    (ret) => {
      ret = JSON.parse(ret);
      console.log('stop : get response');
      console.log(ret);
      if ((ret.succeed == 0) || (ret.message.indexOf('not running') != -1)) {
        finished = true;
        $('#button_stop').css('display', 'none');
        $('#button_run').css('display', 'inline');
        if (curr_id != null)
          $('#button_single_run').css('display', 'inline');
      }
      else {
        alert('stop failed : ' + ret.message);
      }
    }
  );
}

function run_button() {
  if (!finished) {
    alert('still running, please stop the mission first');
    return;
  }
  save_detail();
  let req = G.toJson();
  // NOTE : temp
  render_nodes({});
  req['project_id'] = 'temp';
  $.post(
    routes['graph_run'],
    JSON.stringify(req),
    (ret)=> {
      ret = JSON.parse(ret);
      console.log('run : get response');
      console.log(ret);
      if (ret.succeed == 0) {
        finished = false;
        setTimeout("check_progress()", 1000);
        $('#button_stop').css('display', 'inline');
        $('#button_run').css('display', 'none');
        $('#button_single_run').css('display', 'none');
      }
    }
  );
}

function run_single_button() {
  if (!finished) {
    alert('still running, please stop the mission first');
    return;
  }
  save_detail();
  let req = G.toJson();
  // NOTE : temp
  req['project_id'] = 'temp';
  req['run'] = [curr_id];
  render_nodes({});
  $.post(
    routes['graph_run'],
    JSON.stringify(req),
    (ret)=> {
      ret = JSON.parse(ret);
      console.log('run : get response');
      console.log(ret);
      if (ret.succeed == 0) {
        finished = false;
        setTimeout("check_progress()", 1000);
        $('#button_stop').css('display', 'inline');
        $('#button_run').css('display', 'none');
        $('#button_single_run').css('display', 'none');
      }
    }
  );
}

function delete_button(){
  if (curr_id != null)
    G.delNode(curr_id);
  curr_id = null;
  let button_single = $('#button_single_run');
  let dele = $('#button_delete');
  button_single.css('display', 'none');
  dele.css('display', 'none');

  let detail = $('#detail-box');
  let data = $('#table-box');
  data.children().remove();
  detail.children().remove();
}

// ================================================= component event ================================================
function comp_dragstart(e) {
  let class_type = drag_data.get('class_type');
  console.log('comp drag start :', class_type);

  e.dataTransfer.effectAllowed = "copy";
  drag_data.set("class_type", "component");
  drag_data.set("type", e.target.id);
  drag_data.set("text", e.target.innerHTML);
  let comp_scroll_y = $('#navi>ul')[0].scrollTop;
  let bias_x = e.clientX - getX($('#'+e.target.id)[0]);
  let bias_y = e.clientY - getY($('#'+e.target.id)[0]) + comp_scroll_y;
  drag_data.set("bias_x", bias_x);
  drag_data.set("bias_y", bias_y);
  e.dataTransfer.setDragImage(e.target, bias_x, bias_y);
  return true;
}
function comp_dragend(e) {
  drag_data.delete("class_type");
  drag_data.delete("type");
  drag_data.delete("text");
  drag_data.delete("bias_x");
  drag_data.delete("bias_y");
  return false;
}

function comp_dragover(e) {
  e.preventDefault();
  return false;
}

function comp_drop(e) {
  e.preventDefault();
  return false;
}

// ================================================= node event ================================================
function node_dragstart(e) {
  let class_type = drag_data.get("class_type");
  console.log('node drag start :', class_type);
  if (drag_data.get('class_type') == 'circle') {
    return true;
  }
  e.dataTransfer.effectAllowed = "move";
  drag_data.set("class_type", "node");
  drag_data.set("node_id", e.target.id);
  drag_data.set("text", null);
  let bias_x = e.clientX - getX($('#'+e.target.id)[0]);
  let bias_y = e.clientY - getY($('#'+e.target.id)[0]);
  drag_data.set("bias_x", bias_x);
  drag_data.set("bias_y", bias_y);
  e.dataTransfer.setDragImage(e.target, bias_x, bias_y);
  return true;
}

function node_dragover(e) {
  e.preventDefault();
}

function node_dragend(e) {
  drag_data.delete("class_type");
  drag_data.delete("node_id");
  drag_data.delete("text");
  drag_data.delete("bias_x");
  drag_data.delete("bias_y");
  return false;
}

function node_dragenter(e) {
  e.preventDefault();
  let class_type = drag_data.get('class_type');
  console.log('node drag enter:', class_type);
  if (class_type == 'circle') {
    if (drag_data.has('enter')) {
      let id = drag_data.get('enter');
      let temp = $('#' + id);
      temp.css('border-width', '2px');
      drag_data.delete('enter');
    }
    let id = e.target.id;
    let temp = $('#'+id);
    temp.css('border-width', '3px');
    drag_data.set('enter', id);
  }
}

function node_dragleave(e) {
  e.preventDefault();
  let class_type = drag_data.get('class_type');
  console.log('node drag leave:', class_type);
  if (class_type == 'circle') {
    if (drag_data.has('enter')) {
      let id = drag_data.get('enter');
      if (e.target.id == id) {
        let temp = $('#' + id);
        temp.css('border-width', '2px');
        drag_data.delete('enter');
      }
    }
  }
}

function node_drop(e) {
  e.preventDefault();
  let class_type = drag_data.get("class_type");
  console.log('node drop :', class_type);
  if (class_type == 'circle') {
    let id = e.target.id;
    let from_id = drag_data.get('from_id');
    if (id.split('-').length == 2) {
      let itype = type_detail.get(id.split('-')[0]);
      if (from_id.split('-')[2] == 'in') {
        for (let i = 0;i < itype.out_port.length; ++ i) {
          if (G.testEdge(id + '-out-' + i, from_id) == 0) {
            G.addEdge(id + '-out-' + i, from_id);
            return true;
          }
        }
      } else {
        for (let i = 0;i < itype.in_port.length; ++ i) {
          if (G.testEdge(from_id, id + '-in-' + i) == 0) {
            G.addEdge(from_id, id + '-in-' + i);
            return true;
          }
        }
      }
    }
    return false;
  }
  else if (class_type == 'node') {
    let bias_x = parseInt(drag_data.get("bias_x"));
    let bias_y = parseInt(drag_data.get("bias_y"));
    let x = e.clientX - getX($(".canvas")[0]) + document.body.scrollLeft - bias_x;
    let y = e.clientY - getY($(".canvas")[0]) + document.body.scrollTop - bias_y;
    G.setPosition(drag_data.get('node_id'), x, y);
  }
}

function node_click(e) {
  //   0. show button
  // v 1. save detail 
  // v 2. change id
  // v 3. del old param
  // 4. render new param
  let id = e.target.id;
  // check is not circle
  if (id.split('-').length > 2)
    return;

  if (curr_id == null) {
    $('#button_single_run').css('display', 'inline');
    $('#button_delete').css('display', 'inline');
  }

  let node = $("#"+id);
  if (curr_id != null) {
    let old_node = $('#'+curr_id);
    old_node.css('border-color', 'black');
    save_detail();
  }

  curr_id = id;
  node.css('border-color', 'rgb(220,20,60)');

  let detailBox = $('#detail-box');
  let tableBox = $('#table-box');
  detailBox.empty();
  tableBox.empty();

  let params = G.getParam(id);
  let itype = type_detail.get(id.split('-')[0]);
  let iparams = itype.params;

  for (let i = 0;i < iparams.length; ++ i) {
    let param_detail = iparams[i];
    let key = param_detail.name;
    let value = params[key];
    let param_type = param_detail.type;
    let note = param_detail.note;

    let $border = $('<div class="param-border"></div>');
    let $name = $('<div class="param-key"></div>');

    $name.text(param_detail.display);

    let choice = {
      'text' : () => {
        let $param = $('<input></input>');
        $param.attr("type", "text");
        return $param;
      },
      'file' : () => {
        let $param = $('<input></input>');
        $param.attr("type", "text");
        return $param;
      },
      'model' : () => {
        let $param = $('<input></input>');
        $param.attr("type", "text");
        return $param;
      },
      'password' : () => {
        let $param = $('<input></input>');
        $param.attr("type", "password");
        return $param;
      },
      'list' : () => {
        let $param = $('<select></select>');
        for (let j=0;j < param_detail.list.length; ++j) {
          let $tmp = $('<option></option>');
          $tmp.attr("value", param_detail.list[j]);
          $tmp.text(param_detail.list[j]);
          $param.append($tmp);
        }
        return $param;
      },
      'int' : () => {
        let $param = $('<input></input>');
        $param.attr("type", "number");
        return $param;
      },
      'float': () => {
        let $param = $('<input></input>');
        $param.attr("type", "number");
        return $param;
      },
      'richtext' : () => {
        let $param = $('<textarea rows="10" cols="30"></textarea>');
        $param.attr("type", "richtext");
        return $param;
      },
    };

    if (!(param_type in choice)) {
      alert("there is something wrong, unknown type found : " + param_type);
      return false;
    }
    let $param = choice[param_type]();

    $param.attr("class", "param-value");
    $param.attr("name", key);
    $param.val(value);
    $param.attr("data-type", param_type);
    $name.css("order", "1");
    $name.attr("title", note);
    $param.css("order", "2");
    $border.css("order", i);
    $border.prepend($name);
    $border.prepend($param);

    detailBox.prepend($border);
  }
  var req = {
    "number":10,
    "node_id":id
  };

  // NOTE : temp
  req['project_id'] = 'temp';

  $.post(
    routes['graph_sample'],
    JSON.stringify(req),
    function(ret) {
      ret = JSON.parse(ret);
      console.log('get', ret);
      if (ret.succeed == 0) {
        if (ret.data.length == 0)
          return;
        let show = ret.data[0];
        if (show.type == 'DataFrame') {
          if (show.row_num > 0) {
            let table = $('<table class="table" border="1"></table>');
            let row = show.row_num;
            let col = show.col_num;
            let tr = $('<tr></tr>');
            for (let i = 0;i < show.col_index.length;++ i) {
              let value = show.col_index[i] + '(' + show.col_type[i] + ')';
              let th = $('<th>'+value+'</th>');
              tr.append(th);
            }
            table.append(tr);
            show.data.forEach(function (rowValue) {
              let tr = $('<tr></tr>');
              rowValue.forEach(function (value) {
                let td = $('<td>'+value+'</td>');
                tr.append(td);
              });
              table.append(tr);
            });
            let $shape = $('<a></a>');
            $shape.text('Shape:(' + show.shape + ')');
            tableBox.append($shape);
            tableBox.append(table);
          }
        }
        else if (show.type == 'Image') {
          let $shape = $('<a></a>');
          let $img = $('<img></img>');
          let shape = show.data.shape;
          if (shape.length == 2) {
            shape.push(1);
          }
          $shape.text('Shape:' + shape[0] + 'X' + shape[1] + 'X' + shape[2]);
          $img.attr('src', show.data.url);
          tableBox.append($shape);
          tableBox.append($img);
        }
        else {
          alert('type ' + show.type + ' not implemented');
        }
      }
    }
  );
}

function file_name(){
  let file = document.getElementById('pathbt');
  $("#path").val(file.name);
}

// ================================================= circle event ================================================
function circle_dragstart(e) {
  let class_type = drag_data.get("class_type");
  console.log('circle drag start :', class_type);
  if (class_type == null) {
    e.dataTransfer.effectAllowed = "all";
    drag_data.set("from_id", e.target.id);
    drag_data.set("class_type", "circle");

    let circle = $("#" + e.target.id);
    let x1 = parseInt(circle.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(circle.parent().css('left'));
    let y1 = parseInt(circle.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(circle.parent().css('top'));

    let $line = $('<line id="line"/>');
    $line.css("stroke", "rgb(99,99,99)");
    $line.css("stroke-width", "2");
    $line.attr("x1", x1);
    $line.attr("y1", y1);
    $line.attr("x2", x1);
    $line.attr("y2", y1);
    $("#svg").append($line);
  }
}

function circle_drag(e) {
  // TODO: drag on node, auto link
  let x = e.clientX - getX($(".canvas")[0]) + document.body.scrollLeft;
  let y = e.clientY - getY($(".canvas")[0]) + document.body.scrollTop;
  $("#line").attr("x2", x);
  $("#line").attr("y2", y);
  let svg = $("#svg");
  svg.html(svg.html());
}

function circle_dragend(e) {
  drag_data.delete("from_id");
  drag_data.delete("class_type");
  if (drag_data.has('enter')) {
    let id = drag_data.get('enter');
    let temp = $('#'+id);
    temp.css('border-width', '2px');
    drag_data.delete('enter');
  }
  $("#line").remove();
}

function circle_dragenter(e) {
  // TODO: check fit
}

function circle_dragover(e) {
  e.preventDefault();
}

function circle_drop(e) {
  e.preventDefault();
  let class_type = drag_data.get('class_type');
  console.log('circle drop :', class_type);
  if (class_type != 'circle')
    return false;
  let from_id = drag_data.get("from_id");
  let to_id = e.target.id;
  if ((from_id.split('-')[2] == 'in') ^ (to_id.split('-')[2] == 'in')) {
    if (from_id.split('-')[2] == 'out') {
      let ret = G.addEdge(from_id, to_id);
      console.log('create edge', ret);
    }
    else {
      G.addEdge(to_id, from_id);
    }
  }
  return true;
}

// ================================================= canvas event ================================================
function canvas_dragover(e) {
  e.preventDefault();
}

function canvas_dragenter(e) {}

function canvas_drop(e) {
  e.preventDefault();
  let class_type = drag_data.get('class_type');
  console.log('canvas drop :', class_type);
  if (!(['node', 'component'].includes(class_type))) {
    return false;
  }
  let bias_x = parseInt(drag_data.get("bias_x"));
  let bias_y = parseInt(drag_data.get("bias_y"));
  let x = e.clientX - getX($(".canvas")[0]) + document.body.scrollLeft - bias_x;
  let y = e.clientY - getY($(".canvas")[0]) + document.body.scrollTop - bias_y;
  if (class_type == "component") {
    let type = drag_data.get('type');
    let ret = G.addNode(type, x, y);
    console.log('add node', ret);
  } else if (class_type == "node") {
    G.setPosition(drag_data.get('node_id'), x, y);
  }
  return false;
}

// ================================================= bind canvas drag drop event ======================================
function bind_canvas(selector_or_obj) {
  let obj = selector_or_obj;
  if (typeof(selector_or_obj) == 'string')
    obj = $(selector_or_obj);
  obj.attr("ondragover", "canvas_dragover(event)");
  obj.attr("ondragenter", "canvas_dragenter(event)");
  obj.attr('ondragover', 'canvas_dragover(event)');
  obj.attr("ondrop", "canvas_drop(event)");
}

function bind_component(selector_or_obj) {
  let obj = selector_or_obj;
  if (typeof(selector_or_obj) == 'string')
    obj = $(selector_or_obj);
  obj.attr("draggable", "true");
  obj.attr("ondragstart", "comp_dragstart(event)");
  obj.attr("ondragend", "comp_dragend(event)");
  obj.attr('ondragover', 'comp_dragover(event)');
  obj.attr('ondrop', 'comp_drop(event)');
}

function bind_circle(selector_or_obj) {
  let obj = selector_or_obj;
  if (typeof(selector_or_obj) == 'string')
    obj = $(selector_or_obj);
  obj.attr('draggable', 'true');
  obj.attr('ondragstart', 'circle_dragstart(event)');
  obj.attr('ondrag', 'circle_drag(event)');
  obj.attr('ondragend', 'circle_dragend(event)');
  obj.attr('ondragenter', 'circle_dragenter(event)');
  obj.attr('ondragover', 'circle_dragover(event)');
  obj.attr('ondrop', 'circle_drop(event)');
}

function bind_node(selector_or_obj) {
  let obj = selector_or_obj;
  if (typeof(selector_or_obj) == 'string')
    obj = $(selector_or_obj);
  obj.attr('draggable', 'true');
  obj.attr('ondragstart', 'node_dragstart(event)');
  obj.attr('ondragend', 'node_dragend(event)');
  obj.attr('ondragover', 'node_dragover(event)');
  obj.attr('ondragenter', 'node_dragenter(event)');
  obj.attr('ondragleave', 'node_dragleave(event)');
  obj.attr('ondrop', 'node_drop(event)');
}

// ================================================= component sizebar =========================================
function nodes_build(paren, lis) {
  let $new_lis = $('<ul></ul>');
  for (let key in lis) {
    if (typeof(lis[key]) == 'object') {
      let $new_sublis = $('<li><a><b>'+key+'</b></a></li>');
      nodes_build($new_sublis, lis[key]);
      $new_lis.append($new_sublis);
    }
    else {
      let $new_type = $(
        '<li><div class="component" id="' + key +'">' + 
        lis[key] + 
        '</div></li>');
      $new_lis.append($new_type);
    }
  }
  paren.append($new_lis);
}

function component_init() {
  $.post(
    routes['component_list'],
    (data) => {
      let div = $("#navi");
      let compo_list = JSON.parse(data)['structure'];
      console.log(compo_list);
      nodes_build(div, compo_list);
      // component attr
      bind_component('.component');
    }
  );
}

// =================================================== init all ====================================================
$.post(
  routes['component_param'],
  (data) => {
    data = JSON.parse(data).component;
    // TODO: check response format is right
    data.forEach(
      a => type_detail.set(a.name, a)
    );
    console.log(data);

    G = new Graph();
    G.startRender();

    component_init();
    bind_canvas('#svg');
    console.log('READY');
    // NOTE : temp
    load_button();
  }
);
