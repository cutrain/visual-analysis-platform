<template>
  <div>
    <div
      v-for="(item, index) in border_items"
      :key="item.order"
      :class="item.class"
      :style="{order:item.order}"
    >
      <div>
         <!--v-model=? -->
        <el-input
          v-show="item.bt.type === 'file'"
          :id="item.bt.id"
          :style="{order: item.bt.order}"
          v-bind:change="file_name()"
          type="file"
        >
        </el-input>

        <el-input
          v-show="item.value.data_type === 'text'"
          v-bind:class="[item.value.data_type === 'text' ? 'param-value' : 'param-value-inactive']"
          type="text"
          :name="item.value.name"
          :data_type="item.value.data_type"
          v-model="input[index]"
          :style="{order: item.value.order}"
        >
        </el-input>

        <el-input
          v-show="item.value.data_type === 'file'"
          v-bind:class="[item.value.data_type === 'file' ? 'param-value' : 'param-value-inactive']"
          type="text"
          :name="item.value.name"
          :data_type="item.value.data_type"
          v-model="input[index]"
          :id="item.value.id"
          :style="{order: item.value.order}"
        >
        </el-input>

        <el-input
          v-show="item.value.data_type === 'password'"
          v-bind:class="[item.value.data_type === 'password' ? 'param-value' : 'param-value-inactive']"
          type="password"
          :name="item.value.name"
          :data_type="item.value.data_type"
          v-model="input[index]"
          :style="{order: item.value.order}"

        ><!--show-password-->
        </el-input>

        <el-select
          v-show="item.value.data_type === 'list'"
          v-bind:class="[item.value.data_type === 'list' ? 'param-value' : 'param-value-inactive']"
          :name="item.value.name"
          :data_type="item.value.data_type"
          v-model="input[index]"
          placeholder="请选择"
          :style="{order:item.value.order}">
          <el-option
            v-for="(subItem, index) in item.value.lists"
            :key="index"
            :label="subItem.value"
            :value="subItem.value">
          </el-option>
        </el-select>

        <el-input
          v-show="item.value.data_type === 'number'"
          v-bind:class="[item.value.data_type === 'number' ? 'param-value' : 'param-value-inactive']"
          :name="item.value.name"
          :data_type="item.value.data_type"
          v-model="input[index]"
          type="number"
          :style="{order: item.value.order}"
        >
        </el-input>

        <el-input
          v-show="item.value.data_type === 'richtext'"
          v-bind:class="[item.value.data_type === 'richtext' ? 'param-value' : 'param-value-inactive']"
          :name="item.value.name"
          :data_type="item.value.data_type"
          type="textarea"
          :autosize="{ minRows: 3}"
          placeholder="请输入内容"
          v-model="input[index]"
          :style="{order: item.value.order}"
        >
        </el-input>

        <div
          class="param-key"
          :style="{order: item.key.order}"
        >{{item.key.text}}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "paramBorder",
    props:['border_items', 'curr_id'],
    data() {
      return {
        param_data: {                  // have to be saved
          value: null,
          name: null,
        },
        input_text: '',                 // input value
        input_file:'',
        input_password: '',
        input_list: '',
        input_number: 0,
        input_richtext: '',
        input: [],
        input_name: [],
      }
    },
    created() {
      console.log('---------border_items----------------');
      console.log(this.border_items);
      console.log('-------------------------------------');
    },
    mounted() {

      this.setInputName();
    },
    watch: {
      curr_id(newValue, oldValue) {
        this.save_input();
        this.$emit('update:param_list', this.param_data);
      }
    },
    methods: {
      // TODO: input file v-model = ?
      setInputName() {
        for (let key in this.border_items) {
          if (this.border_items.hasOwnProperty(key)) {
            console.log(key);
          }
          //this.input_name.push(this.border_items.value.name);
        }
        console.log('-----------input_name-------------');
        console.log(this.input_name);
        console.log('----------------------------------');
      },

      file_name() {},

      save_input() {
        for (let i=0;i < this.input_name.length; ++i) {
          this.param_data[this.input_name[i]] = input[i];
        }

        // console.log(this.param_data);

      },
    }
  }
</script>

<style scoped>

</style>
