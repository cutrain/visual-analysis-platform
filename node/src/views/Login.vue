<template>
  <div id="login-body">
    <div class="right">
      <h1>{{ msg }}</h1>
    </div>
    <el-form id="login-form"
             label-position="right"
             label-width="80px"
             :model="ruleForm"
             :rules="rules"
             ref="ruleForm"
    >
      <el-form-item label="用户名" prop="name">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <el-row>
      <el-button type="primary" round @click="login">登录</el-button>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "Login",
    data() {
      var validateName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else {
          /*if (this.ruleForm.name !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();*/
        }
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          /*if (this.ruleForm.password !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();*/
        }
      };
      return {
        msg: '可视化数据分析平台',
        ruleForm: {
          name: '',
          password: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
          ]
        }
      }
    },
    methods:{
      login() {
        if (this.ruleForm.name === 'test' && this.ruleForm.password === 'test') {
          this.$router.push('/index/projectView');
        } else {
          this.$message({
            message: "用户名或密码不正确",
            type: "error",
            showClose: true,
            duration: "2000"
          });
        }
      }
    }
  }
</script>

<style scoped>

  .right h1, h2 {
    font-weight: normal;
    font-size: 30px;
  }

  #login-body {
    padding-left: 40%;
    padding-right: 40%;
  }

  #login-form {

  }

</style>
