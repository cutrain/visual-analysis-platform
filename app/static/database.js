var database_v = new Vue({
  el:'#database-v',
  methods: {
    click: function() {
      console.log("database-v clicked");
      change_page('database');
    }
  }
});

Vue.component('database-row', {
  props:['dataname', 'create_time', 'dataid'],
  template:`<tr>
  <td>{{dataname}}</td>
  <td>{{create_time}}</td>
  <td>
    <button v-on:click='$emit("view_data")'>
    查看数据
    </button>
  </td>
  </tr>`
});

var database_page = new Vue({
  el:'#database-page',
  data:{
    cols:[
      // TODO: get real data
      {
        dataid:111,
        dataname:"股票数据",
        create_time:"2019.1.20",
      }
    ],
    visi:'index',
  },
  methods:{
    show_data: function(e) {
      console.log("show_data");
      var temp_data = [
        ['a','b','c','d','e','f','g','h','label'],
        [140.56,55.68,-0.23,-0.69,3.19,19.11,7.97,74.24,0],
        [102.50,58.88,0.46,-0.51,1.67,14.86,10.57,127.39,0],
        [103.01,39.34,0.32,1.05,3.12,21.74,7.73,63.17,0],
        [136.75,57.17,-0.06,-0.63,3.64,20.95,6.89,53.59,0],
        [88.72,40.67,0.60,1.12,1.17,11.46,14.26,252.56,0],
        [93.57,46.69,0.53,0.41,1.63,14.54,10.62,131.39,0],
        [119.48,48.76,0.03,-0.11,0.99,9.27,19.20,479.75,0],
        [130.38,39.84,-0.15,0.38,1.22,14.37,13.53,198.23,0],
        [107.25,52.62,0.45,0.17,2.33,14.48,9.00,107.97,0],
        [107.25,39.49,0.46,1.16,4.07,24.98,7.39,57.78,0]
      ];
        alert(temp_data);
        //var $tabledata = $('<table class="float-table"></table>');
        //for (var i in temp_data) {
        //var $new_row = $('<tr></tr>');
        //for (var j in temp_data[i]) {
        //var $new_col= $('<td>'+temp_data[i][j]+'</td>');
        //$new_row.append($new_col);
        //}
        //$tabledata.append($new_row);
          //}
      // TODO:
    }
  }
});

