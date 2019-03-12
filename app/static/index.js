var index_v = new Vue({
  el:'#index-v',
  methods: {
    click: function() {
      console.log("index-v clicked");
      change_page('index');
    }
  }
});

Vue.component('index-row', {
  props:['gname', 'create_time', 'gid'],
  template:`<tr>
  <td>{{gname}}</td>
  <td>{{create_time}}</td>
  <td>
    <button v-on:click='$emit("enter_graph")'>
    进入项目
    </button>
  </td>
  </tr>`
});

var index_page = new Vue({
  el:'#index-page',
  data: {
    cols:[
      // TODO:get real data
      {
        gid:123,
        gname:"流程图1",
        create_time:"2019.1.20",
      }
    ],
    project_ids:[],
    visi:'index',
  },
  methods: {
    show_graph: function(e) {
      change_page('graph');
      console.log("show_graph");
      // TODO:
    },
    new_graph: function() {
      change_page('graph');
      console.log("new_graph");
      // TODO:
    },
  }
});

var graph_page = new Vue({
  el:'#graph-page',
  data:{
    visi:'index',
  },
  methods:{
  }
});


