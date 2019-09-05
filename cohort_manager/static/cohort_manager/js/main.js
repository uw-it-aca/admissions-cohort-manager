import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueAnalytics from "vue-analytics";

import App from "./App.vue";
import Landing from './pages/landing.vue';
import Cohort from './pages/cohort.vue';
import Major from './pages/major.vue';
import Log from './pages/log.vue';


//TODO: Replace with real key, vue analytics requires *a* key!
//const gaCode = $("body").data("google-analytics");
const gaCode = "UA-12345-6";
const debugMode = $("body").data("django-debug");

Vue.use(VueRouter);
Vue.use(BootstrapVue);

var router = new VueRouter({
  mode: "history",
  routes: [
    { path: '/', component: Landing },
    { path: '/cohort/', component: Cohort },
    { path: '/major/', component: Major },
    { path: '/log/', component: Log },
  ]
});


Vue.use(VueAnalytics, {
  id: gaCode,
  router,
  set: [
    { field: 'anonymizeIp', value: true }
  ],
  debug: {
    // enabled: false
    enabled: debugMode
  }
});

// vue app will be rendered inside of #main div found in index.html using webpack_loader
new Vue({
  router,
  render: h => h(App)
}).$mount("#main");
