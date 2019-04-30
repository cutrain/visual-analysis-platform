<template>
  <div class="circle"
       @drop="circle_drop($event)"
       @dragstart="circle_dragstart($event)"
       @drag="circle_drag($event)"
       @dragend="circle_dragend($event)"
       @dragover="circle_dragover($event)"
       @dragenter="circle_dragenter($event)"
       draggable="true"
  >
  </div>
</template>
<script>
  import $ from 'jquery'
  const LINE_CIRCLE_X_BIAS = 8;
  const LINE_CIRCLE_Y_BIAS = 8;
  export default {
    name: "circleDraggable",
    props: ['drag_data', 'G'],
    created() {

    },
    mounted() {

    },
    methods: {

      circle_dragstart(e) {
        let class_type = this.drag_data.get("class_type");
        console.log('circle drag start :', class_type);
        if (class_type == null) {
          e.dataTransfer.effectAllowed = "all";
          this.drag_data.set("from_id", e.target.id);
          this.drag_data.set("class_type", "circle");

          let circle = $("#" + e.target.id);
          let x1 = parseInt(circle.css("left")) + LINE_CIRCLE_X_BIAS + parseInt(circle.parent().css('left'));
          let y1 = parseInt(circle.css("top")) + LINE_CIRCLE_Y_BIAS + parseInt(circle.parent().css('top'));

          let $line = $('<line id="line"/>');
          $line.css("stroke", "rgb(99,99,99)");
          $line.css("stroke-width", "2");
          $line.attr("x1", x1);
          $line.attr("y1", y1);
          $line.attr("x2", x1);
          $line.attr("y2", y1);
          $("#svg").append($line);
        }
      },

      circle_drag(e) {
        // TODO: drag on node, auto link
        let x = e.clientX - this.getX($(".canvas")[0]) + document.body.scrollLeft; // this.getX()
        let y = e.clientY - this.getY($(".canvas")[0]) + document.body.scrollTop;  // this.getY()
        $("#line").attr("x2", x);
        $("#line").attr("y2", y);
        let svg = $("#svg");
        svg.html(svg.html());
      },

      circle_dragend(e) {
        this.drag_data.delete("from_id");
        this.drag_data.delete("class_type");
        if (this.drag_data.has('enter')) {
          let id = this.drag_data.get('enter');
          let temp = $('#' + id);
          temp.css('border-width', '2px');
          this.drag_data.delete('enter');
        }
        $("#line").remove();
      },

      circle_dragenter(e) {
        // TODO: check fit
      },

      circle_dragover(e) {
        e.preventDefault();
      },

      circle_drop(e) {
        e.preventDefault();
        let class_type = this.drag_data.get('class_type');
        console.log('circle drop :', class_type);
        if (class_type != 'circle')
          return false;
        let from_id = this.drag_data.get("from_id");
        let to_id = e.target.id;
        if ((from_id.split('-')[2] == 'in') ^ (to_id.split('-')[2] == 'in')) {
          if (from_id.split('-')[2] == 'out') {
            let ret = this.G.addEdge(from_id, to_id);
            console.log('create edge', ret);
          } else {
            this.G.addEdge(to_id, from_id);
          }
        }
        return true;
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
    }
  }
</script>
