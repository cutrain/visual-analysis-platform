<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h2>Visual Analysis Platform</h2>
    <div >

    </div>
    <el-button @click="toIndex" round>
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-jinru"></use>
      </svg> 进入主页
    </el-button>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: '可视化数据分析平台'
    }
  },
  methods: {
    toIndex() {
      this.$router.push('/index/graphShow');
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
