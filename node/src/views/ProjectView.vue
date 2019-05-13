<template>
  <div class="projectView">
    <el-table :data="tableData"
              class="el-table-graph-detail"
              style="width: 100%"
              :cell-style="cellStyle"
              :header-cell-style="headerCellStyle"
              :default-sort = "{prop: 'date', order: 'descending'}">
      <el-table-column prop="name"
                       label="项目名"
                       sortable
                       width="180">
      </el-table-column>
      <el-table-column prop="date"
                       label="创建时间"
                       sortable
                       width="180">
      </el-table-column>
      <el-table-column>
        <template slot-scope="scope">
          <el-button size="mini"
                     type="primary"
                     @click="projectRename(scope.$index, scope.row)"
          >重命名</el-button>
          <el-button size="mini"
                     type="danger"
                     @click="projectDelete(scope.$index, scope.row)"
          >删除</el-button>
          <el-button size="mini"
                     @click="projectEnter(scope.$index, scope.row)"
          >进入项目</el-button>
        </template>
      </el-table-column>
    </el-table>

    <br />
    <el-button type="primary"
               icon="el-icon-circle-plus-outline"
               @click="projectCreate">
      创建新项目
    </el-button>
  </div>
</template>


<script>
  import * as axios from "axios";

  export default {
      name: "projectView",
      data () {
        return {
          tableData: []
        }
      },
      created() {
        this.projectView();
      },
      methods: {
// ====================================================== project ======================================================
        projectView() {
          axios.post(this.$api.projectView)
            .then(res => {
              res = res.data;
              if (res.succeed === 0) {
                let dataTemple = [];
                for (let key in res) {
                  if (res.hasOwnProperty(key) && (key !== 'succeed' && key !== 'message')) {
                    let obj = {};
                    obj.date = res[key].create_time;
                    obj.name = res[key].project_name;
                    obj.id = res[key].project_id;
                    dataTemple.push(obj);
                  }
                }
                this.tableData = dataTemple;
              } else {
                this.$message({
                  message: "获取项目列表失败！" + res.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                })
              }
            })
            .catch(err => {});
        },

        projectEnter (index, row) {
          this.$router.push({name:"projectDetail", params: {project_id: row.id}});
        },

        projectRename (index, row) {
          this.$prompt('请输入数据集名称', '重命名', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputValue: row.name
          }).then(({ value }) => {
            let postData = JSON.stringify({ // JSON格式，另 qs.stringify (xxx&xxx格式)
              project_id: row.id,
              project_name: value
            });
            axios.post(this.$api.projectRename, postData)
              .then(res => {
                if (res.data.succeed === 0) { // 重命名成功
                  this.$message({
                    message: res.data.message,
                    type: "success",
                    showClose: true,
                    duration: "1000"
                  });
                  this.projectView();
                } else {
                  this.$message({
                    message: "重命名失败！" + res.data.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  })
                }
              })
              .catch(err => {});
          }).catch(() => {});
        },

        projectDelete (index, row) {
          this.$confirm('确认删除文件，是否继续？','提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning' // success error info warning
          }).then(() => {
            let postData = JSON.stringify({
              project_id: row.id
            });
            axios.post(this.$api.projectDelete, postData)
              .then(res => {
                if (res.data.succeed === 0) { // delete successfully
                  this.$message({
                    message: res.data.message,
                    type: "success",
                    showClose: true,
                    duration: "1000"
                  });
                  this.projectView();
                } else {
                  this.$message({
                    message: res.data.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  })
                }
              })
              .catch(err => {});
          }).catch(() => {})
        },

        getDefaultFileName() {
          let date = new Date();
          return date.getFullYear().toString()
            + '-' + (date.getMonth() + 1).toString()
            + '-' + date.getDate().toString()
            + '-' + date.getHours().toString()
            + ':' + date.getMinutes().toString()
            + ':' + date.getSeconds().toString();
        },

        projectCreate() {
          let name = this.getDefaultFileName();
          let dataPost = JSON.stringify({
            project_name: name
          });

          axios.post(this.$api.projectCreate, dataPost)
            .then(res => {
              if (res.data.succeed === 0) {
                this.projectView();
                // route
                // this.$router.push({path:"/index/graphNew", params: {project_id: id}});
              } else {
                this.$message({
                  message: "创建项目失败！" + res.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                })
              }
            })
            .catch(err => {});
        },

// ==================================================== table style ====================================================
        cellStyle() {
          return "text-align:center"
        },

        headerCellStyle({row, column, rowIndex, columnIndex}) {
          return "text-align:center"
        }
      }
    }
</script>

<style scoped>

  .projectView {
    padding-left: 5%;
    padding-right: 5%;
    text-align: center;
  }

  .el-table-graph-detail {
    margin: 30px auto 0;
    width: 80%;
    text-align: center;
  }

</style>
