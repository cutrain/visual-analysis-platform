<template>
  <div>
    <!-- v-model=? -->
    <!--<el-input-->
      <!--v-show="border.bt.type === 'file'"-->
      <!--:id="border.bt.id"-->
      <!--:style="{order: border.bt.order}"-->
      <!--v-bind:change="file_name()"-->
      <!--type="file">-->
    <!--</el-input>-->

    <el-input
      v-show="border.value.data_type === 'text'"
      v-bind:class="[border.value.data_type === 'text' ? 'param-value' : 'param-value-inactive']"
      type="text"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_text"
      :style="{order: border.value.order}"
    >
    </el-input>

    <!--<el-input
      v-show="border.value.data_type === 'file'"
      v-bind:class="[border.value.data_type === 'file' ? 'param-value' : 'param-value-inactive']"
      type="text"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_file"
      :id="border.value.id"
      :style="{order: border.value.order}"
    >
    </el-input>-->
    <div v-show="border.value.data_type === 'file'"
         :style="{order: border.value.order}"
    >
      <el-button v-show="border.value.data_type === 'file'"
                 v-bind:class="[border.value.data_type === 'file' ? 'param-value' : 'param-value-inactive']"
                 :name="border.value.name"
                 :data_type="border.value.data_type"
                 :id="border.value.id"

                 @click="fileSelect()"
      >文件目录</el-button>
      已选择：{{this.msgFileName}}
    </div>

    <!--<el-input
      v-show="border.value.data_type === 'model'"
      v-bind:class="[border.value.data_type === 'model' ? 'param-value' : 'param-value-inactive']"
      type="text"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_file"
      :id="border.value.id"
      :style="{order: border.value.order}"
    >
    </el-input>-->
    <div v-show="border.value.data_type === 'model'"
         :style="{order: border.value.order}"
    >
      <el-button v-show="border.value.data_type === 'model'"
                 v-bind:class="[border.value.data_type === 'model' ? 'param-value' : 'param-value-inactive']"
                 :name="border.value.name"
                 :data_type="border.value.data_type"
                 :id="border.value.id"

                 @click="modelSelect()"
      >模型目录</el-button>
      已选择：{{this.msgModelName}}
    </div>

    <el-input
      v-show="border.value.data_type === 'password'"
      v-bind:class="[border.value.data_type === 'password' ? 'param-value' : 'param-value-inactive']"
      type="password"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_password"
      :style="{order: border.value.order}"

    ><!--show-password-->
    </el-input>

    <el-select
      v-show="border.value.data_type === 'list'"
      v-bind:class="[border.value.data_type === 'list' ? 'param-value' : 'param-value-inactive']"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_list"
      placeholder="请选择"
      :style="{order:border.value.order}">
      <el-option
        v-for="(item, index) in border.value.lists"
        :key="index"
        :label="item.value"
        :value="item.value">
      </el-option>
    </el-select>

    <!-- number: int, float -->
    <el-input
      v-show="border.value.data_type === 'number'"
      v-bind:class="[border.value.data_type === 'number' ? 'param-value' : 'param-value-inactive']"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_int"
      type="number"
      :style="{order: border.value.order}"
    >
    </el-input>

    <el-input
      v-show="border.value.data_type === 'int'"
      v-bind:class="[border.value.data_type === 'int' ? 'param-value' : 'param-value-inactive']"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_int"
      type="number"
      :style="{order: border.value.order}"
    >
    </el-input>

    <el-input
      v-show="border.value.data_type === 'float'"
      v-bind:class="[border.value.data_type === 'float' ? 'param-value' : 'param-value-inactive']"
      :name="border.value.name"
      :data_type="border.value.data_type"
      v-model="input_float"
      type="number"
      :style="{order: border.value.order}"
    >
    </el-input>

    <el-input
      v-show="border.value.data_type === 'richtext'"
      v-bind:class="[border.value.data_type === 'richtext' ? 'param-value' : 'param-value-inactive']"
      :name="border.value.name"
      :data_type="border.value.data_type"
      type="textarea"
      :autosize="{ minRows: 3}"
      placeholder="请输入内容"
      v-model="input_richtext"
      :style="{order: border.value.order}"
    >
    </el-input>

    <div
      class="param-key"
      :style="{order: border.key.order}"
    >
      {{border.key.text}}
    </div>
  </div>
</template>

<script>
  export default {
    name: "paramBorder",
    props:['border', 'curr_id', 'props_list', 'back_flag', 'msgFileName', 'msgModelName'],
    data() {
      return {
        param_data: {                  // have to be saved
          value: null,
          name: null,
        },
        input_text: '',                 // input value
        input_file: '',
        input_model: '',
        input_password: '',
        input_list: '',
        input_int: 0,
        input_float: 0,
        input_number: 0,
        input_richtext: '',
      }
    },
    created() {
      for (let key in this.props_list) {
        if (this.props_list.hasOwnProperty(key)) {
          if (this.border.value.name === key) {
            switch (this.border.value.data_type) {
              case 'text': {
                this.input_text = this.props_list[key];
                break;
              }
              case 'file': {
                this.input_file = this.props_list[key];
                break;
              }
              case 'model': {
                this.input_model = this.props_list[key];
                break;
              }
              case 'password': {
                this.input_password = this.props_list[key];
                break;
              }
              case 'list': {
                this.input_list = this.props_list[key];
                break;
              }
              case 'number': { // TODO
                this.input_number = this.props_list[key];
                break;
              }
              case 'int': {
                this.input_int = this.props_list[key];
                break;
              }
              case 'float': {
                this.input_float = this.props_list[key];
                break;
              }
              case 'richtext': {
                this.input_richtext = this.props_list[key];
                break;
              }
              default: {
                console.log('There is no type of '+ this.border.value.data_type + '.');
              }
            }
            console.log('refresh.');
            break;
          }
        }
      }
    },
    watch: {
      curr_id(newValue, oldValue) {
        // 无需判断情况，ProjectDetail中判断
        // 传回输入框中的值
        this.save_input();
        this.$emit('update:param_list', this.param_data);

        // 填入新点击node的param
        this.$nextTick(()=>{
          setTimeout(() => {
            for (let key in this.props_list) {
              if (this.props_list.hasOwnProperty(key)) {
                if (this.border.value.name === key) {
                  switch (this.border.value.data_type) {
                    case 'text': {
                      this.input_text = this.props_list[key];
                      break;
                    }
                    case 'file': {
                      this.input_file = this.props_list[key];
                      break;
                    }
                    case 'model': {
                      this.input_model = this.props_list[key];
                      break;
                    }
                    case 'password': {
                      this.input_password = this.props_list[key];
                      break;
                    }
                    case 'list': {
                      this.input_list = this.props_list[key];
                      break;
                    }
                    case 'number': {
                      this.input_number = this.props_list[key];
                      break;
                    }
                    case 'int': {
                      this.input_int = this.props_list[key];
                      break;
                    }
                    case 'float': {
                      this.input_float = this.props_list[key];
                      break;
                    }
                    case 'richtext': {
                      this.input_richtext = this.props_list[key];
                      break;
                    }
                    default: {
                      console.log('There is no type of '+ this.border.value.data_type + '.');
                    }
                  }
                  console.log('paramBorder refresh.');
                  break;
                }
              }
            }
          }, 200)
        });

      },
      back_flag(newValue, oldValue) {
        if (newValue === true) {
          this.save_input();
          this.$emit('update:last_lists', this.param_data);
          console.log('save the last node.');
        }
      },
      msgFileName(newValue, oldValue) {
        this.input_file = newValue;
      }
    },
    methods: {
      // TODO: input file v-model; delete border.bt
      file_name(){
        /*if (this.border.bt.type === 'file') {
          let file = document.getElementById('pathbt');
          $("#path").val(file.name);
        }
        else {

        }*/
      },

      save_input() {
        let obj = {};
        obj.name = this.border.value.name;

        switch (this.border.value.data_type) {
          case 'text': {
            obj.value = this.input_text;
            break;
          }
          case 'file': {
            obj.value = this.input_file;
            break;
          }
          case 'model': {
            obj.value = this.input_model;
            break;
          }
          case 'password': {
            obj.value = this.input_password;
            break;
          }
          case 'list': {
            obj.value = this.input_list;
            break;
          }
          case 'int': {
            obj.value = this.input_int;
            break;
          }
          case 'float': {
            obj.value = this.input_float;
            break;
          }
          case 'richtext': {
            obj.value = this.input_richtext;
            break;
          }
          default: {
            obj.value = null;
            console.log('There is no type of '+ this.border.value.data_type + '.');
          }
        }

        this.param_data = obj;
      },

      fileSelect() {
        //this.$emit('update:selectFileInDialog', this.input_file);
        this.$emit('update:fileSelectVisible', true);
      },

      modelSelect() {
        //this.$emit('update:selectModelInDialog', this.input_model);
        this.$emit('update:modelSelectVisible', true);
      }
    }
  }
</script>

<style scoped>

</style>
