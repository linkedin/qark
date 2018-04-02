import Vue from 'vue'
import Router from 'vue-router'

// Containers
import Full from '@/containers/Full'

// Views
import Report from '@/views/Report'

// Cards
import Webview from '@/views/Webview'
import Broadcast from '@/views/Broadcast'
import Crypto from '@/views/Crypto'
import File from '@/views/File'
import Generic from '@/views/Generic'
import Intent from '@/views/Intent'
import Manifest from '@/views/Manifest'
import Certificate from '@/views/Certificate'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/report',
      name: 'Home',
      component: Full,
      children: [
        {
          path: 'report',
          name: 'Report',
          component: Report
        },
        {
          path: 'broadcast',
          name: 'Broadcast',
          component: Broadcast
        },
        {
          path: 'cert',
          name: 'Certificate Issues',
          component: Certificate
        },
        {
          path: 'crypto',
          name: 'Crypto Issues',
          component: Crypto
        },
        {
          path: 'file-permission',
          name: 'File Permissions',
          component: File
        },
        {
          path: 'manifest',
          name: 'Manifest File Checks',
          component: Manifest
        },
        {
          path: 'intent',
          name: 'Intent',
          component: Intent
        },
        {
          path: 'webview',
          name: 'Webview',
          component: Webview
        },
        {
          path: 'generic',
          name: 'Generic Issues',
          component: Generic
        }
      ]
    }
  ]
})
