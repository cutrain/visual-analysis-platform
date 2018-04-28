// constant
in0out1 = ["data-instream", "sql-instream", "model-instream"];
in1out0 = ["data-outstream", "sql-outstream", "model-outstream"];
in1out1 = ["random", "sql-execute"];
in2out1 = ["naive-bayes", "decision-tree", "svm", "knn", "adaboost", "neural-network", "predict", "merge-row", "merge-col"];
in1out2 = ["split-row", "split-col"];

typeList = [];
typeList = typeList.concat(in0out1);
typeList = typeList.concat(in1out0);
typeList = typeList.concat(in1out1);
typeList = typeList.concat(in2out1);
typeList = typeList.concat(in1out2);

details = {
  "data-instream" : [
  {
    "name":"path",
    "display":"路径",
    "type":"file",
    "default":"",
  },
  ],

  "model-instream" : [
  {
    "name":"path",
    "display":"路径",
    "type":"file",
    "default":"",
  },
  ],

  "data-outstream" : [
  {
    "name":"path",
    "display":"路径",
    "type":"file",
    "default":"",
  },
  ],

  "model-outstream" : [
  {
    "name":"path",
    "display":"路径",
    "type":"file",
    "default":"",
  },
  ],

  "sql-instream" : [
  {
    "name":"database-type",
    "display":"数据库类型",
    "type":"list",
    "default":"MySQL",
    "list": ["MySQL"],
  },
  {
    "name":"address",
    "display":"地址",
    "type":"text",
    "default":"localhost",
  },
  {
    "name":"port",
    "display":"端口",
    "type":"text",
    "default":"3306",
  },
  {
    "name":"user",
    "display":"账号",
    "type":"text",
    "default":"root",
  },
  {
    "name":"password",
    "display":"密码",
    "type":"password",
    "default":"123",
  },
  {
    "name":"database-name",
    "display":"数据库名",
    "type":"text",
    "default":"",
  },
  {
    "name":"table-name",
    "display":"表名",
    "type":"text",
    "default":"",
  },
  ],

  "sql-outstream" : [
  {
    "name":"database-type",
    "display":"数据库类型",
    "type":"list",
    "default":"MySQL",
    "list": ["MySQL"],
  },
  {
    "name":"address",
    "display":"地址",
    "type":"text",
    "default":"localhost",
  },
  {
    "name":"port",
    "display":"端口",
    "type":"text",
    "default":"3306",
  },
  {
    "name":"user",
    "display":"账号",
    "type":"text",
    "default":"root",
  },
  {
    "name":"password",
    "display":"密码",
    "type":"password",
    "default":"root",
  },
  {
    "name":"database-name",
    "display":"数据库名",
    "type":"text",
    "default":"",
  },
  {
    "name":"table-name",
    "display":"表名",
    "type":"text",
    "default":"",
  },
  ],

  "random" : [
  ],

  "merge-row" : [
  ],

  "merge-col" : [
  ],

  "split-row" : [
  {
    "name":"ratio",
    "display":"拆分比例(0-100%)",
    "type":"number",
    "default":"75"
  }
  ],

  "split-col" : [
  {
    "name":"cols",
    "display":"列名(逗号分隔)",
    "type":"text",
    "default":""
  }
  ],

  "naive-bayes" : [
  ],

  "decision-tree" : [
  {
    "name":"method",
    "display":"方法",
    "type":"list",
    "default":"classify",
    "list":["classify", "regress"]
  }
  ],

  "svm" : [
  {
    "name":"method",
    "display":"方法",
    "type":"list",
    "default":"classify",
    "list":["classify", "regress"]
  }
  ],

  "knn" : [
  {
    "name":"method",
    "display":"方法",
    "type":"list",
    "default":"classify",
    "list":["classify", "regress"]
  }
  ],

  "adaboost" : [
  {
    "name":"method",
    "display":"方法",
    "type":"list",
    "default":"classify",
    "list":["classify", "regress"]
  }
  ],

  "neural-network" : [
  {
    "name":"method",
    "display":"方法",
    "type":"list",
    "default":"classify",
    "list":["classify", "regress"]
  },
  {
    "name":"activation",
    "display":"激发函数",
    "type":"list",
    "default":"relu",
    "list":["relu", "identity", "logistic", "tanh"]
  },
  {
    "name":"solver",
    "display":"优化器",
    "type":"list",
    "default":"adam",
    "list":["adam", "lbfgs", "sgd"]
  },
  {
    "name":"alpha",
    "display":"alpha",
    "type":"number",
    "default":"0.0001",
  },
  ],

  "sql-execute": [
  {
    "name":"sql_command",
    "display":"SQL语句,用{this}指代该表",
    "type":"richtext",
    "default":"SELECT * \nFROM {this}"
  }
  ],

  "predict" : [
  ],
};

// initialize
// count all type [type, num(int)]
var typeCount = {};
for (var i in typeList) {
  typeCount[typeList[i]] = 0;
}
// *count all nodes with types [node_id, type]
var all_nodes = {};

// *count all lines [line_id, [out_circle_id, in_circle_id]]
var all_lines = {};
// node have lines [node_id, [line_id, dir]]
var in_lines = {};
// all line from the node [node_id, map:[line_id, out_circle_id]]
var line_from = {};
// all line to the node [node_id, map:[line_id, in_circle_id]]
var line_to = {};

var now_node_id= null;
// *all nodes details [node_id, map:[detail_key, detail_value]]
var nodes_details = {};

// common functions
function getX(obj) {
  var parObj = obj;
  var left = obj.offsetLeft;
  while (parObj = parObj.offsetParent) {
    left += parObj.offsetLeft;
  }
  return left;
}

function getY(obj) {
  var parObj = obj;
  var top = obj.offsetTop;
  while (parObj = parObj.offsetParent) {
    top += parObj.offsetTop;
  }
  return top;
}

function in_array(ele, arr) {
  for (var i=0;i < arr.length;++i) {
    if (ele==arr[i])
      return true;
  }
  return false;
}

function save_detail() {
  if (now_node_id == null)
    return;
  var node_details;
  if (now_node_id in nodes_details)
    node_details = nodes_details[now_node_id];
  else {
    alert("<function 'save_detail'>there is something wrong, node not found: " + now_node_id);
    return;
  }

  $(".param-value").each(function() {
    var tnode = $(this);
    var key = tnode.attr("name");
    var value;
    var type = tnode.attr("data-type");

    if (type == "text") {
      value = tnode.val();
    }else if (type == "file") {
      value = tnode.val();
    }else if (type == "password") {
      value = tnode.val();
    }else if (type == "select") {
      value = tnode.val();
    }else if (type == "number") {
      value = tnode.val();
    }else if (type == "list") {
      value = tnode.val();
    }else if (type == "richtext") {
      value = tnode.val();
    }else {
      alert("<function 'save_detail'>there is something wrong, unknown type found : " + type);
    }
    node_details[key] = value;
  });

}

function render_nodes(data) {
  for (var key in all_nodes) {
    $("#"+key).css("background", "#ffffff");
  }
  for (var key in data) {
    var node = $("#"+key);
    var color;
    if (data[key] == '0')
      color = 'rgba(0,128,0,0.6)';
    else if (data[key] == '-1')
      color = 'rgba(255,0,0,0.6)';
    else if (data[key] == '1')
      color = 'rgba(255,255,0,0.6)';
    else
      color = 'rgba(128,128,128,0.6)';
    node.css("background", color);
  }
}

function check_progress() {
  if (window.progress == 0)
    return;
  setTimeout("check_progress()", 1000);
  $.post(
    '/main/progress',
    function(data) {
      data = JSON.parse(data);
      console.log(data);
      if (data["status"] == "0")
        window.progress = 0;
      render_nodes(data["progress"]);
    }
    );
}

function run_button() {
  if (window.progress == 1)
    return;
  save_detail();
  var data = {
    "all_nodes":all_nodes,
    "all_lines":all_lines,
    "nodes_details":nodes_details
  };
  $.post(
    '/main/run',
    JSON.stringify(data),
    function() {
      window.progress = 1;
      setTimeout("check_progress()", 200);
    }
  );
}

function run_single(node_name) {
  if (window.progress == 1)
    return;
  save_detail();
  var data = {
    "all_nodes":all_nodes,
    "all_lines":all_lines,
    "nodes_details":nodes_details,
    "run":[node_name]
  };
  $.post(
    '/main/run',
    JSON.stringify(data),
    function() {
      window.progress = 1;
      setTimeout("check_progress()", 200);
    }
  );
}

function circle2node(circle_name) {
  while (circle_name[circle_name.length-1] >= '0' && circle_name[circle_name.length-1] <= '9')
    circle_name = circle_name.substring(0, circle_name.length - 1);
  if (circle_name.substring(circle_name.length-2, circle_name.length) == 'in')
    circle_name = circle_name.substring(0, circle_name.length-2);
  else
    circle_name = circle_name.substring(0, circle_name.length-3);
  return circle_name;
}

function delete_node(node_name) {
  var node = $("#"+node_name);
  if (!(node_name in all_nodes))
    return;
  for (var line_name in in_lines[node_name]) {
    var line = all_lines[line_name];
    var dir = in_lines[node_name][line_name];
    var o_node_name = circle2node(line[1-dir]);
    if (dir == 0)
      delete line_to[o_node_name][line_name];
    else
      delete line_from[o_node_name][line_name];
    delete all_lines[line_name];
    delete in_lines[o_node_name][line_name];
    $("#"+line_name).remove();
  }
  delete all_nodes[node_name];
  delete nodes_details[node_name];
  delete in_lines[node_name];
  delete line_from[node_name];
  delete line_to[node_name];
  var circles = $(".circle[id^='"+node_name+"']");
  circles.remove();
  node.remove();
  if (now_node_id == node_name)
    now_node_id = null;
}

// component event
function comp_dragstart(e) {
  e.dataTransfer.effectAllowed = "copy";
  e.dataTransfer.setData("type", e.target.id);
  e.dataTransfer.setData("text", e.target.innerHTML);
  e.dataTransfer.setDragImage(e.target, 0, 0);
  return true;
}
function comp_dragend(e) {
  e.dataTransfer.clearData("type");
  e.dataTransfer.clearData("text");
  return false;
}

// node event
function node_dragstart(e) {
  e.dataTransfer.effectAllowed = "move";
  e.dataTransfer.setData("type", "move");
  e.dataTransfer.setData("text", e.target.id);
  e.dataTransfer.setDragImage(e.target, 0, 0);
  return true;
}

function node_click(e) {
  var id = e.target.id;
  var node = $("#"+id);
  var type = node.attr("data-type");
  var list = details[type];
  console.log(list);
  if (list == null) {
    alert(type);
  }

  var detailBox = $("#detail-box");
  if(detailBox.css('display')=='none'){
    detailBox.css("display","flex");
    detailBox.css("flex-direction","column");
    detailBox.css("align-items","flex-start");
  }
  $("#button_run").css("display",'table-cell');
  save_detail();
  now_node_id = id;
  detailBox.empty();
  var saved = nodes_details[id];


  for (var i=0;i < list.length; ++i) {
    var $border = $('<div class="param-border"></div>');
    var $name = $('<div class="param-key"></div>');
    var $param;

    var ele = list[i];
    $name.text(ele['display']);

    if (ele["type"] == "text") {
      $param = $('<input></input>');
      $param.attr("type", "text");
    }else if (ele["type"] == "file") {
      $param = $('<input></input>');
      $param.attr("type", "text");
      $param.attr("id", "path");
    }else if (ele["type"] == "password") {
      $param = $('<input></input>');
      $param.attr("type", "password");
    }else if (ele["type"] == "list") {
      $param = $('<select></select>');
      for (var j=0;j < ele["list"].length; ++j) {
        var $tmp = $('<option></option>');
        $tmp.attr("value", ele["list"][j]);
        $tmp.text(ele["list"][j]);
        $param.append($tmp);
      }
    }else if (ele["type"] == "number") {
      $param = $('<input></input>');
      $param.attr("type", "number");
    }else if (ele["type"] == "richtext") {
      $param = $('<textarea rows="10" cols="30"></textarea>');
      $param.attr("type", "richtext");
    }else {
      alert("there is something wrong, unknown type found : " + ele["type"]);
    }

    $param.attr("class", "param-value");
    $param.attr("name", ele["name"]);
    $param.val(saved[ele["name"]]);
    $param.attr("data-type", ele["type"]);
    $name.css("order", "1");
    $param.css("order", "2");
    $border.css("order", i);
    $border.prepend($name);
    $border.prepend($param);

    if (ele["type"] == "file") {
      var $bt = $('<input></input>');
      $bt.attr("type", "file");
      $bt.attr("id", "pathbt");
      $bt.attr("onchange", '$("#path").val($("#pathbt").val())');
      $bt.css("order", "3");
      $border.prepend($bt);
    }

    detailBox.prepend($border);
  }  
  var $detail_top = $("<div class='detail-top'style='order:0;'>属性</div>")
  detailBox.prepend($detail_top);
}



// circle event
function circle_dragstart(e) {
  e.dataTransfer.effectAllowed = "all";
  e.dataTransfer.setData("from", e.target.id);
  var circle = $("#" + e.target.id);
  var x1 = parseInt(circle.css("left")) + 5;
  var y1 = parseInt(circle.css("top")) + 5;

  var $line = $('<line id="line"/>');
  $line.css("stroke", "rgb(99,99,99)");
  $line.css("stroke-width", "2");
  $line.attr("x1", x1);
  $line.attr("y1", y1);
  $line.attr("x2", x1);
  $line.attr("y2", y1);
  $("#svg").append($line);
}

function circle_drag(e) {
  var x = e.clientX - getX($(".canvas")[0]) + document.body.scrollLeft;
  var y = e.clientY - getY($(".canvas")[0]) + document.body.scrollTop;
  $("#line").attr("x2", x);
  $("#line").attr("y2", y);
  var svg = $("#svg");
  svg.html(svg.html());
}

function circle_dragend(e) {
  e.dataTransfer.clearData("from");
  $("#line").remove();
}

function circle_dragenter(e) {
}

function circle_dragover(e) {
  e.preventDefault();
}

function circle_drop(e) {
  var from_id = e.dataTransfer.getData("from");
  if (from_id == null)
    return false;
  var to_id = e.target.id;
  var id = from_id + to_id;
  var from_type = from_id;
  var to_type = to_id;
  while (from_type[from_type.length-1] >= '0' && from_type[from_type.length-1] <= '9')
    from_type = from_type.substring(0, from_type.length - 1);
  while (to_type[to_type.length-1] >= '0' && to_type[to_type.length-1] <= '9')
    to_type = to_type.substring(0, to_type.length - 1);
  if (from_type.substring(from_type.length-2, from_type.length) == "in") {
    var temp = from_id;
    from_id = to_id;
    to_id = temp
    temp = from_type;
    from_type = to_type;
    to_type = temp;
  }
  var from_node_id = from_type.substring(0, from_type.length - 3);
  var to_node_id = to_type.substring(0, to_type.length - 2);

  var from = $("#" + from_id);
  var to = $("#" + to_id);
  var x1 = parseInt(from.css("left")) + 5;
  var y1 = parseInt(from.css("top")) + 5;
  var x2 = parseInt(to.css("left")) + 5;
  var y2 = parseInt(to.css("top")) + 5;

  var from_list = line_from[from_node_id];
  var to_list = line_to[to_node_id];;
  from_list[id] = from_id;
  to_list[id] = to_id;
  all_lines[id] = [from_id, to_id];
  in_lines[from_node_id][id] = 0;
  in_lines[to_node_id][id] = 1;


  var $line = $('<line class="line"/>');
  $line.attr("id", id);
  $line.attr("x1", x1);
  $line.attr("y1", y1);
  $line.attr("x2", x2);
  $line.attr("y2", y2);
  var svg = $("#svg");
  svg.append($line);
  svg.html(svg.html());
}

// component attr
var ele_components = $(".component");
ele_components.attr("draggable", "true");
ele_components.attr("ondragstart", "comp_dragstart(event)");
ele_components.attr("ondragend", "comp_dragend(event)");

// canvas event
function canvas_dragover(e) {
  e.preventDefault();
}

function canvas_dragenter(e) {
}

function canvas_drop(e) {
  var type = e.dataTransfer.getData("type");
  if (!(type in typeCount) && type != "move") {
    return false;
  }
  var x = e.clientX - getX($(".canvas")[0]) + document.body.scrollLeft;
  var y = e.clientY - getY($(".canvas")[0]) + document.body.scrollTop;
  if (type != "move") {
    var num = typeCount[type] + 1;
    var id = type + num;
    typeCount[type] = num;
    var $node = $('<div></div>');
    $node.attr("class", "node noselect");
    $node.attr("id", id);
    $node.attr("ondragstart", "node_dragstart(event)");
    $node.attr("ondragend", "comp_dragend(event)"); // use component's dragend
    $node.attr("draggable", "true");
    $node.attr("data-type",type);
    $node.css({"top":y, "left":x});
    $node.text(e.dataTransfer.getData("text"));
    $node.click(node_click);

    $(".canvas").append($node);
    line_from[id] = {};
    line_to[id] = {};
    in_lines[id] = {};
    all_nodes[id] = type;
    var list = details[type];
    if (!(id in nodes_details)) {
      var tmp = {};
      nodes_details[id] = tmp;
      for (var i=0;i < list.length; ++i)
        tmp[list[i]["name"]] = list[i]["default"];
    }

    var node = $('#'+id).append(out1);
    var $circle = $('<div class="circle noselect" ' +
      'draggable="true"' +
      'ondragstart="circle_dragstart(event)" ' +
      'ondrag="circle_drag(event)" ' +
      'ondragend="circle_dragend(event)" ' +
      'ondragenter="circle_dragenter(event)" ' +
      'ondragover="circle_dragover(event)" ' +
      'ondrop="circle_drop(event)" ' +
      '></div>');

    if (in_array(type,in0out1)) {
      var out1 = $circle.clone();
      out1.attr("id", id + "out1");
      out1.css("top", y + node[0].clientHeight);
      out1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(out1);

    }else if (in_array(type,in1out0)) {
      var in1 = $circle.clone();
      in1.attr("id", id + "in1");
      in1.css("top", y - 5);
      in1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(in1);

    }else if (in_array(type,in1out1)) {
      var in1 = $circle.clone();
      in1.attr("id", id + "in1");
      in1.css("top", y - 5);
      in1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(in1);

      var out1 = $circle.clone();
      out1.attr("id", id + "out1");
      out1.css("top", y + node[0].clientHeight);
      out1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(out1);

    }else if (in_array(type,in1out2)) {
      var in1 = $circle.clone();
      in1.attr("id", id + "in1");
      in1.css("top", y - 5);
      in1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(in1);

      var out1 = $circle.clone();
      out1.attr("id", id + "out1");
      out1.css("top", y + node[0].clientHeight);
      out1.css("left", x + node[0].clientWidth/3 - 2.5);
      node.after(out1);

      var out2 = $circle.clone();
      out2.attr("id", id + "out2");
      out2.css("top", y + node[0].clientHeight);
      out2.css("left", x + node[0].clientWidth*2/3 - 2.5);
      node.after(out2);

    }else if (in_array(type,in2out1)) {
      var in1 = $circle.clone();
      in1.attr("id", id + "in1");
      in1.css("top", y - 5);
      in1.css("left", x + node[0].clientWidth/3 - 2.5);
      node.after(in1);

      var in2 = $circle.clone();
      in2.attr("id", id + "in2");
      in2.css("top", y - 5);
      in2.css("left", x + node[0].clientWidth*2/3 - 2.5);
      node.after(in2);

      var out1 = $circle.clone();
      out1.attr("id", id + "out1");
      out1.css("top", y + node[0].clientHeight);
      out1.css("left", x + node[0].clientWidth/2 - 2.5);
      node.after(out1);
    }

  }else {
    // node move
    var id = e.dataTransfer.getData("text");
    var node = $("#"+e.dataTransfer.getData("text"));
    var circles = $(".circle[id^='"+id+"']");
    var offy = y - parseInt(node.css('top'));
    var offx = x - parseInt(node.css('left'));
    node.css("top", y);
    node.css("left", x);

    for (var i=0;i < circles.length; ++i) {
      var t = parseInt(circles[i].style.top);
      var l = parseInt(circles[i].style.left);
      circles[i].style.top = (t + offy) + "px";
      circles[i].style.left = (l + offx) + "px";
    }

    var from_list = line_from[id];
    var to_list = line_to[id];
    for (var line_name in from_list) {
      var circle_name = from_list[line_name];
      console.log("get " + line_name + " " + circle_name);
      var line = $("#"+line_name);
      var circle = $("#"+circle_name);
      line.attr("x1", parseInt(circle.css("left"))+5);
      line.attr("y1", parseInt(circle.css("top"))+5);
    }
    for (var line_name in to_list) {
      var circle_name = to_list[line_name];
      console.log("get " + line_name + " " + circle_name);
      var line = $("#"+line_name);
      var circle = $("#"+circle_name);
      line.attr("x2", parseInt(circle.css("left"))+5);
      line.attr("y2", parseInt(circle.css("top"))+5);
    }
    var svg = $("#svg");
    svg.html(svg.html());
    console.log("end");
  }
  return false;
}

// canvas attr
var ele_canvas = $("#svg");
ele_canvas.attr("ondragover", "canvas_dragover(event)");
ele_canvas.attr("ondragenter", "canvas_dragenter(event)");
ele_canvas.attr("ondrop", "canvas_drop(event)");

