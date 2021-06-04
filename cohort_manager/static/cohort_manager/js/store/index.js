import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import VueAxios from 'vue-axios';
import qs from 'qs';
import majorlist from './api/majorlist';
import cohortlist from './api/cohortlist';
import activities from './api/activities';
import periodlist from "./api/periodlist";
import period from './models/period';
import decisionlist from "./api/decisionlist";

Vue.use(Vuex);
Vue.use(VueAxios, axios);
const store = new Vuex.Store({
  modules: {
    majorlist,
    cohortlist,
    periodlist,
    activities,
    period,
    decisionlist
  },
});
const $axios = axios.create();
store.$axios = $axios;
const $qs = qs;
store.$qs = $qs;
export default store;
