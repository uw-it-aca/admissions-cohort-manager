const state = {
  current_period: []
};

// getters
const getters = {
  current_period: state => {
    return state.current_period;
  }
};

// actions
const actions = {
  set_current_period ({ commit }, period) {
    commit('set_current_period', period);
  }
};

// mutations
const mutations = {
  set_current_period (state, current_period) {
    state.current_period = current_period;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
