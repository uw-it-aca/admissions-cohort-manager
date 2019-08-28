import Vue from "vue/dist/vue.esm.js";
import VueRouter from "vue-router/dist/vue-router.js";
import VueAnalytics from "vue-analytics";
import App from "./app.vue";

//TODO: Replace with real key, vue analytics requires *a* key!
// const gaCode = $("body").data("google-analytics");
const gaCode = "UA-12345-6";
const debugMode = $("body").data("django-debug");

Vue.use(VueRouter);
// import ImportPage from "/app.vue";
var router = new VueRouter({
  mode: "history",
  routes: [
    // {path: "/import", component: ImportPage},
    // // {path: "/review", component: }

  ]
});

Vue.use(VueAnalytics, {
  id: gaCode,
  router,
  set: [
    { field: 'anonymizeIp', value: true }
  ],
  debug: {
    enabled: debugMode
  }
});

new Vue({
  render: h => h(App),
  router
}).$mount("#import");
