const state = {
  activities: [],
  is_loading: false,
  request_status: undefined
};

// getters
const getters = {
  activities: state => {
    return state.activities;
  },
  is_loading: state => {
    return state.is_loading;
  }
};

// actions
const actions = {
  get_activities ({ commit }, filters) {
    commit('set_loading', true);
    this.$axios.get(`/api/activity/`)
      .then(response => response.data)
      .catch(function (error) {
        console.log(error);
      })
      .then(items => {
        commit('set_activities', items.activities);
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
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
