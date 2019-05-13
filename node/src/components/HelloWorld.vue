<template>
  <div class="hello">
    <el-carousel :interval="3000" height="500px" arrow="always" type="card">
      <el-carousel-item v-for="(item, index) in introduction_items" :key="index">
        <div style="position: relative;">
          <div class="image_list">
            <img class="image_item"
                 v-if="item.id === 1"
                 src="../assets/earth_2.jpg"
                 alt=""/>
            <img class="image_item"
                 v-else-if="item.id === 2"
                 src="../assets/plain_earth.jpg"
                 alt=""/>
            <img class="image_item"
                 v-else-if="item.id === 3"
                 src="../assets/top_earth.jpg"
                 alt=""/>
            <img class="image_item"
                 v-else
                 src="../assets/plain_earth.jpg"
                 alt=""/>
          </div>
          <span style="position: absolute; top: 7%; bottom: 7%; left: 5%; right: 5%;">
            <h3 class="medium">
              <svg class="icon"
                   aria-hidden="true"
                   style="{pointer-events: none;}"
              >
                <use xlink:href="#icon-diqiu"
                     v-if="item.id === 1"
                ></use>
                <use xlink:href="#icon-algorithm"
                     v-else-if="item.id === 2"
                ></use>
                <use xlink:href="#icon-bulb"
                     v-else-if="item.id === 3"
                ></use>
                <use xlink:href="#icon-black-gear"
                     v-else
                ></use>
              </svg>
              {{ item.title }}
            </h3>
            <h4>{{ item.content }}</h4>
          </span>
        </div>

      </el-carousel-item>
    </el-carousel>
    <br/>

    <div id="title">
      <div class="left">
        <img id="welcome_logo" src="../assets/logo.jpg" alt="logo">
      </div>
      <div class="middle">

      </div>
      <div class="right">
        <h1>{{ msg }}</h1>
        <h2>{{ msgEn }}</h2>
        <div class="right-bottom">
          <el-button id="toIndex_button" @click="toIndex" round>
            <svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-jinru"></use>
            </svg> 进入主页
          </el-button>
        </div>
      </div>
    </div>
    <br/><br/>
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        msg: '可视化数据分析平台',
        msgEn: 'Visual Analysis Platform',
        introduction_items: [
          {
            'title': '交互设计理念，数据分析可视化',
            'content': '将数据挖掘等领域算法封装为模块，以期通过拖拽、连线模块的简便方式，帮助使用者用以快速搭建模型。',
            'id': 1
          },{
            'title': '优选数据挖掘算法',
            'content': '多种类型的经典算法，一应俱全。',
            'id': 2
          },/*{
            'title': '实现数据挖掘的全过程',
            'content': '支持对数据库文件的导入、基本操作，对训练数据的预处理等操作。',
            'id': 3
          },*/{
            'title': '轻松管理项目、数据',
            'content': '轻松管理生成的项目、导入平台的数据，如拖拽移动数据集等。',
            'id': 3
          },
        ]
      }
    },
    methods: {
      toIndex() {
        this.$router.push('/index/projectView');
      }
    }
  }
</script>

<style scoped>
  .image_list {
    background-image: linear-gradient(rgba(255,255,255,0),rgba(255,255,255,0.65));
  }

  .image_list .image_item {
    mix-blend-mode: overlay;
  }

  #title {
    display: block;
  }

  #title .left #welcome_logo {
    height: 151px;
    width: 148px;
    -webkit-clip-path: circle(50% at 50% 50%);
    clip-path: circle(50% at 50% 50%);
    margin-left: 10px;
    min-height: 51px;
    min-width: 48px;
    -webkit-box-align: end;
    -ms-flex-align: end;
    align-items: flex-end;
  }

  #title .right h1, h2 {
    font-weight: normal;
    font-size: 30px;
    text-align: left;

  }
  #title .right .right-bottom {
    display: block;
    text-align: left;
  }

  #title .left, #title .middle, #title .right {
    display: inline-block;
    vertical-align: baseline;
    margin-left: 10px;
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

  .el-carousel__item h3 {
    color: #ffffff;
    font-size: 20px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }

  .el-carousel__item h4 {
    color: #ffffff;
    font-size: 16px;
    opacity: 0.75;
    margin: 0;

  }

  /*.el-carousel__item:nth-child(2n) {
    background-color: #c0d1e7;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #e4edf7;
  }*/
</style>
