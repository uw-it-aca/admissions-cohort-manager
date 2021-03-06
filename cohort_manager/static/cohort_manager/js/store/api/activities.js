const state = {
  activities: [],
  is_loading: false,
};

// getters
const getters = {
  activities: state => {
    return state.activities;
  },
  is_loading: state => {
    return state.is_loading;
  },
};

// actions
const actions = {
  get_activities ({ commit }, filters) {
    commit('set_loading', true);
    var vuex = this;
    this.$axios({
      method: 'get',
      url: '/api/activity/',
      paramsSerializer: function (params) {
        return vuex.$qs.stringify(params, {arrayFormat: 'repeat'});
      },
      params: filters,
    })
      .then(response => response.data)
      .catch(function(){
        commit('set_activities', []);
      })
      .then(items => {
        if(items !== undefined){
          commit('set_activities', items.activities);
        }
        commit('set_loading', false);
      });
  }
};

// mutations
const mutations = {
  set_activities (state, activities) {
    state.activities = activities;
  },
  set_loading (state, is_loading) {
    state.is_loading = is_loading;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
