import Vue from 'vue'
import Router from 'vue-router'
import Show_All from '@/components/Show_All'
import Edit from '@/components/edit'
import Add from '@/components/add'
import Handle from '@/components/handle'
import Check from '@/components/check'
import Login from '@/components/login'
import Admin from '@/admin/admin'
import User from '@/admin/user'
import Group from '@/admin/group'
import Password from '@/admin/password'
import KeyID from '@/components/KeyID'
import Product_group from '@/admin/product_group'
import Region from '@/admin/region'
import Product from '@/admin/product'
import Option from '@/admin/option'
import Signup from '@/components/signup'
import ResetPassword from '@/components/resetPassword'
import New_user from '@/admin/new_user'
Vue.use(Router)

export default new Router({
  routes: [
    {//防止有人亂try結構
      path: '*',
      redirect: '/',
    },
    {
      path: '/login',
      name: 'login',
      component: Login

    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup

    },
    {
      path: '/resetPassword',
      name: 'resetPassword',
      component: ResetPassword

    },
    {
      path: '/',
      name: 'Show_All',
      component: Show_All
    },
    {//KeyID模式
      path: '/keyid',
      name: 'KeyID',
      component: KeyID
    },
    {
      path: '/edit',
      name: 'edit',
      component: Edit
    },
    {
      path: '/add',
      name: 'add',
      component: Add
    },
    {
      path: '/handle',
      name: 'handle',
      component: Handle
    },
    {
      path: '/check/:verifyname',
      name: 'check',
      component: Check
    },
    {//後台
      path: '/admin',
      name: 'admin',
      component: Admin
    },
    {//後台
      path: '/password',
      name: 'password',
      component: Password
    },
    {//後台
      path: '/new_user/:verifyname',
      name: 'new_user',
      component: New_user,
    },
    {//後台
      path: '/user',
      name: 'user',
      component: User,
    },
    {//後台
      path: '/group',
      name: 'group',
      component: Group,
    },
    {//後台
      path: '/product',
      name: 'product',
      component: Product,
    },
    {//後台
      path: '/option',
      name: 'option',
      component: Option,
    },
    {//後台
      path: '/region',
      name: 'region',
      component: Region,
    },
    {//後台 product_group
      path: '/product_group',
      name: 'product_group',
      component: Product_group,
    },
  ]
})
