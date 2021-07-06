const state = {
  decisions: []
};

// getters
const getters = {
  decisions: state => {
    return state.decisions;
  }
};

// actions
const actions = {
  get_decisions ({ commit }, quarter) {
    this.$axios.get(`/api/collection/dd/${quarter}/`)
      .then(response => response.data)
      .then(items => {
        commit('set_decisions', items);
      });
  }
};

// mutations
const mutations = {
  set_decisions (state, decisions) {
    state.decisions = decisions;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
