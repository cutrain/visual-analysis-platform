var component_v = new Vue({
  el:'#component-v',
  methods: {
    click: function() {
      console.log("component-v clicked");
      change_page('component');
    }
  }
});

var component_page = new Vue({
  el:'#component-page',
  data:{
    visi:'index',
  },
  methods:{
  }
});

