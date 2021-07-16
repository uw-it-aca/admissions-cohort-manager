const state = {
  cohorts: []
};

// getters
const getters = {
  cohorts: state => {
    return state.cohorts;
  }
};

// actions
const actions = {
  get_cohorts ({ commit }, quarter) {
    this.$axios.get(`/api/collection/cohort/${quarter}/`)
      .then(response => response.data)
      .then(items => {
        commit('set_cohorts', items);
      }).catch(function(){
        commit('set_cohorts', []);
    });
  }
};

// mutations
const mutations = {
  set_cohorts (state, cohorts) {
    state.cohorts = cohorts;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
