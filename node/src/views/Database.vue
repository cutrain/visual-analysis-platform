<template>
  <div class="database">
    <!-- 可拖动表格，即包含移动操作 -->
    <dragTreeTable :data="treeData" :onDrag="onTreeDataChange"></dragTreeTable>
    <p id="textAddFolder">
      {{textAddFolder}}
      <el-button type="primary" size="mini" @click="FolderRootAdd" circle>
        <svg class="icon" aria-hidden="true">
          <use xlink:href="#icon-biaoshilei_tianjiawenjianjia"></use>
        </svg>
      </el-button>
    </p>
    <br />
    <!-- 不可拖动表格 -->
    <!--
     <el-table
      :data="tableData"
      style="width: 100%"
      align="center"
      :default-sort = "{prop: 'date', order: 'descending'}">
      <el-table-column
        prop="dataset_name"
        label="所属数据集"
        sortable>
      </el-table-column>
      <el-table-column
        prop="file_name"
        label="文件名"
        sortable>
      </el-table-column>
      <el-table-column
        prop="file_size"
        label="文件大小(单位：字节)"
        sortable>
      </el-table-column>
      <el-table-column>
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="info"
            @click="fileGet(scope.$index, scope.row)">查看</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fileOrFolderDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
     -->
    <br />
    <div align="left"><h2>导入数据</h2></div>
    <!--:show-file-list="false"-->
    <el-upload
      class="upload-data"
      drag
      action="https://jsonplaceholder.typicode.com/posts/"
      :on-success="uploadSuccess"
      :on-error="uploadError"
      :http-request="fileUpload"
      :before-remove="beforeRemove"
      accept="image/jpeg,image/png,image/jpg,.csv"

      multiple>
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">
        <p>上传格式包括string, dataframe, image</p>
        <p>上传前请先选择 <el-button type="primary" size="mini" @click="handleselectDataset()">目录</el-button>，已选中目录： {{selectDataset}}</p>
      </div>

    </el-upload>
    <!--
     <el-upload
      class="upload-data-manual"
      ref="upload"
      action="https://jsonplaceholder.typicode.com/posts/"
      :http-request="fileUpload"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :file-list="fileList"
      :auto-upload="false">
      <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
      <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
      <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>
     -->

    <!-- 操作:查看 -->
    <el-dialog title="文件详情" :visible.sync="dialogTableVisible">
      <el-table :data="gridData" :visible.sync="DataFrameVisible">
        <el-table-column v-for="(item, index) in col_index"
                         :label="item"
                         :prop="item"
                         sortable
                         :key="index">
        </el-table-column>
      </el-table>
      <div :visible.sync="StringVisible">{{stringGet}}</div>
      <div :visible.sync="ImageVisible">
        <img :src=returnSrc()  alt=""/>
      </div>
    </el-dialog>
    <br/>
    <!-- 上传:选择目录 -->
    <el-dialog title="选择上传目录" :visible.sync="dialogTableUploadVisible">
      <dragTreeTable :data="treeDataUpload" :onDrag="onTreeDataUploadChange" v-bind:isdraggable="false"></dragTreeTable>
      <p>选择上述目录，或选择 <el-button size="mini" @click="selectDatasetInDialog = '/'">根目录</el-button></p>
      <p>已选中目录：{{selectDatasetInDialog}}</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogTableUploadVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleHasSelected">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import * as axios from "axios";
  import dragTreeTable from "../components/dragTreeTable";

  export default {

    name: "database",
    components: {
      dragTreeTable
    },
    data () {
      return {
        tableData: [],              // dataset_name 数据集名（即目录） file_name 文件名 file_size 文件大小
        sum: 1,                     // 节点总数。无父节点，填0，故需从1开始编号
        levelNum: [],               // 每层节点总数，从0开始(0,1,2,...)
        gridData:  [],              // "查看"弹出对话框
        col_num: 0,                 // DataFrame类型返回参数
        col_index: [],
        col_type: [],
        row_num: 0,
        imageUrl: '',               // Image类型返回参数
        stringGet: '',              // String类型返回参数
        dialogTableVisible: false,
        DataFrameVisible: false,
        StringVisible: false,
        ImageVisible: false,
        dialogTableUploadVisible: false,
        dragId: '',
        selectDataset: '/',         // 上传：选择目录，即选中的数据集
        selectDatasetInDialog: '/',
        fileList: [],               // 上传序列
        // state
        treeData: {
          lists: [],
          columns: [{
            type: 'selection',
            title: '目录/文件名',
            field: 'name',
            align: 'left',
            flex: 1,
            formatter: (item) => {
              return '<a>'+item.name+'</a>'
            }
          }, {
            title: '文件大小(单位：字节)',
            field: 'file_size',
            align: 'center',
            flex: 1,
          }, {
            title: '操作(拖动可移动文件/目录)',
            type: 'action',
            flex: 1,
            align: 'right',
            actions: [{
              text: '添加',
              onclick: this.folderAdd,
              formatter: (item) => {
                return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-biaoshilei_tianjiawenjianjia"></use></svg>'+'添加    </i>'
              }
            }, {
              text: '查看',
              onclick: this.fileGet,
              formatter: (item) => {
                return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-chakan"></use></svg>'+'查看    </i>'
              }
            }, {
              text: '编辑',
              onclick: this.fileOrFolderDelete,
              formatter: (item) => {
                return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-shanchu1"></use></svg>'+'删除 </i>'
              }
            }]
          },
          ],
        },
        treeDataUpload: {
          radio: 0,
          lists: [],
          columns: [{
            type: 'selection',
            title: '文件夹',
            field: 'name',
            align: 'left',
            flex: 1,
            formatter: (item) => {
              return '<a>'+item.name+'</a>'
            }
          },{
            title: '',
            type: 'action',
            flex: 1,
            align: 'center',
            actions: [{
              text: '选择',
              onclick: this.folderUploadSelect,
              formatter: (item) => {
                return '<i>选择 </i>'
              }
            }]
          },
          ],
        },
        textAddFolder: '在根目录中新增文件夹'
      }
    },
    created() {
      // this.dataView();
      this.dragableDataView();
      this.folderView();
    },
    methods: {
     /*
      * view
      * */
      isNumber(obj) {
        return (typeof obj === 'number');
      },
      
      dataInsertByParentId(dataList) {
        let point = dataList.length - 1;
        if (point === -1) {
          console.log('dataList读取失败,查看dataViewTransformDragable()');
        }
        while (point !== -1) {
          let pro_point = point - 1;
          let parent = dataList[point].parent_id;
          if (parent !== 0) {
            while(dataList[pro_point].id !== parent) {
              if (pro_point !== -1) {
                pro_point--;
              } else {
                break;
              }
            }
            if (pro_point !== -1) {
              if (dataList[pro_point].id === parent) {
                dataList[pro_point].lists.push(dataList[point]);
              }
            }
          }
          point--;
        }
      },

      dataListDeleteExceptRootLevel(dataList, newDataList) {
        for (let i=0;i<dataList.length;i++) {
          if (dataList[i].parent_id === 0) { // 保留级别最高的节点
            newDataList.push(dataList[i]);
          }
        }
      },

      folderView() { // 上传：选择需要上传的目录
        let dataTemple = [];
        const _this = this;

        function transform(obj, dataList, preId, preName) { // 上传

          for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
              if (!_this.isNumber(obj[key])) { // 文件夹
                let data = {};
                data.id = _this.sum;
                _this.sum++;
                if (preId.length === 0) {
                  data.parent_id = 0;
                } else {
                  data.parent_id = preId[preId.length-1]; // 最后一个
                }
                preId.push(data.id);
                data.name = key;
                data.open = true;
                data.directory = true;
                data.lists = [];
                //levelNum
                let len = _this.levelNum.length;
                if (len === 0) {
                  _this.levelNum.push(0);
                } else {
                  if(len === preId.length) {
                    _this.levelNum[len-1]++;
                  } else { // len < preId.length
                    _this.levelNum.push(0);
                  }
                }
                data.order = _this.levelNum[_this.levelNum.length-1];
                data.dataset_name = preName.join('/');
                dataList.push(data);
                preName.push(key);
                transform(obj[key], dataList, preId, preName);
                preId.pop();
                preName.pop();
              }
            }
          }
        }

        axios.post(this.$api.dataView)
          .then(res => {
            let structure = res.data.structure;
            structure = JSON.parse(structure);
            if (typeof structure === 'object' && typeof structure !== 'number') { // object对象
              let preId = [], preName = [];
              transform(structure, dataTemple, preId, preName);
            }
            this.dataInsertByParentId(dataTemple);
            let newDataTemple = [];
            this.dataListDeleteExceptRootLevel(dataTemple, newDataTemple);
            this.onTreeDataUploadChange(newDataTemple);
          })
          .catch(err => {});
      },

      dataView() {
        let dataTemple = [];
        const _this = this;

        function dataViewTransform(obj, dataList, preName) {
          for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
              if (_this.isNumber(obj[key])) { // 判断为文件
                let data = {};
                data.dataset_name = preName.join('/');
                data.file_name = key;
                data.file_size = obj[key];
                dataList.push(data);
              } else {
                preName.push(key);
                dataViewTransform(obj[key], dataList, preName);
                preName.pop();
              }
            }
          }
        }

        axios.post(this.$api.dataView)
          .then(res => {
            let structure = res.data.structure;
            structure = JSON.parse(structure);
            if (typeof structure === 'object' && typeof structure !== 'number') { // object对象
              let preName = [];
              dataViewTransform(structure, dataTemple, preName);
              // console.log(dataTemple);
              /*for (let key in structure) {
                if (structure.hasOwnProperty(key)) {
                  console.log(key);
                  console.log(structure[key]);
                  let obj = structure[key];
                  for (let i in obj) {
                    if (obj.hasOwnProperty(i)) {
                      console.log(i);
                      console.log(obj[i]);
                      if(typeof obj[i] ===  'number') {
                        console.log('yes');
                      }
                    }
                  }
                }
              }*/
            }
            let dataT = [];
            let len = dataTemple.length;
            for (let i = 0; i < len; i++) {
              var obj = {};
              obj.dataset_name = dataTemple[i].dataset_name;
              obj.file_name = dataTemple[i].file_name;
              obj.file_size = dataTemple[i].file_size;
              dataT[i] = obj;
            }
            this.tableData = dataT;
          })
          .catch(err => {});
      },

      dragableDataView() {
        const _this = this;

        function dataViewTransformDragable(obj, dataList, preId, preName) { // 用于可拖拽
          let num = 0;
          for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
              if (_this.isNumber(obj[key])) { // 判断为文件
                let data = {};
                data.id = _this.sum;
                _this.sum++;
                data.parent_id = preId[preId.length-1];
                data.name = key;
                data.file_size = obj[key];
                data.open = false;
                data.directory = false; // 文件为false, 目录为true
                data.lists = [];
                data.order = num;
                num++;
                data.dataset_name = preName.join('/');
                dataList.push(data);
              }
              else {
                let data = {};
                data.id = _this.sum;
                _this.sum++;
                if (preId.length === 0) {
                  data.parent_id = 0;
                } else {
                  data.parent_id = preId[preId.length-1]; // 最后一个
                }
                preId.push(data.id);
                data.name = key;
                data.open = false;
                data.directory = true;
                data.lists = [];
                //levelNum
                let len = _this.levelNum.length;
                if (len === 0) {
                  _this.levelNum.push(0);
                } else {
                  if(len === preId.length) {
                    _this.levelNum[len-1]++;
                  } else { // len < preId.length
                    _this.levelNum.push(0);
                  }
                }
                data.order = _this.levelNum[_this.levelNum.length-1];
                data.dataset_name = preName.join('/');
                dataList.push(data);
                preName.push(key);
                dataViewTransformDragable(obj[key], dataList, preId, preName);
                preId.pop();
                preName.pop();
              }
            }
          }
        }

        axios.post(this.$api.dataView)
          .then(res => {
            let dataTemple = [];
            let structure = res.data.structure;
            structure = JSON.parse(structure);

            if (typeof structure === 'object' && typeof structure !== 'number') { // object对象
              let preId = [], preName = [];
              dataViewTransformDragable(structure, dataTemple, preId, preName);
              // console.log(dataTemple);
            }
            this.dataInsertByParentId(dataTemple);
            // this.treeData.lists = dataTemple;
            let newDataTemple = [];
            this.dataListDeleteExceptRootLevel(dataTemple,newDataTemple);
            this.onTreeDataChange(newDataTemple);
            // console.log(newDataTemple)
          })
          .catch(err => {});
      },

     /*
      * data manage
      * */
      onTreeDataChange(list) {
        this.treeData.lists = list
      },
      // todo
      folderAdd(item) { // 向该文件夹中，添加新文件夹//  弹框获取文件夹名 -> axios -> success: treeTable更新//                           -> failure
        function getCurrentTimeString() {
          let date = new Date();
          return date.getFullYear().toString()
            + '-' + (date.getMonth() + 1).toString()
            + '-' + date.getDate().toString()
            + '-' + date.getHours().toString()
            + ':' + date.getMinutes().toString()
            + ':' + date.getSeconds().toString();
        }

        let newFolderNameDefault = getCurrentTimeString();
        let newFolderName = newFolderNameDefault;

        this.$prompt('请输入文件夹名', '命名', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputValue: newFolderNameDefault
        })
          .then(({ value }) => {
            newFolderName = value;
            let dataset = '';
            if (item.dataset_name === '') {
              dataset = value;
            } else {
              dataset = item.dataset_name + '/' + value;
            }

            let dataPost = JSON.stringify({
              dataset: dataset,
              file: ''
            });
            axios.post(this.$api.dataUpload, dataPost)
              .then(res => {
                res = JSON.parse(res);
                res = res.data;
                if (res.succeed === 0) {
                  // todo 更新table

                  let data = {};
                  data.id = this.sum;
                  this.sum++;
                  if (preId.length === 0) {
                    data.parent_id = 0;
                  } else {
                    data.parent_id = preId[preId.length-1]; // 最后一个
                  }
                  preId.push(data.id);
                  data.name = key;
                  data.open = true;
                  data.directory = true;
                  data.lists = [];
                  //levelNum
                  let len = this.levelNum.length;
                  if (len === 0) {
                    this.levelNum.push(0);
                  } else {
                    if(len === preId.length) {
                      this.levelNum[len-1]++;
                    } else { // len < preId.length
                      this.levelNum.push(0);
                    }
                  }
                  data.order = this.levelNum[this.levelNum.length-1];
                  data.dataset_name = preName.join('/');

                  this.resetTreeData(this.treeData.lists);
                  console.log('treeData update succeed.');
                  this.resetTreeData(this.treeDataUpload.lists);
                  console.log('treeDataUpload update succeed.');
                  this.$message({
                    type: 'success',
                    message: '创建文件夹: ' + value
                  });
                } else {
                  this.$message({
                    message: "创建文件夹失败！" + res.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  })
                }
              })
              .catch(err => {})
          }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },

      FolderRootAdd() {
        // todo folderAdd()修改
      },

      resetTreeData(curList) {
        let flag = true;
        const newList = [];
        const parentName = [];
        const _this = this;

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
        function resetOrder(list) {
          for (let i = 0; i< list.length; i++) {
            list[i].order = i;
            if (list[i].lists && list[i].lists.length) {
              this.resetOrder(list[i].lists)
            }
          }
        }
        pushData(curList, newList, parentName);
        if (flag) {
          resetOrder(newList);
        }
      },

      getDatasetName(obj) {
        let datasetName = '';
        if (obj.dataset_name === '') { // 不属于任何数据集，'/'
          datasetName = '/';
        } else {
          datasetName = obj.dataset_name;
        }
        return datasetName;
      },

      // image png
      fileGet (item) { // 查看
        let datasetName = this.getDatasetName(item);

        let dataPost = JSON.stringify({
          dataset: datasetName,
          name: item.name
        });

        axios.post(this.$api.dataGet, dataPost)
          .then(res => {
            res = res.data;

            if (res.succeed === 0) {
              this.dialogTableVisible = true; // 显示对话框
              console.log(res.type);
              switch (res.type) {
                case 'DataFrame':
                  this.DataFrameVisible = true;
                  /*this.col_num = res.data.col_num + 1;
                  this.row_num = res.data.row_num;
                  this.col_index = res.data.col_index;
                  this.col_index.splice(0, 0, 'index');
                  this.col_type = res.data.col_type;
                  let dataTemple = [];
                  let num = 1;
                  for (let i=0;i < this.row_num; ++i) {
                    let obj = {};
                    obj.index = num++;
                    for (let j=1;j < this.col_num; ++j) {
                      let key = this.col_index[j];
                      obj[key] = res.data.data[i][j-1];
                    }
                    dataTemple[i] = obj;
                  }*/
                  this.col_num = res.data.col_num;
                  this.row_num = res.data.row_num;
                  this.col_index = res.data.col_index;
                  this.col_type = res.data.col_type;
                  let dataTemple = [];
                  let num = 1;
                  for (let i=0;i<this.row_num;i++) {
                    let obj = {};
                    obj.index = num++;
                    for (let j=0;j<this.col_num;j++) {
                      let key = this.col_index[j];
                      obj[key] = res.data.data[i][j];
                    }
                    dataTemple.push(obj);
                  }
                  this.gridData = dataTemple;
                  break;
                case 'String':
                  this.StringVisible = true;
                  this.stringGet = res.data;
                  break;
                case 'Image':
                  this.ImageVisible = true;
                  this.imageUrl = res.data;
                  break;
                default:
                  this.$message({
                    message: "返回数据类型异常！" + res.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  });
              }
            }
            else {
              this.$message({
                message: "请求失败！" + res.message,
                type: "error",
                showClose: true,
                duration: "2000"
              })
            }
          })
          .catch(() => {});
      },
      // TODO: fix delete bug. error path
      fileOrFolderDelete(item) { // 删除
        this.$confirm('确认删除数据，是否继续？','提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning' // success error info warning
        }).then(() => {
          let datasetName = this.getDatasetName(item);
          let postData = JSON.stringify({
            dataset: datasetName,
            name: item.name
          });
          console.log(postData);
          axios.post(this.$api.dataDelete, postData)
            .then(res => {
              res = JSON.parse(res);
              console.log(res);
              if (res.data.succeed === 0) { // 删除项目成功
                this.$message({
                  message: res.data.message,
                  type: "success",
                  showClose: true,
                  duration: "1000"
                });
                this.dragableDataView();
              } else {
                this.$message({
                  message: res.data.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                })
              }
            })
            .catch(err => {
              console.log(err.message);
            });
        }).catch(() => {})
      },
      
      returnSrc() {
        return this.imageUrl;
      },

     /*
      * data upload
      * */
      onTreeDataUploadChange(list) {
        this.treeDataUpload.lists = list
      },

      fileUpload(param) { // 上传操作：覆盖el-upload action//  多文件上传
        console.log(param.file);
        let name = '';
        if (this.selectDataset === '/') { // 不属于任何数据集，'/'
          name = param.file.name;
        } else {
          name = this.selectDataset + '/' + param.file.name;
        }

        let formDataPost = new FormData();
        formDataPost.append('file',param.file);
        formDataPost.append('dataset',name);
        console.log(formDataPost.getAll('dataset'));

        /*let dataPost = JSON.stringify({
          dataset: '',
          file: param.file
        });*/

        axios.post(this.$api.dataUpload, formDataPost, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
          .then(res => {
            res = res.data;
            res = JSON.parse(res);
            if (res.succeed === 0) {
              this.$message({
                message: "上传成功！" + res.message,
                type: "success",
                showClose: true,
                duration: "1000"
              });
              this.dragableDataView();
            } else {
              this.$message({
                message: "上传失败！" + res.message,
                type: "error",
                showClose: true,
                duration: "2000"
              })
              console.log(res.message);
            }
          })
          .catch(() => {});
      },

      handleHasSelected() {
        this.selectDataset = this.selectDatasetInDialog;
        this.dialogTableUploadVisible = false;
      },

      handleselectDataset() {
        this.dialogTableUploadVisible = true;
        this.selectDatasetInDialog = this.selectDataset;
        this.folderView(); // 显示“选择目录对话框”时(即dialogTableUploadVisible为true)，刷新目录
      },

      folderUploadSelect(item) { // Dialog
        let datasetName = '';
        if (item.dataset_name === '') {
          datasetName = item.name;
        } else {
          datasetName = item.dataset_name + '/'+item.name;
        }
        this.selectDatasetInDialog = datasetName;
        console.log(datasetName);
      },

      uploadSuccess() {
        // console.log('上传成功');
      },

      uploadError() {
        // console.log('上传失败');
      },

      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },

      handleRemove() {
        console.log('handleRemove.');
      },

      handlePreview(file) {
        console.log('handlePreview.');
      },

      submitUpload() {
        // this.$refs.upload.submit();
        console.log('submitUpload.');
      },

      getFullName(obj) { // 上传步骤：获取上传文件的全名，即包括所在的数据集名
        let name = '';
        if (this.selectDataset === '/') { // 不属于任何数据集，'/'
          name = obj.name;
        } else {
          name = this.selectDataset + '/' + obj.name;
        }
        return name;
      },

    }
  }
</script>

<style scoped>
  .database {
    margin: 30px auto 0;
    width: 80%;
    text-align: center;
  }

  #textAddFolder {
    font-size: 12px;
    color: #606266;
  }
</style>
