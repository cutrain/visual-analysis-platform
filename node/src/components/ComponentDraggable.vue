<template>
  <div v-if="!model.isdraggable"
       class="component-directory">
    <ul>
      <div class="directory-row"
           @click="toggle">
        <br/>
        <b>
          <span v-if = "model.lists && model.lists.length"
                class="zip-icon"
                v-bind:class="[model.open ? 'arrow-bottom' : 'arrow-right']"
          ></span>
          <span v-else
                class="zip-icon arrow-transparent"
          ></span>
          <svg class="icon"
               aria-hidden="true"
               v-if="!model.open">
            <use xlink:href="#icon-putongwenjianjia"></use>
          </svg>
          <svg class="icon"
               aria-hidden="true"
               v-if="model.open">
            <use xlink:href="#icon-wenjianjia"></use>
          </svg>
          <span>{{model.display}}</span>
        </b>
      </div>
      <component-draggable v-show="model.open"
                           v-for="(item, index) in model.lists"
                           :key="index"
                           :model="item"
                           :drag_data="drag_data"
      ></component-draggable>
    </ul>
  </div>
  <li v-else="model.isdraggable">
    <br/>

    <div class="component"
         :id="model.name"
         @drop="comp_drop($event)"
         @dragstart="comp_dragstart($event)"
         @dragend="comp_dragend($event)"
         @dragover="comp_dragover($event)"
         :draggable="model.isdraggable"
    >
      <svg class="icon" aria-hidden="true">
        <use
          xlink:href="#icon-shujuku"
          v-if="model.icon_type === 'sql'"></use>
        <use
          xlink:href="#icon-ico-"
          v-else-if="model.icon_type === 'classify'"></use>
        <use
          xlink:href="#icon-tuxingtuxiangchuli"
          v-else-if="model.icon_type === 'image'"></use>
        <use
          xlink:href="#icon-shipin"
          v-else-if="model.icon_type === 'video'"></use>
        <use
          xlink:href="#icon-x_fudonghuigui"
          v-else-if="model.icon_type === 'regression'"></use>
        <use
          xlink:href="#icon-leibiefenlei"
          v-else-if="model.icon_type === 'clustering'"></use>
        <use
          xlink:href="#icon-daorumoxing30"
          v-else-if="model.icon_type === 'model'"></use>
        <use
          xlink:href="#icon-moshubang"
          v-else></use>
      </svg>
      {{model.display}}
    </div>
  </li>

</template>
<script>
  import $ from 'jquery';
  export default {
    name: "componentDraggable",
    props: ['drag_data', 'model', 'node_items'],
    data() {
      return {
        icon_database: false,
        icon_others: false,
      }
    },
    computed: {
      isFolder() {
        return this.model.lists && this.model.lists.length
      }
    },
    methods: {
      comp_dragstart(e) {
        let class_type = this.drag_data.get('class_type');
        console.log('comp drag start :', class_type);
        this.drag_data.set("class_type", "component");
        this.drag_data.set("type", e.target.id);
        this.drag_data.set("text", e.target.innerHTML);
        let comp_scroll_y = $('#scrollBar').children().scrollTop();
        let bias_x = e.clientX - this.getX($('#' + e.target.id)[0]);
        let bias_y = e.clientY - this.getY($('#' + e.target.id)[0]) + comp_scroll_y;
        this.drag_data.set("bias_x", bias_x);
        this.drag_data.set("bias_y", bias_y);
        // console.log('bias_y : ', parseInt(this.drag_data.get("bias_y")));
        e.dataTransfer.setDragImage(e.target, bias_x, bias_y);
      },

      comp_dragend(e) {
        this.drag_data.delete("class_type");
        this.drag_data.delete("type");
        this.drag_data.delete("text");
        this.drag_data.delete("bias_x");
        this.drag_data.delete("bias_y");
      },

      comp_dragover(e) {
        console.log('comp drag over');
        e.preventDefault();
      },

      comp_drop(e) {
        console.log('comp drop');
        e.preventDefault();
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

      toggle() {
        if(this.isFolder) {
          this.model.open = !this.model.open
        }
      },

      getIconType(icon_type) {
        switch (icon_type) {
          case 1:

        }
      },
    }
  }
</script>

<style>
  .directory-row {
    text-align: left;
  }
  .zip-icon{
    display: inline-block;
    width: 8px;
    height: 8px;
    vertical-align: middle;
    background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAf0lEQVQ4T7XT0Q2AMAhF0dvNdALdSEdzBB3BDXQD85LGRNMCauS7nAKBxMdIhfwemIAtYpeAEeiANoLUgAGYI4gFqAMX8QAXiQBCNFDNRBVdIgpUkSfADjT3KqLACmg/XrWw5J+Li+VVYCZrMBbgJluA+tXA3Hv45ZgiR3i+OQBeSyYRPEyeUAAAAABJRU5ErkJggg==') no-repeat center;
    background-size: cover;
  }
  .arrow-transparent{
    visibility: hidden;
  }
  .arrow-right{

  }
  .arrow-bottom{
    transform: rotate(90deg)
  }
</style>
