import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import router from './router'
import Axios from 'axios'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Create our Vuex store
Vue.use(Vuex)
const store = new Vuex.Store({
  // Define our store variables
  state: {
    userInfo: null,  // will contain our user object pulled from Azure
    loggedIn: false  // logged in status for easy reference in components
  },
  // Permitted processes for mutating the items in store.state
  mutations: {
    updateUserInfo (state, userObject) {
      if (userObject == null) { // == is same as === null || === undefined
        state.userInfo = {}
        state.loggedIn = false
      } else {
        state.userInfo = userObject
        if (userObject.userRoles.includes("authenticated")) {
          state.loggedIn = true
        } else {
          state.loggedIn = false
        }
      }
      console.log(state.loggedIn)
      console.log(state.userInfo)
    },
  },
  // Asychronous actions permitted to mutate the items in state
  // This is what we call from components when we want to recheck login status
  actions: {
    async refreshUserInfo (context) {
        const response = await fetch('/.auth/me');
        const payload = await response.json();
        const { clientPrincipal } = payload;
        context.commit('updateUserInfo', clientPrincipal)
      // TODO: set $root.isLoading to true while calling API?
    }
  }
})

// Make BootstrapVue available throughout
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

// Register Axios globally as $http
Vue.prototype.$http = Axios

// Turn off the production tip warnings
Vue.config.productionTip = false

// Create our Vue app
const app = new Vue({
  data: { 
    isLoading: false,  // global attribute to signify loading status
  },
  store: store,  // inject the Vuex store into all child components
  router,  // inject the router into all child components
  render: h => h(App),
}).$mount('#app')

// Set global attributes when navigating
router.beforeEach((to, from, next) => {
  app.isLoading = true  // set loading to true before navigating to new view
    next()
})
router.afterEach(() => {
  //setTimeout(() => app.isLoading = false, 300) // set minimum loading milliseconds
  app.isLoading = false
  })
