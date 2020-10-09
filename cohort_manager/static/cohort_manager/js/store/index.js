import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import VueAxios from 'vue-axios';
import majorlist from './api/majorlist';
import cohortlist from './api/cohortlist';
import activities from './api/activities';

Vue.use(Vuex);
Vue.use(VueAxios, axios);
const store = new Vuex.Store({
  modules: {
    majorlist,
    cohortlist,
    activities
  },
});
const $axios = axios.create();
store.$axios = $axios;
export default store;
