const state = {
  activities: []
};

// getters
const getters = {
  activities: state => {
    return state.activities;
  }
};

// actions
const actions = {
  get_activities ({ commit }, filters) {
    this.$axios.get(`/api/activity/`)
      .then(response => response.data)
      .then(items => {
        commit('set_activities', items.activities);
      });
  }
};

// mutations
const mutations = {
  set_activities (state, activities) {
    state.activities = activities;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
