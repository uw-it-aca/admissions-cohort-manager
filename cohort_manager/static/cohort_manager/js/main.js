import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueAnalytics from 'vue-analytics';
import VuePluralize from 'vue-pluralize';
import VueMoment from 'vue-moment';
import moment from 'moment-timezone';

import App from "./App.vue";
import Cohort from './pages/cohort.vue';
import Major from './pages/major.vue';
import CohortList from './pages/cohort_list.vue';
import MajorList from './pages/major_list.vue';
import Log from './pages/log.vue';
import BulkHandler from './pages/bulk_handler.vue';
import store from './store';

// import the bootstrap / bootstrap-vue base css
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

//TODO: Replace with real key, vue analytics requires *a* key!
//const gaCode = $("body").data("google-analytics");
const gaCode = "UA-12345-6";
const debugMode = $("body").data("django-debug");

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(VuePluralize);
Vue.use(VueMoment, {moment});

export const EventBus = new Vue();

var router = new VueRouter({
  mode: "history",
  routes: [
    { path: '/', redirect: '/cohort_list/' },
    { path: '/cohort/', component: Cohort },
    { path: '/cohort/:id', component: Cohort },
    { path: '/major/', component: Major },
    { path: '/major/:id', component: Major },
    { path: '/cohort_list/', component: CohortList },
    { path: '/major_list/', component: MajorList },
    { path: '/log/', component: Log },
    { path: '/log/:id', component: Log },
    { path: '/iframe/bulk_view/:id', component: BulkHandler},
    { path: '/iframe/log/', component: Log },
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
  store,
  render: h => h(App)
}).$mount("#main");
