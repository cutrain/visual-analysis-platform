var deeplearning_v= new Vue({
  el:'#deeplearning-v',
  methods: {
    click: function() {
      console.log("deeplearning-v clicked");
      change_page('deeplearning');
    }
  }
});

var deeplearning_page = new Vue({
  el:'#deeplearning-page',
  data:{
    visi:'index',
  },
  methods:{
  }
});

