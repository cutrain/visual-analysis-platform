import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld'
import Index from '../views/Index.vue'
import Database from '../views/Database.vue'
import ProjectDetail from '../views/ProjectDetail.vue'
import ProjectView from "../views/ProjectView.vue"

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      //redirect: '/index'
    }, {
      path: '/index',
      component: Index,
      children: [
          {
            path: 'projectDetail',
            name: 'projectDetail',
            component: ProjectDetail,
          }, {
            path: 'projectView',
            name: 'projectView',
            component: ProjectView
          }, {
            path: '',
            component: ProjectView
        }
      ],
    }, {
      path: '/database',
      name: 'database',
      component: Database
    }
  ]
})
