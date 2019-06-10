<template>
  <div :class="isSelected ? 'node-select node' : 'node'"
       :id="id"
       @drop="node_drop($event)"
       @dragstart="node_dragstart($event)"
       @dragend="node_dragend($event)"
       @dragover="node_dragover($event)"
       @dragenter="node_dragenter($event)"
       @dragleave="node_dragleave($event)"
       draggable="true"
       v-on:click="node_click($event)"
       ref="noderef"
  >
    <el-button circle
               disabled
               size="mini"
               type="primary"
               class="node-picture">
      <svg class="icon"
           aria-hidden="true"
           style="{pointer-events: none;}">
        <use xlink:href="#icon-shujuku"
             v-if="node.icon_type === 'sql'"></use>
        <use xlink:href="#icon-ico--copy"
             v-else-if="node.icon_type === 'classify'"></use>
        <use xlink:href="#icon-tuxingtuxiangchuli"
             v-else-if="node.icon_type === 'image'"></use>
        <use xlink:href="#icon-shipin-copy"
             v-else-if="node.icon_type === 'video'"></use>
        <use xlink:href="#icon-x_fudonghuigui-copy"
             v-else-if="node.icon_type === 'regression'"></use>
        <use xlink:href="#icon-leibiefenlei"
             v-else-if="node.icon_type === 'clustering'"></use>
        <use xlink:href="#icon-daorumoxing30"
             v-else-if="node.icon_type === 'model'"></use>
        <use xlink:href="#icon-moshubang"
             v-else></use>
      </svg>
    </el-button>

    {{getType()}}
    <circleDraggable v-for="item in items_in"
                     :style="{top:item.posiY, left:item.posiX}"
                     :key="item.index"
                     :id="item.id"
                     :G="G"
                     :drag_data="drag_data"
    ></circleDraggable>
    <circleDraggable v-for="item in items_out"
                     :style="{top:item.posiY, left:item.posiX}"
                     :key="item.index"
                     :id="item.id"
                     :G="G"
                     :drag_data="drag_data"
    ></circleDraggable>
  </div>
</template>

<script>
  import circleDraggable from './CircleDraggable.vue';
  import $ from 'jquery';
  import * as axios from "axios";
  export default {
    name: "node",
    props: ['project_id', 'select_id', 'drag_data', 'G', 'type_detail', 'id', 'node', 'show_detail_box', 'show_data_box', 'show_button_lists', 'dataTypeInBorder', 'imageInBorder', 'stringInBorder', 'addressInBorder'],
    components: {
      circleDraggable
    },
    watch: {
      select_id(oldValue, newValue) {
        this.isSelected = (this.select_id === this.id);
      }
    },
    data () {
      return {
        isSelected: false,
        items_in: [],
        items_out: [],
        curr_id: null,
        node_show_button_lists: false,
        node_show_detail_box: false,
        node_show_data_box: false,
      }
    },
    mounted() {
      let this_type = this.type_detail.get(this.id.split('-')[0]);
      let in_port_num = this_type.in_port.length;
      let out_port_num = this_type.out_port.length;
      function get_full_width(obj) {
        return obj.width() + parseInt(obj.css('padding-left')) + parseInt(obj.css('padding-right'));
      }
      function get_full_height(obj) {
        return obj.height() + parseInt(obj.css('padding-top')) + parseInt(obj.css('padding-bottom'));
      }
      const CIRCLE_X_BIAS = -6;
      const CIRCLE_Y_BIAS = -6;
      const CIRCLE_Y_AWAY = 3;
      let $node = $(this.$refs.noderef);
      let index = 0;
      let circle_width = get_full_width($node);
      let circle_height = get_full_height($node);
      for (let i = 0;i < in_port_num; ++i) {
        let new_circle = {};
        new_circle.id = this.id + '-in-' + i;
        new_circle.index = index++;
        new_circle.posiX = Math.floor(circle_width/(1+in_port_num) * (i + 1) + CIRCLE_X_BIAS) + 'px';
        new_circle.posiY = CIRCLE_Y_BIAS - CIRCLE_Y_AWAY + 'px';
        this.items_in.push(new_circle);
      }
      for (let i = 0;i < out_port_num; ++i) {
        let new_circle = {};
        new_circle.id = this.id + '-out-' + i;
        new_circle.index = index++;
        new_circle.posiX = Math.floor(circle_width/(1+out_port_num) * (i + 1) + CIRCLE_X_BIAS) + 'px';
        new_circle.posiY = Math.floor(circle_height + CIRCLE_Y_BIAS + CIRCLE_Y_AWAY) + 'px';
        this.items_out.push(new_circle);
      }
    },
    methods: {
      node_dragstart(e) {
        let class_type = this.drag_data.get("class_type");
        console.log('node drag start :', class_type);
        if (this.drag_data.get('class_type') == 'circle') {
          return true;
        }
        e.dataTransfer.effectAllowed = "move";
        this.drag_data.set("class_type", "node");
        this.drag_data.set("node_id", e.target.id);
        this.drag_data.set("text", null);
        let bias_x = e.clientX - this.getX($('#'+e.target.id)[0]);
        let bias_y = e.clientY - this.getY($('#'+e.target.id)[0]);
        this.drag_data.set("bias_x", bias_x);
        this.drag_data.set("bias_y", bias_y);
        e.dataTransfer.setDragImage(e.target, bias_x, bias_y);
        return true;
      },

      node_dragover(e) {
        e.preventDefault();
      },

      node_dragend(e) {
        this.drag_data.delete("class_type");
        this.drag_data.delete("node_id");
        this.drag_data.delete("text");
        this.drag_data.delete("bias_x");
        this.drag_data.delete("bias_y");
        return false;
      },

      node_dragenter(e) {
        e.preventDefault();
        let class_type = this.drag_data.get('class_type');
        console.log('node drag enter:', class_type);
        if (class_type == 'circle') {
          if (this.drag_data.has('enter')) {
            let id = this.drag_data.get('enter');
            let temp = $('#' + id);
            temp.css('border-width', '2px');
            this.drag_data.delete('enter');
          }
          let id = e.target.id;
          let temp = $('#'+id);
          temp.css('border-width', '3px');
          this.drag_data.set('enter', id);
        }
      },

      node_dragleave(e) {
        e.preventDefault();
        let class_type = this.drag_data.get('class_type');
        console.log('node drag leave:', class_type);
        if (class_type == 'circle') {
          if (this.drag_data.has('enter')) {
            let id = this.drag_data.get('enter');
            if (e.target.id == id) {
              let temp = $('#' + id);
              temp.css('border-width', '2px');
              this.drag_data.delete('enter');
            }
          }
        }
      },

      node_drop(e) {
        e.preventDefault();
        let class_type = this.drag_data.get("class_type");
        console.log('node drop :', class_type);
        if (class_type == 'circle') {
          let id = e.target.id;
          let from_id = this.drag_data.get('from_id');
          if (id.split('-').length == 2) {
            let itype = this.type_detail.get(id.split('-')[0]);
            if (from_id.split('-')[2] == 'in') {
              for (let i = 0;i < itype.out_port.length; ++ i) {
                if (this.G.testEdge(id + '-out-' + i, from_id) == 0) {
                  this.G.addEdge(id + '-out-' + i, from_id);
                  return true;
                }
              }
            } else {
              for (let i = 0;i < itype.in_port.length; ++ i) {
                if (this.G.testEdge(from_id, id + '-in-' + i) == 0) {
                  this.G.addEdge(from_id, id + '-in-' + i);
                  return true;
                }
              }
            }
          }
          return false;
        }
        else if (class_type == 'node') {
          let bias_x = parseInt(this.drag_data.get("bias_x"));
          let bias_y = parseInt(this.drag_data.get("bias_y"));
          let x = e.clientX - this.getX($(".canvas")[0]) + document.body.scrollLeft - bias_x;
          let y = e.clientY - this.getY($(".canvas")[0]) + document.body.scrollTop - bias_y;
          this.G.setPosition(this.drag_data.get('node_id'), x, y);
          this.$emit('update:G', this.G);
        }
      },

      getX(obj) {
        let parObj = obj;
        let left = obj.offsetLeft;
        while (parObj = parObj.offsetParent) {
          left += parObj.offsetLeft;
        }
        return left;
      },

      getY(obj) {
        let parObj = obj;
        let top = obj.offsetTop;
        while (parObj = parObj.offsetParent) {
          top += parObj.offsetTop;
        }
        return top;
      },

      getType() {
        return this.type_detail.get(this.id.split('-')[0]).display;
      },

      node_click(e) {
        // 1. 保存之前点击的节点的参数（G.setParam(node_id, param)
        // 2. 记录当前节点id
        // 3. 渲染前端参数表
        // 4. 请求节点数据（如果没有数据，不显示）并渲染

        let id = e.target.id;
        console.log('id: ', id);

        this.curr_id = id;
        this.$emit('update:curr_id', id);
        let tableBox = $("#table-box");
        tableBox.empty();

        if (this.show_detail_box === false) {
          this.node_show_detail_box = true;
          this.$emit('update:node_show_detail_box', this.node_show_detail_box);
        }
        if (this.show_data_box === false) {
          this.node_show_data_box = true;
          this.$emit('update:node_show_data_box', this.node_show_data_box);
        }
        if (this.show_button_lists === false) {
          this.node_show_button_lists = true;
          this.$emit('update:node_show_button_lists', this.node_show_button_lists);
        }

        // before loading, clear
        let table = {}, data = [], title = [];
        let key = 'title';
        table[key] = title;
        key = 'data';
        table[key] = data;
        this.$emit('update:tableInBorder', table);
        this.$emit('update:stringInBorder', '正在读取...');
        this.$emit('update:imageInBorder', {url:'',shape:''});
        this.$emit('update:addressInBorder','');

        let $detail_top = $("<div class='detail-top' style='order:0;'>属性</div>")
        let dataPost =JSON.stringify({
          "project_id": this.project_id,
          "node_id": id
        });

        axios.post(this.$api.graphSample, dataPost)
          .then(ret => {
            ret = ret.data;
            console.log(ret);
            console.log('-----------');
            if (ret.succeed == 0) {
              if (ret.data.length == 0)
                return;
              let show = ret.data[0];
              if (show.type == 'DataFrame') {
                let table = {};
                let data = [], title = [];
                if (show.row_num > 0) {
                  let row = show.row_num;
                  let col = show.col_num;
                  for (let i = 0;i < show.col_index.length;++ i) {
                    let value = show.col_index[i] + '(' + show.col_type[i] + ')';
                    title.push(value);
                  }
                  show = show.data;
                  console.log(show);
                  for (let i=0;i < row; ++i) {
                    let rowValue = {};
                    for (let j=0;j < col; ++j) {
                      let key = title[j];
                      rowValue[key] = show[i][j];
                    }
                    data.push(rowValue);
                  }
                }
                let key = 'title';
                table[key] = title;
                key = 'data';
                table[key] = data;

                this.$emit('update:tableInBorder', table);
                this.$emit('update:dataTypeInBorder', 'DataFrame');
              }
              else if (show.type == 'Image') {
                let image = {};
                let shape = show.data.shape;
                if (shape.length === 2) {
                  shape.push(1);
                }
                let string_shape = 'Shape:' + shape[0] + 'X' + shape[1] + 'X' + shape[2];

                image.url = show.data.url;
                image.shape = string_shape;

                this.$emit('update:imageInBorder', image);
                this.$emit('update:dataTypeInBorder', 'Image');
              }
              else if (show.type == 'String') {
                let str = show.value;
                this.$emit('update:stringInBorder', str);
                this.$emit('update:dataTypeInBorder', 'String');
              }
              else if (show.type == 'Video' || show.type == 'Graph') {
                let addr = show.value; //TODO: 确认
                this.$emit('update:addressInBorder', addr);
                this.$emit('update:dataTypeInBorder', 'Address');
              }
              else {
                alert('type ' + ret.type + ' not implemented');
              }
            } else {
              let table = {};
              let data = [], title = [];
              let key = 'title';
              table[key] = title;
              key = 'data';
              table[key] = data;
              this.$emit('update:tableInBorder', table);
              this.$emit('update:dataTypeInBorder', 'DataFrame')
            }
          })
          .catch(() => {});
      },
    }
  }
</script>

<style scoped>
  .node-picture {
    cursor: default;
    pointer-events: none;
    box-shadow: none;
    opacity: 1;
  }
</style>
