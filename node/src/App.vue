<template>
  <div id="app">
    <el-menu :default-active="activeIndex"
             class="el-menu-top"
             mode="horizontal"
             @select="handleSelect"
             text-color="#7BBFEA"
             active-text-color="#409EFF"
    >
      <el-menu-item index="index">主页</el-menu-item>
      <el-menu-item index="database">数据</el-menu-item>
      <section id='user' v-show="$route.path !== '/'">
        <section>
          <img id="logo"
               src="./assets/logo.jpg"
               alt="logo"/>
          <section>
            <section id="name"
                     align="right">可视化数据分析平台</section>
            <section id="actions"
                     align="right"><a>Visual Analysis Platform</a></section>
          </section>
        </section>
      </section>
    </el-menu>

    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return {
        activeIndex: 'index'// $route.path
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        // console.log(key, keyPath)
        switch (key) {
          case "index":
            this.$router.push("/index/projectView");
            break;
          case "database":
            this.$router.push("/database");
            break;
          case "projectDetail":
            this.$router.push("/projectDetail");
            break;
          case "projectView":
            this.$router.push("/projectView");
            break;
          default:
            this.$router.push("/index/projectView");
            break;
        }
      }
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  .el-menu-top {
    padding-left:5%;
    padding-right:5%;
  }

  #logo {
    margin-right: 3%;
    margin-bottom: 1%;
    float: right;
    border-radius: 100%;
    overflow: hidden;

    height: 51px;
    width: 48px;
    -webkit-clip-path: circle(50% at 50% 50%);
    clip-path: circle(50% at 50% 50%);
    margin-left: 10px;
    min-height: 51px;
    min-width: 48px;
    -webkit-box-align: end;
    -ms-flex-align: end;
    align-items: flex-end;
  }

  h3 {
    color: #409EFF;
  }

  h5 {
    color: #409EFF;
  }

</style>
