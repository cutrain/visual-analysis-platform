import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld'
import Index from '../views/Index'
import Database from '../views/Database'
import ProjectDetail from '../views/ProjectDetail'
import ProjectView from "../views/ProjectView"
import Login from '../views/Login'
import Welcome from '../views/Welcome'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      //name: 'HelloWorld',
      component: HelloWorld,
      children: [
        {
          path: 'login',
          name: 'login',
          component: Login,
        },
        {
          path: 'welcome',
          name: 'welcome',
          component: Welcome,
        },
      ],
      redirect: '/welcome'
    }, {
      path: '/index',
      component: Index,
      children: [
        {
          path: 'projectDetail',
          name: 'projectDetail',
          component: ProjectDetail,
        },
        {
          path: 'projectView',
          name: 'projectView',
          component: ProjectView
        },
        {
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
