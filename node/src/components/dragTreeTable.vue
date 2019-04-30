<template>
  <div class="drag-tree-table" ref="table">
    <div class="drag-tree-table-header">
      <column
        v-for="(item, index) in data.columns"
        :width="item.width"
        :flex="item.flex"
        :key="index" >
        {{item.title}}
      </column>
    </div>
    <div class="drag-tree-table-body" @dragover="draging" @dragend="drop"  :class="isDraing ? 'is-draging' : '' ">
      <row depth="0" :columns="data.columns" :isdraggable="isdraggable"
           :model="item" v-for="(item, index) in data.lists" :key="index">
      </row>
    </div>
  </div>
</template>

<script>
  import row from './row.vue'
  import column from './column.vue'
  import space from './space.vue'
  import * as axios from "axios";
  document.body.ondrop = function (event) {
    event.preventDefault();
    event.stopPropagation();
  };
  export default {
    name: "dragTreeTable",
    components: {
      row,
      column,
      space
    },
    props: {
      isdraggable: {
        type: Boolean,
        default: true
      },
      data: Object,
      onDrag: Function,
    },
    data() {
      return {
        treeData: [],
        dragX: 0,
        dragY: 0,
        dragId: '',
        targetId: '',
        whereInsert: '',
        isDraing: false,
      }
    },
    methods: {
      getDragId() {
        return window.dragId;
      },
      getCurDatasetName() {
        return this.srcDatasetName;
      },
      getNewDatasetName() {
        return this.destDatasetName;
      },
      getElementLeft(element) {
        var actualLeft = element.offsetLeft;
        var current = element.offsetParent;
        while (current !== null){
          actualLeft += current.offsetLeft;
          current = current.offsetParent;
        }
        return actualLeft
      },
      getElementTop(element) {
        // 如果表格在容器中滚动，需要做特殊计算
        let scrollTop = this.$refs.table.parentElement.scrollTop;
        var actualTop = element.offsetTop - scrollTop;
        var current = element.offsetParent;
        while (current !== null) {
          actualTop += current.offsetTop;
          current = current.offsetParent;
        }
        return actualTop
      },
      draging(e) {
        this.isDraing = true;
        if (e.pageX == this.dragX && e.pageY == this.dragY) return;
        this.dragX = e.pageX;
        this.dragY = e.pageY;
        this.filter(e.pageX, e.pageY);
        if (e.clientY < 100) {
          window.scrollTo(0, scrollY - 6)
        } else if (e.clientY > (document.body.clientHeight - 160)) {
          window.scrollTo(0, scrollY + 6)
        }
      },
      drop(event) {
        this.clearHoverStatus();
        this.resetTreeData();
        this.isDraing = false;
      },
      filter(x,y) {
        var rows = document.querySelectorAll('.tree-row');
        this.targetId = undefined;
        const dragOriginElementTop = this.getElementTop(dragParentNode);
        const dragOriginElementLeft = this.getElementLeft(dragParentNode);
        const dragW = dragOriginElementLeft + dragParentNode.clientWidth;
        const dragH = dragOriginElementTop + dragParentNode.clientHeight;
        if (x >= dragOriginElementLeft && x <= dragW && y >= dragOriginElementTop && y <= dragH) {
          // 当前正在拖拽原始块不允许插入
          return
        }
        for(let i=0; i < rows.length; i++) {
          const row = rows[i];
          const rx = this.getElementLeft(row);
          const ry = this.getElementTop(row);
          const rw = row.clientWidth;
          const rh = row.clientHeight;
          if (x > rx && x < (rx + rw) && y > ry && y < (ry + rh)) {
            const diffY = y - ry;
            const hoverBlock = row.children[row.children.length - 1];
            hoverBlock.style.display = 'block';
            const targetId = row.getAttribute('tree-id');
            this.targetId = targetId;
            let whereInsert = '';
            var rowHeight = row.offsetHeight;

            if (diffY/rowHeight > 3/4) {
              if (hoverBlock.children[2].style.opacity !== '0.5') {
                this.clearHoverStatus();
                hoverBlock.children[2].style.opacity = 0.5
              }
              whereInsert = 'bottom'
            } else if (diffY/rowHeight > 1/4) {
              if (hoverBlock.children[1].style.opacity !== '0.5') {
                this.clearHoverStatus();
                hoverBlock.children[1].style.opacity = 0.5
              }
              whereInsert = 'center'
            } else {
              if (hoverBlock.children[0].style.opacity !== '0.5') {
                this.clearHoverStatus();
                hoverBlock.children[0].style.opacity = 0.5
              }
              whereInsert = 'top'
            }
            this.whereInsert = whereInsert
          }
        }
      },
      clearHoverStatus() {
        var rows = document.querySelectorAll('.tree-row');
        for(let i=0; i < rows.length; i++) {
          const row = rows[i];
          const hoverBlock = row.children[row.children.length - 1];
          hoverBlock.style.display = 'none';
          hoverBlock.children[0].style.opacity = 0.1;
          hoverBlock.children[1].style.opacity = 0.1;
          hoverBlock.children[2].style.opacity = 0.1;
        }
      },
      resetTreeData() {
        if (this.targetId === undefined) return ;
        let flag = true;
        const newList = [];
        const curList = this.data.lists;
        const parentName = [];
        const _this = this;
        // let parentName = [];
        function pushData(curList, needPushList, parentName) {
          for( let i = 0; i < curList.length; i++) {
            const item = curList[i]; // curList当前项
            parentName.push(item.name);

            var obj = _this.deepClone(item);
            obj.dataset_name = parentName.join('/');
            obj.lists = [];          // needPushList项。没有子list
            if (_this.targetId == item.id) {
              const curDragItem = _this.getCurDragItem(_this.data.lists, window.dragId);
              if (_this.whereInsert === 'top') {
                curDragItem.parent_id = item.parent_id;
                needPushList.push(curDragItem);
                needPushList.push(obj)
              } else if (_this.whereInsert === 'center'){
                if (item.directory === false) {
                  flag = false;
                  _this.$message({
                    message: "请移动文件/目录到目录下。",
                    type: "warning",
                    showClose: true,
                    duration: "2000"
                  });
                  return;
                }
                curDragItem.parent_id = item.id;
                obj.lists.push(curDragItem);
                needPushList.push(obj)
              } else {
                curDragItem.parent_id = item.parent_id;
                needPushList.push(obj);
                needPushList.push(curDragItem)
              }
            } else {
              if (window.dragId != item.id){
                needPushList.push(obj);
              }
            }
            if (item.lists && item.lists.length) {
              pushData(item.lists, obj.lists, parentName)
            }
            parentName.pop();
          }
        }
        pushData(curList, newList, parentName);
        if (flag) {
          this.resetOrder(newList);

          let preName = [];
          let srcDatasetName = '', destDatasetName = '';
          srcDatasetName = this.getDatasetName(curList, window.dragId, preName);
          preName = []; //
          destDatasetName = this.getDatasetName(newList, window.dragId, preName);

          let dataPost = JSON.stringify({
            src_path: srcDatasetName,
            dest_path: destDatasetName
          });
          axios.post(this.$api.dataMove, dataPost)
            .then(res => {
              res = res.data;
              if (res.succeed === 0) {
                this.onDrag(newList);
                this.$message({
                  message: "移动文件/文件夹成功" + res.message,
                  type: "success",
                  showClose: true,
                  duration: "1000"
                })
              } else {
                //console.log(newList);
                // console.log(window.dragId);
                this.$message({
                  message: "移动文件/文件夹失败" + res.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                })
              }
            })
            .catch(() => {});
        }
      },
      resetOrder(list) {
        for (let i = 0; i< list.length; i++) {
          list[i].order = i;
          if (list[i].lists && list[i].lists.length) {
            this.resetOrder(list[i].lists)
          }
        }
      },
      deepClone (aObject) {
        if (!aObject) {
          return aObject;
        }
        var bObject, v, k;
        bObject = Array.isArray(aObject) ? [] : {};
        for (k in aObject) {
          if (aObject.hasOwnProperty(k)) {
            v = aObject[k];
            bObject[k] = (typeof v === "object") ? this.deepClone(v) : v;
          }
        }
        return bObject;
      },
      getCurDragItem(lists, id) {
        var curItem = null;
        var _this = this;
        function getchild(curList) {
          for( let i = 0; i < curList.length; i++) {
            var item = curList[i];
            if (item.id == id) {
              curItem = JSON.parse(JSON.stringify(item));
              break
            } else if (item.lists && item.lists.length) {
              getchild(item.lists)
            }
          }
        }
        getchild(lists);
        return curItem;
      },
      getDatasetName(lists, id) { // 所在数据集名
        let preName = [];
        let datasetName = '';
        function getchild(curList, preName) {
          for (let i=0;i < curList.length;i++) {
            let item = curList[i];
            if (item.id == id) {
              if (preName.length === 0) { // root level
                datasetName = '/';
              } else {
                datasetName = preName.join('/');
              }
              datasetName = datasetName + '/' + item.name;
              console.log('datasetName:',datasetName);
              break;
            } else if (item.lists && item.lists.length) {
              preName.push(item.name);
              getchild(item.lists, preName);
              preName.pop();
            }
          }
        }
        getchild(lists, preName);
        return datasetName;
      }
    }
  }
</script>

<style lang="scss">
  .drag-tree-table{
    margin: 20px 0;
    color: #606266;
    font-size: 12px;
  }
  .drag-tree-table-header{
    display: flex;
    padding: 15px 10px;
    background: #f5f7fa;
    height: 66px;
    line-height: 36px;
    box-sizing: border-box;
    font-weight: 600;
  }
  .tree-icon-hidden{
    visibility: hidden;
  }
  .is-draging .tree-row:hover{
    background: transparent !important;
  }
</style>
