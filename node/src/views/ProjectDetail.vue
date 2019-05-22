<template>
  <div class="projectDetail" id="graph">

    <nav class="primnav"
         id="navi">
      <el-scrollbar id="scrollBar"
                    view-class="view-box"
                    view-style="font-weight: bold;"
                    :native="false">
        <component-draggable
          v-for="(item, index) in component_items"
          :id="item.name"
          :model="item"
          :drag_data="drag_data"
          :node_items="node_items"
          :key="index"
          depth="20"
          padding="0"
          :draggable="item.isdraggable">
        </component-draggable>
      </el-scrollbar>
    </nav>
    <div class="main-scope">

      <div class="canvas"
           @dragover="canvas_dragover($event)"
           @dragenter="canvas_dragenter($event)"
           @drop="canvas_drop($event)">

        <img id="bg" src="../assets/bg.png" alt="" draggable="false">

        <svg id="svg"
             width="100%"
             height="100%"
             version="1.1"
             xmlns="http://www.w3.org/2000/svg"
             style="position:absolute;top:0;left:0;"
        ><!-- pointer-events: none;-->
          <!--<line class="line"
                v-for="(item, index) in line_items"
                :id="item.id"
                :key="index"
                :x1="item.x1"
                :y1="item.y1"
                :x2="item.x2"
                :y2="item.y2"
          >
          </line>-->
        </svg>

        <el-scrollbar id="scrollBar-dragResize"
                      wrap-class="list-dragResize"
                      view-class="view-box"
                      view-style="font-weight: bold;"
                      :native="false">

        </el-scrollbar>

        <node v-for="(item, index) in node_items"
              :style="{top:item.posiY+'px', left:item.posiX+'px'}"
              v-if=item.node_id
              :id=item.node_id
              :drag_data="drag_data"
              :type_detail="type_detail"
              :G="G"
              :project_id="project_id"
              :show_detail_box="show_detail_box"
              :show_data_box="show_data_box"
              :show_button_lists.sync="show_button_lists"
              :node="item"
              :select_id="curr_id"
              ref="noderef"
              v-bind:curr_id.sync="curr_id"
              v-bind:G.sync="G"
              v-bind:node_show_button_lists.sync="node_show_button_lists"
              v-bind:node_show_detail_box.sync="node_show_detail_box"
              v-bind:node_show_data_box.sync="node_show_data_box"
              v-bind:tableInBorder.sync="tableInBorder"
              v-bind:imageInBorder.sync="imageInBorder"
              v-bind:stringInBorder.sync="stringInBorder"
              v-bind:addressInBorder.sync="addressInBorder"
              v-bind:dataTypeInBorder.sync="dataTypeInBorder"
              :key="index"
        ></node>

        <div id="button_lists" class="button-lists" >
          <div id="button-save">
            <el-button class="bubbly-button-save" type="text" @click="save_button()">
              <svg class="icon" aria-hidden="true">
                <use xlink:href="#icon-baocunwendang"></use>
              </svg>
              保存</el-button>
          </div>
          <div id="button-cancel">
            <el-button class="bubbly-button-cancel" type="text" @click="load_button()">
              <svg class="icon" aria-hidden="true">
                <use xlink:href="#icon-shuaxin"></use>
              </svg>
              重载</el-button>
          </div>
          <div id="button-run" v-show="finished">
            <el-button class="bubbly-button" type="text" icon="el-icon-caret-right" @click="run_button()">运行全部</el-button>
          </div>
          <div id="button-run-inactive" v-show="!finished">
            <el-button class="bubbly-button" type="text" icon="el-icon-caret-right" disabled="disabled">运行全部</el-button>
          </div>
          <div id="button-stop" v-show="!finished">
            <el-button class="bubbly-button-stop" type="text"  @click="stop_button()">
              <svg class="icon" aria-hidden="true"><use xlink:href="#icon-tingzhi"></use></svg>
              停止</el-button>
          </div>
          <div id="button-stop-inactive" v-show="finished">
            <el-button class="bubbly-button-stop" type="text" disabled>
              <svg class="icon" aria-hidden="true"><use xlink:href="#icon-tingzhi"></use></svg>
              停止</el-button>
          </div>
          <div id="button-clear">
            <el-button class="bubbly-button-clear" type="text"  @click="clear_button()">
              <svg class="icon" aria-hidden="true">
                <use xlink:href="#icon-qingkonghuancun"></use>
              </svg>
              清空</el-button>
          </div>
          <div id="button-delete" v-show="curr_id !== null">
            <el-button class="bubbly-button-delete" type="text" icon="el-icon-delete" @click="delete_button()">删除节点</el-button>
          </div>
          <div id="button-run-single" v-show="curr_id !== null">
            <el-button class="bubbly-button-run-single" type="text" icon="el-icon-caret-right" @click="run_single_button()">运行单个</el-button>
          </div>
        </div>

        <!--  v-show="!finished" -->
        <div id="nodes_running_states">
          <ul id="states_list">
            <li>
              <el-button type="text">
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-none-running"></use>
                </svg>未运行
              </el-button>
            </li>
            <li>
              <el-button type="text">
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-running"></use>
                </svg>运行中
              </el-button>
            </li>
            <li>
              <el-button type="text">
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-waiting"></use>
                </svg>等待
              </el-button>
            </li>
            <li>
              <el-button type="text">
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-failed"></use>
                </svg>失败
              </el-button>
            </li>
            <li>
              <el-button type="text">
                <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-finished"></use>
                </svg>完成
              </el-button>
            </li>
          </ul>
        </div>
      </div>

      <div class="detail-bound">
        <el-scrollbar view-class="view-box" :native="false" style="height: 100%;">
          <div :class="node_show_detail_box ? 'detail-view' : 'none-detail-view'"
               id="detail-box">
            <param-border v-for="(item, index) in border_items"
                          :key="item.order"
                          :border="item"
                          :class="item.class"
                          :curr_id="curr_id"
                          :props_list="props_list"
                          :back_flag="back_flag"
                          v-bind:param_list.sync="param_list[index]"
                          v-bind:last_lists.sync="last_lists[index]"
                          v-bind:fileSelectVisible.sync="fileSelectVisible"
                          v-bind:modelSelectVisible.sync="modelSelectVisible"
                          v-bind:dialogUploadVisible.sync="dialogUploadVisible"
                          v-bind:msgFileName="msgFileName"
                          v-bind:msgModelName="msgModelName"
                          v-bind:msgUploadName="msgUploadName"
                          ref="refborder"
                          :style="{order:item.order}"
            ></param-border>
          </div>
          <div :class="node_show_data_box? 'data-view' : 'none-data-view'"
               id="data-box">
            <div class='detail-top'>数据</div>
            <el-table :data="tableInBorder.data"
                      style="width: 100%"
                      v-if="dataTypeInBorder === 'DataFrame'">
              <el-table-column v-for="(item, index) in tableInBorder.title"
                               :key="index"
                               :prop="item"
                               :label="item"
                               width="150"
              ></el-table-column>
            </el-table>
            <div v-else-if="dataTypeInBorder === 'String'">{{stringInBorder}}</div>
            <div v-else-if="dataTypeInBorder === 'Image'">
              <p>{{imageInBorder.shape}}</p>
              <el-scrollbar view-class="view-box" :native="false" style="height: 100%;">
                <img :src="server+imageInBorder.url"/>
              </el-scrollbar>
            </div>
            <div v-else-if="dataTypeInBorder === 'Address'">{{addressInBorder}}</div>
          </div>
        </el-scrollbar>
      </div>
    </div>

    <svg style="position: absolute; width: 0; height: 0;" width="0" height="0" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <defs>
        <symbol id="icon-th-large" viewBox="0 0 30 32">
          <title>th-large</title>
          <path class="path1" d="M13.714 18.286v6.857c0 1.25-1.036 2.286-2.286 2.286h-9.143c-1.25 0-2.286-1.036-2.286-2.286v-6.857c0-1.25 1.036-2.286 2.286-2.286h9.143c1.25 0 2.286 1.036 2.286 2.286zM13.714 4.571v6.857c0 1.25-1.036 2.286-2.286 2.286h-9.143c-1.25 0-2.286-1.036-2.286-2.286v-6.857c0-1.25 1.036-2.286 2.286-2.286h9.143c1.25 0 2.286 1.036 2.286 2.286zM29.714 18.286v6.857c0 1.25-1.036 2.286-2.286 2.286h-9.143c-1.25 0-2.286-1.036-2.286-2.286v-6.857c0-1.25 1.036-2.286 2.286-2.286h9.143c1.25 0 2.286 1.036 2.286 2.286zM29.714 4.571v6.857c0 1.25-1.036 2.286-2.286 2.286h-9.143c-1.25 0-2.286-1.036-2.286-2.286v-6.857c0-1.25 1.036-2.286 2.286-2.286h9.143c1.25 0 2.286 1.036 2.286 2.286z"></path>
        </symbol>
        <symbol id="icon-other" viewBox="0 0 1000 1000">
          <title>other</title>
          <path class="path1" d="M500,10C229.4,10,10,229.4,10,500c0,270.6,219.4,490,490,490c270.6,0,490-219.4,490-490C990,229.4,770.6,10,500,10z M223,581.9c-39.6,0-71.7-32.1-71.7-71.7c0-39.6,32.1-71.7,71.7-71.7s71.7,32.1,71.7,71.7C294.9,549.8,262.8,581.9,223,581.9z M500,581.9c-39.6,0-71.7-32.1-71.7-71.7c0-39.6,32.1-71.7,71.7-71.7s71.7,32.1,71.7,71.7C571.7,549.8,539.6,581.9,500,581.9z M777,581.9c-39.6,0-71.7-32.1-71.7-71.7c0-39.6,32.1-71.7,71.7-71.7s71.7,32.1,71.7,71.7C848.7,549.8,816.6,581.9,777,581.9z"></path>
        </symbol>
        <symbol id="icon-data" viewBox="0 0 1000 1000">
          <title>data</title>
          <path d="M10,98.8v802.5c0,21.8,17.7,39.5,39.5,39.5h900.9c21.8,0,39.5-17.7,39.5-39.5c0-21.8-17.7-39.5-39.5-39.5H89.1V98.8c0-21.8-17.7-39.5-39.5-39.5C27.7,59.2,10,76.9,10,98.8z"></path><path d="M937,645.7v148.8H763.1V645.7c0-20.6,16.7-37.3,37.3-37.3h99.2C920.3,608.3,937,625.1,937,645.7z"/><path d="M519.7,116.4v678.1H345.7V116.4c0-20.6,16.7-37.4,37.4-37.4h99.2C502.9,79,519.7,95.7,519.7,116.4z"/><path d="M311,336.2v458.3H137V336.2c0-20.6,16.7-37.4,37.4-37.4h99.2C294.3,298.9,311,315.6,311,336.2z"/><path d="M728.3,398.4v396.1H554.4V398.4c0-20.6,16.7-37.4,37.4-37.4H691C711.6,361.1,728.3,377.8,728.3,398.4z"/>
        </symbol>
        <symbol id="icon-algorithm" viewBox="0 0 1000 1000">
          <title>algorithm</title>
          <path d="M835.2,680.6c-37.3,0-71.6,13.2-98.4,35.2l0.2-0.5c0,0-50.2,51.5-130.4,33.6l-240.4-64.4c-49.4-17.9-70.8-53.4-78.7-71.1c-5.5-17.8-14.2-34-25.7-48.1h0.2c0,0-43.9-50.7-26.9-123.6l37.3-139.4c14.1-42.6,45.6-59.5,61.6-67.6c22.6-8.4,41.9-23.7,55.2-43.3c9.7-11.8,35.9-37.2,82.3-39.6h216.9c35.4,2.9,56.1,25.7,62.6,34c0.4,0.6,0.9,1.2,1.2,1.8l0,0c0,0,26.8,36.1,15.5,78l0,0l-23.4,87.7c-0.2,0.7-0.5,1.4-0.7,2.3c-9.3,34.9-29.7,52-41.2,59.1c-15.5,5.4-29.2,14.9-39.6,27.3c-0.1,0.1-0.3,0.3-0.5,0.5c-3.2,4-6.3,8.3-8.8,12.7c-17.2,18.4-44.3,18.9-46.2,18.9h-0.1h-3.6c-7.6-0.4-26-3.3-42.8-21.6c-0.6-0.9-1.3-1.7-1.9-2.5c-10.2-14.4-10.2-28.3-9.1-36.2l2.3-8.5c2-5,8.5-18.6,22.1-25.5c24.3-9.3,41.7-32.8,41.7-60.3c0-35.7-28.8-64.5-64.5-64.5c-35.6,0-64.5,28.8-64.5,64.5c0,12.2,3.4,23.4,9.2,33.2c8.3,24,5.4,42.3,5.4,42.3s0,0.1-0.1,0.2l-1.7,6.5c-2.7,6.8-9.6,17.1-27.1,25.8c-29.3,11.1-50.2,39.3-50.2,72.4c0,42.7,34.6,77.4,77.4,77.4c25,0,47.2-11.8,61.3-30c22.3-20.9,43.9-21.6,43.9-21.6h7.7c10.1,0.8,28.4,4.9,43.4,23.2c16.2,24.9,44,41.3,75.8,41.3c49.8,0,90.3-40.4,90.3-90.3c0-21.6-7.6-41.4-20.1-57c-6.4-13.7-17-41.4-10.1-67.5c0.4-1.3,0.6-2.6,0.9-4l23.8-89c12.6-37.5,45.9-55.7,56.5-60.7c38.2-15.1,65.2-52.3,65.2-95.9c0-57-46.3-103.2-103.3-103.2c-31.9,0-60.6,14.7-79.5,37.5l0.1-0.4c0,0-28,40.3-81.3,40.3H481.6c-53.3-0.1-81-26.1-91.2-38.5C369.5,30.6,334,10,293.7,10c-64.1,0-116.1,51.9-116.1,116.1c0,27.5,9.5,52.6,25.4,72.5c19.7,28.2,26.8,64.3,17.5,98.3c-0.1,0.9-0.4,1.6-0.5,2.3l-34.6,129.2c-21.7,76.9-85.1,93.9-85.1,93.9l0.6,0.2C47.8,542.9,10,594.4,10,654.8c0,78.2,63.5,141.8,141.8,141.8c36.5,0,69.9-13.9,95-36.6c16.3-11.2,62-37,121.9-20.9c4,1.1,7.7,1.9,11.4,2.6l213.4,57.1c62.7,19.4,89.8,74,96,88.3C710.8,947.1,768.1,990,835.3,990c85.5,0,154.7-69.3,154.7-154.7C989.9,749.8,920.7,680.6,835.2,680.6L835.2,680.6z"></path>
        </symbol>
        <symbol id="icon-basic" viewBox="0 0 1000 1000">
          <title>basic</title>
          <g transform="translate(0.000000,511.000000) scale(0.100000,-0.100000)"><path d="M1238.1,4905.8c-209.1-55-303.8-96.9-477.7-213.5c-264.2-173.9-473.3-446.9-583.3-759.4c-50.6-143.1-59.4-202.5-68.2-550.3l-8.8-391.8h3801.6h3801.6l-8.8,380.8c-8.8,334.6-17.6,398.4-68.2,554.7c-145.3,440.2-493.1,788-950.9,950.9l-176.1,61.6l-2553.5,4.4C1511,4947.7,1385.5,4945.5,1238.1,4905.8z"></path><path d="M104.4,1427.9V437.3h3797.2h3797.2v990.6v990.6H3901.6H104.4V1427.9z"/><path d="M104.4-1103.6v-990.6h2892.5c1932.7,0,2899.1,6.6,2907.9,22c35.2,55,222.3,118.9,686.8,233.3c277.4,68.3,512.9,134.3,528.3,149.7c13.2,13.2,149.7,239.9,301.6,504.1L7698.7-703v295v295H3901.6H104.4V-1103.6z"/><path d="M8070.8-1466.8c-39.6-19.8-123.3-154.1-270.8-433.7c-118.9-222.3-224.5-411.6-233.3-420.4c-8.8-8.8-233.3-57.2-497.5-107.9c-449.1-81.4-486.5-92.5-541.5-151.9c-46.2-48.4-61.6-85.8-61.6-154.1c0-83.7,15.4-105.7,314.8-418.2c171.7-182.7,321.4-345.6,332.4-361c15.4-19.8,0-198.1-39.6-515.1c-52.8-411.6-57.2-497.5-35.2-552.5c30.8-74.9,121.1-132.1,204.7-132.1c28.6,0,237.7,88,464.5,198.1c226.7,107.9,422.6,198.1,438,198.1c15.4,0,224.6-94.6,466.7-211.3c488.7-233.3,532.7-240,636.2-116.7c70.4,83.7,70.4,99.1,0,627.4l-57.2,427.1l220.1,237.7c121.1,129.9,266.4,279.6,323.6,334.6c107.9,103.5,165.1,193.7,165.1,253.1c0,57.2-61.6,173.9-107.9,202.5c-24.2,15.4-244.3,61.6-490.9,105.7c-244.3,44-457.9,92.5-471.1,105.7c-15.4,15.4-123.3,204.7-239.9,422.6c-116.7,217.9-237.7,418.2-266.3,446.9C8260.1-1427.2,8156.6-1420.6,8070.8-1466.8z"/><path d="M104.4-2959.2c0-376.4,39.6-565.7,176.1-825.5c162.9-317,385.2-534.9,693.4-689c317-156.3,206.9-151.9,2910.1-151.9h2423.6l13.2,61.6c6.6,33,33,224.5,59.4,429.2l46.3,367.6l-295,321.4c-402.8,440.3-433.6,486.5-488.7,741.8l-13.2,59.4H2867H104.4V-2959.2z"/></g>
        </symbol>
      </defs>
    </svg>

    <el-dialog title="选择文件" :visible.sync="fileSelectVisible">
      <dragTreeTable :data="treeDataFile"
                     :onDrag="onTreeDataChangeFile"
                     v-bind:isdraggable="false"
      ></dragTreeTable>
      <span slot="footer" class="dialog-footer">
        <el-button @click="fileSelectVisible = false">取 消</el-button>
        <el-button type="primary" @click="fileSelected">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="选择模型" :visible.sync="modelSelectVisible">
      <dragTreeTable :data="treeDataModel"
                     :onDrag="onTreeDataChangeModel"
                     v-bind:isdraggable="false"
      ></dragTreeTable>
      <span slot="footer" class="dialog-footer">
        <el-button @click="modelSelectVisible = false">取 消</el-button>
        <el-button type="primary" @click="modelSelected">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="导出"
               :visible.sync="dialogUploadVisible">
      <dragTreeTable :data="treeDataUpload"
                     :onDrag="onTreeDataUploadChange"
                     v-bind:isdraggable="false"
      ></dragTreeTable>
      <p>导出到上述某目录下，或选择导出到 <el-button size="mini" @click="selectDatasetInDialog = '/'">根目录</el-button> 下</p>
      <p>已选中目录：{{selectDatasetInDialog}}</p>
      <el-input v-model="input" placeholder="请输入名称" minlength="1"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogUploadVisible = false">取 消</el-button>
        <el-button type="primary" @click="nameUploadFolder">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import * as axios from "axios";
  import $ from 'jquery';
  import componentDraggable from '../components/ComponentDraggable.vue';
  import circleDraggable from '../components/CircleDraggable.vue';
  import node from '../components/Node.vue';
  import paramBorder from '../components/paramBorder';
  import dragTreeTable from '../components/dragTreeTable'
  import api from '../utils/api-config.js'

  const LINE_CIRCLE_X_BIAS = 8;
  const LINE_CIRCLE_Y_BIAS = 8;

  export default {
    name: "projectDetail",
    components: {
      componentDraggable,
      node,
      circleDraggable,
      paramBorder,
      dragTreeTable,
    },
    data() {
      return {
        server: api.server, //'http://10.141.2.231:8081/' ,  // TODO:
        dataTypeInBorder: '',           // border: about data view
        stringInBorder: '',
        addressInBorder: '',
        imageInBorder: {},
        tableInBorder: {},              // { 'title': [ 'head1' , 'head2' ], 'data': [{ 'head1': 1, 'head2': 'a' }, { 'head1': 7, 'head2': 'b' }, { 'head1': 8, 'head2': 'c' }]}
        sum: 1,                         // 节点总数。无父节点，填0，故需从1开始编号
        levelNum: [],                   // 每层节点总数，从0开始(0,1,2,...)
        finished: true,                 // node state
        curr_model_id: 0,
        curr_file_id: 0,
        curr_upload_id: 0,
        treeDataModel: {
          radio: 0,
          lists: [],
          columns: [{
            type: 'selection',
            title: '文件/模型',
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
              text: 'border_dialog',
              onclick: this.dialogModelSelect,
              formatter: (item) => {
                if (item.id === this.curr_model_id)
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-select"></use></svg>'+'</i>';
                else
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-empty"></use></svg>'+'</i>'
              }
            }]
          },
          ],
        },           // data in dialog
        treeDataFile: {
          radio: 0,
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
          },{
            title: '',
            type: 'action',
            flex: 1,
            align: 'center',
            actions: [{
              text: 'border_dialog',
              onclick: this.dialogFileSelect,
              formatter: (item) => {
                if (item.id === this.curr_file_id)
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-select"></use></svg>'+'</i>';
                else
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-empty"></use></svg>'+'</i>'
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
                if (item.id === this.curr_upload_id)
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-select"></use></svg>'+'</i>';
                else
                  return '<i>'+'<svg class="icon" aria-hidden="true"><use xlink:href="#icon-radio-empty"></use></svg>'+'</i>'
              }
            }]
          },
          ],
        },
        msgFileName: '',                // dialog: select file
        selectFileInDialog: '',
        fileSelectVisible: false,
        msgModelName: '',               // dialog: select model
        selectModelInDialog: '',
        modelSelectVisible: false,
        msgUploadName: {                // dialog: export ,that's upload
          dataset: '',
          file: '',
        },
        selectDatasetInDialog: '/',
        dialogUploadVisible: false,
        input: '',
        back_flag: false,               // save the last node
        last_lists: [],
        show_button_lists: false,       // control the visibility of buttons
        show_detail_box: false,
        show_data_box: false,
        node_show_button_lists: false,
        node_show_detail_box: false,
        node_show_data_box: false,
        type_detail:new Map(),          // {param_name:param_value}
        curr_id:null,
        G: null,
        drag_data: new Map(),
        node_items:[],
        component_items:[],
        param_items:[],
        border_items:[],
        line_items: [],
        project_id : 0,                 // get id from router
        component_id: 1,                // draggable component id: 1,2,3,...
        param_list: [],
        props_list: [],
      }
    },
    watch: {
      project_id(newValue) {
        console.log('Current project id: ', newValue);
        if (newValue == null) {
          this.$router.push({name:"projectView"});
        }
      },

      dataTypeInBorder(newValue) {
        if (newValue === 'Image') {
          this.imageInBorder = {};
        }

      },

      curr_id(newValue, oldValue) {
        let params = {};
        this.$nextTick(()=>{
          setTimeout(() => {
            if (oldValue !== null && newValue !== null) {
              // 保存上一个node的所有参数
              console.log('---------old node-----------');
              for (let i=0;i < this.param_list.length; ++i) {
                params[this.param_list[i].name] = this.param_list[i].value;
              }
              this.G.setParam(oldValue, params);
              console.log('----------------------------');
            }

            if (newValue !== null) {
              console.log('---------current node-----------');
              // 获取当前点击node的参数，并传入border
              this.props_list = this.G.getParam(newValue);

              // 更新border
              this.getNodeParams(newValue);
            }
          }, 100);
        });
      }
    },
    created() {
      const _this = this;
      this.project_id = this.$route.params['project_id'];
// ==================================================== Renderer class =================================================
      class Renderer{
        constructor(container_selector = '.canvas') {
          this.svg_selector = '#svg';
          this.lines = [];
        }

        addNode(node_id, name, posiX, posiY) {
          let node_type = node_id.split('-')[0];
          let itype = _this.type_detail.get(node_type);
          let node_name = itype.display;
          let in_port_num = itype.in_port.length;
          let out_port_num = itype.out_port.length;

          // TODO : spec canvas id
          let new_node = {};
          new_node.node_id = node_id;
          new_node.posiX = posiX;
          new_node.posiY = posiY;
          new_node.icon_type = name.split('_', 1)[0];
          _this.node_items.push(new_node);
          console.log('created');
        }

        addEdge(node_from, port_from, node_to, port_to) {
          // TODO: check parseInt & x/y bias
          let node_out = node_from + '-out-' + port_from;
          let node_in = node_to + '-in-' + port_to;

          let from = $("#" + node_out);
          let to = $("#" + node_in);
          let x1 = parseInt(from.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(from.parent().css('left'));
          let y1 = parseInt(from.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(from.parent().css('top'));
          let x2 = parseInt(to.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(to.parent().css('left'));
          let y2 = parseInt(to.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(to.parent().css('top'));

          let $line = $('<line/>');
          $line.attr('class', 'line');
          let id = node_out + "-" + node_in;
          $line.attr("id", id);
          $line.attr("x1", x1);
          $line.attr("y1", y1);
          $line.attr("x2", x2);
          $line.attr("y2", y2);
          let svg = $(this.svg_selector);
          svg.append($line);
          svg.html(svg.html());

          this.lines.push(id);

          let new_line = {};
          new_line.id = node_out + "-" + node_in;
          new_line.x1 = x1;
          new_line.y1 = y1;
          new_line.x2 = x2;
          new_line.y2 = y2;
          _this.line_items.push(new_line);
        }

        delNode(node_id) {
          for(let i = 0;i < _this.node_items.length;++i)
            if (node_id == _this.node_items[i].node_id){
              _this.node_items[i] = {};
              break;
            }

          // delete lines
          let last_lines = [];
          for (let line_id in this.lines) {
            if (this.lines[line_id].indexOf(node_id) !== -1) {
              console.log('need to be deleted.');
              $("#"+this.lines[line_id]).remove();
            }
            else {
              last_lines.push(this.lines[line_id]);
            }
          }
          this.lines = last_lines;
        }

        delEdge(node_from, port_from, node_to, port_to) {
          let node_out = node_from + '-out-' + port_from;
          let node_in = node_to + '-in-' + port_to;
          let line_id = node_out + '-' + node_in;
          let last_lines = [];
          for (let i in this.lines) {
            if (i == line_id) {
              $('#'+line_id).remove();
            }
            else {
              last_lines.push(i);
            }
          }
          this.lines = last_lines;
        }

        setPosition(node_id, posiX, posiY) {
          // TODO check paseInt
          let node = $("#" + node_id);
          node.css("top", posiY);
          node.css("left", posiX);

          this.lines.forEach((line_id) => {
            if (line_id.indexOf(node_id+'-') != -1) {
              let sp = line_id.split('-');
              if (sp[0] + '-' + sp[1] == node_id) {
                let line = $('#' + line_id);
                let circle = $('#' + sp[0] + '-' + sp[1] + '-' + sp[2] + '-' + sp[3]);
                line.attr('x1', parseInt(circle.css('left')) + LINE_CIRCLE_X_BIAS + posiX);
                line.attr('y1', parseInt(circle.css('top')) + LINE_CIRCLE_Y_BIAS + posiY);
              }
              else if (sp[4] + '-' + sp[5] == node_id) {
                let line = $('#' + line_id);
                let circle = $('#' + sp[4] + '-' + sp[5] + '-' + sp[6] + '-' + sp[7]);
                line.attr('x2', parseInt(circle.css('left')) + LINE_CIRCLE_X_BIAS + posiX);
                line.attr('y2', parseInt(circle.css('top')) + LINE_CIRCLE_Y_BIAS + posiY);
              }
              else {
                alert('bug : Class Renderer : setPosition, node_id wrong');
              }
            }
          });
          let svg = $("#svg");
          svg.html(svg.html());
        }

        clear() {
          let node_list = [];
          for (let i in _this.node_items)
            node_list.push(_this.node_items[i]);
          for (let i in node_list) {
            let inode = node_list[i].node_id;
            this.delNode(inode);
          }
        }
      }
// ===================================================== Graph class ===================================================
      class Graph {
        constructor() {
          console.log('Graph init');
          // console.log(this);  // Graph()
          // console.log(_this); // VueComponent
          this.node = new Map(); // {node_id: {'id':id, 'type':type, 'position':[1,1], 'param':{param_key:param_value} }}
          this.edge = new Map(); // {(node_id-in|out-1):Set() }
          this.type_count = new Map(); // {node_type:counter}
          for (let key of _this.type_detail.keys()) {
            this.type_count.set(key, 0)
          }
          // TODO
          this.isrender = false;
          this.renderer = null;
        }

        addNode(node_type, posiX=0, posiY=0, load_id=null) {
          console.log('Graph call : addNode');
          // check node type
          // console.log(_this.type_detail);
          if (!_this.type_detail.has(node_type)) {
            alert(node_type + " not in component list");
            return -1;
          }

          // create node
          let itype = _this.type_detail.get(node_type);
          let node_param = itype.params;
          let param = {};
          for (let key in node_param) {
            if (node_param.hasOwnProperty(key)) {
              let x = node_param[key];
              param[x.name] = x.default;
            }
          }
          let type_number = this.type_count.get(node_type);
          let node_id = node_type + '-' + type_number;
          if (load_id != null)
            node_id = load_id;
          let new_node = {
            "id" : node_id,
            "type" : node_type,
            "position" : [posiX, posiY],
            "param" : param,
          };
          if (load_id == null) {
            this.type_count.set(node_type, type_number+1);
          }
          this.node.set(new_node.id, new_node);

          // initialize edge
          let in_port = itype.in_port;
          for (let i = 0;i < in_port.length;++ i) {
            this.edge.set(node_id + '-in-' + i, new Set());
          }
          let out_port = itype.out_port;
          for (let i = 0;i < out_port.length;++ i) {
            this.edge.set(node_id + '-out-' + i, new Set());
          }

          if (this.isrender)
            this.renderer.addNode(node_id, itype.name, posiX, posiY);
          return node_id;
        }

        testEdge(node_from, port_from, node_to=null, port_to=null) {
          console.log('Graph call : testEdge');
          // check node exists
          let node_out = '';
          let node_in = '';
          if (node_to == null && port_to == null) {
            node_out = node_from;
            node_in = port_from;
            node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
            port_from = node_out.split('-')[3];
            node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
            port_to = node_in.split('-')[3];
          }
          else {
            node_out = node_from + '-out-' + port_from;
            node_in = node_to + '-in-' + port_to;
          }
          if (!this.edge.has(node_out)) {
            return node_out + " not in node list, please check code";
          }
          if (!this.edge.has(node_in)) {
            return node_in + " not in node list, please check code";
          }

          // check there is no duplicate edge
          let node_out_set = this.edge.get(node_out);
          let node_in_set = this.edge.get(node_in);
          if (node_out_set.has(node_in)) {
            return node_in + " already in " + node_out;
          }
          if (node_in_set.has(node_out)) {
            return node_out + " already in " + node_in;
          }

          // check in port is unique
          if (node_in_set.size >= 1) {
            return node_in + " already has input";
          }

          // check port data type match
          let out_data_type = _this.type_detail.get(this.node.get(node_from).type).out_port[parseInt(port_from)];
          let in_data_type = _this.type_detail.get(this.node.get(node_to).type).in_port[parseInt(port_to)];
          if (out_data_type != in_data_type) {
            return 'type not match : ' + out_data_type + ' & ' + in_data_type;
          }
          return 0;
        }

        addEdge(node_from, port_from, node_to=null, port_to=null) {
          console.log('Graph call : addEdge');
          let node_out = '';
          let node_in = '';
          if (node_to == null && port_to == null) {
            node_out = node_from;
            node_in = port_from;
            node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
            port_from = node_out.split('-')[3];
            node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
            port_to = node_in.split('-')[3];
          }
          else {
            node_out = node_from + '-out-' + port_from;
            node_in = node_to + '-in-' + port_to;
          }
          let test_ret = this.testEdge(node_from, port_from, node_to, port_to);
          if (test_ret != 0) {
            alert(test_ret);
            return -1;
          }

          // add edge
          let node_out_set = this.edge.get(node_out);
          let node_in_set = this.edge.get(node_in);
          node_out_set.add(node_in);
          node_in_set.add(node_out);


          if (this.isrender)
            this.renderer.addEdge(node_from, port_from, node_to, port_to);
          return 0;
        }

        delNode(node_id) {
          console.log('Graph call : delNode');
          // check node id
          if (!this.node.has(node_id)) {
            alert(node_id + ' node exist, please check');
            return -1;
          }

          // delete edge
          let node_type = this.node.get(node_id).type;
          let node_detail = _this.type_detail.get(node_type);
          // delete in edge
          for (let i = 0;i < node_detail.in_port.length; ++ i) {
            let this_in_port = node_id + '-in-' + i;
            let in_edge_set = this.edge.get(this_in_port);
            for (let x of in_edge_set) {
              this.edge.get(x).delete(this_in_port);
            }
            this.edge.delete(this_in_port);
          }
          // delete out edge
          for (let i = 0;i < node_detail.out_port.length; ++ i) {
            let this_out_port = node_id + '-out-' + i;
            let out_edge_set = this.edge.get(this_out_port);
            for (let x of out_edge_set) {
              this.edge.get(x).delete(this_out_port);
            }
            this.edge.delete(this_out_port);
          }

          // delete node
          this.node.delete(node_id);

          if (this.isrender)
            this.renderer.delNode(node_id);
          return 0;
        }

        delEdge(node_from, port_from=null, node_to=null, port_to=null) {
          console.log('Graph call : delEdge');
          let node_out = '';
          let node_in = '';
          if (node_to == null && port_to == null && port_from == null) {
            let sp = node_from.split('-');
            node_from = sp[0] + '-' + sp[1];
            port_from = sp[3];
            node_to = sp[4] + '-' + sp[5];
            port_to = sp[7];
            node_out = sp[0] + '-' + sp[1] + '-' + sp[2] + '-' + sp[3];
            node_in = sp[4] + '-' + sp[5] + '-' + sp[6] + '-' + sp[7];
          }
          else if (node_to == null && port_to == null) {
            node_out = node_from;
            node_in = port_from;
            node_from = node_out.split('-')[0] + '-' + node_out.split('-')[1];
            port_from = node_out.split('-')[3];
            node_to = node_in.split('-')[0] + '-' + node_in.split('-')[1];
            port_to = node_in.split('-')[3];
          }
          else {
            node_out = node_from + '-out-' + port_from;
            node_in = node_to + '-in-' + port_to;
          }
          // check node exists
          if (!this.edge.has(node_out)) {
            alert(node_out + " not in node list, please check code");
            return -1;
          }
          if (!this.edge.has(node_in)) {
            alert(node_in + " not in node list, please check code");
            return -1;
          }

          // check edge exist
          let node_out_set = this.edge.get(node_out);
          let node_in_set = this.edge.get(node_in);
          let find = -1;
          if (!node_in_set.has(node_out)) {
            alert('delete edge not match : ' + node_out + ' & ' + node_in);
            return -1;
          }
          if (!node_out_set.has(node_in)) {
            alert("!!ERROR!! there is a bug in Graph class, edge not match");
            return -1;
          }

          // delete edge
          node_in_set.delete(node_out);
          node_out_set.delete(node_in);

          if (this.isrender)
            this.renderer.delEdge(node_from, port_from, node_to, port_to);
          return 0;
        }

        setParam(node_id, param) {
          console.log('Graph call : setParam');
          // check node exist
          if (!this.node.has(node_id)) {
            console.log('WARNING!');
            console.log(node_id + ' not exist, please check 1');
            return -1;
          }
          let node_param = this.node.get(node_id).param;
          for (let key in param) {
            if (param.hasOwnProperty(key)) {
              node_param[key] = param[key];
            }
          }
          return 0;
        }

        getParam(node_id) {
          console.log('Graph call : getParam');
          // check node exist
          if (!this.node.has(node_id)) {
            console.log('WARNING!');
            console.log(node_id + ' not exist, please check 2');
            return {};
          }
          let node_param = this.node.get(node_id).param;
          return node_param;
        }

        setPosition(node_id, posiX, posiY) {
          console.log('Graph call : setPosition');
          // check node exist
          if (!this.node.has(node_id)) {
            console.log('WARNING!');
            console.log(node_id + ' not exist, please check 3');
            return -1;
          }
          this.node.get(node_id).position = [posiX, posiY];
          if (this.isrender)
            this.renderer.setPosition(node_id, posiX, posiY);
          return 0;
        }

        clear() {
          console.log('Graph call : clear');
          this.node.clear();
          this.edge.clear();
          for (let key in this.type_count.keys()) {
            this.type_count.set(key, 0);
          }

          if (this.isrender)
            this.renderer.clear();
          return 0;
        }

        toJson() {
          console.log('Graph call : toJson');
          // nodes
          let all_nodes = [];
          for (let [key, value] of this.node) {
            let detail = {
              'node_name' : key,
              'node_type' : value.type,
              'node_position' : value.position,
              'details' : value.param,
            };
            all_nodes.push(detail);
          }

          // lines
          let all_lines = [];
          for (let [key, value] of this.edge) {
            if (key.indexOf('-out-') != -1) {
              for (let item of value) {
                let detail = {
                  'line_name' : key + '-' + item,
                  'line_from' : key.split('-')[0] + '-' + key.split('-')[1],
                  'line_from_port' : key.split('-')[3],
                  'line_to' : item.split('-')[0] + '-' + item.split('-')[1],
                  'line_to_port' : item.split('-')[3],
                };
                all_lines.push(detail);
              }
            }
          }
          let ret = {
            project_id: _this.project_id,
            all_nodes: all_nodes,
            all_lines: all_lines,
          };
          return ret;
        }

        loadJson(string_or_obj) {
          console.log('Graph call : loadJson');
          this.clear();
          let obj = string_or_obj;
          if (typeof(string_or_obj) == 'string')
            obj = JSON.parse(string_or_obj);

          // solve nodes
          let nodes = obj.all_nodes;

          console.log('------load nodes-----------');
          console.log(nodes);

          for (let key in nodes) {
            let x = nodes[key];
            let node_id = this.addNode(x.node_type, x.node_position[0], x.node_position[1], x.node_name);
            if (node_id == -1) {
              alert('bug in loadJson');
              return -1;
            }
            if (this.type_count.get(x.node_type) <= parseInt(node_id.split('-')[1])) {
              this.type_count.set(x.node_type, parseInt(node_id.split('-')[1]) + 1);
            }
            this.setParam(node_id, x.details);
          }

          // solve lines
          setTimeout(() => {
            let lines = obj.all_lines;
            lines.forEach((x) => {
              this.addEdge(x.line_from, x.line_from_port, x.line_to, x.line_to_port);
            });
          },100);
          return 0;
        }

        startRender(canvas_selector='.canvas') {
          console.log('Graph call : startRender');
          this.renderer = new Renderer(canvas_selector);
          this.isrender = true;
          // TODO
          return -1;
        }

        endRender() {
          console.log('Graph call : endRender');
          this.renderer.clear();
          this.renderer = null;
          this.isrender = false;
          return 0;
        }
      }
// ====================================================== init all =====================================================
      axios.post(this.$api.componentParameter)
        .then((data) => {
          data = data.data.component;
          data.forEach(
            a => this.type_detail.set(a.name, a)
          );
          console.log('component', data);

          this.G = new Graph();
          this.G.startRender();

          // console.log('-----load button---------');
          this.load_button();

          this.component_init();
          console.log('READY');
        })
        .catch(() => {});

      console.log('-------dialogView------------');
      this.dialogView(); // only file now TODO: model
      console.log('-----------------------------');
    },
    methods: {

// ====================================================== buttons ======================================================
      load_button() {
        if (this.project_id === null) {
          return;
        }

        let postData = JSON.stringify({
          project_id: this.project_id,
        });
        axios.post(this.$api.graphGet, postData)
          .then((res) => {
            console.log('-----res----');
            console.log(res);
            console.log('------------');
            res = res.data;
            if (res.succeed === 0) {

              let succeed_loadJson = this.G.loadJson(res);
              if (succeed_loadJson === 1) {
                this.$message({
                  message: 'Loading failed when creating graph',
                  type: "error",
                  showClose: true,
                  duration: "2000"
                });
                console.log('load failed:');
                console.log(res);
              }
            } else {
              this.$message({
                message: '请重试！',
                type: "warning",
                showClose: true,
                duration: "1000"
              });
            }
          })
          .catch(() => {
          });

      },

      save_button() {
        if (this.project_id !== null) {

          this.back_flag = true;
          console.log('set back_flag true.');

          this.$nextTick(()=>{
            setTimeout(() => {
              // 保存当前节点
              if (this.curr_id !== null) {
                let params = {};
                console.log('---------last node-----------');
                for (let i=0;i < this.last_lists.length; ++i) {
                  params[this.last_lists[i].name] = this.last_lists[i].value;
                }
                // console.log(params);
                this.G.setParam(this.curr_id, params);
                console.log('----------------------------');
              }

              let dataPost = JSON.stringify(this.G.toJson());
              axios.post(this.$api.graphSave, dataPost)
                .then((res) => {
                  console.log('-----res----');
                  console.log(res);
                  console.log('------------');
                  res = res.data;
                  if (res.succeed === 0) {
                    this.$message({
                      message: res.message,
                      type: "success",
                      showClose: true,
                      duration: "1000"
                    });
                  } else {
                    this.$message({
                      message: res.message,
                      type: "error",
                      showClose: true,
                      duration: "2000"
                    });
                  }
                })
                .catch(() => {});
            }, 300)
          });

          this.$nextTick(()=>{
            setTimeout(() => {
              this.back_flag = false;
              console.log('set back_flag false.');
            }, 350)
          });
        } else {
          this.$message({
            message: '无法获取项目id, 请回到主页重新进入项目！',
            type: "warning",
            showClose: true,
            duration: "3000"
          });
        }
      },

      // TODO: check
      stop_button() {
        if (this.finished) {
          console.log('already stopped.');
          return;
        }

        if (this.project_id !== null) {
          let postData = JSON.stringify({
            project_id: this.project_id,
          });
          axios.post(this.$api.graphStop, postData)
            .then((res) => {
              console.log('-----res----');
              console.log(res);
              console.log('------------');
              res = res.data;
              if ((res.succeed === 0) || (res.message.indexOf('not running') != -1)) {
                this.finished = true;
                this.$message({
                  message: res.message,
                  type: "success",
                  showClose: true,
                  duration: "1000"
                });
              } else {
                this.$message({
                  message: res.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                });
              }
            })
            .catch(() => {});
        } else {
          this.$message({
            message: '无法获取项目id, 请回到主页重新进入项目！',
            type: "warning",
            showClose: true,
            duration: "3000"
          });
        }
      },

      clear_button() {
        if (this.project_id !== null) {
          let postData = JSON.stringify({
            project_id: this.project_id,
          });
          axios.post(this.$api.graphInit, postData)
            .then((res) => {
              console.log('-----res----');
              console.log(res);
              console.log('------------');
              res = res.data;
              if (res.succeed === 0) {
                this.$message({
                  message: res.message,
                  type: "success",
                  showClose: true,
                  duration: "1000"
                });
                this.render_nodes({});
                $('.node-select').css('background-color', '')
              } else {
                this.$message({
                  message: res.message,
                  type: "error",
                  showClose: true,
                  duration: "2000"
                });
              }
            })
            .catch(() => {});
        } else {
          this.$message({
            message: '无法获取项目id, 请回到主页重新进入项目！',
            type: "warning",
            showClose: true,
            duration: "3000"
          });
        }
      },

      render_nodes(data) {
        $('.canvas>.node').css('background-color', '#ffffff');
        for (let i in data) {
          if (data.hasOwnProperty(i)) {
            let node = data[i];
            let key = node.node_name;
            let status = node.node_status;
            let inode = $('#'+key);
            let color;
            if (status == '0') {
              // finish
              color = '#D5F5E3';
            }
            else if (status == '1') {
              // wait
              color = 'rgba(255,255,255,1)';
            }
            else if (status == '2') {
              // running
              color = '#FCF3CF';
            }
            else if (status == '-1') {
              // fail
              color = '#FADBD8';
            }
            else {
              alert('unknown node status' + status);
            }
            inode.css('background-color', color);
          }
        }
      },

      check_progress() {
        if (this.finished) {
          return;
        }
        let dataPost = JSON.stringify({
          project_id: this.project_id,
        });
        axios.post(this.$api.graphProgress, dataPost)
          .then(res => {
            res = res.data;
            console.log('----res-----');
            console.log(res);
            console.log('111');
            if (res.status === 0) {
              this.finished = true;
            }
            else {
              setTimeout(() => {
                this.check_progress();
              }, 1000);
              console.log('222');
            }
            this.render_nodes(res.progress);
          })
          .catch(() => {})
      },

      run_button() {
        // TODO : 前端加入運行按鈕，並測試
        // 判断是否有仍然在运行的节点
        if (!this.finished) {
          this.$message({
            message: '仍在运行中...',
            type: "warning",
            showClose: true,
            duration: "2000"
          });
          return;
        }

        // 保存当前节点
        this.back_flag = true;
        console.log('set back_flag true.');

        this.$nextTick(()=>{
          setTimeout(() => {
            if (this.curr_id !== null) { // 保存当前右侧边栏填写的节点内容
              let params = {};
              console.log('---------last node-----------');
              for (let i=0;i < this.last_lists.length; ++i) {
                params[this.last_lists[i].name] = this.last_lists[i].value;
              }
              this.G.setParam(this.curr_id, params);
              console.log('----------------------------');
            }

            // 运行节点
            axios.post(this.$api.graphRun, JSON.stringify(this.G.toJson()))
              .then((res)=> {
                console.log('run : get response');
                res = res.data;
                if (res.succeed === 0) {
                  this.finished = false;
                  this.$message({
                    message: '开始运行。' + res.message,
                    type: "success",
                    showClose: true,
                    duration: "1000"
                  });
                  setTimeout(() => {
                    this.check_progress();
                  }, 1000);
                } else {
                  this.$message({
                    message: '运行失败。' + res.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  });
                }
              })
              .catch(() => {});
          }, 500)
        });

        this.$nextTick(()=>{
          setTimeout(() => {
            this.back_flag = false;
            console.log('set back_flag false.');
          }, 550)
        })
      },

      delete_button() {
        // TODO ：删除节点和边 并输出检查是否正确删除
        // TODO : finished
        // 显示数据删除
        for (let i = 0;i < this.node_items.length; ++i)
          if (this.node_items.node_id === this.curr_id) {
            this.node_items[i] = null;
            console.log('Succeed. '); // Found the node need to be deleted and deleted it in list node_items successfully.
            break;
          }
        // G, 删除
        this.G.delNode(this.curr_id);
        this.curr_id = null;
        this.node_show_detail_box = false;
        this.node_show_data_box = false;
      },

      run_single_button() {
        if (!this.finished) {
          this.$message({
            message: '仍在运行中...',
            type: "warning",
            showClose: true,
            duration: "2000"
          });
          return;
        }

        // 保存当前节点
        this.back_flag = true;
        console.log('set back_flag true.');

        this.$nextTick(()=>{
          setTimeout(() => {

            if (this.curr_id !== null) {
              let params = {};
              console.log('---------last node-----------');
              for (let i=0;i < this.last_lists.length; ++i) {
                params[this.last_lists[i].name] = this.last_lists[i].value;
              }
              this.G.setParam(this.curr_id, params);
              console.log('----------------------------');
            }

            // 运行节点
            let dataPost = this.G.toJson();
            let key = 'run';
            dataPost[key] = [this.curr_id];
            axios.post(this.$api.graphRun, JSON.stringify(dataPost))
              .then((res)=> {
                console.log('run : get response');
                res = res.data;
                if (res.succeed === 0) {
                  this.finished = false;
                  this.$message({
                    message: '开始运行...' + res.message,
                    type: "success",
                    showClose: true,
                    duration: "1000"
                  });
                  setTimeout(() => {
                    this.check_progress();
                  }, 1000);
                } else {
                  this.$message({
                    message: '运行失败！' + res.message,
                    type: "error",
                    showClose: true,
                    duration: "2000"
                  });
                }
              })
              .catch(() => {});
          }, 500)
        });

        this.$nextTick(()=>{
          setTimeout(() => {
            this.back_flag = false;
            console.log('set back_flag false.');
          }, 550)
        })
      },

// ======================================================= dialog ======================================================
      isNumber(obj) {
        return (typeof obj === 'number');
      },

      dataInsertByParentId(dataList) {
        let point = dataList.length - 1;
        if (point === -1) {
          console.log('dataList is empty, check function dataViewTransformDraggable().');
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

      dialogView() {
        let dataTemple = [];
        const _this = this;

        function transform(obj, dataList, preId, preName) {
          let num = 0;
          for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
              if (Array.isArray(obj[key])) { // file
                let file_size = obj[key][0], file_type = obj[key][1];
                let data = {};
                data.id = _this.sum;
                _this.sum++;
                if (preId.length === 0) {
                  data.parent_id = 0;
                } else {
                  data.parent_id = preId[preId.length-1];
                }
                data.name = key;
                data.file_size = file_size;
                data.file_type = file_type;
                data.open = false;
                data.directory = false; // file: false, folder: true
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
                  data.parent_id = preId[preId.length-1]; // the last one
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
            this.onTreeDataChangeFile(newDataTemple);
            this.onTreeDataChangeModel(newDataTemple);
            this.onTreeDataUploadChange(newDataTemple);
          })
          .catch(err => {});
      },

      onTreeDataChangeFile(list) {
        this.treeDataFile.lists = list
      },

      onTreeDataChangeModel(list) {
        this.treeDataModel.lists = list
      },

      fileSelected() {
        this.msgFileName = this.selectFileInDialog;
        this.fileSelectVisible = false;

      },

      modelSelected() {
        this.msgModelName = this.selectModelInDialog;
        this.modelSelectVisible = false;
      },

      dialogFileSelect(item) { // Dialog
        this.curr_file_id = item.id;
        let datasetName = '';
        if (item.dataset_name === '') {
          datasetName = item.name;
        } else {
          datasetName = item.dataset_name + '/'+item.name;
        }
        this.selectFileInDialog = datasetName;
        console.log(datasetName);
      },

      dialogModelSelect(item) { // Dialog
        this.curr_model_id = item.id;
        let datasetName = '';
        if (item.dataset_name === '') {
          datasetName = item.name;
        } else {
          datasetName = item.dataset_name + '/'+item.name;
        }
        this.selectModelInDialog = datasetName;
        console.log(datasetName);
      },

      // upload
      onTreeDataUploadChange(list) {
        this.treeDataUpload.lists = list
      },

      nameUploadFolder() {
        if (this.input !== '') {
          this.msgUploadName.file = this.input;
          this.msgUploadName.dataset = this.selectDatasetInDialog;
          console.log('-------------msgUploadName------------');
          console.log(this.msgUploadName);
          this.dialogUploadVisible = false;
          this.dialogView();
        } else {
          console.log('input need to be not empty.');
        }
      },

      selectDataset_button() {
        this.dialogUploadVisible = true;
        this.selectDatasetInDialog = this.msgUploadName.dataset;
      },

      folderUploadSelect(item) { // Dialog
        this.curr_upload_id = item.id;
        let datasetName = '';
        if (item.dataset_name === '') {
          datasetName = item.name;
        } else {
          datasetName = item.dataset_name + '/' + item.name;
        }
        this.selectDatasetInDialog = datasetName;
        console.log(datasetName);
      },
// ================================================== component ========================================================
      component_init() {
        let _this = this;
        function nodes_build(dataList, parentId, parentName, lis) {
          for (let key in lis) {
            if (lis.hasOwnProperty(key)) {
              if (typeof(lis[key]) == 'object') {
                let data = {};
                data.name = key;
                data.open = true;
                data.level = parentId.length;
                data.id = _this.component_id;
                _this.component_id++;
                data.isDirectory = true;
                data.display = key;
                if (parentId.length === 0) {
                  data.parent_id = 0;
                } else {
                  data.parent_id = parentId[parentId.length - 1];
                }
                parentId.push(data.id);
                parentName.push(data.name);
                data.lists = [];
                data.isdraggable = false;
                dataList.push(data);
                nodes_build(dataList, parentId, parentName, lis[key]);
                parentId.pop();
                parentName.pop();
              }
              else {
                let data = {};
                data.name = key;
                data.open = true;
                data.level = parentId.length;
                data.id = _this.component_id;
                _this.component_id++;
                data.isDirectory = false;
                data.display = lis[key];
                data.parent_id = parentId[parentId.length - 1];
                data.lists = [];
                data.isdraggable = true;
                data.icon_type = key.split('_',1)[0];
                dataList.push(data);
              }
            }
          }
        }

        function dataListDeleteExceptRootLevel(dataList, newDataList) {
          for (let i=0;i<dataList.length;i++) {
            if (dataList[i].parent_id === 0) { // 保留级别最高的节点
              newDataList.push(dataList[i]);
            }
          }
        }

        function dataInsertByParentId(dataList) {
          let point = dataList.length - 1;
          if (point === -1) {
            console.log('dataList is empty.');
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
                  dataList[pro_point].lists.splice(0, 0, dataList[point]);
                }
              }
            }
            point--;
          }
        }

        axios.post(this.$api.componentListView)
          .then((data) => {
            let dataList = [], parentId = [], parentName = [];
            let compo_list = data.data.structure;
            nodes_build(dataList, parentId, parentName, compo_list);
            dataInsertByParentId(dataList);
            let newDataList = [];
            dataListDeleteExceptRootLevel(dataList, newDataList);
            this.component_items = newDataList;
            console.log(this.component_items);
          })
          .catch(() => {});
      },
// =============================================== canvas functions ====================================================
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

      canvas_dragover(e) {
        e.preventDefault();
      },

      canvas_dragenter(e) {
        e.preventDefault()
      },

      canvas_drop(e) {
        e.preventDefault();
        let class_type = this.drag_data.get('class_type');
        console.log('canvas drop :', class_type);
        if (!(['node', 'component'].includes(class_type))) {
          return false;
        }
        let bias_x = parseInt(this.drag_data.get("bias_x"));
        let bias_y = parseInt(this.drag_data.get("bias_y"));
        let x = e.clientX - this.getX($(".canvas")[0]) + document.body.scrollLeft - bias_x;
        let y = e.clientY - this.getY($(".canvas")[0]) + document.body.scrollTop - bias_y;
        if (class_type == "component") {
          let type = this.drag_data.get('type');
          let ret = this.G.addNode(type, x, y);
          console.log('add node', ret);
        } else if (class_type == "node") {
          this.G.setPosition(this.drag_data.get('node_id'), x, y);
        }
      },

      getNodeParams(id) {

        let params = this.G.getParam(id);
        let itype = this.type_detail.get(id.split('-')[0]);
        console.log('itype: ',itype);
        let iparams = itype.params;

        this.border_items = JSON.parse(JSON.stringify(this.border_items));
        let old_length = this.border_items.length;
        for (let j=0;j< old_length; ++j) {
          this.border_items.pop();
        }

        for (let i = 0;i < iparams.length; ++ i) {
          let param_detail = iparams[i];
          let key = param_detail.name;
          let value = params[key];
          let param_type = param_detail.type;

          let border = {};

          border.class = 'param-border';

          let name = {};
          name.class = 'param-key';
          name.text = param_detail.display;

          let type_list = ['text', 'list', 'file', 'model', 'richtext', 'password', 'int', 'float', 'number', 'upload'];

          let param = {};
          switch (param_type) {
            case 'text': {
              param.html = 'input';
              param.type = 'text';
              break;
            }
            case 'file': {
              param.html = 'input';
              param.id = 'path';
              param.type = 'text';
              break;
            }
            case 'model': {
              param.html = 'input';
              param.id = 'path';
              param.type = 'text';
              break;
            }
            case 'password': {
              param.html = 'input';
              param.type = 'password';
              break;
            }
            case 'list': {
              param.html = 'select';
              param.type = 'text';
              param.lists = [];
              for (let j=0;j < param_detail.list.length; ++j) {
                let sub_item = {};
                sub_item.html = 'option';
                sub_item.value = param_detail.list[j];
                param.lists.push(sub_item);
              }
              break;
            }
            case 'int': {
              param.html = 'input';
              param.type = 'number';
              break;
            }
            case 'float': {
              param.html = 'input';
              param.type = 'number';
              break;
            }
            case 'richtext': {
              param.html = 'textarea';
              param.type = 'richtext';
              break;
            }
            case 'upload': {
              param.html = 'input';
              param.id = 'path';
              param.type = 'text';
              break;
            }
            default: {

            }
          }
          if (!type_list.includes(param_type)) {
            alert("there is something wrong, unknown type found : " + param_type);
            return false;
          }

          param.class = 'param-value';
          param.name = key;
          param.value = value;
          param.data_type = param_type;
          name.order = 1;
          param.order = 2;
          border.order = i;

          border.key = name;
          border.value = param;
          this.border_items.push(border);
        }
      },
    }
  }
</script>

<style scoped>
  .detail-view {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  .none-detail-view {
    display: none;
  }
  .data-view {
    display: block;
  }
  .none-data-view {
    display: none;
  }
  .table-div {
    display: flex;
  }
  .none-table-div {
    display: none;
  }
  .button-div {
    display: table-cell;
  }
  .none-button-div {
    display: none;
  }
  .delete-div {
    display: table-cell;
  }
  .none-delete-div {
    display: none;
  }
  .none-button-lists {
    display: none;
  }
  .button-lists {
    display: block;
    top: 15px;
    left: 20px;
    position: absolute;
    background-color: #ecf5ff;
    border-radius:10px;
  }
  #nodes_running_states {
    display: block;
    top: 81px;
    right: 350px;
    position: fixed;
    background-color: #ecf5ff;
    border-radius:10px;
  }
  #states_list {
    text-align: left;
    padding-left: 10%;
    padding-right: 15%;
  }
  #button-save {
    display: table-cell;
    width: 80px;
    left: 50px;
  }
  #button-cancel {
    display: table-cell;
    width: 80px;
    left: 80px;
  }
  #button-run {
    display: table-cell;
    width: 100px;
    left: 110px;
  }
  #button-run-inactive {
    display: table-cell;
    width: 80px;
    left: 110px;
  }
  #button-stop {
    display: table-cell;
    width: 80px;
    left: 140px;
  }
  #button-stop-inactive {
    display: table-cell;
    width: 80px;
    left: 140px;
  }
  #button-clear {
    display: table-cell;
    width: 80px;
    left: 170px;
  }
  #button-delete {
    display: table-cell;
    width: 100px;
    left: 200px;
  }
  #button-run-single {
    display: table-cell;
    width: 100px;
    left: 230px;
  }
  #data-box {
    overflow: hidden;
  }
  .list-dragResize {
    max-height: 100px;
  }
  .test {
    overflow: hidden;
    height: 100px;
    width: 50px;
  }
  .testlist {
    max-height: 100px;
  }
</style>
